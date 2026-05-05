"""
Configuration settings for Virtual Mouse and Keyboard
Adjust these values to customize behavior and performance
"""

# ============================================================================
# CAMERA SETTINGS
# ============================================================================
CAMERA_INDEX = 0  # Try 0, 1, 2 if camera not detected
FRAME_WIDTH = 1280  # Increased from 640 for larger display
FRAME_HEIGHT = 720  # Increased from 480 for larger display

# Window Settings
WINDOW_FULLSCREEN = False  # Set to True for fullscreen mode
WINDOW_MAXIMIZED = True    # Set to True to maximize window on startup
WINDOW_RESIZABLE = True    # Allow window resizing

# ============================================================================
# HAND DETECTION SETTINGS - OPTIMIZED FOR EASY DETECTION + SMOOTH PERFORMANCE
# ============================================================================
MIN_DETECTION_CONFIDENCE = 0.1  # EXTREMELY LOW = Detects hand very easily!
MIN_TRACKING_CONFIDENCE = 0.1   # EXTREMELY LOW = Keeps tracking smoothly
MAX_NUM_HANDS = 2  # Support both hands (uses first detected hand)

# Image Enhancement for Better Detection (Optimized for Speed)
ENABLE_IMAGE_ENHANCEMENT = True  # Enhance image for better detection
BRIGHTNESS_BOOST = 1.4           # Increased for better visibility
CONTRAST_BOOST = 1.3             # Increased for hand to stand out more
ENABLE_HISTOGRAM_EQ = True       # Equalize histogram for better lighting
ENABLE_DENOISE = False           # DISABLED for better performance (saves ~15ms)

# ============================================================================
# MOUSE SETTINGS
# ============================================================================
MOUSE_SMOOTHING = 3  # Optimized for faster response with minimal jitter
MOUSE_SPEED = 1.8    # Faster cursor movement
CLICK_THRESHOLD = 35  # Easier click detection
DRAG_THRESHOLD = 40   # Distance threshold for drag detection
SCROLL_SPEED = 25     # Enhanced scroll sensitivity
SCROLL_SMOOTHING = 2  # Smooth scrolling buffer

# ============================================================================
# KEYBOARD SETTINGS
# ============================================================================
DWELL_TIME = 0.8  # Faster key activation
KEY_SIZE = 80     # Larger keys for easier targeting
KEY_PADDING = 20  # More space between keys

# Keyboard Layout - Spread out for easier use
KEYBOARD_LAYOUT = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BACKSPACE'],
    ['SPACE', 'ENTER']
]

# ============================================================================
# VISUAL SETTINGS
# ============================================================================
SHOW_FPS = True          # Display FPS counter
SHOW_LANDMARKS = True    # Show hand skeleton overlay
SHOW_INSTRUCTIONS = True # Show on-screen instructions

# Colors (B, G, R format for OpenCV)
CURSOR_COLOR = (0, 255, 0)      # Green - Normal cursor
CLICK_COLOR = (0, 0, 255)       # Red - Click detected
KEY_HOVER_COLOR = (255, 200, 0) # Light blue - Key hover
KEY_PRESS_COLOR = (0, 255, 0)   # Green - Key pressed

# ============================================================================
# GESTURE THRESHOLDS
# ============================================================================
PINCH_THRESHOLD = 40  # Distance for pinch gesture (lower = must pinch tighter)
FINGER_UP_THRESHOLD = 0.1  # Sensitivity for finger up detection

# ============================================================================
# PERFORMANCE TUNING
# ============================================================================
# For better performance on slower computers:
# - Set FRAME_WIDTH = 640, FRAME_HEIGHT = 480
# - Set MOUSE_SMOOTHING = 3
# - Set MIN_DETECTION_CONFIDENCE = 0.6
# - Set SHOW_LANDMARKS = False

# For better accuracy:
# - Set MIN_DETECTION_CONFIDENCE = 0.8
# - Set MOUSE_SMOOTHING = 7
# - Ensure good lighting conditions

# For larger display:
# - Set FRAME_WIDTH = 1280, FRAME_HEIGHT = 720 (current)
# - Set FRAME_WIDTH = 1920, FRAME_HEIGHT = 1080 (full HD)
# - Set WINDOW_FULLSCREEN = True for fullscreen mode
