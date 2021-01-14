from sympy import randprime, isprime
import random

 #  <p>Clase principal para Diffie-Hellman.</p>

 #  Diffie Helman V 1.0

 #	Montoya Montes Pedro-----31219536-2
 #	Calo Dizy Fabio G.

#Calcula el maximo comun divisor.
def mcd(a, b):
	while b != 0:
		a, b = b, a % b
	return a

'''
	Método que, dado un entero n, regresa la función phi(n)
	Entrada: Un entero n a calcular su phi(n)
	Salida: Un entero que es el resultado de phi(n)
'''
def phi(n):
	cantidad = 0        
	i = 0
	while i < n:
		if mcd(n, i) == 1:
			cantidad += 1
		i = i +1
	return cantidad

'''
	Método que, dado un entero a y m, calcula el orden de a respecto del módulo m.
	Entrada: Un entero a y un entero m para calcular Ord_m(a)
	Salida: Un entero que es el resultado de Ord_m(a)
'''
def orden(a, m, phi_m):
	# Revisamos si efectivamente podemos hacer el algoritmo.
	if mcd(a,m) != 1:
		print("No se puede, (a,m) no son primos relativos", a,m)
		sys.exit()
	#Ahora ciclamos con las potencias.
	pot=1
	while pot<=phi_m: #Usamos el teorema de que Ord_m(a)<=phi(m)
		if (phi_m%pot) != 0 : #Usamos el teorema de que ord_m(a)|phi(m)
			pot=pot+1
		r=(a**pot)
		if r%m==1:  #Si el módulo de a^m=1, acabamos y encontramos solución (r).
			return (pot,r)
		pot=pot+1 


# Función para calcular raíces primitivas de un entero positivo m
def raices_primitivas(m):
	phi_m =phi(m)
	total_raices=phi(phi_m)

	raices = []
	posible_raiz = 1
	while len(raices) < total_raices and posible_raiz < m: # and i < total_raices:
		while mcd(posible_raiz,m) != 1 and posible_raiz < m:
			posible_raiz = posible_raiz+1
		orden1 = orden(posible_raiz,m,phi_m)[0]
		if phi_m==orden1:
			raices.append(posible_raiz)	
		posible_raiz = posible_raiz +1

	else:
		return(raices,total_raices)


#Clase Diffie-Hellman
class DH:
	p = 0
	g = 0

	def __init__(self):
		DH.num_range = 2**10 			   						#Creamos el tamaño de nuestro primo, debe ser 1024
		DH.p = randprime(DH.num_range/2,DH.num_range) 			#Generamos el primer primo aleatorio.
		DH.primitive_root = raices_primitivas(DH.p) 			#Calculamos las raíces primitivas y guardamos.
		DH.primitive_roots = self.primitive_root[0] 			#El arreglo de las raíces primitivas.
		DH.total_roots = self.primitive_root[1]					#El total de raíces primitivas.
		DH.random_primitive_root = random.randint(0,DH.total_roots-1)#Valor aleatorio entre 0-phi(phi(p))
		DH.g= DH.primitive_roots[DH.random_primitive_root]		#Tomamos una raíz primitiva aleatoria

	#Función que calcula lo que se enviará
	def envia(self, num):
		return ((DH.g**num)%DH.p)	

	#Función que calcula lo que se rescibió.
	def recibe(self,mensaje,num):
		return((mensaje**num)%DH.p)

	#Clase auxiliar para ver toda la información que se está manejando, útil para programadores.
	def displayInfo(self):
		print("P   = ", self.p)
		print("g   = ", self.g)
		#print("Raíces raices_primitivas =",DH.primitive_roots) #Comentado para evitar mucha basura visual

#Clase para crear usuarios que tendrán un valor aleatorio
class user:
	n=0
	def __init__(self):
		user.n = random.randint(1,DH.p-1)
	def displayInfo(self):
		print(self.n)	


if __name__ == '__main__':
	dh = DH()			#Iniciamos Diffie-Hellman
	dh.displayInfo()	#Mostramos información para usuarios

	#Usuarios
	alice = user() 
	randA = alice.n
	print("El valor aleatorio de Alice es :")
	alice.displayInfo()

	bob = user()
	randB= bob.n
	print("El valor aleatorio de Bob es :")
	bob.displayInfo()

	#Mensajes que envia cada uno
	mensajeAlice =	dh.envia(randA)
	print("Alice envia a Bob: A=",DH.g,"^",randA," (módulo ",DH.p,") =", mensajeAlice)

	mensajeBob = dh.envia(randB)
	print("Bob envia a Alice: B=",DH.g,"^",randB," (módulo ",DH.p,") =", mensajeBob)	


	#Mensajes que reciben
	print("Alice calcula:     s=",mensajeBob,"^",randA, " (módulo ",DH.p,") =", dh.recibe(mensajeBob,randA))
	print("Bob calcula:       s=",mensajeAlice,"^",randB," (módulo ",DH.p,") =",  dh.recibe(mensajeAlice,randB))	