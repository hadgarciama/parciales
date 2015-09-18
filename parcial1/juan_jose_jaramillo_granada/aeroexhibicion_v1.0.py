#Aeroexhibicion v1.0
import os
import sys
import shutil
#-------------------------------Definicion de Variables e Inicializacion---------------------------------------
directorio_raiz = os.getcwd()
argumentos = sys.argv
#-------------------------------Definicion de Funciones---------------------------------------
def escribir_archivo(nombre_archivo,escribir):
	try:
		archivo = open(nombre_archivo,'a')
		archivo.write(str(escribir)+'\n')
		archivo.close()
	except IOError:
		guardar_error('Error al escribir en archivo '+nombre_archivo)
		return False
	return True
		
def guardar_error(error):
	escribir_archivo('error.txt',error)
	
def guardar_registro(registro):
	escribir_archivo('registro.txt',registro)
	
def crear_archivo(nombre_archivo):
	try:
		archivo = open(nombre_archivo, 'w')
		archivo.close()
		guardar_registro('Archivo '+nombre_archivo+' creado')
	except:
		guardar_error('Error creando archivo '+nombre_archivo)
		return False
	return True

def leer_archivo(nombre_archivo):
	lineas = []
	try:
		archivo = open(nombre_archivo,'r')
		lineas = archivo.readlines()
		archivo.close()
	except IOError:
		guardar_error("Error leyendo archivo "+nombre_archivo)
	return lineas 
	
def fatal_error():
	guardar_registro('TERMINO EL PROGRAMA')
	print '\nEL PROGRAMA HA FINALIZADO'
	sys.exit()

#-------------------------------Validaciones--------------------------------------
crear_archivo('error.txt')
crear_archivo('registro.txt')

#Validacion 1
if len(argumentos) != 3:
	guardar_error('Numero de argumentos suministrados incorrectos')
	print 'No a suministrado los argumentos necesarios'
	fatal_error()
else:
	elementos = argumentos[1]
	requisitos = argumentos[2]
	guardar_registro('Se valido el ingreso del correcto numero de argumentos en la linea de comandos')

#Validacion 2
if os.path.exists(directorio_raiz+'\modelos') == False:
	print 'No se han suministrado los modelos a inspeccionar'
	guardar_error('No se han suministrado los modelos a inspeccionar')
	fatal_error()
else:
	guardar_registro('Verificada la existencia del directorio modelos')
	
contenido_raiz = []
pcontenido_raiz = os.listdir(directorio_raiz)
nombre_elementos = elementos.split('.')
nombre_elementos = nombre_elementos[0]
nombre_requisitos = requisitos.split('.')
nombre_requisitos = nombre_requisitos[0]
for i in pcontenido_raiz:
	k = i.split('.')
	k = k[0]
	contenido_raiz.append(k)
	
if nombre_elementos in contenido_raiz:
	guardar_registro('Comprobada la concordancia del archivo de elementos que existe con el nombre suministrado')
	if (nombre_elementos+'.txt') in pcontenido_raiz:
		elementos = nombre_elementos+'.txt'
		guardar_registro('Comprobada la existencia de archivos con elementos y su respectiva extension')
	else:
		print 'El nombre suministrado de elementos no concuerda con el archivo existente.\nPor Favor Revisar'
		guardar_error('El nombre suministrado de elementos no concuerda con el archivo existente')
		fatal_error()
else:
	print 'Archivo con elementos no existe'
	guardar_error('Archivo con elementos no existe')
	fatal_error()
	
if nombre_requisitos in contenido_raiz:
	guardar_registro('Comprobada la concordancia del archivo de requisitos que existe con el nombre suministrado')
	if (nombre_requisitos+'.txt') in pcontenido_raiz:
		requisitos = nombre_requisitos+'.txt'
		guardar_registro('Comprobada la existencia de archivos con requisitos y su respectiva extension')
	else:
		print 'El nombre suministrado para requisitos no concuerda con el archivo existente.\nPor Favor Revisar'
		guardar_error('El nombre suministrado para requisitos no concuerda con el archivo existente')
		fatal_error()
