"""
Troubleshooting and diagnostic tool
"""

import sys
import platform


def check_system():
    """Check system information"""
    print("="*60)
    print("SYSTEM INFORMATION")
    print("="*60)
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Platform: {platform.platform()}")
    print(f"Python Version: {sys.version}")
    print(f"Architecture: {platform.machine()}")
    print()


def check_camera_devices():
    """Check available camera devices"""
    print("="*60)
    print("CAMERA DEVICES")
    print("="*60)
    
    try:
        import cv2
        
        # Test first 5 camera indices
        available_cameras = []
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    available_cameras.append(i)
                    print(f"✓ Camera {i}: Available ({frame.shape[1]}x{frame.shape[0]})")
                cap.release()
        
        if not available_cameras:
            print("✗ No cameras detected")
            print("\nTroubleshooting:")
            print("  1. Check if webcam is connected")
            print("  2. Check camera permissions")
            print("  3. Close other apps using the camera")
        else:
            print(f"\nFound {len(available_cameras)} camera(s)")
            print(f"Update config.py CAMERA_INDEX to use: {available_cameras[0]}")
        
    except ImportError:
        print("✗ OpenCV not installed")
        print("  Run: pip install opencv-python")
    except Exception as e:
        print(f"✗ Error checking cameras: {e}")
    
    print()


def check_permissions():
    """Check system permissions"""
    print("="*60)
    print("PERMISSIONS CHECK")
    print("="*60)
    
    # Check if running with appropriate permissions
    if platform.system() == "Windows":
        print("Windows detected")
        print("  - Camera permission: Check Windows Settings > Privacy > Camera")
        print("  - Allow desktop apps to access camera")
    elif platform.system() == "Darwin":
        print("macOS detected")
        print("  - Camera permission: System Preferences > Security & Privacy > Camera")
        print("  - Accessibility: System Preferences > Security & Privacy > Accessibility")
    elif platform.system() == "Linux":
        print("Linux detected")
        print("  - Check if user is in 'video' group: groups $USER")
        print("  - Add to video group: sudo usermod -a -G video $USER")
    
    print()


def check_dependencies():
    """Check all dependencies with versions"""
    print("="*60)
    print("DEPENDENCY VERSIONS")
    print("="*60)
    
    dependencies = [
        'cv2',
        'mediapipe',
        'pyautogui',
        'pynput',
        'mouse',
        'numpy',
        'PIL'
    ]
    
    for dep in dependencies:
        try:
            module = __import__(dep)
            version = getattr(module, '__version__', 'unknown')
            print(f"✓ {dep:15} {version}")
        except ImportError:
            print(f"✗ {dep:15} NOT INSTALLED")
    
    print()


def test_hand_detection():
    """Test hand detection with live camera"""
    print("="*60)
    print("HAND DETECTION TEST")
    print("="*60)
    print("Starting camera... Show your hand to the camera")
    print("Press 'q' to quit\n")
    
    try:
        import cv2
        import mediapipe as mp
        
        mp_hands = mp.solutions.hands
        mp_draw = mp.solutions.drawing_utils
        
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7
        )
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("✗ Cannot open camera")
            return
        
        print("✓ Camera opened successfully")
        print("  Show your hand to test detection...")
        
        hand_detected = False
        frame_count = 0
        
        while frame_count < 300:  # Run for ~10 seconds at 30fps
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)
            
            if results.multi_hand_landmarks:
                hand_detected = True
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(
                        frame, 
                        hand_landmarks, 
                        mp_hands.HAND_CONNECTIONS
                    )
                cv2.putText(frame, "HAND DETECTED!", (10, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "No hand detected", (10, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow("Hand Detection Test", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            frame_count += 1
        
        cap.release()
        cv2.destroyAllWindows()
        hands.close()
        
        if hand_detected:
            print("\n✓ Hand detection working!")
        else:
            print("\n✗ No hand detected during test")
            print("  Make sure your hand is visible and well-lit")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
    
    print()


def main():
    """Run all diagnostic checks"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "VIRTUAL MOUSE & KEYBOARD DIAGNOSTICS" + " "*12 + "║")
    print("╚" + "="*58 + "╝")
    print()
    
    check_system()
    check_dependencies()
    check_camera_devices()
    check_permissions()
    
    print("="*60)
    print("INTERACTIVE TESTS")
    print("="*60)
    
    response = input("Run hand detection test? (y/n): ").lower()
    if response == 'y':
        test_hand_detection()
    
    print("="*60)
    print("Diagnostics complete!")
    print("="*60)


if __name__ == "__main__":
    main()
