from clases.libro import Libro
from clases.biblioteca import Biblioteca
from clases.usuario import Usuario
from clases.prestamo import Prestamo

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
            try:
                isbn = input('Ingrese el ISBN del libro: ')
            except:
                print('YA EXISTE ESE LIBRO...')
                continue
            nombre = input('Ingrese el nombre del libro: ')
            autor = input('Ingrese el nombre del autor: ')
            cantidad_disponible = int(input('Ingrese la cantidad disponible de este libro: '))
            biblioteca.agregar_libro(nombre, autor, isbn, cantidad_disponible)

        elif opsion == '2': # eliminar un libro
            isbn = input('Ingrese el ISBN del libro: ')
            biblioteca.eliminar_libro(isbn)

        elif opsion == '3': # buscar un libro por autor
            autor = input('Ingrese el nombre del autor: ')
            libros = biblioteca.buscar_libro_por_autor(autor)

            print('\nLibros disponibles de ese autor: ')
            for libro in libros:
                print(libro)
            input()

        elif opsion == '4': # buscar un libro por nombre
            nombre = input('Ingrese el nombre del libro: ')
            libros = biblioteca.buscar_libro_por_nombre(nombre)

            print('\nLibros disponibles con ese nombre: ')
            for libro in libros:
                print(libro)
            input()

        elif opsion == '5': # mostrar libros disponibles
            biblioteca.mostrar_libros_disponibles()
            input()

        elif opsion == '6': # volver al menu anterior
            break

        else:
            print('OPSIÓN INVÁLIDA...')

def gestionar_prestamos(usuario):
    print('\nGESTION DE LA PRESTAMOS')
    menu(2)

def gestion_de_cuenta(op):
    if op == '1':
        print('\nINICIAR SESIÓN:')
        nombre_usuario = input('Ingrese el nombre de usuario: ')
        try:
            usuario = usuarios[nombre_usuario]

            print('\nSe a iniciado sesión...')
            return usuario
        except:
            print('\nNO SE ENCONTRÓ ESE USUARIO...')

    elif op == '2':
        print('\nCREAR CUENTA:')
        nombre_usuario = input('Ingrese el nombre de usuario: ')

        try:
            usuario = usuarios[nombre_usuario]

            print('\nYA EXISTE ESE USUARIO...')
            return None
        except:
            nombre = input('Ingrese su nombre: ')
            apellido = input('Ingrese su apellido: ')

            usuario = Usuario(nombre_usuario=nombre_usuario, nombre=nombre, apellido=apellido)
            usuarios[nombre_usuario] = usuario

            print('\nSe creó la cuenta con éxito...')
            return usuario
    else: 
        return None
    # va a retornar el usuario si inicia sesión o crea uno y si resibe otra opsión va a volver hacia atras en el menú

biblioteca = Biblioteca()
usuarios = {}
seleccion = 0

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
            print(usuario)
            input()
            gestionar_prestamos(usuario)
    elif seleccion == '3': # fin del programa
        print('Fin del programa...')
        break
    else: # ingreso cualquier cosa
        print('OPSIÓN INVÁLIDA...')