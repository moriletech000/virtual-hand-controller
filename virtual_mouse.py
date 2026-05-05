"""
Virtual Mouse Controller using Hand Gestures
"""

import cv2
import numpy as np
import pyautogui
import time
from collections import deque
from hand_detector import HandDetector
import config

# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False


class VirtualMouse:
    def __init__(self):
        self.detector = HandDetector()
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Smoothing
        self.smooth_x = deque(maxlen=config.MOUSE_SMOOTHING)
        self.smooth_y = deque(maxlen=config.MOUSE_SMOOTHING)
        
        # Scroll smoothing
        self.scroll_buffer = deque(maxlen=config.SCROLL_SMOOTHING)
        
        # State tracking
        self.prev_time = 0
        self.is_dragging = False
        self.prev_scroll_y = 0
        self.last_click_time = 0
        self.last_right_click_time = 0
        
    def run(self):
        """
        Main loop for virtual mouse
        """
        cap = cv2.VideoCapture(config.CAMERA_INDEX)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        
        # Create window with specific properties
        window_name = "Virtual Mouse"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL if config.WINDOW_RESIZABLE else cv2.WINDOW_AUTOSIZE)
        
        # Set window to fullscreen or maximized
        if config.WINDOW_FULLSCREEN:
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        elif config.WINDOW_MAXIMIZED:
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_name, 1280, 720)
        
        print("Virtual Mouse Started!")
        print("Works with EITHER left or right hand!")
        print("\n🔥 EXTREME DETECTION - Detects hand VERY easily!")
        print("   - Ultra-low threshold (0.1 - MAXIMUM sensitivity!)")
        print("   - Fast image enhancement (no lag)")
        print("   - Optimized for smooth performance")
        print("\n💡 TIPS:")
        print("   - Just raise your hand - it will detect instantly!")
        print("   - Works in any condition")
        print("   - Spread fingers for best results")
        print("\nGestures:")
        print("- Index finger up: Move cursor (fast & smooth)")
        print("- Thumb + Index pinch: Left click")
        print("- Thumb + Middle pinch: Right click")
        print("- Index + Middle fingers up: Scroll (smooth)")
        print("\nControls:")
        print("Press 'F' to toggle fullscreen")
        print("Press 'Q' to quit")
        
        fullscreen = config.WINDOW_FULLSCREEN
        
        while True:
            success, frame = cap.read()
            if not success:
                break
            
            frame = cv2.flip(frame, 1)
            frame = self.detector.find_hands(frame)
            landmark_list = self.detector.get_position(frame)
            
            if len(landmark_list) > 0:
                # Get finger states
                fingers = self.detector.fingers_up(landmark_list)
                
                # Index finger up - Move cursor (faster, smoother)
                if fingers[1] == 1 and fingers[2] == 0:
                    x1, y1 = landmark_list[8][1], landmark_list[8][2]
                    
                    # Convert coordinates with speed multiplier
                    x3 = np.interp(x1, (80, config.FRAME_WIDTH - 80), 
                                   (0, self.screen_width)) * config.MOUSE_SPEED
                    y3 = np.interp(y1, (80, config.FRAME_HEIGHT - 80), 
                                   (0, self.screen_height)) * config.MOUSE_SPEED
                    
                    # Clamp to screen bounds
                    x3 = max(0, min(self.screen_width - 1, x3))
                    y3 = max(0, min(self.screen_height - 1, y3))
                    
                    # Smooth movement
                    self.smooth_x.append(x3)
                    self.smooth_y.append(y3)
                    smooth_x = sum(self.smooth_x) / len(self.smooth_x)
                    smooth_y = sum(self.smooth_y) / len(self.smooth_y)
                    
                    # Move cursor instantly
                    pyautogui.moveTo(smooth_x, smooth_y)
                    
                    # Draw cursor position
                    cv2.circle(frame, (x1, y1), 15, config.CURSOR_COLOR, cv2.FILLED)
                
                # Left Click - Thumb and Index pinch (with debounce)
                if fingers[0] == 1 and fingers[1] == 1:
                    length, x1, y1, x2, y2 = self.detector.get_distance(
                        4, 8, landmark_list
                    )
                    
                    current_time = time.time()
                    if length < config.CLICK_THRESHOLD:
                        cv2.circle(frame, (x1, y1), 15, config.CLICK_COLOR, cv2.FILLED)
                        if current_time - self.last_click_time > 0.3:
                            pyautogui.click()
                            self.last_click_time = current_time
                            print("Left Click")
                
                # Right Click - Thumb and Middle pinch (with debounce)
                if fingers[0] == 1 and fingers[2] == 1 and fingers[1] == 0:
                    length, x1, y1, x2, y2 = self.detector.get_distance(
                        4, 12, landmark_list
                    )
                    
                    current_time = time.time()
                    if length < config.CLICK_THRESHOLD:
                        cv2.circle(frame, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                        if current_time - self.last_right_click_time > 0.3:
                            pyautogui.rightClick()
                            self.last_right_click_time = current_time
                            print("Right Click")
                
                # Enhanced Scroll - Index and Middle finger up (smoother)
                if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0:
                    # Use middle point between index and middle finger for stability
                    y_index = landmark_list[8][2]
                    y_middle = landmark_list[12][2]
                    y_pos = (y_index + y_middle) // 2
                    
                    if self.prev_scroll_y != 0:
                        scroll_delta = (self.prev_scroll_y - y_pos)
                        self.scroll_buffer.append(scroll_delta)
                        
                        # Average scroll for smoothness
                        avg_scroll = sum(self.scroll_buffer) / len(self.scroll_buffer)
                        scroll_amount = int(avg_scroll / 8)
                        
                        if abs(scroll_amount) > 0:
                            pyautogui.scroll(scroll_amount * config.SCROLL_SPEED)
                    
                    self.prev_scroll_y = y_pos
                    
                    # Visual feedback
                    cv2.putText(frame, "SCROLL MODE", (10, 100), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    cv2.circle(frame, (landmark_list[8][1], y_pos), 12, (255, 255, 0), cv2.FILLED)
                else:
                    self.prev_scroll_y = 0
                    self.scroll_buffer.clear()
            
            # Show instructions
            if config.SHOW_INSTRUCTIONS:
                cv2.putText(frame, "F: Fullscreen | Q: Quit", (10, frame.shape[0] - 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            # FPS
            if config.SHOW_FPS:
                curr_time = time.time()
                fps = 1 / (curr_time - self.prev_time) if self.prev_time > 0 else 0
                self.prev_time = curr_time
                cv2.putText(frame, f'FPS: {int(fps)}', (10, 40), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow(window_name, frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('f'):
                # Toggle fullscreen
                fullscreen = not fullscreen
                if fullscreen:
                    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                    print("Fullscreen mode ON")
                else:
                    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
                    print("Fullscreen mode OFF")
        
        cap.release()
        cv2.destroyAllWindows()
        self.detector.close()


if __name__ == "__main__":
    mouse = VirtualMouse()
    mouse.run()
