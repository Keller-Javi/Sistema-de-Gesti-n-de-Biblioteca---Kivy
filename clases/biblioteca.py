from clases.libro import Libro

class Biblioteca():
    def __init__(self):
        self.libros = {}
    
    def agregar_libro(self, nombre, autor, isbn, cantidad_disponible):
       self.libros[isbn] = Libro(nombre, autor, isbn, cantidad_disponible)

    def eliminar_libro(self, isbn):
        del self.libros[isbn]
    # En si no se elimina la instancia del libro pero como ninguna variable hace referencia a ese objeto, el recolector de basura va a librerar su memoria

    def buscar_libro_por_autor(self, autor):
        return [libro for libro in self.libros.values() if libro.autor.upper() == autor.upper()]

    def buscar_libro_por_nombre(self, nombre):
        return [libro for libro in self.libros.values() if libro.nombre == nombre]

    def mostrar_libros_disponibles(self):
        print('\nLibros disponibles en la biblioteca:')
        for libro in self.libros.values(): 
            print(libro)