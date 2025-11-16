import tkinter as tk
from tkinter import Toplevel, messagebox, simpledialog, ttk
import mariadb
from conexion import conectar_bd

# --- CONFIGURACIONES GENERALES ---
APP_TITLE = 'Gestión de Ventas'
BG = "#f4f3ec"
ACCENT = "#36448B"
ACCENT_DARK = "#2A3E75"
TEXT_COLOR = "#222"

class Ventana_Ventas(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title(APP_TITLE)
        self.geometry("700x600")
        self.config(bg=BG)
       
        # --- FORMULARIO ---
        form = tk.LabelFrame(
            self, text="Formulario de Ventas",
            bg=BG, fg=ACCENT, font=("Arial", 12, "bold"),
            padx=10, pady=10
        )
        form.pack(pady=25, fill="x", padx=20)

        labels = [
            "ID Animal:", "ID Pesaje:",
            "Clave:", "Precio ($):",
            "Fecha (AAAA-MM-DD):"
        ]
        self.campos_venta = {}

        # --- Usamos GRID dentro del formulario ---
        for i, campo in enumerate(labels):
            tk.Label(
                form, text=campo, bg=BG, fg=TEXT_COLOR,
                font=("Arial", 10, "bold"), width=35, anchor="w"
            ).grid(row=i, column=0, padx=10, pady=8, sticky="w")

            entry = tk.Entry(form, width=40, relief="solid", justify="center")
            entry.grid(row=i, column=1, padx=10, pady=8)
            self.campos_venta[campo] = entry

        # --- BOTONES EXTRA ---
        acciones = tk.Frame(self, bg=BG)
        acciones.pack(pady=15)

        tk.Button(
            acciones, text="Limpiar Campos",
            command=self.limpiar_campos_venta,
            bg="#6c757d", fg="white", relief="flat",
            padx=20, pady=8, font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side="left", padx=10)

        # --- PANEL DE BOTONES CRUD ---
        panel = tk.Frame(self, bg=BG)
        panel.pack(pady=10)

        botones = [
            ("Registrar Venta", ACCENT, self.registrar_venta),
            ("Modificar Venta", ACCENT, self.modificar_venta),
            ("Consultar Ventas", ACCENT_DARK, self.consultar_ventas),
            ("Eliminar Venta", "#B33A3A", self.eliminar_venta)
        ]

        for texto, color, comando in botones:
            tk.Button(
                panel, text=texto, command=comando,
                bg=color, fg="white", activebackground=ACCENT_DARK,
                relief="flat", padx=16, pady=10,
                font=("Arial", 10, "bold"), cursor="hand2", width=20
            ).pack(pady=6)

    # --- LIMPIAR CAMPOS ---
    def limpiar_campos_venta(self):
        for entry in self.campos_venta.values():
            entry.delete(0, tk.END)

    # --- CRUD: REGISTRAR ---
    def registrar_venta(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            fk_animal = self.campos_venta["ID Animal:"].get()
            fk_pesaje = self.campos_venta["ID Pesaje:"].get()
            clave = self.campos_venta["Clave:"].get()
            precio = self.campos_venta["Precio ($):"].get()
            fecha = self.campos_venta["Fecha (AAAA-MM-DD):"].get()

            if not all([fk_animal, fk_pesaje, clave, precio, fecha]):
                messagebox.showwarning("Campos vacíos", "Todos los campos son requeridos.")
                return

            # Validar que el animal exista
            cursor.execute("SELECT pk_animal FROM Animales WHERE pk_animal = %s", (fk_animal,))
            if not cursor.fetchone():
                messagebox.showwarning("Error", "El ID de animal no existe.")
                return

            # Validar que el pesaje exista
            cursor.execute("SELECT pk_pesaje FROM Pesajes WHERE pk_pesaje = %s", (fk_pesaje,))
            if not cursor.fetchone():
                messagebox.showwarning("Error", "El ID de pesaje no existe.")
                return

            sql = """INSERT INTO Ventas (fk_animal, fk_pesaje, clave, precio, fecha_venta)
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (fk_animal, fk_pesaje, clave, precio, fecha))
            conn.commit()
            messagebox.showinfo("Éxito", "Venta registrada correctamente.")
            self.limpiar_campos_venta()

        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar la venta:\n{e}")
        finally:
            conn.close()

    # --- CRUD: MODIFICAR ---
    def modificar_venta(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            pk = simpledialog.askinteger("Modificar", "Ingrese el ID de la venta a modificar:")
            if not pk:
                return

            fk_animal = self.campos_venta["ID Animal:"].get()
            fk_pesaje = self.campos_venta["ID Pesaje:"].get()
            clave = self.campos_venta["Clave:"].get()
            precio = self.campos_venta["Precio ($):"].get()
            fecha = self.campos_venta["Fecha (AAAA-MM-DD):"].get()

            if not all([fk_animal, fk_pesaje, clave, precio, fecha]):
                messagebox.showwarning("Campos vacíos", "Todos los campos son requeridos.")
                return

            sql = """UPDATE Ventas 
                     SET fk_animal=%s, fk_pesaje=%s, clave=%s, precio=%s, fecha_venta=%s
                     WHERE pk_venta=%s"""
            cursor.execute(sql, (fk_animal, fk_pesaje, clave, precio, fecha, pk))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Venta ID {pk} modificada correctamente.")
            else:
                messagebox.showwarning("No encontrado", f"No se encontró la venta con ID {pk}.")
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo modificar:\n{e}")
        finally:
            conn.close()

    # --- CRUD: ELIMINAR ---
    def eliminar_venta(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            pk = simpledialog.askinteger("Eliminar", "Ingrese el ID de la venta a eliminar:")
            if not pk:
                return

            confirm = messagebox.askyesno("Confirmar", f"¿Deseas eliminar la venta con ID {pk}?")
            if not confirm:
                return

            cursor.execute("DELETE FROM Ventas WHERE pk_venta=%s", (pk,))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Venta ID {pk} eliminada.")
            else:
                messagebox.showwarning("No encontrado", "ID inexistente.")
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")
        finally:
            conn.close()

    # --- CRUD: CONSULTAR ---
    def consultar_ventas(self):
        conn, cursor = conectar_bd()
        if not conn:
            return
        try:
            cursor.execute("""
                SELECT v.pk_venta, v.clave, v.precio, v.fecha_venta,
                       a.nombre as nombre_animal, p.peso as peso_animal
                FROM Ventas v
                LEFT JOIN Animales a ON v.fk_animal = a.pk_animal
                LEFT JOIN Pesajes p ON v.fk_pesaje = p.pk_pesaje
                ORDER BY v.fecha_venta DESC
            """)
            datos = cursor.fetchall()

            ventana = Toplevel(self)
            ventana.title("Consulta de Ventas")
            ventana.geometry("1000x400")
            ventana.config(bg=BG)

            cols = ("ID", "Clave", "Precio", "Fecha", "Animal", "Peso")
            tabla = ttk.Treeview(ventana, columns=cols, show="headings", height=15)
            for c in cols:
                tabla.heading(c, text=c)
                tabla.column(c, anchor="center", width=150)

            for fila in datos:
                tabla.insert("", "end", values=fila)

            # Agregar scrollbar
            scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=tabla.yview)
            scrollbar.pack(side="right", fill="y")
            tabla.configure(yscrollcommand=scrollbar.set)

            tabla.pack(padx=10, pady=10, fill="both", expand=True)
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo consultar:\n{e}")
        finally:
            conn.close()
