import tkinter as tk
import random

class VacuumCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Aspiradora")
        
        self.create_ui()
        self.clean_button_created = False  # Variable de control para evitar duplicar el botón
    
    def create_ui(self):
        self.frame_left = tk.Frame(self.root)
        self.frame_left.pack(side=tk.LEFT)
        
        self.frame_right = tk.Frame(self.root)
        self.frame_right.pack(side=tk.RIGHT, padx=10)
        
        tk.Label(self.frame_right, text="Largo (1-10):").pack()
        self.entry_largo = tk.Entry(self.frame_right)
        self.entry_largo.pack()
        
        tk.Label(self.frame_right, text="Ancho (1-10):").pack()
        self.entry_ancho = tk.Entry(self.frame_right)
        self.entry_ancho.pack()
        
        tk.Label(self.frame_right, text="Fila Aspiradora:").pack()
        self.entry_x = tk.Entry(self.frame_right)
        self.entry_x.pack()
        
        tk.Label(self.frame_right, text="Columna Aspiradora:").pack()
        self.entry_y = tk.Entry(self.frame_right)
        self.entry_y.pack()
        
        tk.Button(self.frame_right, text="Iniciar", command=self.start_simulation).pack()
        self.message_label = tk.Label(self.frame_right, text="")
        self.message_label.pack()
    
    def start_simulation(self):
        try:
            self.rows = int(self.entry_largo.get())
            self.cols = int(self.entry_ancho.get())
            self.vacuum_x = int(self.entry_x.get())
            self.vacuum_y = int(self.entry_y.get())
            
            if not (1 <= self.rows <= 10 and 1 <= self.cols <= 10):
                self.message_label.config(text="Tamaño fuera de rango")
                return
            if not (0 <= self.vacuum_x < self.rows and 0 <= self.vacuum_y < self.cols):
                self.message_label.config(text="Posición fuera del área")
                return
            
            self.create_grid()
        except ValueError:
            self.message_label.config(text="Ingrese valores válidos")
    
    def create_grid(self):
        if hasattr(self, 'canvas'):
            self.canvas.destroy()
        
        self.canvas = tk.Canvas(self.frame_left, width=self.cols * 50, height=self.rows * 50)
        self.canvas.pack()
        
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        for _ in range(random.randint(1, (self.rows * self.cols) // 3)):
            x, y = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if (x, y) != (self.vacuum_x, self.vacuum_y):
                self.grid[x][y] = 1  # Casilla sucia
        
        self.draw_grid()
        
        if not self.clean_button_created:  # Solo crear el botón si no ha sido creado antes
            tk.Button(self.frame_right, text="Empezar limpieza", command=self.clean_adjacent).pack()
            self.clean_button_created = True  # Marcar que el botón fue creado
    
    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                color = "white"
                if (i, j) == (self.vacuum_x, self.vacuum_y):
                    color = "blue"  # Aspiradora
                elif self.grid[i][j] == 1:
                    color = "red"  # Suciedad
                
                self.canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill=color, outline="black")
    
    def clean_adjacent(self):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        cleaned = []
        
        for dx, dy in directions:
            nx, ny = self.vacuum_x + dx, self.vacuum_y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols and self.grid[nx][ny] == 1:
                self.grid[nx][ny] = 0  # Limpiar
                cleaned.append((nx, ny))
        
        self.draw_grid()
        self.message_label.config(text=f"Vecinos limpiados: {cleaned}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VacuumCleaner(root)
    root.mainloop()
