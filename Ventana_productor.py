import tkinter as tk
from tkinter import Toplevel, messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import mariadb

# --- CONFIGURACIONES GENERALES ---
APP_TITLE = 'Gestión de Productores'
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
    
class Ventana_Productor(tk.Toplevel):  # ← hereda de Toplevel, no Frame
    def __init__(self, master=None):
        super().__init__(master)
        self.title(APP_TITLE)
        self.geometry("700x550")
        self.config(bg=BG)

        # --- FORMULARIO ---
        form = tk.LabelFrame(
            self, text="Formulario de Productores",
            bg=BG, fg=ACCENT, font=("Arial", 12, "bold"),
            padx=10, pady=10
        )
        form.pack(pady=10, fill="x", padx=20)

        labels = [
            "Nombre:", "Apellido Pat:","Apellido Mat:","Predio:"
        ]
        self.campos_Productor = {}

        for i, campo in enumerate(labels):
            tk.Label(
                form, text=campo, bg=BG, fg=TEXT_COLOR,
                font=("Arial", 10, "bold"), width=12, anchor="w"
            ).grid(row=i, column=0, padx=5, pady=8, sticky="w")

            entry = tk.Entry(form, width=40, relief="solid", justify="center")
            entry.grid(row=i, column=1, padx=10, pady=8)
            self.campos_Productor[campo] = entry

       
        # --- BOTONES EXTRA ---
        acciones = tk.Frame(self, bg=BG)
        acciones.pack(pady=15)

        tk.Button(
            acciones, text="Limpiar Campos",
            command=self.limpiar_campos_Productor,
            bg="#6c757d", fg="white", relief="flat",
            padx=20, pady=8, font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=10)

     # --- PANEL DE BOTONES CRUD ---
        panel = tk.Frame(self, bg=BG)
        panel.pack(pady=10)

        botones = [
            ("Registrar Productor", ACCENT, self.registrar_Productor),
            ("Modificar Productor", ACCENT, self.modificar_Productor),
            ("Consultar Productor", ACCENT_DARK, self.consultar_Productor),
            ("Eliminar Productor", "#B33A3A", self.eliminar_Productor)
        ]

        for texto, color, comando in botones:
            tk.Button(
                panel, text=texto, command=comando,
                bg=color, fg="white", activebackground=ACCENT_DARK,
                relief="flat", padx=16, pady=10,
                font=("Arial", 10, "bold"), cursor="hand2", width=20
            ).pack(pady=6)


    # --- LIMPIAR CAMPOS ---
    def limpiar_campos_Productor(self):
        for entry in self.campos_Productor.values():
            entry.delete(0, tk.END)

    # --- CRUD: REGISTRAR ---
    def registrar_Productor(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            nombre = self.campos_Productor["Nombre:"].get()
            apellido_pat = self.campos_Productor["Apellido Pat:"].get()
            apellido_mat = self.campos_Productor["Apellido Mat:"].get()
            predio = self.campos_Productor["Predio:"].get()

            if not  nombre or not predio:
                messagebox.showwarning("Campos vacíos", "Debes ingresar nombre y predio.")
                return

            sql = """INSERT INTO Productores ( nombre, apellido_pat, apellido_mat, fk_predio)
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, ( nombre, apellido_pat, apellido_mat, predio))
            conn.commit()
            messagebox.showinfo("Éxito", f"Productor '{ nombre}' registrado correctamente.")
            self.limpiar_campos_predio()

        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el Productor:\n{e}")
        finally:
            conn.close()

    # --- CRUD: MODIFICAR ---
    def modificar_Productor(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            pk = simpledialog.askinteger("Modificar", "Ingrese el ID del productor a modificar:")
            if not pk:
                return

            nombre = self.campos_Productor["Nombre:"].get()
            apellido_pat = self.campos_Productor["Apellido Pat:"].get()
            apellido_mat = self.campos_Productor["Apellido Mat:"].get()
            predio = self.campos_Productor["Predio:"].get()

            sql = """UPDATE Productores
                     SET nombre=%s, apellido_pat=%s, apellido_mat=%s, fk_predio=%s WHERE pk_productor=%s"""
            cursor.execute(sql, (nombre, apellido_pat, apellido_mat, predio, pk))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Productor ID {pk} modificado correctamente.")
            else:
                messagebox.showwarning("No encontrado", f"No se encontró el Productor con ID {pk}.")
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo modificar:\n{e}")
        finally:
            conn.close()

    # --- CRUD: ELIMINAR ---
    def eliminar_Productor(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            pk = simpledialog.askinteger("Eliminar", "Ingrese el ID del Productor a eliminar:")
            if not pk:
                return

            confirm = messagebox.askyesno("Confirmar", f"¿Deseas eliminar el Productor con ID {pk}?")
            if not confirm:
                return

            cursor.execute("DELETE FROM Productores WHERE pk_productor=%s", (pk,))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Productor ID {pk} eliminado.")
            else:
                messagebox.showwarning("No encontrado", "ID inexistente.")
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")
        finally:
            conn.close()

    # --- CRUD: CONSULTAR ---
    def consultar_Productor(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            cursor.execute("SELECT pk_productor, nombre, apellido_pat, apellido_mat, fk_predio FROM Productores")
            datos = cursor.fetchall()

            ventana = Toplevel(self)
            ventana.title("Consulta de Produtores")
            ventana.geometry("800x400")
            ventana.config(bg=BG)

            cols = ("ID", "nombre", "apellido Pat", "appellido Mat", "predio")
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