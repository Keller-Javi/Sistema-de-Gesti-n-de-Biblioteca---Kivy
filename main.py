import sqlite3
from clases.libro import Libro
from clases.biblioteca import Biblioteca
from clases.usuario import Usuario
from clases.prestamo import Prestamo
from datetime import datetime
import json

def menu(op):
    if op == 0:
        print("1. Gestionar la bilioteca")
        print("2. Gestionar prestamos")
        print('3. Fin del programa')
    elif op == 1:
        print("1. Iniciar sesión")
        print("2. Crear usuario")
        print("3. Volver")
    elif op == 2:
        print('1. Tomar prestado un libro')
        print('2. Devolver un libro')
        print('3. Ver libros prestados')
        print('4. Ver libros disponibles')
        print('5. Volver')
    elif op == 3:
        print('1. Agregar un libro')
        print('2. Eliminar un libro')
        print('3. Buscar un libro por autor')
        print('4. Buscar un libro por nombre')
        print('5. Ver todos los libros disponibles')
        print('6. Volver')

def gestionar_biblioteca():
    while True:
        print('\nGESTION DE LA BIBLIOTECA:')
        menu(3)
        opsion = input('\nIngrese una opsion: ')

        if opsion == '1': # agregar un libro
            isbn = input('Ingrese el ISBN del libro: ')

            cursor.execute('SELECT * FROM libros WHERE isbn = ?', (isbn,))
            libro = cursor.fetchone()

            if libro:
                print('')
                print('YA EXISTE UN LIBRO CON ESE ISBN...')
                input('')
                continue

            nombre = input('Ingrese el nombre del libro: ')
            autor = input('Ingrese el nombre del autor: ')
            try:
                cantidad_disponible = int(input('Ingrese la catidad de libros: '))
                libro = Libro(nombre, autor, isbn, cantidad_disponible)
                biblioteca.agregar_libro(libro)
            except:
                print('DEBE INGRESAR UN NUMERO ENTERO...')

        elif opsion == '2': # eliminar un libro
            isbn = input('Ingrese el isbn del libro: ')
            if biblioteca.buscar_libro_por_isbn(isbn):
                biblioteca.eliminar_libro(isbn)
                print('Se eliminoó correctamente...')
                input()
            else:
                print('NO EXISTE ESE LIBRO EN LA BIBLIOTECA...')
                input()

        elif opsion == '3': # buscar un libro por autor
            autor = input('Ingrese el nombre del autor: ')
            libros = biblioteca.buscar_libros_por_autor(autor)

            if libros:
                print('\nLibros disponibles de ese autor: ')
                for libro in libros:
                    print(libro)
            else:
                print('NO SE ENCONTRÓ NINGÚN LIBRO DE ESE AUTOR...')
            input()

        elif opsion == '4': # buscar un libro por nombre
            nombre = input('Ingrese el nombre del libro: ')
            libros = biblioteca.buscar_libros_por_nombre(nombre)

            if libros:
                print('\nLibros disponibles con ese nombre: ')
                for libro in libros:
                    print(libro)
            else:
                print('NO SE ENCONTRÓ NINGÚN LIBRO CON ESE NOMBRE...')
            input()

        elif opsion == '5': # mostrar libros disponibles
            biblioteca.mostrar_libros_disponibles()
            input()

        elif opsion == '6': # volver al menu anterior
            break

        else:
            print('OPSIÓN INVÁLIDA...')

