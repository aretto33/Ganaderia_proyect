import tkinter as tk
from tkinter import Toplevel, messagebox, simpledialog, ttk
import mariadb
from conexion import conectar_bd

# --- CONFIGURACIONES GENERALES ---
APP_TITLE = 'Gestión de Pesajes'
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
        return conn, cursor
    except mariadb.Error as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar:\n{e}")
        return None, None


class Ventana_Pesajes(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master)
        self.title(APP_TITLE)
        self.geometry("700x550")
        self.config(bg=BG)

        # --- FORMULARIO ---
        form = tk.LabelFrame(
            self, text="Registro de Pesajes",
            bg=BG, fg=ACCENT, font=("Arial", 12, "bold"),
            padx=10, pady=10
        )
        form.pack(pady=10, fill="x", padx=20)

        labels = [
            "Peso (kg):",
            "Fecha (AAAA-MM-DD):",
            "ID Animal:"
        ]

        self.campos_pesaje = {}

        for i, campo in enumerate(labels):
            tk.Label(
                form, text=campo, bg=BG, fg=TEXT_COLOR,
                font=("Arial", 10, "bold"), width=15, anchor="w"
            ).grid(row=i, column=0, padx=5, pady=8)

            entry = tk.Entry(form, width=40, relief="solid", justify="center")
            entry.grid(row=i, column=1, padx=10, pady=8)
            self.campos_pesaje[campo] = entry

        # --- BOTONES EXTRA ---
        acciones = tk.Frame(self, bg=BG)
        acciones.pack(pady=15)

        tk.Button(
            acciones, text="Limpiar Campos",
            command=self.limpiar_campos_pesaje,
            bg="#6c757d", fg="white", relief="flat",
            padx=20, pady=8, font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=10)

        # --- PANEL DE BOTONES CRUD ---
        panel = tk.Frame(self, bg=BG)
        panel.pack()

        botones = [
            ("Registrar Pesaje", ACCENT, self.registrar_pesaje),
            ("Modificar Pesaje", ACCENT, self.modificar_pesaje),
            ("Consultar Pesajes", ACCENT_DARK, self.consultar_pesaje),
            ("Eliminar Pesaje", "#B33A3A", self.eliminar_pesaje)
        ]

        for texto, color, comando in botones:
            tk.Button(
                panel, text=texto, command=comando,
                bg=color, fg="white", activebackground=ACCENT_DARK,
                relief="flat", padx=16, pady=10,
                font=("Arial", 10, "bold"), cursor="hand2", width=20
            ).pack(pady=6)

    # --- LIMPIAR FORMULARIO ---
    def limpiar_campos_pesaje(self):
        for entry in self.campos_pesaje.values():
            entry.delete(0, tk.END)

    # --- REGISTRAR PESAJE ---
    def registrar_pesaje(self):
        conn, cursor = conectar_bd()
        if not conn: return

        try:
            peso = self.campos_pesaje["Peso (kg):"].get()
            fecha = self.campos_pesaje["Fecha (AAAA-MM-DD):"].get()
            fk_animal = self.campos_pesaje["ID Animal:"].get()

            if not peso or not fecha or not fk_animal:
                messagebox.showwarning("Campos vacíos", "Debes completar todos los campos.")
                return

            sql = """INSERT INTO Pesajes (peso, fecha, fk_animal)
                     VALUES (%s, %s, %s)"""
            cursor.execute(sql, (peso, fecha, fk_animal))
            conn.commit()

            messagebox.showinfo("Éxito", "Pesaje registrado correctamente.")
            self.limpiar_campos_pesaje()
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar:\n{e}")
        finally:
            conn.close()

    # --- MODIFICAR ---
    def modificar_pesaje(self):
        conn, cursor = conectar_bd()
        if not conn: return

        try:
            pk = simpledialog.askinteger("Modificar", "Ingrese el ID del pesaje a modificar:")
            if not pk: return

            peso = self.campos_pesaje["Peso (kg):"].get()
            fecha = self.campos_pesaje["Fecha (AAAA-MM-DD):"].get()
            fk_animal = self.campos_pesaje["ID Animal:"].get()

            sql = """UPDATE Pesajes
                     SET peso=%s, fecha=%s, fk_animal=%s
                     WHERE pk_pesaje=%s"""
            cursor.execute(sql, (peso, fecha, fk_animal, pk))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Pesaje ID {pk} modificado correctamente.")
            else:
                messagebox.showwarning("No encontrado", "ID inexistente.")
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo modificar:\n{e}")
        finally:
            conn.close()

    # --- ELIMINAR ---
    def eliminar_pesaje(self):
        conn, cursor = conectar_bd()
        if not conn: return

        try:
            pk = simpledialog.askinteger("Eliminar", "Ingrese el ID del pesaje a eliminar:")
            if not pk: return

            confirm = messagebox.askyesno("Confirmar", f"¿Deseas eliminar el pesaje con ID {pk}?")
            if not confirm: return

            cursor.execute("DELETE FROM Pesajes WHERE pk_pesaje=%s", (pk,))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Pesaje ID {pk} eliminado.")
            else:
                messagebox.showwarning("No encontrado", "ID inexistente.")
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")
        finally:
            conn.close()

    # --- CONSULTAR ---
    def consultar_pesaje(self):
        conn, cursor = conectar_bd()
        if not conn: return

        try:
            cursor.execute("SELECT pk_pesaje, peso, fecha, fk_animal FROM Pesajes")
            datos = cursor.fetchall()

            ventana = Toplevel(self)
            ventana.title("Consulta de Pesajes")
            ventana.geometry("650x350")
            ventana.config(bg=BG)

            cols = ("ID", "Peso (kg)", "Fecha", "ID Animal")
            tabla = ttk.Treeview(ventana, columns=cols, show="headings", height=15)

            for c in cols:
                tabla.heading(c, text=c)
                tabla.column(c, anchor="center", width=140)

            for fila in datos:
                tabla.insert("", "end", values=fila)

            tabla.pack(padx=10, pady=10, fill="both", expand=True)
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo consultar:\n{e}")
        finally:
            conn.close()
