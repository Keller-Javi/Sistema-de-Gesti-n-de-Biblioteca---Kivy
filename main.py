from ast import Pass, Try
from pickle import NONE
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
            isbn = input('Ingrese el ISBN del libro: ')

            if isbn in biblioteca.libros.keys():
                print('')
                print('YA EXISTE UN LIBRO CON ESE ISBN...')
                input('')
                continue

            nombre = input('Ingrese el nombre del libro: ')
            autor = input('Ingrese el nombre del autor: ')
            cantidad_disponible = int(input('Ingrese la cantidad disponible de este libro: '))
            biblioteca.agregar_libro(nombre, autor, isbn, cantidad_disponible)

        elif opsion == '2': # eliminar un libro
            try:
                isbn = input('Ingrese el ISBN del libro: ')
                biblioteca.eliminar_libro(isbn)
            except:
                print('')
                print('HUBO UN ERROR AL ELIMINAR EL LIBRO...')
                input()

        elif opsion == '3': # buscar un libro por autor
            autor = input('Ingrese el nombre del autor: ')
            libros = biblioteca.buscar_libro_por_autor(autor)

            if libros:
                print('\nLibros disponibles de ese autor: ')
                for libro in libros:
                    print(libro)
            else:
                print('NO SE ENCONTRÓ NINGÚN LIBRO DE ESE AUTOR...')
            input()

        elif opsion == '4': # buscar un libro por nombre
            nombre = input('Ingrese el nombre del libro: ')
            libros = biblioteca.buscar_libro_por_nombre(nombre)

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
                lista_libros = biblioteca.buscar_libro_por_autor(autor)
            elif ops == '2':
                nombre = input('Ingrese el nombre del libro: ')
                lista_libros = biblioteca.buscar_libro_por_autor(nombre)
            
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

                if libro is not None:
                    print(f'Desea tomar prestado el siguiente libro: {libro}')
                    ud = input('Si/No: ').upper()

                    if ud == 'SI':
                        usuario.tomar_prestado_libro(libro)
                        prestamo = Prestamo(libro, usuario)
                        prestamos.append(prestamo)
                        biblioteca.libros[libro.isbn].cantidad_disponible -= 1
                        print(prestamo)
                        print('Se realizo correctamente el prestamo.')
                    else:
                        print('Se cancela la devolución...')
            else:
                print('NO SE ENCONTRÓ NINÚN LIBRO...')
        elif op == '2': # Devolver un libro
            if usuario.libros_prestados:
                libro = None
                numero_libro = -1

                if len(usuario.libros_prestados) > 1:
                    print('Elige un libro: ')
                    for x,libro in enumerate(usuario.libros_prestados):
                        print(f'{x+1}. {libro}')
                    
                    try:
                        numero_libro = int(input('Ingrese una opsión: '))
                        numero_libro -= 1

                        libro = usuario.libros_prestados[numero_libro]
                    except:
                        print('NO EXISTE ESA OPSIÓN...')
                else:
                    libro = usuario.libros_prestados[0]
                
                if libro:
                    usuario.devolver_libro(libro)

                    prestamos_del_usuario = [prestamo for prestamo in prestamos if prestamo.usuario == usuario]

                    for prestamo in prestamos_del_usuario:
                        if prestamo.libro == libro:
                            prestamos.remove(prestamo)
                    
                    biblioteca.libros[libro.isbn].cantidad_disponible += 1
                    print('Se devolvión el libro correctamente...')
                    input('')
                
            else:
                print('NO HAY NINGÚN LIBRO PRESTADO...')
                input('')
        elif op == '3': # Ver libros prestados
            for libro in usuario.libros_prestados:
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
prestamos = []
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
            input()
            gestionar_prestamos(usuario)
    elif seleccion == '3': # fin del programa
        print('Fin del programa...')
        break
    else: # ingreso cualquier cosa
        print('OPSIÓN INVÁLIDA...')