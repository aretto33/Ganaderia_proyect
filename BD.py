import tkinter as tk
from tkinter import Toplevel
from tkinter import messagebox
from PIL import Image, ImageTk
import mariadb


APP_TITLE = 'GANA_CONTROL'
WINDOW_SIZE = "900x600"
BG = "#f4f3ec"
ACCENT = "#36448B"
ACCENT_DARK = "#2A3E75"
TEXT_COLOR = "#222"

class APP_BD(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.config(bg=BG)
        self.menu_widgets()

        self.create_banner()
    def conectar_bd():
        try:
            conn = mariadb.connect(
                host='localhost',
                user='arletteg',
                password='123456',
                database='Proyecto_Ganaderia'
            )
            cursor = conn.cursor()
            print("Conexión exitosa a la base de datos.")
            messagebox.showinfo("Conexión", "Conexión exitosa a la base de datos.")
            return conn, cursor
        except mariadb.Error as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar:\n{e}")
            return None, None
   

    def create_banner(self):
        banner_frame = tk.Frame(self, bg=ACCENT)
        banner_frame.pack(fill="x")

        try:
            img = Image.open("banner.png")
            img = img.resize((900, 180))
            self.banner_img = ImageTk.PhotoImage(img)
            banner = tk.Label(banner_frame, image=self.banner_img, bg=ACCENT)
            banner.pack(fill="x")
        except Exception:
            banner_label = tk.Label(
                banner_frame,
                text="🐄 Bienvenido a GANA_CONTROL",
                font=("Arial", 20, "bold"),
                bg=ACCENT,
                fg="white",
                height=3
            )
            banner_label.pack(fill="x")

    def menu_widgets(self):
        self.side_panel_frame = tk.Frame(self.master, bg="lightblue", width=60)
        self.side_panel_frame.pack(side="left", fill = "y")

        self.menu_button = tk.Button(self.side_panel_frame, text="-")
        self.menu_button.pack(side="top", pady=10)

    def toggle_menu():
        if not self.menu_open:
            self.button.pack(side="top", pady =5)





 
    




if __name__ == "__main__":
    app = APP_BD()
    app.mainloop()