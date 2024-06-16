import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageEnhance, ImageOps, ImageTk
from PIL.ExifTags import TAGS


class ExifViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EXIF Viewer")
        self.root.geometry("700x600")
        self.root.minsize(700, 600)
        self.root.iconbitmap("assets/icon.ico")
        self.set_window_icon(self.root, "assets/icon.ico")
        self.status_var = tk.StringVar()

        self.show_startup_window()

    def set_window_icon(self, window, icon_path):
        icon = Image.open(icon_path)
        icon = ImageTk.PhotoImage(icon)
        window.iconphoto(False, icon)

    def show_startup_window(self):
        startup_window = tk.Toplevel(self.root)
        startup_window.geometry("300x200")
        startup_window.title("Starting...")
        self.set_window_icon(startup_window, "assets/icon.ico")
        tk.Label(startup_window, text="Starting Application...", font=("Arial", 14)).pack(expand=True)
        self.root.after(3000, startup_window.destroy)
        self.root.after(4000, self.create_main_window)

    def create_main_window(self):
        self.create_menu()
        self.create_widgets()
        self.create_status_bar()
        self.root.deiconify()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save EXIF Data", command=self.save_exif_to_file)
        file_menu.add_command(label="Export EXIF Data to CSV", command=self.export_exif_to_csv)
        file_menu.add_command(label="Clear Image", command=self.clear_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Rotate Image", command=self.rotate_image)
        edit_menu.add_command(label="Apply Grayscale Filter", command=lambda: self.apply_filter("grayscale"))
        edit_menu.add_command(label="Apply Sepia Filter", command=lambda: self.apply_filter("sepia"))
        edit_menu.add_command(label="Invert Colors", command=lambda: self.apply_filter("invert"))
        edit_menu.add_command(label="Enhance Sharpness", command=self.enhance_sharpness)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        batch_menu = tk.Menu(menu_bar, tearoff=0)
        batch_menu.add_command(label="Batch Process Images", command=self.batch_process_images)
        menu_bar.add_cascade(label="Batch", menu=batch_menu)
        
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def create_widgets(self):
        self.image_path_var = tk.StringVar()
        self.image_label = tk.Label(self.root, text="Select Image or Enter Path:", font=("Times New Roman", 14))
        self.image_label.pack()

        self.image_entry = tk.Entry(self.root, textvariable=self.image_path_var, width=40)
        self.image_entry.pack()

        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_image, font=("Times New Roman", 12))
        self.browse_button.pack()

        self.preview_label = tk.Label(self.root)
        self.preview_label.pack()

        self.show_button = tk.Button(self.root, text="Show EXIF", command=self.show_exif, font=("Times New Roman", 12))
        self.show_button.pack()

        self.image_info_label = tk.Label(self.root, text="", font=("Times New Roman", 12))
        self.image_info_label.pack()

    def create_status_bar(self):
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_var.set("Ready")

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.image_path_var.set(file_path)
            self.show_preview(file_path)
            self.display_image_info(file_path)
            self.status_var.set("Image Loaded: " + file_path)

    def show_preview(self, image_path):
        try:
            self.img = Image.open(image_path)
            self.img.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(self.img)
            self.preview_label.config(image=photo)
            self.preview_label.image = photo
        except Exception as e:
            self.status_var.set("Error displaying image preview")
            print("Error displaying image preview:", e)

    def display_image_info(self, image_path):
        try:
            with Image.open(image_path) as img:
                info = f"Dimensions: {img.size[0]} x {img.size[1]}\n"
                info += f"File Size: {os.path.getsize(image_path)} bytes\n"
                info += f"Color Mode: {img.mode}\n"
                self.image_info_label.config(text=info)
        except Exception as e:
            self.status_var.set("Error getting image info")
            print("Error getting image info:", e)

    def show_exif(self):
        image_path = self.image_path_var.get()
        if image_path and (os.path.exists(image_path) and image_path.lower().endswith(('.jpg', '.jpeg', '.png'))):
            exif_data = self.get_exif_data(image_path)
            if exif_data:
                exif_info = "EXIF Data:\n"
                for tag, value in exif_data.items():
                    exif_info += f"{tag}: {value}\n"
                self.show_popup("EXIF Information", exif_info)
            else:
                self.show_popup("EXIF Information", "No EXIF data found.")
        else:
            self.show_popup("Error", "Invalid file path or format.")
            self.status_var.set("Invalid file path or format.")

    def get_exif_data(self, image_path):
        try:
            with Image.open(image_path) as img:
                exif_data = img._getexif()
                if exif_data:
                    exif_info = {}
                    for tag, value in exif_data.items():
                        if tag in TAGS:
                            exif_info[TAGS[tag]] = value
                    return exif_info
                else:
                    return None
        except Exception as e:
            self.status_var.set("Error reading EXIF data")
            print("Error reading EXIF data:", e)
            return None

    def show_popup(self, title, message):
        popup = tk.Toplevel()
        popup.title(title)
        text = tk.Text(popup)
        text.insert(tk.END, message)
        text.pack()

    def save_exif_to_file(self):
        exif_data = self.get_exif_data(self.image_path_var.get())
        if exif_data:
            save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if save_path:
                with open(save_path, 'w') as file:
                    for tag, value in exif_data.items():
                        file.write(f"{tag}: {value}\n")
                self.status_var.set("EXIF data saved: " + save_path)
        else:
            self.show_popup("Error", "No EXIF data to save.")
            self.status_var.set("No EXIF data to save.")

    def export_exif_to_csv(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if file_paths:
            save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if save_path:
                with open(save_path, 'w', newline='') as csvfile:
                    fieldnames = ['File', 'Tag', 'Value']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for file_path in file_paths:
                        exif_data = self.get_exif_data(file_path)
                        if exif_data:
                            for tag, value in exif_data.items():
                                writer.writerow({'File': file_path, 'Tag': tag, 'Value': value})
                self.status_var.set("EXIF data exported to CSV: " + save_path)
        else:
            self.show_popup("Error", "No files selected for export.")
            self.status_var.set("No files selected for export.")

    def clear_image(self):
        self.image_path_var.set("")
        self.preview_label.config(image="")
        self.image_info_label.config(text="")
        self.status_var.set("Image and data cleared")

    def rotate_image(self):
        if hasattr(self, 'img'):
            self.img = self.img.rotate(90, expand=True)
            photo = ImageTk.PhotoImage(self.img)
            self.preview_label.config(image=photo)
            self.preview_label.image = photo
            self.status_var.set("Image rotated 90 degrees")
        else:
            self.show_popup("Error", "No image to rotate.")
            self.status_var.set("No image to rotate.")

    def apply_filter(self, filter_type):
        if hasattr(self, 'img'):
            if filter_type == "grayscale":
                self.img = ImageOps.grayscale(self.img)
            elif filter_type == "sepia":
                sepia = [(r//2, g//2, b//2) for r, g, b in self.img.getdata()]
                self.img.putdata(sepia)
            elif filter_type == "invert":
                self.img = ImageOps.invert(self.img.convert("RGB"))
            photo = ImageTk.PhotoImage(self.img)
            self.preview_label.config(image=photo)
            self.preview_label.image = photo
            self.status_var.set(f"Applied {filter_type} filter")
        else:
            self.show_popup("Error", f"No image to apply {filter_type} filter.")
            self.status_var.set(f"No image to apply {filter_type} filter.")

    def enhance_sharpness(self):
        if hasattr(self, 'img'):
            enhancer = ImageEnhance.Sharpness(self.img)
            self.img = enhancer.enhance(2.0)
            photo = ImageTk.PhotoImage(self.img)
            self.preview_label.config(image=photo)
            self.preview_label.image = photo
            self.status_var.set("Image sharpness enhanced")
        else:
            self.show_popup("Error", "No image to enhance sharpness.")
            self.status_var.set("No image to enhance sharpness.")

    def batch_process_images(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if file_paths:
            for file_path in file_paths:
                exif_data = self.get_exif_data(file_path)
                if exif_data:
                    print(f"EXIF data for {file_path}:")
                    for tag, value in exif_data.items():
                        print(f"{tag}: {value}")
            self.status_var.set("Batch processing completed")
        else:
            self.show_popup("Error", "No files selected for batch processing.")
            self.status_var.set("No files selected for batch processing.")

    def show_about(self):
        about_message = "EXIF Viewer v2.0\nDeveloped by Johann Kramer"
        self.show_popup("About", about_message)

def main():
    root = tk.Tk()
    app = ExifViewerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
