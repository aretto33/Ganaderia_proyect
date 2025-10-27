import sys
import tkinter as tk
from tkinter import Toplevel
from tkinter import messagebox
from PIL import Image, ImageTk
import mariadb
import subprocess


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
        user='AdminGanaderia',
        password='2025',
        database='Proyecto_Ganaderia'
        )
        cursor = conn.cursor()
        print("Conexión exitosa a la base de datos.")
        messagebox.showinfo("Conexión", "Conexión exitosa a la base de datos.")
        return conn, cursor
    except mariadb.Error as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar:\n{e}")
        return None, None
    
    # --- Validar credenciales de usuario ---
def verificar_credenciales(usuario, password, rol):
    conn, cursor = conectar_bd()
    if not conn:
        return False, "Error de conexión"

    try:
        query = "SELECT usuario, password, rol FROM usuarios WHERE usuario=%s AND rol=%s"
        cursor.execute(query, (usuario, rol))
        resultado = cursor.fetchone() 

        if resultado:
            db_user, db_pass, db_rol = resultado
            if password == db_pass:  
                return True, db_rol
            else:
                return False, "Contraseña incorrecta"
        else:
            return False, "Usuario o rol no encontrado"
    except Exception as e:
        return False, f"Error: {e}"
    finally:
        conn.close()


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
    
    # --- Sección descriptiva principal ---
    def create_main_description(self):
        main_descripcion = tk.Frame(self, bg="#e9eaf6")
        main_descripcion.pack(fill="both", expand=True, pady=10, padx=20)

        # --- Título ---
        titulo = tk.Label(
            main_descripcion,
            text="🐄 Bienvenido a GANA_CONTROL",
            font=("Arial", 20, "bold"),
            bg="#e9eaf6",
            fg="#2A3E75"
        )
        titulo.pack(pady=(15, 10))

        # --- Subtítulo ---
        subtitulo = tk.Label(
            main_descripcion,
            text="Sistema integral de gestión ganadera",
            font=("Arial", 14, "italic"),
            bg="#e9eaf6",
            fg="#555"
        )
        subtitulo.pack(pady=(0, 15))

        # --- Texto principal ---
        descripcion = tk.Label(
            main_descripcion,
            text=(
                "GANA_CONTROL es una herramienta diseñada para optimizar la administración de la "
                "producción ganadera. Permite registrar información sobre animales, controlar la "
                "alimentación, gestionar ventas y llevar trazabilidad de los datos en una base "
                "de datos centralizada.\n\n"
                "Su objetivo principal es facilitar la toma de decisiones mediante el control "
                "efectivo y digitalizado de las actividades del sector pecuario."
            ),
            wraplength=800,
            justify="center",
            bg="#e9eaf6",
            fg="#222",
            font=("Arial", 12)
        )
        descripcion.pack(pady=10)

        # --- Imagen ilustrativa ---
        try:
            img = Image.open("principal.png")
            img = img.resize((700, 400))
            self.main_photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(main_descripcion, image=self.main_photo, bg="#e9eaf6")
            img_label.pack(pady=15)
        except Exception as e:
            print("Error al cargar la imagen:", e)
            tk.Label(
                main_descripcion,
                text="(Imagen ilustrativa no disponible)",
                bg="#e9eaf6",
                fg="#888",
                font=("Arial", 10, "italic")
            ).pack(pady=15)

        # --- Frase final ---
        lema = tk.Label(
            main_descripcion,
            text="📊 Innovación y control para un futuro ganadero sostenible",
            font=("Arial", 11, "bold"),
            fg="#36448B",
            bg="#e9eaf6"
        )
        lema.pack(pady=(5, 20))


    # --- Métodos de botones ---
    def login(self):
        #crear la interfaz para iniciar sesión , lo cual se requiere para ingresar a la base de datos principal
        ventana_login = Toplevel(self)
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
            cursor="hand2",
            command=self.nuevo_user
        )


        regis_button.pack(pady=10)
                # --- Acción del botón "Iniciar sesión" ---
        def intentar_login():
            usuario = log_user.get()
            contra = log_passw.get()
            rol = rol_usuario.get()

            exito, info = verificar_credenciales(usuario, contra, rol)
            if exito:
                messagebox.showinfo("Acceso permitido", f"Bienvenido {usuario} ({info})")
                ventana_login.destroy()
                #Abrir la ventana principal de la BD
                try:
                    subprocess.Popen(["python", "BD.py", usuario, info])

                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo abrir el sistema principal:\n{e}")


            
            else:
                messagebox.showerror("Error de inicio de sesión", info)
        
        # Asociar función al botón
        log_button.config(command=intentar_login)
