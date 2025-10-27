import tkinter as tk
from tkinter import Toplevel
from tkinter import messagebox
from PIL import Image, ImageTk
import mariadb
from Ventana_Animal import Ventana_Animales
from Ventana_Predio import Ventana_Predios
from fpdf import FPDF
import sys


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

        self.menu_open = False # Estado del menú
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

    usuario = sys.argv[1] if len(sys.argv) > 1 else "Desconocido"
    rol = sys.argv[2] if len(sys.argv) > 2 else "Sin rol"
    print(f"Inició sesión: {usuario} ({rol})")

    def create_banner(self):
        banner_frame = tk.Frame(self, bg=ACCENT)
        banner_frame.pack(fill="x")

        tk.Label(self, text=f"🐮 Bienvenido {usuario} ({rol})", font=("Arial", 14, "bold"), bg=BG, fg="#2A3E75").pack(pady=10)
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
    

# Recibir usuario y rol del login


    def menu_widgets(self):
        self.side_panel_frame = tk.Frame(self, bg="#916D4C", width=60)
        self.side_panel_frame.pack(side="left", fill = "y")
        #botón para abrir/cerrar menu
        self.menu_button = tk.Button(
        self.side_panel_frame,
        text="≡",
        bg="#916D4C",
        command=self.toggle_menu)
        self.menu_button.pack(side="top", pady=10)

        self.menu_buttons = []
        opciones = {"Animales":self.abrir_ventana_animales,
                    "Predios":self.abrir_ventana_predio,
                    "Productor": lambda: messagebox.showinfo("Info", "Ventana Productor aún no implementada"),
                    "Pesaje": lambda: messagebox.showinfo("Info", "Ventana Pesaje aún no implementada"),
                    "Registro": lambda: messagebox.showinfo("Info", "Ventana Registro aún no implementada")}
    

        for texto,comando in opciones.items():
            boton = tk.Button(
                self.side_panel_frame,
                text=texto,
                bg="white",
                relief="flat",
                command=comando
            )
            self.menu_buttons.append(boton)
            #botones ocultos

    def toggle_menu(self):
        if not self.menu_open:
            for boton in self.menu_buttons:
                boton.pack(side="top", fill="x", pady=5, padx=5)
                self.menu_open = True
                self.menu_button.config(text="x")
        else:
             for boton in self.menu_buttons:
                boton.pack_forget()
                self.menu_open = False
                self.menu_button.config(text="≡")
        
    def abrir_ventana_animales(self):
        ventana_animales = Ventana_Animales(self)
        ventana_animales.grab_set()  # bloquea interacción con ventana principal mientras esté abierta
        
    def abrir_ventana_predio(self):
        ventana_predio = Ventana_Predios(self)
        ventana_predio.grab_set()  # bloquea interacción con ventana principal mientras esté abierta



if __name__ == "__main__":
    app = APP_BD()
    app.mainloop()
