from clases.libro import Libro
from clases.usuario import Usuario
from datetime import datetime 

class Prestamo():
    def __init__(self, libro, usuario):
        self.libro = libro
        self.usuario = usuario
        self.fecha_prestamo = datetime.now()
        self.fecha_devolucion = None

    def devolución(self):
        self.fecha_devolucion = datetime.now()

    def tiempo_prestamo(self):
        ahora = datetime.now().day
        tiempo_prestado = ahora - self.fecha_prestamo
        return tiempo_prestado.days
    # retorna los dias de diferencia que hay entre el día del prestamo y el día actual 