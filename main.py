import os
import cv2
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from kivy.clock import Clock

class CiviShotEngine:
    """iPhone-style Tone Mapping, Skin Tone & HDR Enhancer"""
    @staticmethod
    def process_image(img):
        if img is None:
            return None
            
        # 1. Lightness Control & Shadow Recovery (CLAHE)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l_enhanced = clahe.apply(l)
        enhanced_lab = cv2.merge((l_enhanced, a, b))
        img_hdr = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

        # 2. Natural Warm Skin Tones & Vibrant Dynamic Colors
        hsv = cv2.cvtColor(img_hdr, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] *= 1.15  # Saturation Boost
        hsv[:, :, 2] *= 1.05  # Brightness Curve
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
        img_color = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

        # 3. Noise Reduction & iPhone Detail Sharpening
        denoised = cv2.fastNlMeansDenoisingColored(img_color, None, 5, 5, 7, 21)
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        final_img = cv2.filter2D(denoised, -1, kernel)

        return final_img

class CiviShotApp(App):
    def build(self):
        self.icon = 'icon.png'
        self.title = 'CiviShot AI'
        
        self.layout = BoxLayout(orientation='vertical')
        self.img_widget = Image()
        self.layout.add_widget(self.img_widget)
        
        self.status_label = Label(text="CiviShot Ready", size_hint_y=0.1)
        self.layout.add_widget(self.status_label)
        
        btn_layout = BoxLayout(size_hint_y=0.15)
        
        btn_cam = Button(text="📸 Take Photo", on_press=self.capture_photo)
        btn_process = Button(text="✨ Process iPhone Look", on_press=self.apply_civishot)
        
        btn_layout.add_widget(btn_cam)
        btn_layout.add_widget(btn_process)
        self.layout.add_widget(btn_layout)
        
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update_live_feed, 1.0 / 30.0)
        
        self.current_frame = None
        return self.layout

    def update_live_feed(self, dt):
        ret, frame = self.capture.read()
        if ret:
            self.current_frame = frame
            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img_widget.texture = texture

    def capture_photo(self, instance):
        if self.current_frame is not None:
            cv2.imwrite("captured.jpg", self.current_frame)
            self.status_label.text = "Photo Captured! Click Process."

    def apply_civishot(self, instance):
        if self.current_frame is not None:
            self.status_label.text = "Processing iPhone Tone & Detail..."
            processed = CiviShotEngine.process_image(self.current_frame)
            cv2.imwrite("civishot_output.jpg", processed)
            
            buf = cv2.flip(processed, 0).tobytes()
            texture = Texture.create(size=(processed.shape[1], processed.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img_widget.texture = texture
            self.status_label.text = "✨ CiviShot Look Applied!"

if __name__ == '__main__':
    CiviShotApp().run()

