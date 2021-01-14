from sympy import randprime, isprime

 #  <p>Clase principal para cifrar y descifrar con algoritmo RSA.</p>

 #  RSA 1.4

 #	Montoya Montes Pedro-----31219536-2
 #	Calo Dizy Fabio G.

#Calcula el maximo comun divisor.
def mcd(a, b):
	while b != 0:
		a, b = b, a % b
	return a

#Calcula con algoritmo extendido de euclides.
def aede(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = aede(b % a, a)
		return (g, x - (b // a) * y, y)

#Calcula el inverso del módulo.
def modinv(a, m):
	g, x, y = aede(a, m)
	if g != 1:
		raise Exception('No existe el inverso del modulo')
	else:
		return x % m

#Clase RSA
class RSA:
	p = 0
	q = 0
	N = 0
	phi = 0
	e = 0
	d = 0

	def __init__(self):
		RSA.num_range = 2**10 			   #Creamos el tamaño de nuestro primo, debe ser 1024
		RSA.p = randprime(RSA.num_range/2,RSA.num_range) #Generamos el primer primo aleatorio.
		RSA.q = randprime(RSA.num_range/2,RSA.num_range) #Generamos el segundo primo aleatorio.
		#Si se da el caso de que ambos primos son el mismo, los volvemos a generar
		while RSA.p == RSA.q:
			RSA.p = randprime(RSA.num_range/2,RSA.num_range) #Generamos el primer primo aleatorio.
			RSA.q = randprime(RSA.num_range/2,RSA.num_range) #Generamos el segundo primo aleatorio.
		RSA.N = RSA.p*RSA.q 			   #Calculamos n = p*q.
		RSA.phi = (RSA.p-1)*(RSA.q-1) 	   #Calculamos phi(n)= (p-1)(q-1).

		RSA.e = randprime(1,RSA.num_range/2)
		
		#Creamos a "e" para que sea menor que phi y que el mcd(phi,e) = 1
		while mcd(RSA.phi, RSA.e) != 1 and RSA.e < RSA.phi:
			RSA.e += 1
			pass

		RSA.d =  modinv(RSA.e, RSA.phi)    #Calculamos d el módulo inverso de e con phi.

	def genera_llaves(self):
		return ((RSA.e, RSA.N), (RSA.N, RSA.d))

	#Clase auxiliar para ver toda la información que se está manejando, útil para programadores.
	def displayInfo(self):
		print("P   = ", self.p)
		print("Q   = ", self.q)
		print("N   = ", self.N)
		print("Phi = ", self.phi)
		print("e   = ", self.e)
		print("d   = ", self.d)

#Clase que dado un plainText, lo encripta con algoritmo de RSA
def encripta(plainText, llavePublica):
	e = llavePublica[0]
	N = llavePublica[1]
	#print("1.Cadena convertida:")
	#textoOriginal = [(ord(char)) for char in plainText]

	#print(textoOriginal)
	#print("2.Cadena encriptada: ")
	cipher = [(ord(char) ** e) % N for char in plainText]	

	#print(cipher)
	return cipher

#Clase que dado un cipherText, lo desencripta con algoritmo de RSA
def desencripta(cipherText, llavePrivada):
	d = llavePrivada[1]
	N = llavePrivada[0]

	cipher = [chr(char ) for char in cipherText]
	print("Cadena Encriptada: ")
	textoCifrado = ''.join(cipher)
	print("\t\t  ",textoCifrado)

	print("Awanta, descifrando...") 					# Mensaje para que no se desespere el ususario.

	plain = [chr((char ** d) % N) for char in cipherText]
	textoDescifrado = ''.join(plain)
	print("Cadena desencriptada: ")
	print("\t\t  ",textoDescifrado)
	return textoDescifrado

if __name__ == '__main__':
	rsa = RSA()											# Creamos un nuevo objeto del tipo RSA

	textoPlano = input("Ingresa el texto: ")	        # Texto dado por el usuario.

	rsa.displayInfo()

	print("Texto original: ") 
	print("\t\t  ", textoPlano)

	llavePublica, llavePrivada = rsa.genera_llaves(); 	#Generamos las llaves públicas y privadas.
	print( "Tu llave pública es: ", llavePublica ," y tu llave privada es: ", llavePrivada)

	text = encripta(textoPlano, llavePublica)			# Texto encriptado en forma su forma númerica.
	desencripta(text, llavePrivada)						# Desencriptamos nuestro texto.
