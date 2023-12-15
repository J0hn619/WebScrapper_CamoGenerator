from PIL import Image, ImageDraw
import tkinter as tk
import os
import random
import time


class ColorCamoGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Camo Generator")
        self.master.geometry("400x500")

        self.selected_color = (255, 255, 255)

        self.color_preview = tk.Canvas(self.master, width=200, height=200, bg="#FFFFFF")
        self.color_preview.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.hex_label = tk.Label(self.master, text="HEX:", font=("Arial", 12))
        self.hex_label.grid(row=1, column=0, padx=10, pady=5)
        self.hex_entry = tk.Entry(self.master)
        self.hex_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5)
        self.hex_entry.insert(tk.END, "#FFFFFF")
        self.hex_entry.bind("<Return>", self.update_color)

        self.red_label = tk.Label(self.master, text="Red:", font=("Arial", 10))
        self.red_label.grid(row=2, column=0, padx=10, pady=5)
        self.red_scale = tk.Scale(self.master, from_=0, to=255, orient="horizontal", length=150,
                                  command=self.update_color_slider)
        self.red_scale.grid(row=2, column=1, padx=10, pady=5)

        self.green_label = tk.Label(self.master, text="Green:", font=("Arial", 10))
        self.green_label.grid(row=3, column=0, padx=10, pady=5)
        self.green_scale = tk.Scale(self.master, from_=0, to=255, orient="horizontal", length=150,
                                    command=self.update_color_slider)
        self.green_scale.grid(row=3, column=1, padx=10, pady=5)

        self.blue_label = tk.Label(self.master, text="Blue:", font=("Arial", 10))
        self.blue_label.grid(row=4, column=0, padx=10, pady=5)
        self.blue_scale = tk.Scale(self.master, from_=0, to=255, orient="horizontal", length=150,
                                   command=self.update_color_slider)
        self.blue_scale.grid(row=4, column=1, padx=10, pady=5)

        self.generate_button = tk.Button(self.master, text="Generate Camo", command=self.generate_camo)
        self.generate_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        self.update_color()

    def update_color_slider(self, event=None):
        red_val = self.red_scale.get()
        green_val = self.green_scale.get()
        blue_val = self.blue_scale.get()
        self.selected_color = (red_val, green_val, blue_val)
        self.update_color()

    def update_color(self, event=None):
        hex_val = self.hex_entry.get()
        try:
            self.selected_color = tuple(int(hex_val[i:i + 2], 16) for i in (1, 3, 5))
        except ValueError:
            pass

        self.red_scale.set(self.selected_color[0])
        self.green_scale.set(self.selected_color[1])
        self.blue_scale.set(self.selected_color[2])
        self.color_preview.config(bg="#%02x%02x%02x" % self.selected_color)

    def generate_camo(self):
        img = self.generate_camo_pattern()
        if img:
            self.save_camo(img)

    def generate_camo_pattern(self):
        width, height = 4096, 4096
        img = Image.new('RGB', (width, height), color=self.selected_color)
        draw = ImageDraw.Draw(img)

        sizes = [10, 30, 60, 100, 150, 200]
        colors = [self.selected_color]
        for i in range(1, 4):
            colors.append(tuple(min(255, max(0, c + random.randint(-20, 20))) for c in self.selected_color))

        for size in sizes:
            for x in range(0, width, size):
                for y in range(0, height, size):
                    color = random.choice(colors)
                    draw.rectangle([x, y, x + size, y + size], fill=color)

        return img

    def save_camo(self, img):
        try:
            file_path = os.path.join(r"J:\webscrap\fullcamodrop", f"camo_4k_{time.strftime('%Y%m%d_%H%M%S')}.png")
            img.save(file_path)
            print(f"Saved camo successfully at {file_path}")
        except Exception as e:
            print(f"Error saving camo: {e}")


def main():
    root = tk.Tk()
    color_camo_generator = ColorCamoGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
