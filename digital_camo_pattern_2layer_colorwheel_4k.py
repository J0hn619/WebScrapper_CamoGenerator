from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
import os
import random

class ColorCamoGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Camo Generator")
        self.master.geometry("400x600")

        self.selected_color = "#FFFFFF"

        self.color_preview = tk.Canvas(self.master, width=200, height=200, bg="#FFFFFF")
        self.color_preview.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.rgb_label = tk.Label(self.master, text="RGB:", font=("Arial", 12))
        self.rgb_label.grid(row=1, column=0, padx=10, pady=5)

        self.red_label = tk.Label(self.master, text="Red:", font=("Arial", 10))
        self.red_label.grid(row=2, column=0, padx=10, pady=5)
        self.red_scale = tk.Scale(self.master, from_=0, to=255, orient="horizontal", length=150,
                                  command=self.update_color)
        self.red_scale.grid(row=2, column=1, padx=10, pady=5)

        self.green_label = tk.Label(self.master, text="Green:", font=("Arial", 10))
        self.green_label.grid(row=3, column=0, padx=10, pady=5)
        self.green_scale = tk.Scale(self.master, from_=0, to=255, orient="horizontal", length=150,
                                    command=self.update_color)
        self.green_scale.grid(row=3, column=1, padx=10, pady=5)

        self.blue_label = tk.Label(self.master, text="Blue:", font=("Arial", 10))
        self.blue_label.grid(row=4, column=0, padx=10, pady=5)
        self.blue_scale = tk.Scale(self.master, from_=0, to=255, orient="horizontal", length=150,
                                   command=self.update_color)
        self.blue_scale.grid(row=4, column=1, padx=10, pady=5)

        self.hex_label = tk.Label(self.master, text="HEX:", font=("Arial", 10))
        self.hex_label.grid(row=5, column=0, padx=10, pady=5)
        self.hex_entry = tk.Entry(self.master, width=10, font=("Arial", 10))
        self.hex_entry.grid(row=5, column=1, padx=10, pady=5)
        self.hex_entry.bind("<Return>", self.update_from_hex)

        self.generate_button = tk.Button(self.master, text="Generate Camo", command=self.generate_camo)
        self.generate_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.update_color()

    def update_color(self, event=None):
        red_val = self.red_scale.get()
        green_val = self.green_scale.get()
        blue_val = self.blue_scale.get()
        self.selected_color = "#{:02x}{:02x}{:02x}".format(red_val, green_val, blue_val)
        self.color_preview.config(bg=self.selected_color)
        self.hex_entry.delete(0, tk.END)
        self.hex_entry.insert(tk.END, self.selected_color)

    def update_from_hex(self, event=None):
        hex_value = self.hex_entry.get()
        if len(hex_value) == 7 and hex_value[0] == '#':
            try:
                red_val = int(hex_value[1:3], 16)
                green_val = int(hex_value[3:5], 16)
                blue_val = int(hex_value[5:], 16)
                self.red_scale.set(red_val)
                self.green_scale.set(green_val)
                self.blue_scale.set(blue_val)
                self.selected_color = hex_value
                self.color_preview.config(bg=self.selected_color)
            except ValueError:
                pass

    def generate_camo(self):
        img = Image.new('RGB', (4096, 4096), color=self.selected_color)
        draw = ImageDraw.Draw(img)

        sizes = [10, 30, 60, 100, 150, 200]
        colors = [self.selected_color]
        for i in range(1, 4):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            colors.append("#{:02x}{:02x}{:02x}".format(r, g, b))

        for size in sizes:
            for x in range(0, 4096, size):
                for y in range(0, 4096, size):
                    color = random.choice(colors)
                    draw.rectangle([x, y, x + size, y + size], fill=color)

        num_images = random.randint(25, 100)
        selected_images = os.listdir(r"J:\webscrap")
        for _ in range(num_images):
            self._paste_resized_image(img, selected_images)

        file_path = os.path.join(r"J:\webscrap\fullcamodrop", f"camo_4k_{Image.new('RGB', (1,1), color=self.selected_color).getpixel((0,0))}.png")
        img.save(file_path)
        print(f"Generated camo saved as {file_path}")

    def _paste_resized_image(self, base_image, image_list):
        image_path = os.path.join(r"J:\webscrap", random.choice(image_list))
        if os.path.isfile(image_path):
            try:
                resize_factor = random.uniform(0.33, 1.0)
                overlay_img = Image.open(image_path)
                overlay_img = overlay_img.convert("RGBA")
                overlay_img = overlay_img.resize((int(overlay_img.width * resize_factor),
                                                 int(overlay_img.height * resize_factor)))
                overlay_location = (random.randint(0, 4096), random.randint(0, 4096))
                base_image.paste(overlay_img, overlay_location, overlay_img)
            except Exception as e:
                print(f"Error processing image: {image_path} - {e}")

def main():
    root = tk.Tk()
    color_camo_generator = ColorCamoGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
