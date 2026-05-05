"""
Hand Detection Module using MediaPipe
Updated for MediaPipe 0.10.35+ (new tasks API)
"""

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import math
import config
import urllib.request
import os


class HandDetector:
    def __init__(self):
        # Download hand landmarker model if not exists
        model_path = 'hand_landmarker.task'
        if not os.path.exists(model_path):
            print("Downloading hand detection model...")
            url = 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task'
            urllib.request.urlretrieve(url, model_path)
            print("Model downloaded!")
        
        # Create hand landmarker
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=config.MAX_NUM_HANDS,
            min_hand_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_hand_presence_confidence=config.MIN_TRACKING_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.results = None
        
    def enhance_image(self, frame):
        """
        Enhance image for better hand detection - OPTIMIZED FOR SPEED
        """
        if not config.ENABLE_IMAGE_ENHANCEMENT:
            return frame
        
        enhanced = frame.copy()
        
        # Fast brightness and contrast adjustment (very fast ~2ms)
        enhanced = cv2.convertScaleAbs(enhanced, 
                                       alpha=config.CONTRAST_BOOST, 
                                       beta=int((config.BRIGHTNESS_BOOST - 1.0) * 50))
        
        # Apply histogram equalization only if enabled (fast ~5ms)
        if config.ENABLE_HISTOGRAM_EQ:
            # Convert to LAB color space for better processing
            lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            
            # Apply CLAHE to L channel
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            
            # Merge back
            lab = cv2.merge([l, a, b])
            enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # Denoise only if enabled (slow ~15ms - disabled by default)
        if config.ENABLE_DENOISE:
            enhanced = cv2.fastNlMeansDenoisingColored(enhanced, None, 10, 10, 7, 21)
        
        return enhanced
        
    def find_hands(self, frame, draw=True):
        """
        Detect hands in the frame with image enhancement
        """
        # Enhance image for better detection
        enhanced_frame = self.enhance_image(frame)
        
        # Convert to MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=enhanced_frame)
        
        # Detect hands
        self.results = self.detector.detect(mp_image)
        
        # Draw landmarks if requested (on original frame for better visibility)
        if draw and self.results.hand_landmarks:
            for hand_landmarks in self.results.hand_landmarks:
                if config.SHOW_LANDMARKS:
                    self._draw_landmarks(frame, hand_landmarks)
        
        return frame
    
    def _draw_landmarks(self, frame, hand_landmarks):
        """
        Draw hand landmarks on frame
        """
        h, w, c = frame.shape
        
        # Draw connections
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8),  # Index
            (0, 9), (9, 10), (10, 11), (11, 12),  # Middle
            (0, 13), (13, 14), (14, 15), (15, 16),  # Ring
            (0, 17), (17, 18), (18, 19), (19, 20),  # Pinky
            (5, 9), (9, 13), (13, 17)  # Palm
        ]
        
        # Draw connections
        for connection in connections:
            start_idx, end_idx = connection
            if start_idx < len(hand_landmarks) and end_idx < len(hand_landmarks):
                start = hand_landmarks[start_idx]
                end = hand_landmarks[end_idx]
                start_point = (int(start.x * w), int(start.y * h))
                end_point = (int(end.x * w), int(end.y * h))
                cv2.line(frame, start_point, end_point, (0, 255, 0), 2)
        
        # Draw landmarks
        for landmark in hand_landmarks:
            cx, cy = int(landmark.x * w), int(landmark.y * h)
            cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
    
    def get_position(self, frame, hand_no=0):
        """
        Get landmark positions for a specific hand
        """
        landmark_list = []
        
        if self.results and self.results.hand_landmarks:
            if hand_no < len(self.results.hand_landmarks):
                hand = self.results.hand_landmarks[hand_no]
                h, w, c = frame.shape
                
                for id, landmark in enumerate(hand):
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    landmark_list.append([id, cx, cy])
        
        return landmark_list
    
    def fingers_up(self, landmark_list):
        """
        Determine which fingers are up
        Returns list: [thumb, index, middle, ring, pinky]
        Works for both left and right hands
        """
        fingers = []
        
        if len(landmark_list) == 0:
            return fingers
        
        # Detect hand orientation (left or right)
        # Compare wrist (0) to pinky base (17) x-coordinates
        is_right_hand = landmark_list[17][1] < landmark_list[0][1]
        
        # Thumb (check based on hand orientation)
        if is_right_hand:
            # Right hand: thumb tip should be to the right of IP joint
            if landmark_list[4][1] > landmark_list[3][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            # Left hand: thumb tip should be to the left of IP joint
            if landmark_list[4][1] < landmark_list[3][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        # Other fingers (check if tip is above PIP joint)
        tip_ids = [8, 12, 16, 20]
        for id in tip_ids:
            if landmark_list[id][2] < landmark_list[id - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers
    
    def get_distance(self, p1, p2, landmark_list):
        """
        Calculate distance between two landmarks
        """
        if len(landmark_list) < max(p1, p2) + 1:
            return 0, 0, 0, 0, 0
        
        x1, y1 = landmark_list[p1][1], landmark_list[p1][2]
        x2, y2 = landmark_list[p2][1], landmark_list[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        
        length = math.hypot(x2 - x1, y2 - y1)
        
        return length, x1, y1, x2, y2
    
    def close(self):
        """
        Release resources
        """
        self.detector.close()