else:
	print 'Archivo con requisitos no existe'
	guardar_error('Archivo con requisitos no existe')
	fatal_error()

directorio_modelos = directorio_raiz+'\modelos'
contenido_modelos = os.listdir(directorio_modelos)
if len(contenido_modelos) == 0:
	print 'El directorio modelo no contiene modelos a revisar'
	guardar_error('El directorio modelo no contiene archivos')
	fatal_error()
else:
	guardar_registro('Se verifico si el directorio modelos contenia archivos')
	
#Validacion 3
contenido_requisitos = leer_archivo(requisitos)
contenido_requisitos = "".join(contenido_requisitos)
contenido_requisitos = contenido_requisitos.split('\n')
if len(contenido_requisitos) == 0:
	print 'No ha ingresado requisitos minimos para la exposicion. \nPor Favor Ingrese Los Requisitos A Evaluar'
	guardar_error('No ha ingresado requisitos minimos para la exposicion')
	guardar_registro('Se realizo la pregunta si continuar sin recomendaciones para exposicion')
	while True:
		pregunta = raw_input('Desea continuar con la inspeccion sin tener obtener recomendaciones para exposicion(Si/No)')
		pregunta = pregunta.upper()
		if pregunta != 'SI' and pregunta != 'NO':
			guardar_registro('El usuario no ingreso una respuesta valida a la pregunta de continuar sin recomendacion')
			print 'Por favor ingrese una respuesta valida Si o No'
		elif pregunta == 'SI':
			guardar_registro('El usuario continuo con la ejecucion del programa')
			break
		elif pregunta == 'NO':
			guardar_registro('El usuario no continuo con la ejecucion del programa')
			fatal_error()
			break
else:
	guardar_registro('Se realizo la verificacion de requisitos para la exposicion')
	
#Validacion 4
contenido_elementos = leer_archivo(elementos)
contenido_elementos = "".join(contenido_elementos)
contenido_elementos = contenido_elementos.split('\n')
contenido_requisitos = "|".join(contenido_requisitos)
contenido_requisitos = list(contenido_requisitos)

ncontenido_requisitos = []
for i in range(len(contenido_requisitos)):
	try:
		contenido_requisitos[i] = int(contenido_requisitos[i])
	except ValueError:
		ncontenido_requisitos.append(contenido_requisitos[i])
		
contenido_requisitos = ncontenido_requisitos
contenido_requisitos = "".join(contenido_requisitos)
contenido_requisitos = contenido_requisitos.split('|')

for i in range(len(contenido_requisitos)):
	if contenido_requisitos[i] in contenido_elementos:
		guardar_registro('El requisito '+contenido_requisitos[i]+' se encuentra en elementos. Hay concordancia')
	else:
		guardar_error('El requisito '+contenido_requisitos[i]+' no se encuentra en elementos')
		while True:
			question = raw_input('Va a evaluar el requisito '+contenido_requisitos[i]+' para exposicion sin considerarlo en elementos(Si/No)?')
			question = question.upper()
			if question != 'SI' and question != 'NO':
				guardar_registro('El usuario no ingreso una respuesta valida a la pregunta de continuar con elementos que no concuerdan')
				print 'Por favor ingrese una respuesta valida Si o No'
			elif question == 'SI':
				guardar_registro('El usuario continuo evaluando el elemento que no concuerda')
				break
			elif question == 'NO':
				guardar_registro('El usuario no continuo evaluando el elemento que no concuerda')
				print 'Entonces por favor corriga los datos suministrados. Muchas Gracias'
				fatal_error()
				break

