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

# --- Conexión a la base de datos ---
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


# --- Clase principal de la aplicación ---
class APP(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.config(bg=BG)

        self.create_banner()
        self.create_navbar()

    # --- Crear banner superior ---
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

    # --- Crear barra de navegación ---
    def create_navbar(self):
        navbar = tk.Frame(self, bg="#e9eaf6", pady=8)
        navbar.pack(fill="x")

        buttons = [
            ("Inicio de sesión", self.login),
            ("Propósito", self.proposito),
            ("Ayuda", self.ayuda)
        ]

        for text, cmd in buttons:
            b = tk.Button(navbar, text=text, command=cmd, bg=ACCENT, fg="white",
                          activebackground=ACCENT_DARK, relief="flat",
                          padx=16, pady=8, font=("Arial", 11, "bold"))
            b.pack(side="left", padx=10)

    # --- Métodos de botones ---
    def login(self):
        #crear la interfaz para iniciar sessión , lo cual se requiere para ingresar a la base de datos principal
        ventana_login = Toplevel(app)
        ventana_login.title("Inicio de sesión")
        ventana_login.geometry("400x950")
        ventana_login.config(background="#DCC197")

        descrip = tk.Label(
        ventana_login,
        text="Se debe iniciar sesión para acceder a la base de datos",
        bg="#DCC197",
        font= ("Comic Sans MS",10,"bold"),
        wraplength=350,
        justify="center"
        )
        descrip.pack(pady=(20,10))
        #---Cargar imágen----
        try:
            log_image=Image.open("login.png")
            log_image=log_image.resize((350,350))
            self.log_photo = ImageTk.PhotoImage(log_image)
            label_img = tk.Label(ventana_login,image=self.log_photo,background="#DCC197")
            label_img.pack(pady=(5,20))
        except Exception as e:
            print("no se pudo cargar la imagen")
            tk.Label(ventana_login, text="error de imágen")

        #----------------------------Sección Usuario---------------------------
        label_user=tk.Label(ventana_login, text="Usuario: ", bg="#DCC197", font=("Arial",10, "bold")).pack(pady=(5,5))
        log_user = tk.Entry(ventana_login, width=30, justify="center", relief="solid", bg="#C09A71")
        log_user.pack(pady=(0, 15))

        label_passw=tk.Label(ventana_login, text="Contraseña: ", bg="#DCB597", font=("Arial",10, "bold")).pack(pady=(5,5))
        log_passw = tk.Entry(ventana_login, show="*", width=30, justify="center", relief="solid", bg="#C09A71")
        log_passw.pack(pady=(0,20))

        label_check=tk.Label(ventana_login, text="Tipo de usuario: ", bg="#DCB597", font=("Arial",10, "bold")).pack(pady=(5,5))
        frame_roles = tk.Frame(ventana_login, bg="#DCC197")
        frame_roles.pack(pady=(2, 10))

                        
        # Variable para guardar la selección (solo uno puede seleccionarse)
        rol_usuario = tk.StringVar(value="")  

        # Frame para colocar los Radiobutton en una sola fila
        frame_roles = tk.Frame(ventana_login, bg="#DCC197")
        frame_roles.pack(pady=(2, 15))

        # Radiobuttons alineados en fila (horizontal)
        tk.Radiobutton(
            frame_roles, text="Veterinario", variable=rol_usuario, value="Veterinario",
            bg="#DCC197", activebackground="#DCC197", font=("Arial", 9)
        ).pack(side="left", padx=15)

        tk.Radiobutton(
            frame_roles, text="Productor", variable=rol_usuario, value="Productor",
            bg="#DCC197", activebackground="#DCC197", font=("Arial", 9)
        ).pack(side="left", padx=15)

        tk.Radiobutton(
            frame_roles, text="Comprador", variable=rol_usuario, value="Comprador",
            bg="#DCC197", activebackground="#DCC197", font=("Arial", 9)
        ).pack(side="left", padx=15)

        opcion = tk.StringVar(value="Seleccionar")
        selec_produc = tk.OptionMenu(ventana_login, opcion, "Opción 1", "Opción 2", "Opción 3")
        selec_produc.pack(pady=(3,3))


        log_button = tk.Button(
        ventana_login,
            text="Iniciar sesión",
            bg="#C09A71",
            font=("Arial", 10, "bold"),
            width=18,
            relief="raised",
            cursor="hand2"
        )

        log_button.pack(pady=10)
        regis_button = tk.Button(
            ventana_login,
            text="Crear usuario",
            bg="#C09A71",
            font=("Arial", 10, "bold"),
            width=18,
            relief="raised",
            cursor="hand2"
        )
        regis_button.pack(pady=10)


    def proposito(self):
        messagebox.showinfo("Propósito", "Sistema de gestión ganadera")

    def ayuda(self):
        messagebox.showinfo("Ayuda", "Contacte al administrador para soporte")

    def logout(self):
        pass


# --- Programa principal ---
if __name__ == "__main__":
    app = APP()
    app.mainloop()
