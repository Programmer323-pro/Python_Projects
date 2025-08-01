from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from PIL import Image as PILImage
import io


class ImageViewer(BoxLayout):
    def __init__(self, **kwargs):
        super(ImageViewer, self).__init__(orientation='vertical', **kwargs)

        # Image Widget
        self.img = Image(allow_stretch=True, keep_ratio=True)
        self.add_widget(self.img)

        # Controls
        controls = BoxLayout(size_hint_y=0.1)
        open_btn = Button(text="📂 باز کردن تصویر")
        open_btn.bind(on_press=self.open_file)

        self.slider = Slider(min=0.1, max=3, value=1, step=0.1)
        self.slider.bind(value=self.zoom_image)

        controls.add_widget(open_btn)
        controls.add_widget(self.slider)
        self.add_widget(controls)

        self.original_texture = None

    def open_file(self, instance):
        content = FileChooserIconView(filters=["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif", "*.webp", "*.*"])
        popup = Popup(title='انتخاب تصویر', content=content, size_hint=(0.9, 0.9))

        def select_file(instance, selection):
            if selection:
                self.load_image(selection[0])
                popup.dismiss()

        content.bind(on_submit=select_file)
        popup.open()

    def load_image(self, filepath):
        try:
            pil_image = PILImage.open(filepath).convert("RGBA")
            data = pil_image.tobytes()
            tex = Texture.create(size=pil_image.size, colorfmt='rgba')
            tex.blit_buffer(data, colorfmt='rgba', bufferfmt='ubyte')
            tex.flip_vertical()

            self.original_texture = tex
            self.img.texture = tex
            self.slider.value = 1  # reset zoom

        except Exception as e:
            print(f"خطا در باز کردن فایل: {e}")

    def zoom_image(self, instance, value):
        if self.original_texture:
            self.img.size_hint = (None, None)
            self.img.size = (self.original_texture.width * value, self.original_texture.height * value)
            self.img.texture = self.original_texture


class ImageViewerApp(App):
    def build(self):
        self.title = "نمایشگر تصویر حرفه‌ای با Kivy"
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        return ImageViewer()


if __name__ == '__main__':
    ImageViewerApp().run()
