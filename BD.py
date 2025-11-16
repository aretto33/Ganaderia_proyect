import tkinter as tk
from tkinter import messagebox, filedialog, Toplevel
from PIL import Image, ImageTk
import mariadb
import shutil
from Ventana_Animal import Ventana_Animales
from Ventana_Predio import Ventana_Predios
from Ventana_productor import Ventana_Productor
import os
import webbrowser   # se usa, estaba bien
import sys
from Ventana_RegistroSiniga import Ventana_registroSiniga
from Ventana_Pesajes import Ventana_Pesajes
from Ventana_SeguimientoVet import Ventana_SeguimientoVet
from Ventana_Razas import Ventana_Razas
from Ventana_Venta import Ventana_Ventas

APP_TITLE = 'GANA_CONTROL'
WINDOW_SIZE = "900x600"
BG = "#ceae93"
ACCENT = "#79634C"
ACCENT_DARK = "#C6AD85"
TEXT_COLOR = "#222"

# -------------------------------
# Conexión a la base de datos
# -------------------------------
def conectar_bd():
    try:
        conn = mariadb.connect(
            host='localhost',
            user='AdminGanaderia',
            password='2025',
            database='Proyecto_Ganaderia'
        )
        cursor = conn.cursor()
        print("Conexión exitosa a la base de datos.")
        return conn, cursor
    except mariadb.Error as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar:\n{e}")
        return None, None


# -------------------------------
# Clase principal del sistema BD
# -------------------------------
class APP_BD(tk.Tk):
    def __init__(self, usuario, rol):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.config(bg=BG)

        self.usuario = usuario
        self.rol = rol
        self.menu_open = False

        self.create_banner()
        self.menu_widgets()
        self.tramites_botones()

    def create_banner(self):
        banner_frame = tk.Frame(self, bg=ACCENT)
        banner_frame.pack(fill="x")

        tk.Label(
            banner_frame,
            text=f"🐮 Bienvenido {self.usuario} ({self.rol})",
            font=("Arial", 14, "bold"),
            bg=ACCENT,
            fg="white"
        ).pack(pady=10)

        try:
            img = Image.open("banner.png")
            img = img.resize((900, 180))
            self.banner_img = ImageTk.PhotoImage(img)
            tk.Label(banner_frame, image=self.banner_img, bg=ACCENT).pack(fill="x")

        except Exception:
            tk.Label(
                banner_frame,
                text="🐄 Bienvenido a GANA_CONTROL",
                font=("Arial", 20, "bold"),
                bg=ACCENT,
                fg="white",
                height=3
            ).pack(fill="x")
#----------Botones --------------------------
    def menu_widgets(self):
        self.side_panel_frame = tk.Frame(self, bg="#916D4C", width=60)
        self.side_panel_frame.pack(side="left", fill="y")

        self.menu_button = tk.Button(
            self.side_panel_frame,
            text="≡",
            bg="#916D4C",
            command=self.toggle_menu
        )
        self.menu_button.pack(side="top", pady=10)
#------------------Opciones de cada tabla----------------------
        self.menu_buttons = []
        opciones = {
            "Animales": self.abrir_ventana_animales,
            "Predios": self.abrir_ventana_predio,
            "Productor": self.abrir_ventana_productores,
            "Pesaje": self.abrir_ventana_pesaje,
            "Registro": self.abrir_ventana_siiniga,
            "SegVet":self.abrir_ventana_SegVet,
            "Venta":self.abrir_ventana_Venta ,
            "Raza":self.abrir_ventana_Razas
        }
