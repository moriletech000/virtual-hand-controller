"""
Quick test to verify Python 3.14 compatibility
"""

import sys

print("="*60)
print("PYTHON 3.14 COMPATIBILITY TEST")
print("="*60)
print(f"\nPython Version: {sys.version}")
print(f"Python Version Info: {sys.version_info}")

# Test imports
print("\nTesting imports...")

try:
    import numpy as np
    print(f"✓ NumPy {np.__version__} - OK")
except Exception as e:
    print(f"✗ NumPy - FAILED: {e}")

try:
    import cv2
    print(f"✓ OpenCV {cv2.__version__} - OK")
except Exception as e:
    print(f"✗ OpenCV - FAILED: {e}")

try:
    import mediapipe as mp
    print(f"✓ MediaPipe {mp.__version__} - OK")
except Exception as e:
    print(f"✗ MediaPipe - FAILED: {e}")

try:
    import pyautogui
    print(f"✓ PyAutoGUI {pyautogui.__version__} - OK")
except Exception as e:
    print(f"✗ PyAutoGUI - FAILED: {e}")

try:
    import pynput
    print(f"✓ Pynput - OK")
except Exception as e:
    print(f"✗ Pynput - FAILED: {e}")

try:
    import PIL
    print(f"✓ Pillow {PIL.__version__} - OK")
except Exception as e:
    print(f"✗ Pillow - FAILED: {e}")

print("\n" + "="*60)
print("Test complete! If all show ✓, you're ready to go!")
print("="*60)
print("\nRun: py main.py")
