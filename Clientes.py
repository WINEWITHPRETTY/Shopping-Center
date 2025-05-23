import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

class Clientes:
    def __init__(self, db):
        self.db = db

    def menu(self, nivel_usuario):
        ventana = tk.Toplevel()
        ventana.title("Gestión de Clientes")
        ventana.geometry("400x400")
        ventana.configure(bg="#f9f9f9")

        tk.Label(ventana, text="Clientes", font=("Arial", 16, "bold"), bg="#f9f9f9", fg="#333").pack(pady=10)

        def ingresar():
            if nivel_usuario > 2:
                messagebox.showwarning("Acceso Denegado", "No tiene permiso para ingresar clientes.")
                return
            id_cliente = simpledialog.askstring("ID", "Ingrese ID del cliente:")
            nombre = simpledialog.askstring("Nombre", "Nombre del cliente:")
            direccion = simpledialog.askstring("Dirección", "Dirección:")
            telefono = simpledialog.askstring("Teléfono", "Teléfono:")
            if id_cliente and nombre and direccion and telefono:
                conn = self.db.conectar()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO clientes VALUES (%s, %s, %s, %s)",
                               (id_cliente, nombre, direccion, telefono))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Éxito", "Cliente agregado")

        def consultar():
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes")
            datos = cursor.fetchall()
            cursor.close()
            conn.close()
            salida = "\n".join([", ".join(row) for row in datos])
            messagebox.showinfo("Clientes", salida or "No hay registros")

        def modificar():
            if nivel_usuario > 2:
                messagebox.showwarning("Acceso Denegado", "No tiene permiso para modificar clientes.")
                return
            id_cliente = simpledialog.askstring("Modificar", "ID del cliente a modificar:")
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id=%s", (id_cliente,))
            cliente = cursor.fetchone()
            if cliente:
                nombre = simpledialog.askstring("Modificar", "Nuevo nombre:", initialvalue=cliente[1])
                direccion = simpledialog.askstring("Modificar", "Nueva dirección:", initialvalue=cliente[2])
                telefono = simpledialog.askstring("Modificar", "Nuevo teléfono:", initialvalue=cliente[3])
                cursor.execute("UPDATE clientes SET nombre=%s, direccion=%s, telefono=%s WHERE id=%s",
                               (nombre, direccion, telefono, id_cliente))
                conn.commit()
                messagebox.showinfo("Éxito", "Cliente modificado")
            else:
                messagebox.showerror("Error", "Cliente no encontrado")
            cursor.close()
            conn.close()

        def eliminar():
            if nivel_usuario != 1:
                messagebox.showwarning("Acceso Denegado", "Solo usuarios de nivel 1 pueden eliminar clientes.")
                return
            id_cliente = simpledialog.askstring("Eliminar", "ID del cliente a eliminar:")
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE id=%s", (id_cliente,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Éxito", "Cliente eliminado")

        acciones = [
            ("➕ Ingresar", ingresar),
            ("🔍 Consultar", consultar),
            ("✏️ Modificar", modificar),
            ("🗑️ Eliminar", eliminar),
            ("❌ Cerrar", ventana.destroy)
        ]

        for texto, accion in acciones:
            tk.Button(ventana, text=texto, command=accion, font=("Arial", 11), bg="#4CAF50", fg="white",
                      activebackground="#45a049", width=30, height=2).pack(pady=6)
