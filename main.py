import os
from PIL import Image, ImageTk
from PIL.ExifTags import TAGS
import tkinter as tk
from tkinter import filedialog, messagebox

class ExifViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EXIF Viewer")

        self.image_path_var = tk.StringVar()
        self.image_label = tk.Label(root, text="Bild auswählen oder Pfad eingeben:", font=("Times New Roman", 14))
        self.image_label.pack()

        self.image_entry = tk.Entry(root, textvariable=self.image_path_var, width=40)
        self.image_entry.pack()

        self.browse_button = tk.Button(root, text="Durchsuchen", command=self.browse_image, font=("Times New Roman", 12))
        self.browse_button.pack()

        self.preview_label = tk.Label(root)
        self.preview_label.pack()

        self.show_button = tk.Button(root, text="EXIF anzeigen", command=self.show_exif, font=("Times New Roman", 12))
        self.show_button.pack()

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Bilddateien", "*.jpg *.jpeg *.png")])
        if file_path:
            self.image_path_var.set(file_path)
            self.show_preview(file_path)

    def show_preview(self, image_path):
        try:
            img = Image.open(image_path)
            img.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(img)
            self.preview_label.config(image=photo)
            self.preview_label.image = photo
        except Exception as e:
            print("Fehler beim Anzeigen der Bildvorschau:", e)

    def show_exif(self):
        image_path = self.image_path_var.get()
        if image_path and (os.path.exists(image_path) and image_path.lower().endswith(('.jpg', '.jpeg', '.png'))):
            exif_data = self.get_exif_data(image_path)
            if exif_data:
                exif_info = "EXIF-Daten:\n"
                for tag, value in exif_data.items():
                    exif_info += f"{tag}: {value}\n"
                self.show_popup("EXIF Informationen", exif_info)
            else:
                self.show_popup("EXIF Informationen", "Keine EXIF-Daten gefunden.")
        else:
            self.show_popup("Fehler", "Ungültiger Dateipfad oder Dateiformat.")

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
            print("Fehler beim Lesen der EXIF-Daten:", e)
            return None

    def show_popup(self, title, message):
        popup = tk.Toplevel()
        popup.title(title)

        text = tk.Text(popup)
        text.insert(tk.END, message)
        text.pack()

def main():
    root = tk.Tk()
    app = ExifViewerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()