def gestionar_prestamos(usuario):
    while usuario: # si hay un usuario funciona
        print('\nGESTION DE LA PRESTAMOS')
        menu(2)
        op = input('Ingrese una opsión: ')
        print('')

        if op == '1': # Tomar prestado un libro
            print('Como desea buscar el libro: ')
            print('1. Por autor')
            print('2. Por el nombre')
            print('Otro. Volver')
            ops = input('Seleccione una opsión: ')

            lista_libros = None # libros relacionados con la busqueda
            if ops == '1':
                autor = input('Ingrese el autor del libro: ')
                lista_libros = biblioteca.buscar_libros_por_autor(autor)
            elif ops == '2':
                nombre = input('Ingrese el nombre del libro: ')
                lista_libros = biblioteca.buscar_libros_por_autor(nombre)
            
            if lista_libros:
                libro = None
                if len(lista_libros) > 1: # si hay muchos libros
                    for x,libro in enumerate(lista_libros):
                        print(f'{x+1}. {libro}')
                    
                    try:
                        numero_libro = int(input('Seleccione una opsión: '))
                        numero_libro = numero_libro -1

                        libro = lista_libros[numero_libro]
                    except:
                        print('NO EXISTE ESA OPSIÓN...')
                else: # Si hay un solo libro
                    libro = lista_libros[0]

                if libro: # deberia haber una sola instacia si funcionó lo anterior
                    if libro.isbn in usuario.libros_prestados:
                        print('YA TIENE PRESTADO ESE LIBRO...')
                        continue

                    print(f'Desea tomar prestado el siguiente libro: {libro}')
                    ud = input('Si/No: ').upper()

                    if ud == 'SI':
                        usuario.tomar_libro_prestado(libro.isbn)

                        hoy = datetime.now()
                        prestamo = Prestamo(libro.isbn, usuario.nombre_usuario, f"{hoy.day}-{hoy.month}-{hoy.year}")
                        crear_prestamo(prestamo) # lo agrega a la base de datos

                        actualizar_tabla_usuario(usuario)
                        biblioteca.modificar_cantidad(libro.isbn,-1)
                        
                        print('Se realizo correctamente el prestamo.')
                    else:
                        print('Se cancela la devolución...')
            else:
                print('NO SE ENCONTRÓ NINÚN LIBRO...')

        elif op == '2': # Devolver un libro
            if usuario.libros_prestados:
                libro = None
                numero_libro = -1

                if len(usuario.libros_prestados) > 1: # muchos libros
                    libros = []
                    for isbn in usuario.libros_prestados:
                        cursor.execute('SELECT * FROM libros WHERE isbn = ?', (isbn,)) 
                        resultado = cursor.fetchone()
                        libros.append(Libro(resultado[1], resultado[2], resultado[0], resultado[3]))

                    print('Elige un libro: ')
                    for x,libro in enumerate(libros):
                        print(f'{x+1}. {libro}')
                    
                    try:
                        numero_libro = int(input('Ingrese una opsión: '))
                        numero_libro -= 1

                        libro = libros[numero_libro]
                    except:
                        print('NO EXISTE ESA OPSIÓN...')
                else: # si hay un solo libro
                    cursor.execute('SELECT * FROM libros WHERE isbn = ?', (usuario.libros_prestados[0],)) 
                    resultado = cursor.fetchone()
                    libro = Libro(resultado[1], resultado[2], resultado[0], resultado[3])
                
                if libro: # debería tener un solo libro en esta parte
                    print(f'Desea devolver el siguiente libro: {libro}')
                    ud = input('Si/No: ').upper()

                    if ud != 'SI':
                        continue

                    usuario.devolver_libro(libro.isbn)

                    cursor.execute('SELECT * FROM prestamos WHERE nombre_usuario =?', (usuario.nombre_usuario,))
                    prestamos_del_usuario = cursor.fetchall()

                    for prestamo_tabla in prestamos_del_usuario:
                        if prestamo_tabla[1] == libro.isbn:
                            hoy = datetime.now()
                            cursor.execute("UPDATE prestamos SET fecha_devolucion = ? WHERE id_prestamo =?", (f"{hoy.day}-{hoy.month}-{hoy.year}", prestamo_tabla[0]))
                            conexion.commit() # cuando encuentra el pretamo en la tabla agrega la fecha del dia en que se devolvió el libro
                    
                    biblioteca.modificar_cantidad(libro.isbn, +1)
                    actualizar_tabla_usuario(usuario)
                    print('Se devolvión el libro correctamente...')
                    input('')
                
            else:
                print('NO HAY NINGÚN LIBRO PRESTADO...')
                input('')

        elif op == '3': # Ver libros prestados
            if usuario.libros_prestados is None:
                print('No tiene ningun libro prestado...')
            for isbn in usuario.libros_prestados:
                cursor.execute('SELECT * FROM libros WHERE isbn = ?', (isbn,)) 
                resultado = cursor.fetchone()
                libro = Libro(resultado[1], resultado[2], resultado[0], resultado[3])
                print(libro)
            input('')
        elif op == '4': # Ver libros disponibles
            biblioteca.mostrar_libros_disponibles()
            input('')
        elif op == '5': # Volver
            break
        else: 
            print('OPSIÓN NO EXISTE...')
            input()

