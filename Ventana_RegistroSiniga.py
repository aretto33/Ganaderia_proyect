import tkinter as tk
from tkinter import Toplevel, messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import mariadb

# --- CONFIGURACIONES GENERALES ---
APP_TITLE = 'Gestión de Registro Siniga'
BG = "#e7d7c1"          # Fondo beige claro
ACCENT = "#8b5e3c"      # Café medio
ACCENT_DARK = "#6b452e" # Café oscuro
TEXT_COLOR = "#000000"  # Café muy oscuro
BTN_LIGHT = "#a9825a"   # Café claro
BTN_DARK = "#7a563b"    # Café fuerte
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
    
class Ventana_registroSiniga(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title(APP_TITLE)
        self.geometry("700x550")
        self.config(bg=BG)

        # --- FORMULARIO ---
        form = tk.LabelFrame(
            self, text="Formulario de Registro",
            bg=BG, fg=ACCENT, font=("Arial", 12, "bold"),
            padx=10, pady=10
        )
        form.pack(side="top", fill="x", padx=20, pady=30)

        labels = ["UPP:", "fk_animal:", "Arete:"]
        self.campos_Registro = {}

        # --- Usamos GRID dentro del formulario ---
        for i, campo in enumerate(labels):
            tk.Label(
                form, text=campo, bg=BG, fg=TEXT_COLOR,
                font=("Arial", 10, "bold"), width=12, anchor="w"
            ).grid(row=i, column=0, padx=5, pady=8, sticky="w")

            entry = tk.Entry(form, width=40, relief="solid", justify="center")
            entry.grid(row=i, column=1, padx=10, pady=8)
            self.campos_Registro[campo] = entry

        # --- BOTÓN EXTRA ABAJO ---
        acciones = tk.Frame(self, bg=BG)
        acciones.pack(side="top", pady=10)
        tk.Button(
            acciones, text="Limpiar Campos",
            command=self.limpiar_campos_Registro,
            bg="#6c757d", fg="white", relief="flat",
            padx=10, pady=8, font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack()

        # --- PANEL DE BOTONES CRUD ---
        panel = tk.Frame(self, bg=BG)
        panel.pack(side="top", pady=10)

        botones = [
            ("Registrar Registro_Siniga", ACCENT, self.registrar_Registro),
            ("Modificar Registro Siniga", ACCENT, self.modificar_Registro),
            ("Consultar Registro Siniga", ACCENT_DARK, self.consultar_Registro),
            ("Eliminar Registro Siniga", "#B33A3A", self.eliminar_Registro)
        ]

        for texto, color, comando in botones:
            tk.Button(
                panel, text=texto, command=comando,
                bg=color, fg="white", activebackground=ACCENT_DARK,
                relief="flat", padx=16, pady=10,
                font=("Arial", 10, "bold"), cursor="hand2", width=25
            ).pack(pady=6)



    # --- LIMPIAR CAMPOS ---
    def limpiar_campos_Registro(self):
        for entry in self.campos_Registro.values():
            entry.delete(0, tk.END)

    # --- CRUD: REGISTRAR ---
    def registrar_Registro(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            UPP = self.campos_Registro["UPP:"].get()
            fk_animal = self.campos_Registro["fk_animal:"].get()
            arete = self.campos_Registro["Arete:"].get() 

            if not UPP or not fk_animal or not arete:
                messagebox.showwarning("Campos vacíos", "Debes ingresar Una UPP y un arete.")
                return

            sql = """INSERT INTO Registro_SINIGA (UPP, fk_animal, arete)
                     VALUES (%s, %s, %s)"""
            cursor.execute(sql, (UPP, fk_animal, arete))
            conn.commit()
            messagebox.showinfo("Éxito", f"UPP'{UPP}' registrado correctamente.")
            self.limpiar_campos_Registro()

        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el UPP:\n{e}")
        finally:
            conn.close()

    # --- CRUD: MODIFICAR ---
    def modificar_Registro(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            pk = simpledialog.askinteger("Modificar", "Ingrese el ID del animal a modificar:")
            if not pk:
                return

            UPP = self.campos_Registro["UPP:"].get()
            fk_animal = self.campos_Registro["fk_animal:"].get()
            arete = self.campos_Registro["Arete:"].get() 

            sql = """UPDATE Registro_SINIGA
                     SET UPP=%s, fk_animal=%s, arete=%s WHERE id=%s"""
            cursor.execute(sql, ( UPP, fk_animal, arete, pk))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"UPP {pk} modificado correctamente.")
            else:
                messagebox.showwarning("No encontrado", f"No se encontró el Registro con ID {pk}.")
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo modificar:\n{e}")
        finally:
            conn.close()

    # --- CRUD: ELIMINAR ---
    def eliminar_Registro(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            pk = simpledialog.askinteger("Eliminar", "Ingrese el ID del Registro a eliminar:")
            if not pk:
                return

            confirm = messagebox.askyesno("Confirmar", f"¿Deseas eliminar el Rergistro con ID {pk}?")
            if not confirm:
                return

            cursor.execute("DELETE FROM Registro_SINIGA WHERE id=%s", (pk,))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Registro ID {pk} eliminado.")
            else:
                messagebox.showwarning("No encontrado", "id inexistente.")
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")
        finally:
            conn.close()

    # --- CRUD: CONSULTAR ---
    def consultar_Registro(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            cursor.execute("SELECT id, UPP, fk_animal,arete FROM Registro_SINIGA")
            datos = cursor.fetchall()

            ventana = Toplevel(self)
            ventana.title("Consulta de Registros Siniga")
            ventana.geometry("800x400")
            ventana.config(bg=BG)

            cols = ("id", "UPP", "fk_animal", "arete")
            tabla = ttk.Treeview(ventana, columns=cols, show="headings", height=15)
            for c in cols:
                tabla.heading(c, text=c)
                tabla.column(c, anchor="center", width=120)

            for fila in datos:
                tabla.insert("", "end", values=fila)

            tabla.pack(padx=10, pady=10, fill="both", expand=True)
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo consultar:\n{e}")
        finally:
            conn.close()        
