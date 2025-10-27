import tkinter as tk
from tkinter import Toplevel, messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import mariadb

# --- CONFIGURACIONES GENERALES ---
APP_TITLE = 'Gestión de Animales'
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
    
class Ventana_Animales(tk.Toplevel):  # ← hereda de Toplevel, no Frame
    def __init__(self, master=None):
        super().__init__(master)
        self.title(APP_TITLE)
        self.geometry("700x500")
        self.config(bg=BG)

        # --- PANEL DE BOTONES CRUD ---
        panel = tk.Frame(self, bg=BG)
        panel.pack(pady=10)

        botones = [
            ("Registrar Animal", ACCENT, self.registrar_animal),
            ("Modificar Animal", ACCENT, self.modificar_animal),
            ("Eliminar Animal", "#B33A3A", self.eliminar_animal),
            ("Consultar Animales", ACCENT_DARK, self.consultar_animales)
        ]

        for texto, color, comando in botones:
            tk.Button(
                panel, text=texto, command=comando,
                bg=color, fg="white", activebackground=ACCENT_DARK,
                relief="flat", padx=16, pady=10,
                font=("Arial", 10, "bold"), cursor="hand2", width=20
            ).pack(pady=6)

        # --- FORMULARIO ---
        form = tk.LabelFrame(
            self, text="Formulario de Animales",
            bg=BG, fg=ACCENT, font=("Arial", 12, "bold"),
            padx=10, pady=10
        )
        form.pack(pady=10, fill="x", padx=20)

        labels = [
            "Nombre:",
            "Fecha de nacimiento (AAAA-MM-DD):",
            "Cruze:",
            "ID Productor (fk):",
            "ID Raza (fk):"
        ]

        self.campos_animal = {}
        for campo in labels:
            fila = tk.Frame(form, bg=BG)
            fila.pack(fill="x", pady=5)
            tk.Label(fila, text=campo, bg=BG, fg=TEXT_COLOR, font=("Arial", 10, "bold")).pack(side="left", padx=5)
            entry = tk.Entry(fila, width=40, relief="solid", justify="center")
            entry.pack(side="left", padx=10)
            self.campos_animal[campo] = entry

        # --- BOTONES EXTRA ---
        acciones = tk.Frame(self, bg=BG)
        acciones.pack(pady=15)

        tk.Button(
            acciones, text="Limpiar Campos",
            command=self.limpiar_campos_animal,
            bg="#6c757d", fg="white", relief="flat",
            padx=20, pady=8, font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=10)

    # --- LIMPIAR CAMPOS ---
    def limpiar_campos_animal(self):
        for entry in self.campos_animal.values():
            entry.delete(0, tk.END)

    # --- CRUD: REGISTRAR ---
    def registrar_animal(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            nombre = self.campos_animal["Nombre:"].get()
            fecha = self.campos_animal["Fecha de nacimiento (AAAA-MM-DD):"].get()
            cruze = self.campos_animal["Cruze:"].get() or "Sin conocer"
            fk_productor = self.campos_animal["ID Productor (fk):"].get()
            fk_raza = self.campos_animal["ID Raza (fk):"].get()

            if not nombre or not fecha:
                messagebox.showwarning("Campos vacíos", "Debes ingresar nombre y fecha.")
                return

            sql = """INSERT INTO Animales (nombre, fecha_nacimiento, cruze, fk_productor, fk_raza)
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (nombre, fecha, cruze, fk_productor or None, fk_raza or None))
            conn.commit()
            messagebox.showinfo("Éxito", f"Animal '{nombre}' registrado correctamente.")
            self.limpiar_campos_animal()

        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el animal:\n{e}")
        finally:
            conn.close()

    # --- CRUD: MODIFICAR ---
    def modificar_animal(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            pk = simpledialog.askinteger("Modificar", "Ingrese el ID del animal a modificar:")
            if not pk:
                return

            nombre = self.campos_animal["Nombre:"].get()
            fecha = self.campos_animal["Fecha de nacimiento (AAAA-MM-DD):"].get()
            cruze = self.campos_animal["Cruze:"].get()
            fk_productor = self.campos_animal["ID Productor (fk):"].get()
            fk_raza = self.campos_animal["ID Raza (fk):"].get()

            sql = """UPDATE Animales
                     SET nombre=%s, fecha_nacimiento=%s, cruze=%s, fk_productor=%s, fk_raza=%s
                     WHERE pk_animal=%s"""
            cursor.execute(sql, (nombre, fecha, cruze, fk_productor or None, fk_raza or None, pk))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Animal ID {pk} modificado correctamente.")
            else:
                messagebox.showwarning("No encontrado", f"No se encontró el animal con ID {pk}.")
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo modificar:\n{e}")
        finally:
            conn.close()

    # --- CRUD: ELIMINAR ---
    def eliminar_animal(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            pk = simpledialog.askinteger("Eliminar", "Ingrese el ID del animal a eliminar:")
            if not pk:
                return

            confirm = messagebox.askyesno("Confirmar", f"¿Deseas eliminar el animal con ID {pk}?")
            if not confirm:
                return

            cursor.execute("DELETE FROM Animales WHERE pk_animal=%s", (pk,))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Animal ID {pk} eliminado.")
            else:
                messagebox.showwarning("No encontrado", "ID inexistente.")
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")
        finally:
            conn.close()

    # --- CRUD: CONSULTAR ---
    def consultar_animales(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            cursor.execute("SELECT pk_animal, nombre, fecha_nacimiento, cruze, fk_productor, fk_raza FROM Animales")
            datos = cursor.fetchall()

            ventana = Toplevel(self)
            ventana.title("Consulta de Animales")
            ventana.geometry("800x400")
            ventana.config(bg=BG)

            cols = ("ID", "Nombre", "Fecha Nac.", "Cruze", "FK Productor", "FK Raza")
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