def gestion_de_cuenta(op):
    if op == '1':
        print('\nINICIAR SESIÓN:')
        nombre_usuario = input('Ingrese el nombre de usuario: ')

        cursor.execute('SELECT * FROM usuarios WHERE nombre_usuario = ?', (nombre_usuario,))
        resultado = cursor.fetchone()

        if resultado:
            usuario =  Usuario(nombre_usuario=resultado[0], nombre=resultado[1], apellido=resultado[2])
            if resultado[3]: # si hay elementos en
                usuario.libros_prestados=json.loads(resultado[3])

            print('\nSe a iniciado sesión...')
            return usuario
        else:
            print('\nNO SE ENCONTRÓ ESE USUARIO...')
            return None

    elif op == '2':
        print('\nCREAR CUENTA:')
        nombre_usuario = input('Ingrese el nombre de usuario: ')

        cursor.execute('SELECT * FROM usuarios WHERE nombre_usuario =? ', (nombre_usuario,))
        usuario = cursor.fetchone()

        if usuario:
            print('\nYA EXISTE ESE USUARIO...')
            return None
        else:
            nombre = input('Ingrese su nombre: ')
            apellido = input('Ingrese su apellido: ')

            usuario = Usuario(nombre_usuario=nombre_usuario, nombre=nombre, apellido=apellido)
            
            cursor.execute('''INSERT INTO usuarios (nombre_usuario, nombre, apellido, libros_prestados) VALUES (?, ?, ?, ?)''', (nombre_usuario, nombre, apellido, ''))
            conexion.commit()

            print('\nSe creó la cuenta con éxito...')
            return usuario
    else: 
        return None
    # va a retornar el usuario si inicia sesión o crea uno y si resibe otra opsión va a volver hacia atras en el menú

def actualizar_tabla_usuario(usuario):
    if usuario.libros_prestados:
        cursor.execute("UPDATE usuarios SET libros_prestados = ? WHERE nombre_usuario = ?", (json.dumps(usuario.libros_prestados), usuario.nombre_usuario))
    else:
        cursor.execute("UPDATE usuarios SET libros_prestados = ? WHERE nombre_usuario = ?", '', usuario.nombre_usuario)
    conexion.commit()

conexion = sqlite3.connect("database.db")
biblioteca = Biblioteca(conexion)

cursor = conexion.cursor()
cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                nombre_usuario TEXT PRIMARY KEY,
                nombre TEXT,
                apellido TEXT,
                libros_prestados TEXT
            )
        ''')
cursor.execute('''
            CREATE TABLE IF NOT EXISTS prestamos (
                id_prestamo INTEGER PRIMARY KEY,
                isbn TEXT,
                nombre_usuario TEXT,
                fecha_prestamo TEXT,
                fecha_devolucion TEXT
            )
        ''')
conexion.commit()

def crear_prestamo(prestamo):
    cursor.execute("SELECT COUNT(*) FROM prestamos")
    cantidad_elementos = cursor.fetchone()[0]
    cursor.execute('''INSERT INTO prestamos (id_prestamo, isbn, nombre_usuario, fecha_prestamo, fecha_devolucion) VALUES (?, ?, ?, ?, ?)''', (cantidad_elementos+1, prestamo.libro, prestamo.usuario, prestamo.fecha_prestamo, '')) 
    conexion.commit()

while True:
    print('')
    menu(0)
    seleccion = input('\nIngrese una opsión: ')
    
    if seleccion == '1': # gestionar biblioteca
        gestionar_biblioteca()
    elif seleccion == '2': # gestionar prestamos
        usuario = None
        menu(1)
        usuario = gestion_de_cuenta(input('\nIngrese una opsión: '))
        if usuario is not None:
            input()
            gestionar_prestamos(usuario)
            actualizar_tabla_usuario(usuario)

    elif seleccion == '3': # fin del programa
        print('Fin del programa...')
        break
    else: # ingreso cualquier cosa
        print('OPSIÓN INVÁLIDA...')

conexion.commit()
conexion.close()