#Validacion 5
validar5 = os.listdir(directorio_modelos)
for i in validar5:
	val = leer_archivo(directorio_modelos+'\\'+i)
	if len(val) == 3:
		guardar_registro('Se realizo la validacion de la correcta estructura de los archivos en el directorio modelos')
	else:
		print 'El archivo '+i+' no tienen la estructura requerida para el correcto funcionamiento del programa\nPor Favor Revisar'
		guardar_error('Los archivos en modelos no tienen la estructura requerida')
		guardar_registro('Se le pregunto al usuario si desea continuar sin evaluar el archivo '+i)
		while True:
			pregunta = raw_input('Desea continuar evaluando los demas modelos?(Si/No)')
			pregunta = pregunta.upper()
			if pregunta != 'SI' and pregunta != 'NO':
				print 'Por favor ingrese una respuesta valida'
				guardar_registro('El usuario ingreso una respuesta valida a si continuar con la inspeccion sin el archivo '+i)
			elif pregunta == 'SI':
				guardar_registro('El usuario respondio SI a la pregunta si continuar con la inspeccion sin el archivo '+i)
				validar5.remove(i)
				contenido_modelos = validar5
				guardar_registro('Se realizara la inspeccion sin el modelo '+i)
				break
			elif pregunta == 'NO':
				guardar_registro('El usuario respondio no a la pregunta si continuar la inspeccion sin el modelo '+i)
				fatal_error()
				
#-------------------------------Logica de Programa---------------------------------------
crear_archivo('veloces.txt')
crear_archivo('candidatos.txt')
crear_archivo('informe.txt')

##Se llena el array que contiene la suma de cada elemento con la cantidad de elementos suministrados
suma_elementos = []
for i in range(len(contenido_elementos)):
	suma_elementos.append(0)

## Se suman cada uno de los elementos suministrados respectivamente
cantidad_requisitos = leer_archivo(requisitos)
cantidad_requisitos = "".join(cantidad_requisitos)
cantidad_requisitos = cantidad_requisitos.split('\n')
ncantidad_requisitos = []
for i in range(len(cantidad_requisitos)):
		evaluar = list(cantidad_requisitos[i])
		numero = []
		for j in range(len(evaluar)):
			try:
				a = int(evaluar[j])
				numero.append(evaluar[j])		
			except ValueError:
				pass
		numero = "".join(numero)
		try:
			numero = int(numero)
		except ValueError:
			print 'Revisar la correcta estructura, orden de los archivos o argumentos ingresados, error poco comun'
			guardar_error('Error poco comun')
			guardar_registro('Error de conversion')
			fatal_error()
		ncantidad_requisitos.append(numero)

guardar_registro('Cantidad de requisitos extraida')
		
while len(ncantidad_requisitos) < len(contenido_elementos):
	ncantidad_requisitos.append(0)
cantidad_requisitos = ncantidad_requisitos

##Se llenan arrays con precios y pasajeros de los modelos respectivamente y se seleccionan candidatos a exhibicion
precios = []
pasajeros = []
for i in range(len(contenido_modelos)):
	buscar = directorio_modelos+'\\'+contenido_modelos[i]
	contenido_archivo = leer_archivo(buscar)
	contenido_archivo = "".join(contenido_archivo)
	contenido_archivo = contenido_archivo.split('\n')
	elementos_modelo = contenido_archivo.pop()
	elementos_modelo = elementos_modelo.split(',')
	for k in range(len(contenido_archivo)):
		contenido_archivo[k] = int(contenido_archivo[k])
	precios.append(contenido_archivo[0])
	pasajeros.append(contenido_archivo[1])
	for k in range(len(elementos_modelo)):
		evaluar = list(elementos_modelo[k])
		numero = []
		for j in range(len(evaluar)):
			try:
				a = int(evaluar[j])
				numero.append(evaluar[j])		
			except ValueError:
				pass
		numero = "".join(numero)
		numero = int(numero)
		suma_elementos[k] = suma_elementos[k] + numero
		if numero >= cantidad_requisitos[k]:
			escribir_archivo('candidatos.txt',contenido_modelos[i])
		
guardar_registro('Sumas realizadas')
guardar_registro('Candidatos para exhibicion escogidos')

#-------------------------------Salidas---------------------------------------
candidatos = leer_archivo('candidatos.txt')
candidatos = "".join(candidatos)
candidatos = candidatos.split('\n')

##Se suman la cantidad total de elementos
total_elementos = 0
for i in range(len(suma_elementos)):
	total_elementos = suma_elementos[i] + total_elementos