#--------------------------------Sección crear usuario-------------------------------------------------------
# --- Métodos de botones ---
    def nuevo_user(self):
        #crear la interfaz para crear usuario , lo cual se requiere para INSERT VALUE en la tabla de Usuarios
        ventana_login = Toplevel(self)
        ventana_login.title("Crear Usuario")
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
            log_image=Image.open("new.png")
            log_image=log_image.resize((350,350))
            self.log_photo = ImageTk.PhotoImage(log_image)
            label_img = tk.Label(ventana_login,image=self.log_photo,background="#DCC197")
            label_img.pack(pady=(5,20))
        except Exception as e:
            print("no se pudo cargar la imagen")
            tk.Label(ventana_login, text="error de imágen")

        #----------------------------Crear Usuario---------------------------
        label_user=tk.Label(ventana_login, text="Usuario: ", bg="#DCC197", font=("Arial",10, "bold")).pack(pady=(5,5))
        self.entry_usuario= tk.Entry(ventana_login, width=30, justify="center", relief="solid", bg="#C09A71")
        self.entry_usuario.pack(pady=(0, 15))

        label_passw=tk.Label(ventana_login, text="Contraseña: ", bg="#DCB597", font=("Arial",10, "bold")).pack(pady=(5,5))
        self.entry_passw= tk.Entry(ventana_login, show="*", width=30, justify="center", relief="solid", bg="#C09A71")
        self.entry_passw.pack(pady=(0,20))

        tk.Label(ventana_login, text="Tipo de usuario:", bg="#DCC197").pack(pady=5)
        self.rol_usuario = tk.StringVar(value="")  
        roles_frame = tk.Frame(ventana_login, bg="#DCC197")
        roles_frame.pack(pady=5)

        for rol in ["Veterinario", "Productor", "Comprador"]:
            tk.Radiobutton(
                roles_frame, text=rol, variable=self.rol_usuario, value=rol,
                bg="#DCC197", font=("Arial", 9)
            ).pack(side="left", padx=10)


        regis_button = tk.Button(
            ventana_login,
            text="Guardar Usuario",
            bg="#C09A71",
            font=("Arial", 10, "bold"),
            width=18,
            relief="raised",
            cursor="hand2",
            command=self.registrar_user
        )
        regis_button.pack(pady=10)
    
    def registrar_user(self):
        usuario = self.entry_usuario.get()
        contra = self.entry_passw.get()
        rol = self.rol_usuario.get()

        if not usuario or not contra or not rol :
            messagebox.showwarning("Campos vacío", "Se deben rellenar los campos")
            return
        
        conn,cursor= conectar_bd()
        if not conn:
            return
        
        try:
            sql ="INSERT INTO Usuarios(usuario, password, rol) VALUES (%s, %s, %s)"
            cursor.execute(sql, (usuario, contra, rol))
            conn.commit()
            messagebox.showinfo("✓",f"Usuario '{usuario}' correctamente")
        except mariadb.Error as e:
            messagebox.showerror("Error",f"No se pudo registrar el usuario:\n{e}")
        finally:
            conn.close()

    
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
