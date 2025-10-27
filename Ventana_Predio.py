import tkinter as tk
from tkinter import Toplevel, messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import mariadb

# --- CONFIGURACIONES GENERALES ---
APP_TITLE = 'Gestión de Predios'
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
    
class Ventana_Predios(tk.Toplevel):  # ← hereda de Toplevel, no Frame
    def __init__(self, master=None):
        super().__init__(master)
        self.title(APP_TITLE)
        self.geometry("700x500")
        self.config(bg=BG)

        # --- PANEL DE BOTONES CRUD ---
        panel = tk.Frame(self, bg=BG)
        panel.pack(pady=10)

        botones = [
            ("Registrar Predio", ACCENT, self.registrar_predio),
            ("Modificar Predio", ACCENT, self.modificar_predio),
            ("Eliminar Predio", "#B33A3A", self.eliminar_predio),
            ("Consultar Predio", ACCENT_DARK, self.consultar_predios)
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
            self, text="Formulario de Predios",
            bg=BG, fg=ACCENT, font=("Arial", 12, "bold"),
            padx=10, pady=10
        )
        form.pack(pady=10, fill="x", padx=20)

        labels = [
            "Direccion:",
            "Estado:",
            "Municipio:"
        ]

        self.campos_predio = {}
        for campo in labels:
            fila = tk.Frame(form, bg=BG)
            fila.pack(fill="x", pady=5)
            tk.Label(fila, text=campo, bg=BG, fg=TEXT_COLOR, font=("Arial", 10, "bold")).pack(side="left", padx=5)
            entry = tk.Entry(fila, width=40, relief="solid", justify="center")
            entry.pack(side="left", padx=10)
            self.campos_predio[campo] = entry

        # --- BOTONES EXTRA ---
        acciones = tk.Frame(self, bg=BG)
        acciones.pack(pady=15)

        tk.Button(
            acciones, text="Limpiar Campos",
            command=self.limpiar_campos_predio,
            bg="#6c757d", fg="white", relief="flat",
            padx=20, pady=8, font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=10)

    # --- LIMPIAR CAMPOS ---
    def limpiar_campos_predio(self):
        for entry in self.campos_predio.values():
            entry.delete(0, tk.END)

    # --- CRUD: REGISTRAR ---
    def registrar_predio(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            direccion = self.campos_predio["Direccion:"].get()
            estado = self.campos_predio["Estado:"].get()
            municipio = self.campos_predio["Municipio:"].get() 

            if not direccion or not estado or not municipio:
                messagebox.showwarning("Campos vacíos", "Debes ingresar nombre y fecha.")
                return

            sql = """INSERT INTO Predios (direccion, estado, municipio)
                     VALUES (%s, %s, %s)"""
            cursor.execute(sql, (direccion, estado, municipio))
            conn.commit()
            messagebox.showinfo("Éxito", f"Predio '{direccion}' registrado correctamente.")
            self.limpiar_campos_predio()

        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el predio:\n{e}")
        finally:
            conn.close()

    # --- CRUD: MODIFICAR ---
    def modificar_predio(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            pk = simpledialog.askinteger("Modificar", "Ingrese el ID del animal a modificar:")
            if not pk:
                return

            direccion = self.campos_predio["Direccion:"].get()
            estado = self.campos_predio["Estado:"].get()
            municipio = self.campos_predio["Municipio:"].get() 

            sql = """UPDATE Predios
                     SET direccion=%s, Estado=%s, Municipio=%s"""
            cursor.execute(sql, (direccion, estado, municipio, pk))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Predio ID {pk} modificado correctamente.")
            else:
                messagebox.showwarning("No encontrado", f"No se encontró el predio con ID {pk}.")
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo modificar:\n{e}")
        finally:
            conn.close()

    # --- CRUD: ELIMINAR ---
    def eliminar_predio(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            pk = simpledialog.askinteger("Eliminar", "Ingrese el ID del predio a eliminar:")
            if not pk:
                return

            confirm = messagebox.askyesno("Confirmar", f"¿Deseas eliminar el predio con ID {pk}?")
            if not confirm:
                return

            cursor.execute("DELETE FROM Predios WHERE pk_predio=%s", (pk,))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Predio ID {pk} eliminado.")
            else:
                messagebox.showwarning("No encontrado", "ID inexistente.")
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")
        finally:
            conn.close()

    # --- CRUD: CONSULTAR ---
    def consultar_predios(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            cursor.execute("SELECT pk_predio, direccion, estado,municipio FROM Predios")
            datos = cursor.fetchall()

            ventana = Toplevel(self)
            ventana.title("Consulta de Predios")
            ventana.geometry("800x400")
            ventana.config(bg=BG)

            cols = ("ID", "Direccion", "Estado", "Municipio")
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
