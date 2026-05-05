"""
Virtual Keyboard Controller using Hand Gestures
"""

import cv2
import numpy as np
import pyautogui
import time
from hand_detector import HandDetector
import config


class Button:
    def __init__(self, pos, text, size=(60, 60)):
        self.pos = pos
        self.text = text
        self.size = size
        self.hover_time = 0
        
    def draw(self, frame, hover=False, pressed=False):
        x, y = self.pos
        w, h = self.size
        
        # Choose color based on state
        if pressed:
            color = config.KEY_PRESS_COLOR
        elif hover:
            color = config.KEY_HOVER_COLOR
        else:
            color = (50, 50, 50)
        
        # Draw button
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, cv2.FILLED)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
        
        # Draw text
        font_scale = 0.5 if len(self.text) > 5 else 1
        text_size = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_SIMPLEX, 
                                     font_scale, 2)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        
        cv2.putText(frame, self.text, (text_x, text_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 2)
        
        return frame


class VirtualKeyboard:
    def __init__(self):
        self.detector = HandDetector()
        self.buttons = []
        self.create_keyboard()
        self.prev_time = 0
        self.last_key_time = 0
        self.hover_start_time = {}
        
    def create_keyboard(self):
        """
        Create spread-out keyboard layout for easier targeting
        """
        start_x = 50
        start_y = 100
        
        for row_idx, row in enumerate(config.KEYBOARD_LAYOUT):
            x_offset = 0
            for col_idx, key in enumerate(row):
                # Special keys have different sizes
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
    
    def check_hover(self, x, y, button):
        """
        Check if finger is hovering over button
        """
        bx, by = button.pos
        bw, bh = button.size
        
        if bx < x < bx + bw and by < y < by + bh:
            return True
        return False
    
    def type_key(self, key):
        """
        Type the key using pyautogui
        """
        current_time = time.time()
        
        # Prevent rapid repeated typing
        if current_time - self.last_key_time < 0.3:
            return
        
        if key == 'SPACE':
            pyautogui.press('space')
        elif key == 'BACKSPACE':
            pyautogui.press('backspace')
        elif key == 'ENTER':
            pyautogui.press('enter')
        else:
            pyautogui.press(key.lower())
        
        self.last_key_time = current_time
        print(f"Typed: {key}")
    
    def run(self):
        """
        Main loop for virtual keyboard
        """
        cap = cv2.VideoCapture(config.CAMERA_INDEX)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        
        print("Virtual Keyboard Started!")
        print("Works with EITHER left or right hand!")
        print("\n🔥 EXTREME DETECTION - Detects hand VERY easily!")
        print("   - Ultra-low threshold (0.1 - MAXIMUM sensitivity!)")
        print("   - Just raise your hand - instant detection!")
        print("\nHover your index finger over a key for 0.8 seconds to type")
        print("Larger keys and more spacing for easier targeting")
        print("Press 'Q' to quit")
        
        while True:
            success, frame = cap.read()
            if not success:
                break
            
            frame = cv2.flip(frame, 1)
            frame = self.detector.find_hands(frame, draw=False)
            landmark_list = self.detector.get_position(frame)
            
            # Draw all buttons
            hovered_button = None
            pressed_button = None
            
            if len(landmark_list) > 0:
                fingers = self.detector.fingers_up(landmark_list)
                
                # Index finger up for selection
                if fingers[1] == 1:
                    x1, y1 = landmark_list[8][1], landmark_list[8][2]
                    
                    # Draw finger position
                    cv2.circle(frame, (x1, y1), 10, (0, 255, 0), cv2.FILLED)
                    
                    # Check which button is hovered
                    for button in self.buttons:
                        if self.check_hover(x1, y1, button):
                            hovered_button = button
                            
                            # Track hover time
                            if button.text not in self.hover_start_time:
                                self.hover_start_time[button.text] = time.time()
                            
                            hover_duration = time.time() - self.hover_start_time[button.text]
                            
                            # Draw progress bar
                            progress = min(hover_duration / config.DWELL_TIME, 1.0)
                            bar_width = int(button.size[0] * progress)
                            bx, by = button.pos
                            cv2.rectangle(frame, (bx, by - 10), 
                                        (bx + bar_width, by - 5), 
                                        (0, 255, 0), cv2.FILLED)
                            
                            # Type if hover time exceeded
                            if hover_duration >= config.DWELL_TIME:
                                self.type_key(button.text)
                                pressed_button = button
                                self.hover_start_time.clear()
                            
                            break
                    
                    # Clear hover times for non-hovered buttons
                    if hovered_button:
                        keys_to_remove = [k for k in self.hover_start_time.keys() 
                                        if k != hovered_button.text]
                        for k in keys_to_remove:
                            del self.hover_start_time[k]
                    else:
                        self.hover_start_time.clear()
            
            # Draw all buttons
            for button in self.buttons:
                is_hover = button == hovered_button
                is_pressed = button == pressed_button
                button.draw(frame, hover=is_hover, pressed=is_pressed)
            
            # FPS
            if config.SHOW_FPS:
                curr_time = time.time()
                fps = 1 / (curr_time - self.prev_time) if self.prev_time > 0 else 0
                self.prev_time = curr_time
                cv2.putText(frame, f'FPS: {int(fps)}', (10, 40), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Instructions
            cv2.putText(frame, "Hover over key for 0.8 sec to type | Works with either hand", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.imshow("Virtual Keyboard", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        self.detector.close()


if __name__ == "__main__":
    keyboard = VirtualKeyboard()
    keyboard.run()
