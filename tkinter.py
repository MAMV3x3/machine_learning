import tkinter 
from tkinter import *

def main():
    ventana = tkinter.Tk()
    ventana.mainloop()
    ventana.geometry("300x300")

    etiqueta = tkinter.Label(ventana, text = "Hola Mundo")
    etiqueta.pack()
if __name__=='__main__':
    main()
