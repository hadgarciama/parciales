#pruebas
import os
import sys
def write_in_file(file_name, line):	
	try:
		file = open(file_name, 'a')
		file.write(line)
		file.close()
	except IOError:
		save_crash("crash writing " + line + " en the file " + file_name + "!")
		return False
	return True
def save_log(message):
	write_in_file(log_file, "\n" + message + "\n")
def save_crash(message):
	write_in_file(error_file, "\n" + message + "\n")
def dir_exist(dir):
	if (os.path.isdir(dir) and os.path.exists(dir)):
		print "directory validated"
		return True

	else:
		print "The directory doesn't exist or is in a wrong route "
		return False
def create_file(name_file):
	try:
		archivo = open(name_file, 'w')
		archivo.close()
		print "file created"
	except:
		print "the file doesn't created, please check permissions"
def array_files(dir):
	for root,dirs,files in os.walk(dir, topdown=False):
		return files
#def read_lines(file_name):
	lines = ()
	try:
		file = open(file_name, 'r')
		lines = file.readlines()
		archivo.close()
	except IOError:
		save_crash("Error leyendo archivo " + file_name + "!")
		
	return lines 
def load_file():
def stru_name_file(name_file):
#valite that the name of file haves one word and its structure be "server.#.txt"
	valid= False
	split_file=name_file.split(".")
	print split_file
	try:
		split_file[1]=int(split_file[1])
		if( len(split_file)==3):
			if(split_file[0]=="server" and split_file[1]>0 and split_file[2]=="txt"):
				valid= True
			else:
				save_log("The file "+name_file+" haves wrong structure")
	except ValueError:
		save_log("Be careful, '"+ split_file[1] + "' is not a number. the second argument must be a number")
	
	return valid

#---------------------------------------------------------------------------------
log_file="log_pruebas.txt"
print "prueba 1: validacion de directorio"
a=dir_exist(sys.argv[1])
print a
print ""
print "prueba 2: creacion del archivo pruebas.txt"
create_file("pruebas.txt")
print ""
print "prueba 3: arreglo con los nombres de los archivos del directorio"
files_in_directory=array_files(sys.argv[1]);
files_in_directory2=[[col for col in range(len(files_in_directory))] for row in range(2)]
print "prueba 4:"
files_in_directory2[0][0]=files_in_directory[0]
files_in_directory2[0][1]=files_in_directory[1]
files_in_directory2[0][2]=files_in_directory[2]
files_in_directory2[0][3]=files_in_directory[3]
files_in_directory2[0][4]=files_in_directory[4]
files_in_directory2[0][5]=files_in_directory[5]
files_in_directory2[0][6]=files_in_directory[6]
print ""
files_in_directory2[1][0]=stru_name_file(files_in_directory[0])
files_in_directory2[1][1]=stru_name_file(files_in_directory[1])
files_in_directory2[1][2]=stru_name_file(files_in_directory[2])
files_in_directory2[1][3]=stru_name_file(files_in_directory[3])
files_in_directory2[1][4]=stru_name_file(files_in_directory[4])
files_in_directory2[1][5]=stru_name_file(files_in_directory[5])
files_in_directory2[1][6]=stru_name_file(files_in_directory[6])
print files_in_directory2
