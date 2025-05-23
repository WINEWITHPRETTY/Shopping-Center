import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import BaseDatos
import Clientes

class Inventarios:
    def __init__(self, db):
        self.db = db

    def menu(self, nivel_usuario):
        ventana = tk.Toplevel()
        ventana.title("Gestión de Inventarios")
        ventana.geometry("400x420")
        ventana.configure(bg="#f9f9f9")

        tk.Label(ventana, text="Inventarios", font=("Arial", 16, "bold"), bg="#f9f9f9", fg="#333").pack(pady=10)

        def ingresar():
            if nivel_usuario > 2:
                messagebox.showwarning("Acceso Denegado", "No tiene permiso para ingresar productos.")
                return
            datos = [
                simpledialog.askstring("Inventario", prompt) for prompt in [
                    "Código del producto:", "Cantidad:", "Stock mínimo:", "Precio:"]
            ]
            if all(datos):
                conn = self.db.conectar()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO inventarios VALUES (%s, %s, %s, %s)", datos)
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Éxito", "Producto agregado")

        def consultar():
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inventarios")
            datos = cursor.fetchall()
            cursor.close()
            conn.close()
            salida = "\n".join([", ".join(row) for row in datos])
            messagebox.showinfo("Inventarios", salida or "No hay registros")

        def modificar():
            if nivel_usuario > 2:
                messagebox.showwarning("Acceso Denegado", "No tiene permiso para modificar productos.")
                return
            cod = simpledialog.askstring("Modificar", "Código del producto:")
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inventarios WHERE cod=%s", (cod,))
            prod = cursor.fetchone()
            if prod:
                nuevos = [
                    simpledialog.askstring("Modificar", campo, initialvalue=prod[i])
                    for i, campo in enumerate(["Código", "Cantidad", "Stock mínimo", "Precio"])
                ]
                cursor.execute("UPDATE inventarios SET cod=%s, cantidad=%s, stock=%s, precio=%s WHERE cod=%s",
                               (*nuevos, cod))
                conn.commit()
                messagebox.showinfo("Éxito", "Inventario modificado")
            else:
                messagebox.showerror("Error", "Producto no encontrado")
            cursor.close()
            conn.close()

        def eliminar():
            if nivel_usuario != 1:
                messagebox.showwarning("Acceso Denegado", "Solo usuarios de nivel 1 pueden eliminar productos.")
                return
            cod = simpledialog.askstring("Eliminar", "Código del producto:")
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM inventarios WHERE cod=%s", (cod,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Éxito", "Producto eliminado")

        acciones = [
            ("➕ Ingresar", ingresar),
            ("🔍 Consultar", consultar),
            ("✏️ Modificar", modificar),
            ("🗑️ Eliminar", eliminar),
            ("❌ Cerrar", ventana.destroy)
        ]

        for texto, accion in acciones:
            tk.Button(ventana, text=texto, command=accion, font=("Arial", 11), bg="#9b59b6", fg="white",
                      activebackground="#8e44ad", width=30, height=2).pack(pady=6)