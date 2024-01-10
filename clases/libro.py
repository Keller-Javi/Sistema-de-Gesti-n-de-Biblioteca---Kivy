class Libro():
    def __init__(self, nombre, autor, isbn, cantidad_disponible):
        self.nombre = nombre
        self.autor = autor
        self.isbn = isbn
        self.cantidad_disponible = cantidad_disponible
    
    def __str__(self):
        return f"{self.nombre} del autor: {self.autor}. Codigo: {self.isbn}"
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(object, Libro):
            return self.isbn == object.isbn
        return False
            