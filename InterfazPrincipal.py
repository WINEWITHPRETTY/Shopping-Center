import tkinter as tk
from BaseDatos import BaseDatos
from Clientes import Clientes
from Inventarios import Inventarios
from Proveedores import Proveedores
from Ventas import Ventas
from Login import Login
from Usuarios import Usuarios  # NUEVO: se importa el módulo Usuarios

class InterfazPrincipal:
    def __init__(self, root, nivel_usuario):
        self.root = root
        self.nivel_usuario = nivel_usuario
        self.root.title("Sistema de Control de Tienda")
        self.root.geometry("500x500")
        self.root.configure(bg="#f2f2f2")

        self.db = BaseDatos()
        self.modulo_clientes = Clientes(self.db)
        self.modulo_proveedores = Proveedores(self.db)
        self.modulo_inventarios = Inventarios(self.db)
        self.modulo_ventas = Ventas(self.db)
        self.modulo_usuarios = Usuarios(self.db)  # NUEVO: se inicializa el módulo Usuarios

        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(self.root, text="\U0001F6D2 SISTEMA DE TIENDA", font=("Arial", 18, "bold"), bg="#f2f2f2", fg="#333").pack(pady=20)

        boton_frame = tk.Frame(self.root, bg="#f2f2f2")
        boton_frame.pack(pady=10)

        botones = [
            ("\U0001F4CB Clientes", lambda: self.modulo_clientes.menu(self.nivel_usuario)),
            ("\U0001F69A Proveedores", lambda: self.modulo_proveedores.menu(self.nivel_usuario)),
            ("\U0001F4E6 Inventarios", lambda: self.modulo_inventarios.menu(self.nivel_usuario)),
            ("\U0001F9FE Ventas", lambda: self.modulo_ventas.menu(self.nivel_usuario)),
        ]

        # NUEVO: Solo usuarios de nivel 1 pueden acceder a la gestión de usuarios
        if self.nivel_usuario == 1:
            botones.append(("\U0001F464 Administrar Usuarios", lambda: self.modulo_usuarios.menu(self.nivel_usuario)))

        botones.append(("\u274C Salir", self.root.destroy))

        for texto, accion in botones:
            color = "#4CAF50" if texto != "\u274C Salir" else "#E74C3C"
            hover = "#45a049" if texto != "\u274C Salir" else "#c0392b"

            boton = tk.Button(
                boton_frame,
                text=texto,
                command=accion,
                font=("Arial", 12),
                width=30,
                height=2,
                bg=color,
                fg="white",
                activebackground=hover,
                relief="raised",
                bd=3
            )
            boton.pack(pady=8)

# Punto de entrada principal
def lanzar_interfaz(nivel_usuario):
    root = tk.Tk()
    app = InterfazPrincipal(root, nivel_usuario)
    root.mainloop()

if __name__ == '__main__':
    login_root = tk.Tk()
    Login(login_root, lanzar_interfaz)
    login_root.mainloop()
