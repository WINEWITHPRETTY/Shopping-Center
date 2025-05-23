import tkinter as tk
from tkinter import messagebox, simpledialog
from BaseDatos import BaseDatos
import hashlib

def encriptar_clave(clave):
    """Devuelve la clave encriptada con SHA256."""
    return hashlib.sha256(clave.encode()).hexdigest()

class Login:
    def __init__(self, root, callback_login):
        """
        Interfaz de inicio de sesión.

        :param root: Ventana raíz de Tkinter
        :param callback_login: Función a ejecutar al iniciar sesión exitosamente
        """
        self.root = root
        self.callback_login = callback_login
        self.db = BaseDatos()

        # Configuración de la ventana
        self.root.title("Inicio de Sesión")
        self.root.geometry("350x280")
        self.root.configure(bg="#ecf0f1")

        # Contenedor principal
        frame = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
        frame.pack(expand=True)

        # Título
        tk.Label(frame, text="Iniciar Sesión", font=("Arial", 16, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=(0, 15))

        # Entrada de usuario
        tk.Label(frame, text="Usuario", bg="#ecf0f1").pack(anchor="w")
        self.usuario_entry = tk.Entry(frame, width=30)
        self.usuario_entry.pack(pady=5)

        # Entrada de contraseña
        tk.Label(frame, text="Contraseña", bg="#ecf0f1").pack(anchor="w")
        self.clave_entry = tk.Entry(frame, show="*", width=30)
        self.clave_entry.pack(pady=5)

        # Botón de inicio de sesión
        tk.Button(frame, text="🔓 Iniciar sesión", command=self.verificar, bg="#27ae60", fg="white",
                  font=("Arial", 10, "bold"), width=30).pack(pady=10)

        # Opción para crear el primer admin si no existen usuarios
        if not self.existe_admin():
            tk.Button(frame, text="⚙ Crear primer usuario administrador", command=self.crear_admin,
                      bg="#2980b9", fg="white", font=("Arial", 9), width=30).pack(pady=5)

    def encriptar(self, clave):
        """Encripta la contraseña usando SHA256."""
        return hashlib.sha256(clave.encode()).hexdigest()

    def existe_admin(self):
        """Verifica si ya existe algún usuario registrado."""
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        cantidad = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return cantidad > 0

    def crear_admin(self):
        """Crea el primer usuario administrador si no existe ninguno."""
        usuario = simpledialog.askstring("Nuevo Admin", "Nombre de usuario:")
        clave = simpledialog.askstring("Nuevo Admin", "Contraseña:", show="*")
        if not usuario or not clave:
            messagebox.showerror("Error", "Debe ingresar usuario y clave.")
            return

        clave_encriptada = self.encriptar(clave)
        try:
            conn = self.db.conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (username, password, nivel) VALUES (%s, %s, %s)",
                           (usuario, clave_encriptada, 1))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Éxito", "Usuario administrador creado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el usuario: {e}")

    def verificar(self):
        """Verifica las credenciales ingresadas."""
        usuario = self.usuario_entry.get()
        clave = self.encriptar(self.clave_entry.get())

        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nivel FROM usuarios WHERE username=%s AND password=%s", (usuario, clave))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()

        if resultado:
            nivel = resultado[0]
            self.root.destroy()  # Cierra la ventana de login
            self.callback_login(nivel)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
