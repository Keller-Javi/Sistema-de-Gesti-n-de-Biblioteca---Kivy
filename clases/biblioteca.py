import sqlite3
from clases.libro import Libro
from busqueda_avanzada import Indexado

class Biblioteca:
    def __init__(self, conexion):
        self.conexion = conexion
        self.crear_tabla_libros()

        self.lista_libros = []
        self.indexado = Indexado()
        self.generar_busqueda()

    def crear_tabla_libros(self):
        cursor = self.conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS libros (
                isbn TEXT PRIMARY KEY,
                nombre TEXT,
                autor TEXT,
                cantidad_disponible INTEGER
            )
        ''')
        self.conexion.commit()

    def agregar_libro(self, libro):
        cursor = self.conexion.cursor()
        cursor.execute('''
            INSERT INTO libros (isbn, nombre, autor, cantidad_disponible)
            VALUES (?, ?, ?, ?)
        ''', (libro.isbn, libro.nombre, libro.autor, libro.cantidad_disponible))
        self.conexion.commit()

        self.lista_libros.append(libro.nombre)
        self.indexado.generar_index(self.lista_libros)
    """ Esta función agrega un libro a la base de datos y actualiza el index de busqueda
    """

    def eliminar_libro(self, isbn):
        cursor = self.conexion.cursor()

        cursor.execute('DELETE FROM libros WHERE isbn = ?', (isbn,))

        self.conexion.commit()

        self.indexado.limpiar_index()
        self.generar_busqueda()
    """ Al eleminar un libro se debe limpiar el indexado y volver a generarlo
    """
    
    def modificar_cantidad(self, isbn, cantidad):
        cursor = self.conexion.cursor()

        cursor.execute('SELECT * FROM libros WHERE isbn = ?', (isbn,))
        resultado = cursor.fetchone()

        if resultado:
            cursor.execute("UPDATE libros SET cantidad_disponible = ? WHERE isbn = ?", (resultado[3] + cantidad, isbn))
            self.conexion.commit()

    def buscar_libro_por_isbn(self, isbn):
        cursor = self.conexion.cursor()
        cursor.execute('SELECT * FROM libros WHERE isbn = ?', (isbn,))
        resultado = cursor.fetchone()
        if resultado:
            return Libro(resultado[1], resultado[2], resultado[0], resultado[3])
        else:
            return None

    def buscar_libros_por_nombre(self, nombre):
        cursor = self.conexion.cursor()
        libros = []
        lista_de_coincidencias = self.indexado.busqueda(nombre)

        for x in lista_de_coincidencias:
            cursor.execute('SELECT * FROM libros WHERE nombre = ?', (self.lista_libros[x],))
            resultados = cursor.fetchall() # En caso de que hayan libros con nombre iguales
            for fila in resultados:
                libros.append(Libro(fila[1], fila[2], fila[0], fila[3]))

        return libros
    """ Esta función utiliza un sistema de busqueda en el que al ingresar una parte del nombre del libro
        se va a obtener las coincidecias, es decir, libros con nombres similares
    """

    def buscar_libros_por_autor(self, autor):
        cursor = self.conexion.cursor()
        cursor.execute('SELECT * FROM libros WHERE autor = ?', (autor,))
        resultados = cursor.fetchall()
        libros = [Libro(fila[1], fila[2], fila[0], fila[3]) for fila in resultados]
        return libros

    def mostrar_libros_disponibles(self):
        cursor = self.conexion.cursor()

        print('\nLibros disponibles en la biblioteca:')
        cursor.execute('SELECT * FROM libros')
        libros = cursor.fetchall()

        for fila in libros:
            libro = Libro(fila[1], fila[2], fila[0], fila[3])
            print(libro)

    def generar_busqueda(self):
        self.lista_libros = []
        cursor = self.conexion.cursor()

        cursor.execute('SELECT * FROM libros')
        libros = cursor.fetchall()

        for fila in libros:
            self.lista_libros.append(fila[1])
        
        self.indexado.generar_index(self.lista_libros)
    """ Esta función se ejecuta al iniciar el programa o al eliminar un libro de la biblioteca
    """