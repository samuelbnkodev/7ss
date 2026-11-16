import os
import cv2
import numpy as np
import pyautogui

class LocalVisionEngine:
    def __init__(self):
        # Initialize any local vision configurations
        pass

    def capture_active_screen(self, region=None):
        """Captures a screenshot of the primary display or a specific region [x, y, w, h]."""
        screenshot = pyautogui.screenshot(region=tuple(region) if region else None)
        frame = np.array(screenshot)
        # Convert RGB to BGR for OpenCV processing
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame_bgr

    def extract_text_from_region(self, region=None):
        """Placeholder for local OCR processing (e.g., PaddleOCR / Tesseract integration)."""
        frame = self.capture_active_screen(region)
        # In future steps, we feed 'frame' into PaddleOCR here
        return {"status": "success", "resolution": frame.shape, "message": "Screen region captured successfully."}

vision_engine = LocalVisionEngine()