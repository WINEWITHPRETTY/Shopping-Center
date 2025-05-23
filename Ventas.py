import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import BaseDatos
import Clientes

import tkinter as tk
from tkinter import messagebox, simpledialog

class Ventas:
    def __init__(self, db):
        self.db = db

    def menu(self, nivel_usuario):
        ventana = tk.Toplevel()
        ventana.title("Gestión de Ventas")
        ventana.geometry("400x400")
        ventana.configure(bg="#f9f9f9")

        tk.Label(ventana, text="Ventas", font=("Arial", 16, "bold"), bg="#f9f9f9", fg="#333").pack(pady=10)

        def registrar():
            if nivel_usuario > 2:
                messagebox.showwarning("Acceso Denegado", "No tiene permiso para registrar ventas.")
                return
            datos = [
                simpledialog.askstring("Venta", prompt) for prompt in [
                    "ID del cliente:", "Código del producto:", "Cantidad:", "Descripción:"]
            ]
            subtotal_str = simpledialog.askstring("Venta", "Subtotal de la venta:")
            if not subtotal_str or not all(datos):
                return
            try:
                subtotal = float(subtotal_str)
            except ValueError:
                messagebox.showerror("Error", "El subtotal debe ser un número.")
                return
            iva = 0.19
            total = subtotal * (1 + iva)
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ventas (id_cliente, cod_prod, cantidad, descripcion, iva, subtotal, total)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (*datos, iva, subtotal, total))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Éxito", "Venta registrada")

        def consultar():
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ventas")
            datos = cursor.fetchall()
            cursor.close()
            conn.close()
            salida = "\n".join([", ".join(map(str, v)) for v in datos])
            messagebox.showinfo("Ventas", salida or "No hay registros")

        acciones = [
            ("➕ Registrar Venta", registrar),
            ("🔍 Consultar Ventas", consultar),
            ("❌ Cerrar", ventana.destroy)
        ]

        for texto, accion in acciones:
            tk.Button(ventana, text=texto, command=accion, font=("Arial", 11), bg="#e67e22", fg="white",
                      activebackground="#d35400", width=30, height=2).pack(pady=6)
