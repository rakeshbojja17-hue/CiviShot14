import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from PIL import Image as PILImage, ImageEnhance, ImageFilter

class CiviShotEngine:
    @staticmethod
    def process_image(image_path):
        if not os.path.exists(image_path):
            return None
        
        img = PILImage.open(image_path)
        
        # 1. Dynamic Tone & Brightness (HDR Recovery)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.15)
        
        # 2. iPhone Contrast & Saturation Boost
        contrast = ImageEnhance.Contrast(img)
        img = contrast.enhance(1.2)
        
        color = ImageEnhance.Color(img)
        img = color.enhance(1.25)
        
        # 3. Sharpening & Noise Reduction Look
        img = img.filter(ImageFilter.SHARPEN)
        
        output_path = "civishot_output.png"
        img.save(output_path)
        return output_path

class CiviShotApp(App):
    def build(self):
        self.title = 'CiviShot AI'
        self.layout = BoxLayout(orientation='vertical')
        
        self.img_widget = Image()
        self.layout.add_widget(self.img_widget)
        
        self.status_label = Label(text="CiviShot Ready", size_hint_y=0.1)
        self.layout.add_widget(self.status_label)
        
        btn_layout = BoxLayout(size_hint_y=0.15)
        btn_process = Button(text="✨ Apply CiviShot iPhone Look", on_press=self.apply_civishot)
        btn_layout.add_widget(btn_process)
        
        self.layout.add_widget(btn_layout)
        return self.layout

    def apply_civishot(self, instance):
        self.status_label.text = "Processing Photo..."
        # Demo processing
        processed_path = CiviShotEngine.process_image("input.png")
        if processed_path:
            self.img_widget.source = processed_path
            self.img_widget.reload()
            self.status_label.text = "✨ iPhone Tone Applied!"

if __name__ == '__main__':
    CiviShotApp().run()

