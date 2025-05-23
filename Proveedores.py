import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import BaseDatos
import Clientes

import tkinter as tk
from tkinter import messagebox, simpledialog

class Proveedores:
    def __init__(self, db):
        self.db = db

    def menu(self, nivel_usuario):
        ventana = tk.Toplevel()
        ventana.title("Gestión de Proveedores")
        ventana.geometry("420x450")
        ventana.configure(bg="#f9f9f9")

        tk.Label(ventana, text="Proveedores", font=("Arial", 16, "bold"), bg="#f9f9f9", fg="#333").pack(pady=10)

        def ingresar():
            if nivel_usuario > 2:
                messagebox.showwarning("Acceso Denegado", "No tiene permiso para ingresar proveedores.")
                return
            datos = [
                simpledialog.askstring("Proveedor", prompt) for prompt in [
                    "ID del proveedor:", "Código del producto:", "Descripción:", "Costo:", "Dirección:", "Teléfono:"]
            ]
            if all(datos):
                conn = self.db.conectar()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO proveedores VALUES (%s, %s, %s, %s, %s, %s)", datos)
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Éxito", "Proveedor agregado")

        def consultar():
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM proveedores")
            datos = cursor.fetchall()
            cursor.close()
            conn.close()
            salida = "\n".join([", ".join(row) for row in datos])
            messagebox.showinfo("Proveedores", salida or "No hay registros")

        def modificar():
            if nivel_usuario > 2:
                messagebox.showwarning("Acceso Denegado", "No tiene permiso para modificar proveedores.")
                return
            id_prov = simpledialog.askstring("Modificar", "ID del proveedor:")
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM proveedores WHERE id=%s", (id_prov,))
            proveedor = cursor.fetchone()
            if proveedor:
                nuevos = [
                    simpledialog.askstring("Modificar", campo, initialvalue=proveedor[i])
                    for i, campo in enumerate([
                        "ID", "Código del producto", "Descripción", "Costo", "Dirección", "Teléfono"])
                ]
                cursor.execute("""
                    UPDATE proveedores SET 
                        id=%s, cod_prod=%s, descripcion=%s, costo=%s, direccion=%s, telefono=%s 
                    WHERE id=%s
                """, (*nuevos, id_prov))
                conn.commit()
                messagebox.showinfo("Éxito", "Proveedor modificado")
            else:
                messagebox.showerror("Error", "Proveedor no encontrado")
            cursor.close()
            conn.close()

        def eliminar():
            if nivel_usuario != 1:
                messagebox.showwarning("Acceso Denegado", "Solo usuarios de nivel 1 pueden eliminar proveedores.")
                return
            id_prov = simpledialog.askstring("Eliminar", "ID del proveedor a eliminar:")
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM proveedores WHERE id=%s", (id_prov,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Éxito", "Proveedor eliminado")

        acciones = [
            ("➕ Ingresar", ingresar),
            ("🔍 Consultar", consultar),
            ("✏️ Modificar", modificar),
            ("🗑️ Eliminar", eliminar),
            ("❌ Cerrar", ventana.destroy)
        ]

        for texto, accion in acciones:
            tk.Button(ventana, text=texto, command=accion, font=("Arial", 11), bg="#3498db", fg="white",
                      activebackground="#2980b9", width=30, height=2).pack(pady=6)
