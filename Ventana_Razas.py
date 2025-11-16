import tkinter as tk
from tkinter import Toplevel, messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import mariadb

# --- CONFIGURACIONES GENERALES ---
APP_TITLE = 'Gestión de Razas'
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


class Ventana_Razas(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title(APP_TITLE)
        self.geometry("700x500")
        self.config(bg=BG)

        # --- FORMULARIO ---
        form = tk.LabelFrame(
            self, text="Formulario de Razas",
            bg=BG, fg=ACCENT, font=("Arial", 12, "bold"),
            padx=10, pady=10
        )
        form.pack(pady=10, fill="x", padx=20)

        labels = ["Nombre:", "Origen:", "Color:"]
        self.campos_raza = {}

        # --- Usamos GRID dentro del formulario ---
        for i, campo in enumerate(labels):
            tk.Label(
                form, text=campo, bg=BG, fg=TEXT_COLOR,
                font=("Arial", 10, "bold"), width=12, anchor="w"
            ).grid(row=i, column=0, padx=5, pady=8, sticky="w")

            entry = tk.Entry(form, width=40, relief="solid", justify="center")
            entry.grid(row=i, column=1, padx=10, pady=8)
            self.campos_raza[campo] = entry

        # --- BOTONES EXTRA ---
        acciones = tk.Frame(self, bg=BG)
        acciones.pack(pady=15)

        tk.Button(
            acciones, text="Limpiar Campos",
            command=self.limpiar_campos_raza,
            bg="#6c757d", fg="white", relief="flat",
            padx=20, pady=8, font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=10)

        # --- PANEL DE BOTONES CRUD ---
        panel = tk.Frame(self, bg=BG)
        panel.pack(pady=10)

        botones = [
            ("Registrar Raza", ACCENT, self.registrar_raza),
            ("Modificar Raza", ACCENT, self.modificar_raza),
            ("Consultar Razas", ACCENT_DARK, self.consultar_razas),
            ("Eliminar Raza", "#B33A3A", self.eliminar_raza)
        ]

        for texto, color, comando in botones:
            tk.Button(
                panel, text=texto, command=comando,
                bg=color, fg="white", activebackground=ACCENT_DARK,
                relief="flat", padx=16, pady=10,
                font=("Arial", 10, "bold"), cursor="hand2", width=20
            ).pack(pady=6)

    # --- LIMPIAR CAMPOS ---
    def limpiar_campos_raza(self):
        for entry in self.campos_raza.values():
            entry.delete(0, tk.END)

    # --- CRUD: REGISTRAR ---
    def registrar_raza(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            nombre = self.campos_raza["Nombre:"].get()
            origen = self.campos_raza["Origen:"].get() or "Sin registro"
            color = self.campos_raza["Color:"].get() or "Sin definir"

            if not nombre:
                messagebox.showwarning("Campos vacíos", "Debes ingresar el nombre de la raza.")
                return

            sql = """INSERT INTO Razas (nombre, origen, color)
                     VALUES (%s, %s, %s)"""
            cursor.execute(sql, (nombre, origen, color))
            conn.commit()
            messagebox.showinfo("Éxito", f"Raza '{nombre}' registrada correctamente.")
            self.limpiar_campos_raza()

        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar la raza:\n{e}")
        finally:
            conn.close()

    # --- CRUD: MODIFICAR ---
    def modificar_raza(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            pk = simpledialog.askinteger("Modificar", "Ingrese el ID de la Raza a modificar:")
            if not pk:
                return

            nombre = self.campos_raza["Nombre:"].get()
            origen = self.campos_raza["Origen:"].get()
            color = self.campos_raza["Color:"].get()

            sql = """UPDATE Razas
                     SET nombre=%s, origen=%s, color=%s
                     WHERE pk_raza=%s"""
            cursor.execute(sql, (nombre, origen, color, pk))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Raza ID {pk} modificada correctamente.")
            else:
                messagebox.showwarning("No encontrado", f"No se encontró la raza con ID {pk}.")
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo modificar:\n{e}")
        finally:
            conn.close()

    # --- CRUD: ELIMINAR ---
    def eliminar_raza(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            pk = simpledialog.askinteger("Eliminar", "Ingrese el ID de la raza a eliminar:")
            if not pk:
                return

            confirm = messagebox.askyesno("Confirmar", f"¿Deseas eliminar la raza con ID {pk}?")
            if not confirm:
                return

            cursor.execute("DELETE FROM Razas WHERE pk_raza=%s", (pk,))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Raza ID {pk} eliminada.")
            else:
                messagebox.showwarning("No encontrado", "ID inexistente.")
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")
        finally:
            conn.close()

    # --- CRUD: CONSULTAR ---
    def consultar_razas(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            cursor.execute("SELECT pk_raza, nombre, origen, color FROM Razas")
            datos = cursor.fetchall()

            ventana = Toplevel(self)
            ventana.title("Consulta de Razas")
            ventana.geometry("800x400")
            ventana.config(bg=BG)

            cols = ("ID", "Nombre", "Origen", "Color")
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
