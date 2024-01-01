from clases.libro import Libro

class Usuario():
    def __init__(self, nombre_usuario, nombre, apellido):
        self.nombre_usuario = nombre_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.libros_prestados = []
    
    def __str__(self) -> str:
        return f'Nombre de usuario: {self.nombre_usuario}, de {self.apellido} {self.nombre}' 
    
    def tomar_prestado_libro(self, libro):
        self.libros_prestados.append(libro)

    def devolver_libro(self, libro):
        if libro in self.libros_prestados:
                self.libros_prestados.remove(libro) 
    
    def ver_libros_prestados(self):
        for libro in self.libros_prestados:
            print(libro)