from clases.libro import Libro
from clases.usuario import Usuario
from datetime import datetime 

class Prestamo():
    def __init__(self, libro, usuario, fecha_prestamo):
        self.libro = libro # isbn del libro
        self.usuario = usuario # nombre de usuario
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = ''

    def __str__(self):
        return f'Libro: {self.libro}, usuario: {self.usuario}'