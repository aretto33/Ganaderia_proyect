import tkinter as tk
from tkinter import Toplevel, messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import mariadb

# --- CONFIGURACIONES GENERALES ---
APP_TITLE = 'Gestión de Seguimiento Veterinario'
BG = "#f4f3ec"
ACCENT = "#36448B"
ACCENT_DARK = "#2A3E75"
TEXT_COLOR = "#222"

# --- CONEXIÓN A LA BASE DE DATOS ---
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


class Ventana_SeguimientoVet(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title(APP_TITLE)
        self.geometry("700x550")
        self.config(bg=BG)

        # --- FORMULARIO ---
        form = tk.LabelFrame(
            self, text="Formulario de Seguimiento Veterinario",
            bg=BG, fg=ACCENT, font=("Arial", 12, "bold"),
            padx=10, pady=10
        )
        form.pack(pady=10, fill="x", padx=20)

        labels = [
            "ID Animal:", "Tipo de Tratamiento:", "Fecha Actual (AAAA-MM-DD):", "Próxima Fecha (AAAA-MM-DD):"
        ]
        self.campos_seg = {}

        # --- CAMPOS ---
        for i, campo in enumerate(labels):
            tk.Label(
                form, text=campo, bg=BG, fg=TEXT_COLOR,
                font=("Arial", 10, "bold"), width=22, anchor="w"
            ).grid(row=i, column=0, padx=5, pady=8, sticky="w")

            entry = tk.Entry(form, width=40, relief="solid", justify="center")
            entry.grid(row=i, column=1, padx=10, pady=8)
            self.campos_seg[campo] = entry

        # --- BOTÓN LIMPIAR ---
        acciones = tk.Frame(self, bg=BG)
        acciones.pack(pady=15)

        tk.Button(
            acciones, text="Limpiar Campos",
            command=self.limpiar_campos_seg,
            bg="#6c757d", fg="white", relief="flat",
            padx=20, pady=8, font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=10)

        # --- PANEL DE BOTONES CRUD ---
        panel = tk.Frame(self, bg=BG)
        panel.pack(pady=10)

        botones = [
            ("Registrar Seguimiento", ACCENT, self.registrar_seguimiento),
            ("Modificar Seguimiento", ACCENT, self.modificar_seguimiento),
            ("Consultar Seguimientos", ACCENT_DARK, self.consultar_seguimientos),
            ("Eliminar Seguimiento", "#B33A3A", self.eliminar_seguimiento)
        ]

        for texto, color, comando in botones:
            tk.Button(
                panel, text=texto, command=comando,
                bg=color, fg="white", activebackground=ACCENT_DARK,
                relief="flat", padx=16, pady=10,
                font=("Arial", 10, "bold"), cursor="hand2", width=22
            ).pack(pady=6)

    # --- LIMPIAR CAMPOS ---
    def limpiar_campos_seg(self):
        for entry in self.campos_seg.values():
            entry.delete(0, tk.END)

    # --- CRUD: REGISTRAR ---
    def registrar_seguimiento(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            fk_animal = self.campos_seg["ID Animal:"].get()
            tipo_tratamiento = self.campos_seg["Tipo de Tratamiento:"].get()
            fecha_actual = self.campos_seg["Fecha Actual (AAAA-MM-DD):"].get()
            prox_fecha = self.campos_seg["Próxima Fecha (AAAA-MM-DD):"].get()

            if not fk_animal or not tipo_tratamiento or not fecha_actual:
                messagebox.showwarning("Campos vacíos", "Los campos con * son obligatorios.")
                return

            sql = """INSERT INTO Seguimiento_vet (fk_animal, tipo_tratamiento, fecha_actual, prox_fecha)
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (fk_animal, tipo_tratamiento, fecha_actual, prox_fecha))
            conn.commit()
            messagebox.showinfo("Éxito", "Seguimiento veterinario registrado correctamente.")
            self.limpiar_campos_seg()

        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el seguimiento:\n{e}")
        finally:
            conn.close()

    # --- CRUD: MODIFICAR ---
    def modificar_seguimiento(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            pk = simpledialog.askinteger("Modificar", "Ingrese el ID del seguimiento a modificar:")
            if not pk:
                return

            fk_animal = self.campos_seg["ID Animal:"].get()
            tipo_tratamiento = self.campos_seg["Tipo de Tratamiento:"].get()
            fecha_actual = self.campos_seg["Fecha Actual (AAAA-MM-DD):"].get()
            prox_fecha = self.campos_seg["Próxima Fecha (AAAA-MM-DD):"].get()

            sql = """UPDATE Seguimiento_vet
                     SET fk_animal=%s, tipo_tratamiento=%s, fecha_actual=%s, prox_fecha=%s
                     WHERE pk_segui_vet=%s"""
            cursor.execute(sql, (fk_animal, tipo_tratamiento, fecha_actual, prox_fecha, pk))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Seguimiento ID {pk} modificado correctamente.")
            else:
                messagebox.showwarning("No encontrado", f"No se encontró el seguimiento con ID {pk}.")
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo modificar:\n{e}")
        finally:
            conn.close()

    # --- CRUD: ELIMINAR ---
    def eliminar_seguimiento(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            pk = simpledialog.askinteger("Eliminar", "Ingrese el ID del seguimiento a eliminar:")
            if not pk:
                return

            confirm = messagebox.askyesno("Confirmar", f"¿Deseas eliminar el seguimiento con ID {pk}?")
            if not confirm:
                return

            cursor.execute("DELETE FROM Seguimiento_vet WHERE pk_segui_vet=%s", (pk,))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Seguimiento ID {pk} eliminado.")
            else:
                messagebox.showwarning("No encontrado", "ID inexistente.")
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")
        finally:
            conn.close()

    # --- CRUD: CONSULTAR ---
    def consultar_seguimientos(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            cursor.execute("SELECT pk_segui_vet, fk_animal, tipo_tratamiento, fecha_actual, prox_fecha FROM Seguimiento_vet")
            datos = cursor.fetchall()

            ventana = Toplevel(self)
            ventana.title("Consulta de Seguimientos Veterinarios")
            ventana.geometry("850x400")
            ventana.config(bg=BG)

            cols = ("ID", "ID Animal", "Tipo Tratamiento", "Fecha Actual", "Próxima Fecha")
            tabla = ttk.Treeview(ventana, columns=cols, show="headings", height=15)
            for c in cols:
                tabla.heading(c, text=c)
                tabla.column(c, anchor="center", width=150)

            for fila in datos:
                tabla.insert("", "end", values=fila)

            tabla.pack(padx=10, pady=10, fill="both", expand=True)
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo consultar:\n{e}")
        finally:
            conn.close()


