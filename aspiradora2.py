import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

class Aspiradora:
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.ventana_principal.title("Simulación de Aspiradora")
        self.ventana_principal.geometry("600x400")
        
        image = Image.open("aspi.png")  # Cargar la imagen de la aspiradora
        image = image.resize((50, 50), Image.LANCZOS)  # Redimensiona al tamaño del cuadro
        self.aspiradora_img = ImageTk.PhotoImage(image)
        
        image_basura = Image.open("trashi.png")  # Cargar la imagen de la aspiradora
        image_basura= image_basura.resize((30, 30), Image.LANCZOS)  # Redimensiona al tamaño del cuadro
        self.trashi_img = ImageTk.PhotoImage(image_basura)
        
        self.crear_interfaz()
        self.boton_limpieza_creado = False  # Variable de control para evitar duplicar el botón
        
    def crear_interfaz(self):
        self.marco_izquierdo = tk.Frame(self.ventana_principal, bg="white")
        self.marco_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.marco_derecho = tk.Frame(self.ventana_principal, bg="#f0f0f0")
        self.marco_derecho.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(self.marco_derecho, text="Largo (1-10):", bg="#f0f0f0").pack(pady=5)
        self.entrada_largo = tk.Entry(self.marco_derecho)
        self.entrada_largo.pack(pady=5)
        
        tk.Label(self.marco_derecho, text="Ancho (1-10):", bg="#f0f0f0").pack(pady=5)
        self.entrada_ancho = tk.Entry(self.marco_derecho)
        self.entrada_ancho.pack(pady=5)
        
        tk.Label(self.marco_derecho, text="Fila Aspiradora:", bg="#f0f0f0").pack(pady=5)
        self.entrada_fila = tk.Entry(self.marco_derecho)
        self.entrada_fila.pack(pady=5)
        
        tk.Label(self.marco_derecho, text="Columna Aspiradora:", bg="#f0f0f0").pack(pady=5)
        self.entrada_columna = tk.Entry(self.marco_derecho)
        self.entrada_columna.pack(pady=5)
        
        tk.Button(self.marco_derecho, text="Iniciar Simulación", command=self.iniciar_simulacion, bg="#4CAF50", fg="white").pack(pady=10)
        self.etiqueta_mensaje = tk.Label(self.marco_derecho, text="", bg="#f0f0f0", fg="red")
        self.etiqueta_mensaje.pack(pady=5)
    
    def iniciar_simulacion(self):
        try:
            self.filas = int(self.entrada_largo.get())
            self.columnas = int(self.entrada_ancho.get())
            self.fila_aspiradora = int(self.entrada_fila.get())
            self.columna_aspiradora = int(self.entrada_columna.get())
            
            if not (1 <= self.filas <= 10 and 1 <= self.columnas <= 10):
                self.etiqueta_mensaje.config(text="Tamaño fuera de rango (1-10)")
                return
            if not (0 <= self.fila_aspiradora < self.filas and 0 <= self.columna_aspiradora < self.columnas):
                self.etiqueta_mensaje.config(text="Posición fuera del área")
                return
            
            self.crear_cuadricula()
        except ValueError:
            self.etiqueta_mensaje.config(text="Ingrese valores válidos")
    
    def crear_cuadricula(self):
        if hasattr(self, 'lienzo'):
            self.lienzo.destroy()
        
        self.lienzo = tk.Canvas(self.marco_izquierdo, width=self.columnas * 50, height=self.filas * 50, bg="white")
        self.lienzo.pack(pady=10, padx=10)
        
        self.cuadricula = [[0 for _ in range(self.columnas)] for _ in range(self.filas)]
        
        for _ in range(random.randint(1, (self.filas * self.columnas) // 3)):
            fila, columna = random.randint(0, self.filas - 1), random.randint(0, self.columnas - 1)
            if (fila, columna) != (self.fila_aspiradora, self.columna_aspiradora):
                self.cuadricula[fila][columna] = 1  # Casilla sucia
        
        self.dibujar_cuadricula()
        
        if not self.boton_limpieza_creado:
            tk.Button(self.marco_derecho, text="Empezar Limpieza", command=self.limpiar_adyacentes, bg="#008CBA", fg="white").pack(pady=10)
            self.boton_limpieza_creado = True
    
    def dibujar_cuadricula(self):
        self.lienzo.delete("all")
        for fila in range(self.filas):
            for columna in range(self.columnas):
                x1, y1 = columna * 50, fila * 50
                x2, y2 = (columna + 1) * 50, (fila + 1) * 50
                
                if (fila, columna) == (self.fila_aspiradora, self.columna_aspiradora):
                    self.lienzo.create_image(x1 + 25, y1 + 25, image=self.aspiradora_img)
                elif self.cuadricula[fila][columna] == 1:
                    self.lienzo.create_image(x1 + 25, y1 + 25, image=self.trashi_img)
                else:
                    self.lienzo.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
    
    def limpiar_adyacentes(self):
        direcciones = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        casillas_limpiadas = []
        
        for dx, dy in direcciones:
            nueva_fila, nueva_columna = self.fila_aspiradora + dx, self.columna_aspiradora + dy
            if 0 <= nueva_fila < self.filas and 0 <= nueva_columna < self.columnas and self.cuadricula[nueva_fila][nueva_columna] == 1:
                self.cuadricula[nueva_fila][nueva_columna] = 0  # Limpiar
                casillas_limpiadas.append((nueva_fila, nueva_columna))
        
        self.dibujar_cuadricula()
        self.etiqueta_mensaje.config(text=f"Vecinos limpiados: {casillas_limpiadas}")

if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = Aspiradora(ventana_principal)
    ventana_principal.mainloop()
