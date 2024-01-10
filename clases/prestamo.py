from clases.libro import Libro
from clases.usuario import Usuario
from datetime import datetime 

class Prestamo():
    def __init__(self, libro, usuario):
        self.libro = libro
        self.usuario = usuario
        self.fecha_prestamo = datetime.now()
        self.fecha_devolucion = None

    def __str__(self):
        return f'Libro: {self.libro}, usuario: {self.usuario.nombre_usuario}'

    def devolución(self):
        self.fecha_devolucion = datetime.now()

        tiempo_prestado = self.fecha_devolucion - self.fecha_prestamo
        return tiempo_prestado.days
    # retorna los dias de diferencia que hay entre el día del prestamo y el día actual 