"""
Combined Virtual Mouse and Keyboard Controller
Switch between modes using keyboard shortcuts
"""

import cv2
import numpy as np
import pyautogui
import time
from collections import deque
from hand_detector import HandDetector
from virtual_keyboard import Button
import config

# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False


class VirtualController:
    def __init__(self):
        self.detector = HandDetector()
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Mouse settings
        self.smooth_x = deque(maxlen=config.MOUSE_SMOOTHING)
        self.smooth_y = deque(maxlen=config.MOUSE_SMOOTHING)
        self.scroll_buffer = deque(maxlen=config.SCROLL_SMOOTHING)
        self.is_dragging = False
        self.prev_scroll_y = 0
        self.last_click_time = 0
        self.last_right_click_time = 0
        
        # Keyboard settings
        self.buttons = []
        self.create_keyboard()
        self.last_key_time = 0
        self.hover_start_time = {}
        
        # Mode control
        self.mode = "mouse"  # "mouse" or "keyboard"
        self.prev_time = 0
        
    def create_keyboard(self):
        """Create spread-out keyboard layout for easier targeting"""
        start_x = 50
        start_y = 100
        
        for row_idx, row in enumerate(config.KEYBOARD_LAYOUT):
            x_offset = 0
            for col_idx, key in enumerate(row):
                if key == 'SPACE':
                    width = 300  # Extra wide space bar
                elif key in ['BACKSPACE', 'ENTER']:
                    width = 150  # Wider special keys
                else:
                    width = config.KEY_SIZE
                
                x = start_x + x_offset
                y = start_y + row_idx * (config.KEY_SIZE + config.KEY_PADDING)
                
                self.buttons.append(Button((x, y), key, (width, config.KEY_SIZE)))
                x_offset += width + config.KEY_PADDING
    
    def mouse_mode(self, frame, landmark_list):
        """Handle mouse gestures - optimized for either hand"""
        if len(landmark_list) == 0:
            return frame
        
        fingers = self.detector.fingers_up(landmark_list)
        
        # Move cursor - Index finger up (faster, smoother)
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
            cv2.circle(frame, (x1, y1), 15, config.CURSOR_COLOR, cv2.FILLED)
        
        # Left Click (with debounce)
        if fingers[0] == 1 and fingers[1] == 1:
            length, x1, y1, x2, y2 = self.detector.get_distance(4, 8, landmark_list)
            
            current_time = time.time()
            if length < config.CLICK_THRESHOLD:
                cv2.circle(frame, (x1, y1), 15, config.CLICK_COLOR, cv2.FILLED)
                if current_time - self.last_click_time > 0.3:
                    pyautogui.click()
                    self.last_click_time = current_time
        
        # Right Click (with debounce)
        if fingers[0] == 1 and fingers[2] == 1 and fingers[1] == 0:
            length, x1, y1, x2, y2 = self.detector.get_distance(4, 12, landmark_list)
            
            current_time = time.time()
            if length < config.CLICK_THRESHOLD:
                cv2.circle(frame, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                if current_time - self.last_right_click_time > 0.3:
                    pyautogui.rightClick()
                    self.last_right_click_time = current_time
        
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
            cv2.putText(frame, "SCROLL MODE", (10, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            cv2.circle(frame, (landmark_list[8][1], y_pos), 12, (255, 255, 0), cv2.FILLED)
        else:
            self.prev_scroll_y = 0
            self.scroll_buffer.clear()
        
        return frame
    
    def keyboard_mode(self, frame, landmark_list):
        """Handle keyboard gestures"""
        hovered_button = None
        pressed_button = None
        
        if len(landmark_list) > 0:
            fingers = self.detector.fingers_up(landmark_list)
            
            if fingers[1] == 1:
                x1, y1 = landmark_list[8][1], landmark_list[8][2]
                cv2.circle(frame, (x1, y1), 10, (0, 255, 0), cv2.FILLED)
                
                for button in self.buttons:
                    bx, by = button.pos
                    bw, bh = button.size
                    
                    if bx < x1 < bx + bw and by < y1 < by + bh:
                        hovered_button = button
                        
                        if button.text not in self.hover_start_time:
                            self.hover_start_time[button.text] = time.time()
                        
                        hover_duration = time.time() - self.hover_start_time[button.text]
                        progress = min(hover_duration / config.DWELL_TIME, 1.0)
                        bar_width = int(button.size[0] * progress)
                        
                        cv2.rectangle(frame, (bx, by - 10), 
                                    (bx + bar_width, by - 5), 
                                    (0, 255, 0), cv2.FILLED)
                        
                        if hover_duration >= config.DWELL_TIME:
                            current_time = time.time()
                            if current_time - self.last_key_time >= 0.3:
                                self.type_key(button.text)
                                pressed_button = button
                                self.hover_start_time.clear()
                        
                        break
                
                if hovered_button:
                    keys_to_remove = [k for k in self.hover_start_time.keys() 
                                    if k != hovered_button.text]
                    for k in keys_to_remove:
                        del self.hover_start_time[k]
                else:
                    self.hover_start_time.clear()
        
        # Draw buttons
        for button in self.buttons:
            is_hover = button == hovered_button
            is_pressed = button == pressed_button
            button.draw(frame, hover=is_hover, pressed=is_pressed)
        
        return frame
    
    def type_key(self, key):
        """Type the key"""
        if key == 'SPACE':
            pyautogui.press('space')
        elif key == 'BACKSPACE':
            pyautogui.press('backspace')
        elif key == 'ENTER':
            pyautogui.press('enter')
        else:
            pyautogui.press(key.lower())
        
        self.last_key_time = time.time()
        print(f"Typed: {key}")
    
    def run(self):
        """Main loop"""
        cap = cv2.VideoCapture(config.CAMERA_INDEX)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        
        # Create window with specific properties
        window_name = "Virtual Controller"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL if config.WINDOW_RESIZABLE else cv2.WINDOW_AUTOSIZE)
        
        # Set window to fullscreen or maximized
        if config.WINDOW_FULLSCREEN:
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        elif config.WINDOW_MAXIMIZED:
            # Maximize window (platform-specific behavior)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_name, 1280, 720)
        
        print("Virtual Controller Started!")
        print("Works with EITHER left or right hand!")
        print("\n🔥 EXTREME DETECTION - Detects hand VERY easily!")
        print("   - Ultra-low threshold (0.1 - MAXIMUM sensitivity!)")
        print("   - Fast image enhancement (no lag)")
        print("   - Just raise your hand - instant detection!")
        print("\nMouse Mode Gestures:")
        print("- Index finger: Move cursor (fast & smooth)")
        print("- Thumb + Index pinch: Left click")
        print("- Thumb + Middle pinch: Right click")
        print("- Index + Middle up: Scroll (smooth)")
        print("\nKeyboard Mode:")
        print("- Hover index finger over key to type")
        print("\nControls:")
        print("Press 'M' for Mouse mode")
        print("Press 'K' for Keyboard mode")
        print("Press 'F' to toggle fullscreen")
        print("Press 'Q' to quit")
        
        fullscreen = config.WINDOW_FULLSCREEN
        
        while True:
            success, frame = cap.read()
            if not success:
                break
            
            frame = cv2.flip(frame, 1)
            
            # Detect hands
            if self.mode == "mouse":
                frame = self.detector.find_hands(frame)
            else:
                frame = self.detector.find_hands(frame, draw=False)
            
            landmark_list = self.detector.get_position(frame)
            
            # Process based on mode
            if self.mode == "mouse":
                frame = self.mouse_mode(frame, landmark_list)
            else:
                frame = self.keyboard_mode(frame, landmark_list)
            
            # Display mode and instructions
            mode_text = f"Mode: {self.mode.upper()}"
            cv2.putText(frame, mode_text, (10, 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
            # Show instructions if enabled
            if config.SHOW_INSTRUCTIONS:
                instructions = [
                    "M: Mouse | K: Keyboard | F: Fullscreen | Q: Quit"
                ]
                y_pos = frame.shape[0] - 20
                for instruction in instructions:
                    cv2.putText(frame, instruction, (10, y_pos), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                    y_pos -= 25
            
            # FPS
            if config.SHOW_FPS:
                curr_time = time.time()
                fps = 1 / (curr_time - self.prev_time) if self.prev_time > 0 else 0
                self.prev_time = curr_time
                cv2.putText(frame, f'FPS: {int(fps)}', (10, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow(window_name, frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('m'):
                self.mode = "mouse"
                print("Switched to Mouse mode")
            elif key == ord('k'):
                self.mode = "keyboard"
                print("Switched to Keyboard mode")
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
    controller = VirtualController()
    controller.run()
