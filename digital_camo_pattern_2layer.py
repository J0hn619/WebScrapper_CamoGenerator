from PIL import Image, ImageDraw, ImageTk
import math
import tkinter as tk
import os
import random
import time
import colorsys


class ColorWheelPicker:
    def __init__(self, master):
        self.master = master
        self.master.title("Color Wheel Picker")
        self.master.geometry("400x500")

        self.canvas = tk.Canvas(self.master, width=300, height=300)
        self.canvas.pack()

        self.colorwheel_image = self.create_colorwheel()
        self.colorwheel_tk = ImageTk.PhotoImage(self.colorwheel_image)

        self.colorwheel_item = self.canvas.create_image(150, 150, image=self.colorwheel_tk)
        self.canvas.bind("<Button-1>", self.on_color_selected)

        self.selected_color = tk.Label(self.master, text="Selected Color: ")
        self.selected_color.pack()

        self.pick_color_button = tk.Button(self.master, text="Pick Color", command=self.pick_color)
        self.pick_color_button.pack()

        self.generate_button = tk.Button(self.master, text="Generate Camo", command=self.generate_camo)
        self.generate_button.pack()

        self.selected_rgb_color = None

    def create_colorwheel(self):
        size = 300
        image = Image.new("RGB", (size, size), "white")
        draw = ImageDraw.Draw(image)

        for y in range(size):
            for x in range(size):
                hue = math.atan2(y - size / 2, x - size / 2) % (2 * math.pi)
                saturation = math.sqrt((x - size / 2) ** 2 + (y - size / 2) ** 2) / (size / 2)
                value = 1.0
                rgb_color = self.hsv_to_rgb(hue, saturation, value)
                draw.point((x, y), fill=(int(rgb_color[0] * 255), int(rgb_color[1] * 255), int(rgb_color[2] * 255)))

        return image

    def hsv_to_rgb(self, h, s, v):
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return r, g, b

    def on_color_selected(self, event):
        x, y = event.x, event.y
        hue = math.atan2(y - 150, x - 150) % (2 * math.pi)
        saturation = math.sqrt((x - 150) ** 2 + (y - 150) ** 2) / 150
        value = 1.0
        rgb_color = self.hsv_to_rgb(hue, saturation, value)
        self.selected_color.config(text=f"Selected Color: {rgb_color}")
        self.selected_rgb_color = (
            int(rgb_color[0] * 255),
            int(rgb_color[1] * 255),
            int(rgb_color[2] * 255)
        )

    def pick_color(self):
        rgb, hex_color = tk.colorchooser.askcolor(title="Pick a color", initialcolor=self.selected_rgb_color)
        if rgb:
            self.selected_color.config(text=f"Selected Color: {rgb}")
            self.selected_rgb_color = rgb

    def generate_camo(self):
        if self.selected_rgb_color:
            try:
                base_camo_pattern = self.create_digital_camo(self.selected_rgb_color)
                if base_camo_pattern:
                    Layer2Generator(base_camo_pattern)
            except Exception as e:
                print(f"Error generating camo: {e}")
        else:
            print("Please select a color first!")

    def create_digital_camo(self, base_color):
        directory = r"J:\webscrap\fullcamodrop"
        if not os.path.exists(directory):
            os.makedirs(directory)

        img = Image.new('RGB', (1024, 1024), color='white')
        draw = ImageDraw.Draw(img)

        # Define three colors based on the selected color
        color1 = base_color
        color2 = self.shift_color(base_color, 20)
        color3 = self.shift_color(base_color, -20)

        colors = [color1, color2, color3]

        # Define sizes of squares
        sizes = [10, 30, 60, 100, 150, 200]

        for size in sizes:
            for x in range(0, 1024, size):
                for y in range(0, 1024, size):
                    color = random.choice(colors)
                    draw.rectangle([x, y, x + size, y + size], fill=color)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(directory, f"camo_pattern_{timestamp}.png")
        try:
            img.save(filename)
            print(f"Layer 1 - Camo pattern saved to {filename}")
            return Image.open(filename)
        except Exception as e:
            print(f"Error saving camo pattern: {e}")
            return None

    def shift_color(self, color, shift):
        r = self.clamp(color[0] + shift)
        g = self.clamp(color[1] + shift)
        b = self.clamp(color[2] + shift)
        return r, g, b

    def clamp(self, value):
        return max(0, min(value, 255))


class Layer2Generator:
    def __init__(self, base_camo_pattern):
        self.directory = r"J:\webscrap"
        self.output_directory = r"J:\webscrap\fullcamodrop"
        if not os.path.exists(self.directory):
            print("Directory not found.")
            return

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        self.image_list = os.listdir(self.directory)
        self.base_camo_pattern = base_camo_pattern
        self.generate_layer_2()

    def generate_layer_2(self):
        num_squares = random.randint(25, 100)
        num_images = random.randint(3, 5)
        selected_images = random.sample(self.image_list, num_images)

        new_img = self.base_camo_pattern.copy()
        draw = ImageDraw.Draw(new_img)

        for _ in range(num_squares):
            image_path = os.path.join(self.directory, random.choice(selected_images))
            if os.path.isfile(image_path):
                try:
                    img = Image.open(image_path)
                    img = img.convert("RGBA")
                    img = img.resize((random.randint(50, 100), random.randint(50, 100)))

                    img_location = (random.randint(0, 1024), random.randint(0, 1024))
                    new_img.paste(img, img_location, img)
                except Exception as e:
                    print(f"Error processing image: {image_path} - {e}")

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        final_filename = f"final_output_{timestamp}.png"
        save_path = os.path.join(self.output_directory, final_filename)
        try:
            new_img.save(save_path)
            print(f"Layer 2 - Image created: {save_path}")
        except Exception as e:
            print(f"Error saving Layer 2 image: {e}")


def main():
    root = tk.Tk()
    color_wheel_picker = ColorWheelPicker(root)
    root.mainloop()


if __name__ == "__main__":
    main()
