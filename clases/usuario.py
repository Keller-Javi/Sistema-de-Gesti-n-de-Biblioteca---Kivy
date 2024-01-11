from clases.libro import Libro

class Usuario():
    def __init__(self, nombre_usuario, nombre, apellido):
        self.nombre_usuario = nombre_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.libros_prestados = []
    
    def __str__(self) -> str:
        return f'Nombre de usuario: {self.nombre_usuario}, de {self.apellido} {self.nombre}' 
    
    def tomar_libro_prestado(self, isbn):
        self.libros_prestados.append(isbn)

    def devolver_libro(self, isbn):
        if isbn in self.libros_prestados:
                self.libros_prestados.remove(isbn) 
    
    def ver_libros_prestados(self):
        return self.libros_prestados