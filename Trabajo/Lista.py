import sqlite3
from tkinter import *
from tkinter import messagebox
from datetime import datetime

# Función para conectar a la base de datos
def conectar_bd():
    conexion = sqlite3.connect('tareas.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY,
            descripcion TEXT NOT NULL,
            fecha_creacion TEXT NOT NULL,
            completada INTEGER
        )
    ''')
    conexion.commit()
    return conexion, cursor

# Función para agregar una nueva tarea
def agregar_tarea():
    descripcion = entrada_descripcion.get()
    if descripcion.strip() == "":
        messagebox.showerror("Error", "Por favor ingrese una descripción para la tarea.")
        return

    conexion, cursor = conectar_bd()
    fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    completada = 0
    cursor.execute('INSERT INTO tareas (descripcion, fecha_creacion, completada) VALUES (?, ?, ?)', (descripcion, fecha_creacion, completada))
    conexion.commit()
    conexion.close()
    messagebox.showinfo("Éxito", "Tarea agregada exitosamente.")
    entrada_descripcion.delete(0, END)
    mostrar_tareas()

# Función para obtener todas las tareas
def obtener_tareas():
    conexion, cursor = conectar_bd()
    cursor.execute('SELECT * FROM tareas ORDER BY completada, fecha_creacion DESC')
    tareas = cursor.fetchall()
    conexion.close()
    return tareas

# Función para marcar una tarea como completada
def completar_tarea(id_tarea):
    conexion, cursor = conectar_bd()
    cursor.execute('UPDATE tareas SET completada = 1 WHERE id = ?', (id_tarea,))
    conexion.commit()
    conexion.close()
    messagebox.showinfo("Éxito", "Tarea marcada como completada.")
    mostrar_tareas()

# Función para mostrar las tareas en la lista
def mostrar_tareas():
    lista_tareas.delete(0, END)
    tareas = obtener_tareas()
    for tarea in tareas:
        if tarea[3] == 0:
            estado = "Pendiente"
        else:
            estado = "Completada"
        lista_tareas.insert(END, f"{tarea[0]}. {tarea[1]} - {estado}")

# Función para manejar la acción de completar una tarea seleccionada
def completar_seleccion():
    seleccion = lista_tareas.curselection()
    if len(seleccion) == 0:
        messagebox.showerror("Error", "Por favor seleccione una tarea.")
        return
    id_tarea = lista_tareas.get(seleccion[0]).split(".")[0]
    completar_tarea(id_tarea)

# Crear la interfaz gráfica
ventana = Tk()
ventana.title("Administrador de Tareas")

# Decoración
titulo = Label(ventana, text="Administrador de Tareas", font=("Arial", 14))
titulo.grid(row=0, column=0, columnspan=4, padx=10, pady=5)

separador = Label(ventana, text="---------------------------------------------")
separador.grid(row=1, column=0, columnspan=4)

# Etiqueta y entrada para la descripción de la tarea
etiqueta_descripcion = Label(ventana, text="Descripción de la Tarea:")
etiqueta_descripcion.grid(row=2, column=0, padx=10, pady=5, sticky=W)
entrada_descripcion = Entry(ventana, width=50)
entrada_descripcion.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

# Botón para agregar una nueva tarea
boton_agregar = Button(ventana, text="Agregar Tarea", command=agregar_tarea)
boton_agregar.grid(row=2, column=3, padx=10, pady=5)

# Lista para mostrar las tareas
lista_tareas = Listbox(ventana, width=60)
lista_tareas.grid(row=3, column=0, columnspan=4, padx=10, pady=5)

# Botón para completar tarea seleccionada
boton_completar = Button(ventana, text="Completar Tarea", command=completar_seleccion)
boton_completar.grid(row=4, column=0, columnspan=4, padx=10, pady=5)

# Mostrar las tareas al iniciar la aplicación
mostrar_tareas()

# Decoración adicional
creditos = Label(ventana, text="Creado por: Tu Nombre", font=("Arial", 10), fg="gray")
creditos.grid(row=5, column=0, columnspan=4, padx=10, pady=5)

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