guardar_registro('Total de elementos calculados')

##Se seleccionan los modelos aprovados para la exposicion
for i in range(len(contenido_modelos)):
	if contenido_modelos[i] in candidatos:
		if candidatos.count(contenido_modelos[i]) == len(cantidad_requisitos):
			paso = contenido_modelos[i].split('.')
			paso = paso[0]
			escribir_archivo('veloces.txt',paso)	

guardar_registro('Modelos aprovados para exhibicion escogidos')
os.remove(directorio_raiz+'\candidatos.txt')
guardar_registro('Archivo con candidatos elminado y modelos para exhibicion correctamente escogidos')			

##Se calculan los porcentajes(promedios) de cada elemento
porcentaje_elementos = []
for i in range(len(suma_elementos)):
	try:
		temp = float(suma_elementos[i]) / float(total_elementos) *100
		temp = round(temp,2)
		porcentaje_elementos.append(temp)
	except ZeroDivisionError:
		guardar_error('Error al dividir por cero')
guardar_registro('Porcentajes de elementos calculados y aproximados')

##Se escribe en el informe los porcentajes y cantidad de elementos suministrados y evaluados		
escribir_archivo('informe.txt','La cantidad total de elementos es: '+str(total_elementos)+'\n')
for i in range(len(contenido_elementos)):
	escribir_archivo('informe.txt','La cantidad de '+contenido_elementos[i]+' es: '+str(suma_elementos[i]))
	escribir_archivo('informe.txt','El porcentaje de '+contenido_elementos[i]+' es: '+str(porcentaje_elementos[i])+'%')

guardar_registro('Cantidad de elementos y su respectivo porcentaje escritos en informe.txt')
escribir_archivo('informe.txt','\n')
##Se quita la extension de los elementos para escribirlo en el informe
for i in range(len(contenido_modelos)):
	a = contenido_modelos[i].split('.')
	contenido_modelos[i]=a[0]

##Se escribe en el informe la informacion de cada modelo	
for i in range(len(contenido_elementos)):
	try:
		escribir_archivo('informe.txt','Un modelo analizado fue: '+contenido_modelos[i])
		escribir_archivo('informe.txt','La cantidad de pasajeros soportados por este modelo es: '+str(pasajeros[i]))
		escribir_archivo('informe.txt','El precio de este modelo es: '+str(precios[i]))
	except IndexError:
		guardar_error('Error de indizacion en informe.txt')
	escribir_archivo('informe.txt','\n')
guardar_registro('Modelos con sus respectivos precios y pasajeros soportados fueron escritos en informe.txt')

while True:
	pregunta = raw_input('Desea hacer sugerencias para mejoras del programa?(Si\No)')
	pregunta = pregunta.upper()
	guardar_registro('Se pregunto por mejoras en el programa')
	if pregunta == 'SI':
		sugerencia = raw_input('Por favor ingrese sus sugerencias: ')
		crear_archivo('sugerencias.txt')
		escribir_archivo('sugerencias.txt',sugerencia)
		print 'Muchas gracias por su opinion'
		guardar_registro('El usuario respondio que si e ingreso sus sugerencias que quedaron registradas en sugerencias.txt')
		break
	elif pregunta == 'NO':
		print 'Muchas gracias por su respuesta, esperamos que tenga los resultados deseados'
		guardar_registro('El usuario respondio que no y el programa continua')
		break
	elif pregunta != 'SI' and pregunta != 'NO':
		guardar_registro('El usuario no respondio correctamente a la pregunta sobre sugerencias')
		print 'Por favor ingrese una respuesta valida'

print 'El programa cumplio las funciones correctamente.'
print 'Revisar los archivos generados.'
print 'Muchas gracias por utilizar este programa'
print 'Dios lo Bendiga.'
print '\nPrograma realizado por Juan Jose Jaramillo Granada'

guardar_registro('FINALIZO EL PROGRAMA CORRECTAMENTE')
guardar_registro('---Aeroexhibicion v1.0---')
guardar_registro('Programa realizado por: Juan Jose Jaramillo Granada')