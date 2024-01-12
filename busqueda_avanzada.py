"""
Se pasa todo a mayúsculas para no tener que distinguir las palabras, por ejemplo: las, Las, lAS, ect... sería iguales para este programa.
"""

class Indexado():
	def __init__(self):
		self.index = {}
		self.ultimo_len = 0  # Se usa para saber cuando y donde se agregaron nuevos elementos

	def generar_index(self, libros):
		for i, libro in enumerate(libros[self.ultimo_len::1]):
			for palabra in libro.split():
				palabra = palabra.upper()
				if palabra not in self.index.keys():
					self.index[palabra] = [i + self.ultimo_len]
				else:
					self.index[palabra].append(i + self.ultimo_len)

		self.ultimo_len = len(libros)
	"""La función genera un index que contiene todas las palabras de la lista de nombre de libros. Proceso llamado índices inversos (Inverted index).
	Este index es un diccionario que tiene como clave la palabra y el valor es la ubicación en la lista de nombres de libros.
	
	Ejemplo:
	    Entrada:
	libros = [ 'The quick brown fox', 'A quick brown dog']
        Salida: (Termino | Documento)
    index = {'The':     [1]
            'quick':  [1, 2]
            'brown':  [1, 2]
            'fox':    [1]
            'A':      [2]
            'dog':    [2]}
	"""

	def busqueda(self, palabras):
		lista_elementos = []
		for palabra in palabras.split():
			if palabra.upper() in self.index.keys():
				lista_elementos.append(self.index[palabra.upper()])
			else:
				lista_elementos = []
				break
		
		if lista_elementos:
			return self.elementos_comunes(lista_elementos)
		
		return []
	"""Esta función va a retornar una lista con la ubicación de los libros que 
	tienen parte de ese nombre del libro.
	Va a retornar una lista vacía si no encuentra el libro.
	Ejemplo:
	
		Entrada: 
	libros = ['Las aventuras de Pepe',
			'Las aventuras de Juan',
			'Jujutsu Kaisen',
			'One Piece',
			'Las extrañas aventuras de Pedro']
	palabras1 = 'Las aventuras de'
	palabras2 = 'aventuras de pepe'
	palabras3 = 'av3nturas de juan'
 	
		Salida:
	- Para palabra1:
	['Las aventuras de Pepe', 'Las aventuras de Juan','Las extrañas aventuras de Pedro']
	- Para palabra2:
	['Las aventuras de Pepe']
	- Para palabra3:
	[]
	
	"""
	
	def elementos_comunes(self, listas):
		elementos_comunes = set(listas[0])
		for lista in listas[1:]:
			elementos_comunes.intersection_update(lista)
		return list(elementos_comunes)
	""" Retorna los elementos de la lista de listas que son similares entre si,
    ya que estos van a indicar las coinsidencias entre los distintos nombres de libros.
	
	Ejemplo:
    	de entrada:
	listas = [[2,3,4,5,6],[1,2,3,4,5],[3,4,5,6,7]]
    	de salida:
	[3,4,5]
	"""

	def limpiar_index(self):
		self.index = {}
		self.ultimo_len = 0
	"""Al momento de eliminar un libro para evitar complejidades se limpia el diccionario
	de indexado y se lo vuelve a hacer, ya dependiendo del caso del libro eliminado la
	sería lo más optimo"""
