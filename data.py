import tkinter as tk
from tkinter import *
from tkinter import ttk

import sqlite3


class Product:
    db_name = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title("BeeHigh Database")

        # Crear frame contenedor
        frame = LabelFrame(self.wind, text = "Registre un nuevo producto")
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Entrada de nombre
        Label(frame, text = "Nombre: ").grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        # Entrada de precio
        Label(frame, text = "Precio ").grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        # Botón agregar producto
        ttk.Button(frame, text = "Guardar producto", command = self.add_producto).grid(row =  3, columnspan = 2, sticky = W + E)

        # Feedback message
        self.mensaje = Label(text = '', fg = 'green')
        self.mensaje.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Tabla
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = "Nombre", anchor = CENTER)
        self.tree.heading('#1', text = "Precio", anchor = CENTER)

        # Llenando filas
        self.ob_producto()

        # Botones inferiores
        ttk.Button(text = 'ELIMINAR', command = self.del_producto).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'EDITAR', command = self.edi_producto).grid(row = 5, column = 1, sticky = W + E)

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def ob_producto(self):
        # Limpiando tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # Consulta de datos
        query = 'SELECT * FROM Producto ORDER BY Nombre DESC'
        db_rows = self.run_query(query)
        # Llenando datos
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_producto(self):
        if self.validation():
            query = 'INSERT INTO Producto VALUES(NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.mensaje['fg'] = 'black'
            self.mensaje['text'] = 'El producto {} ha sido agregado con exito'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.mensaje['fg'] = 'red'
            self.mensaje['text'] = 'Se necesita indicar el nombre y precio'
        self.ob_producto()

    def del_producto(self):
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje['fg'] = 'red'
            self.mensaje['text'] = 'Por favor seleccione un producto'
            return
        self.mensaje['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM Producto WHERE Nombre = ?'
        self.run_query(query, (name, ))
        self.mensaje['fg'] = 'black'
        self.mensaje['text'] = 'El producto {} ha sido eliminado satisfactoriamente'.format(name)
        self.ob_producto()

    def edi_producto(self):
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje['fg'] = 'red'
            self.mensaje['text'] = 'Por favor seleccione un producto'
            return
        name = self.tree.item(self.tree.selection())['text']
        vi_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.iconbitmap("beehigh-b-min.ico")
        self.edit_wind.title("Editar producto")

        # Nombre anterior
        Label(self.edit_wind, text = "Nombre anterior: ").grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        # Nuevo nombre
        Label(self.edit_wind, text = "Nombre nuevo: ").grid(row = 1, column = 1)
        self.new_name = Entry(self.edit_wind)
        self.new_name.grid(row = 1, column = 2)
        # Precio anterior
        Label(self.edit_wind, text = "Precio antrerior: ").grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = vi_price), state = 'readonly').grid(row = 2, column = 2)
        # Nuevo precio
        Label(self.edit_wind, text = "Precio nuevo: ").grid(row = 3, column = 1)
        self.new_price = Entry(self.edit_wind)
        self.new_price.grid(row = 3, column = 2)

        Button(self.edit_wind, text = "Actualizar", command = lambda: self.edit_records(self.new_name.get(), name, self.new_price.get(), vi_price)).grid(row = 4, column = 2, sticky = W + E)

    def validation_rec(self):
        return len(self.new_name.get()) != 0 and len(self.new_price.get()) != 0
    
    def edit_records(self, new_name, name, new_price, vi_price):
        self.mensaje['text'] = ''
        if self.validation_rec():
            query = 'UPDATE Producto SET Nombre = ?, Precio = ? WHERE Nombre = ? AND Precio = ?'
            parameters = (self.new_name.get(), self.new_price.get(), name, vi_price)
            self.run_query(query, parameters)
            self.edit_wind.destroy()
            self.mensaje['text'] = 'El producto {} ha sido actualizado correctamente'.format(name)
        else:
            self.edit_wind.destroy()
            self.mensaje['fg'] = 'red'
            self.mensaje['text'] = 'Se necesita indicar el nombre y precio nuevos'
        self.ob_producto()



if __name__ == '__main__':
    window = Tk()
    style = ttk.Style()
    window.iconbitmap("machine_learning//beehigh-b-min.ico")
    style.theme_use("clam")
    aplication = Product(window)
    window.mainloop()
    