#----------------------------------------
        for texto, comando in opciones.items():
            boton = tk.Button(
                self.side_panel_frame,
                text=texto,
                bg="white",
                relief="flat",
                command=comando
            )
            self.menu_buttons.append(boton)

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

    def tramites_botones(self):
        frame_central = tk.Frame(self, bg=BG)
        frame_central.pack(expand=True, fill="both")

        tk.Label(frame_central,
            text="Tramites",
            font=("Arial", 28, "bold"),
            bg=BG,
            fg=ACCENT
        ).pack(pady=2)

        botones_frame = tk.Frame(frame_central, bg=BG)
        botones_frame.pack(pady=20)

        botones = [
            ("Inscripción UPP", self.opciones_upp),
            ("Trámites Datos", lambda: messagebox.showinfo("Trámite", "Inicie nuevo")),
            ("Trámite 3", lambda: messagebox.showinfo("Trámite", "Inicie nuevo"))
        ]

        for texto, comando in botones:
            btn = tk.Button(
                botones_frame,
                text=texto,
                font=("Arial", 14, "bold"),
                bg=ACCENT,
                width=20,
                height=2,
                relief="flat",
                command=comando
            )
            btn.pack(pady=10)

    def descargar_inscrip(self):
        ruta_pdf = "solicitud_pgn.pdf"

        ruta_destino = filedialog.asksaveasfilename(   # corregido asksaveasfilename
            defaultextension="*.pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Guardar como"
        )

        if ruta_destino:
            try:
                shutil.copyfile(ruta_pdf, ruta_destino)
                messagebox.showinfo("Correcto", "Archivo guardado correctamente ")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

    def abrir_inscrip(self):
        ruta_pdf = "solicitud_pgn.pdf"
        if os.path.exists(ruta_pdf):
            webbrowser.open(ruta_pdf)  #  corregido
        else:
            messagebox.showerror("Error", "No existe el archivo")

    def opciones_upp(self):
        ventana = Toplevel(self)
        ventana.title("Opciones de inscripción UPP")
        ventana.geometry("400x300")
        ventana.config(background="#DCC197")

        tk.Label(
            ventana,
            text="Seleccione la opción preferente",
            bg="#DCC197",
            font=("Comic Sans MS", 10, "bold"),
            wraplength=350,
            justify="center"
        ).pack(pady=(20, 10))

        buton_frame = tk.Frame(ventana, bg=BG)
        buton_frame.pack(pady=20)

        botones = [
            ("Abrir solicitud PDF", self.abrir_inscrip),
            ("Descargar solicitud PDF", self.descargar_inscrip),
        ]

        for texto, comando in botones:
            btn = tk.Button(
                buton_frame,
                text=texto,
                font=("Arial", 14, "bold"),
                bg=ACCENT,
                width=22,
                height=2,
                relief="flat",
                command=comando
            )
            btn.pack(pady=10)

    def abrir_ventana_animales(self):
        ventana_animales = Ventana_Animales(self)
        ventana_animales.grab_set()

    def abrir_ventana_predio(self):
        ventana_predio = Ventana_Predios(self)
        ventana_predio.grab_set()

    def abrir_ventana_productores(self):
        ventana_productor = Ventana_Productor(self)
        ventana_productor.grab_set()
    
    def abrir_ventana_siiniga(self):
        ventana_siiniga = Ventana_registroSiniga(self)
        ventana_siiniga.grab_set

    def abrir_ventana_pesaje(self):
        ventana_pesaje = Ventana_Pesajes(self)
        ventana_pesaje.grab_set()
        
    def abrir_ventana_Razas(self):
        ventana_raza = Ventana_Razas(self)
        ventana_raza.grab_set()
    
    def abrir_ventana_Venta(self):
        ventana_venta = Ventana_Ventas(self)
        ventana_venta.grab_set()
    
    def abrir_ventana_SegVet(self):
        ventana_pesaje = Ventana_Pesajes(self)
        ventana_pesaje.grab_set()
    


# -------------------------------
# Programa principal
# -------------------------------
if __name__ == "__main__":
    usuario = sys.argv[1] if len(sys.argv) > 1 else "Desconocido"
    rol = sys.argv[2] if len(sys.argv) > 2 else "Sin rol"
    print(f"Inició sesión: {usuario} ({rol})")

    app = APP_BD(usuario, rol)
    app.mainloop()
