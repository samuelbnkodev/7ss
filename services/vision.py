import os
import cv2
import numpy as np
import pyautogui

try:
    import pytesseract
    from PIL import Image
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False

class LocalVisionEngine:
    def __init__(self):
        # Fallback or initialization settings for local vision
        pass

    def capture_active_screen(self, region=None):
        """Captures a screenshot of the primary display or specific region [x, y, w, h]."""
        screenshot = pyautogui.screenshot(region=tuple(region) if region else None)
        frame = np.array(screenshot)
        # Convert RGB to BGR for OpenCV processing
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame_bgr

    def extract_text_from_region(self, region=None):
        """Captures screen region and extracts text via Tesseract OCR."""
        screenshot = pyautogui.screenshot(region=tuple(region) if region else None)
        resolution = screenshot.size
        
        extracted_text = ""
        if HAS_TESSERACT:
            try:
                extracted_text = pytesseract.image_to_string(screenshot).strip()
            except Exception as e:
                extracted_text = f"OCR Engine Notice: Tesseract binary required ({str(e)})"
        else:
            extracted_text = "Tesseract library not found. Returning capture metadata."

        return {
            "status": "success", 
            "resolution": resolution, 
            "extracted_text": extracted_text
        }

    def find_text_and_get_coordinates(self, target_text):
        """Scans the screen, performs OCR data mapping, and returns bounding box coordinates."""
        if not HAS_TESSERACT:
            return None
        screenshot = pyautogui.screenshot()
        data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DATAFRAME)
        # Filter non-empty matching text rows
        matches = data[(data['conf'] > 40) & (data['text'].str.contains(target_text, case=False, na=False))]
        if not matches.empty:
            row = matches.iloc[0]
            return {
                "x": int(row['left']), 
                "y": int(row['top']), 
                "w": int(row['width']), 
                "h": int(row['height'])
            }
        return None

    def execute_click_on_text(self, target_text):
        """Automated action trigger: locates target text on screen and simulates a mouse click."""
        coords = self.find_text_and_get_coordinates(target_text)
        if coords:
            center_x = coords['x'] + (coords['w'] // 2)
            center_y = coords['y'] + (coords['h'] // 2)
            pyautogui.moveTo(center_x, center_y, duration=0.25)
            pyautogui.click()
            return {"success": True, "target": target_text, "coordinates": (center_x, center_y)}
        return {"success": False, "message": f"Target text '{target_text}' not visible on current screen."}

vision_engine = LocalVisionEngine()