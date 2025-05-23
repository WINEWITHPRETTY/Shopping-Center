import tkinter as tk
from tkinter import messagebox, simpledialog
import hashlib

class Usuarios:
    def __init__(self, db):
        self.db = db

    def encriptar(self, clave):
        return hashlib.sha256(clave.encode()).hexdigest()

    def menu(self, nivel_usuario):
        if nivel_usuario != 1:
            messagebox.showerror("Acceso Denegado", "Solo los administradores pueden acceder a esta sección.")
            return

        ventana = tk.Toplevel()
        ventana.title("Gestión de Usuarios")
        ventana.geometry("420x450")
        ventana.configure(bg="#f9f9f9")

        tk.Label(ventana, text="Usuarios", font=("Arial", 16, "bold"), bg="#f9f9f9", fg="#333").pack(pady=10)

        def ingresar():
            username = simpledialog.askstring("Usuario", "Nombre de usuario:")
            password = simpledialog.askstring("Contraseña", "Contraseña:", show="*")
            nivel = simpledialog.askinteger("Nivel", "Nivel de acceso (1 = Admin, 2 = Medio, 3 = Básico):")
            if username and password and nivel:
                clave_encriptada = self.encriptar(password)
                conn = self.db.conectar()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO usuarios (username, password, nivel) VALUES (%s, %s, %s)",
                               (username, clave_encriptada, nivel))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Éxito", "Usuario agregado")

        def consultar():
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT username, nivel FROM usuarios")
            datos = cursor.fetchall()
            cursor.close()
            conn.close()
            salida = "\n".join([f"{usuario}, Nivel: {nivel}" for usuario, nivel in datos])
            messagebox.showinfo("Usuarios", salida or "No hay registros")

        def modificar():
            username = simpledialog.askstring("Modificar", "Usuario a modificar:")
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE username=%s", (username,))
            user = cursor.fetchone()
            if user:
                nueva_clave = simpledialog.askstring("Modificar", "Nueva contraseña:", show="*")
                nuevo_nivel = simpledialog.askinteger("Modificar", "Nuevo nivel (1-3):", initialvalue=user[2])
                clave_encriptada = self.encriptar(nueva_clave)
                cursor.execute("UPDATE usuarios SET password=%s, nivel=%s WHERE username=%s",
                               (clave_encriptada, nuevo_nivel, username))
                conn.commit()
                messagebox.showinfo("Éxito", "Usuario modificado")
            else:
                messagebox.showerror("Error", "Usuario no encontrado")
            cursor.close()
            conn.close()

        def eliminar():
            username = simpledialog.askstring("Eliminar", "Nombre del usuario a eliminar:")
            if username:
                conn = self.db.conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM usuarios WHERE username=%s", (username,))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Éxito", "Usuario eliminado")

        acciones = [
            ("➕ Ingresar", ingresar),
            ("🔍 Consultar", consultar),
            ("✏️ Modificar", modificar),
            ("🗑️ Eliminar", eliminar),
            ("❌ Cerrar", ventana.destroy)
        ]

        for texto, accion in acciones:
            tk.Button(ventana, text=texto, command=accion, font=("Arial", 11), bg="#2c3e50", fg="white",
                      activebackground="#34495e", width=30, height=2).pack(pady=6)
