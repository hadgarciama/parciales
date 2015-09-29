'''
SmartRenovation version 2.0
This program help us to define if in the company there are obsolete servers. This is to know which servers should be renewed or repowered. The results of this program are a text file with the list of obsolete servers and other text file when revision process was successful.

Developed by Harry Danilo Garcia Martin, hadgarciama@unal.edu.co
September 26, 2015.
The servers directory is called 'drone_travel'.
'''
#-------------------------import library-----------------------------#
import sys
#libreria para manejo del sistema de archivos del sistema operativo.
import os
#-------------------------Generic functions-------------------------#
def create_file(name_file):
	try:
		archivo = open(name_file, 'w')
		archivo.close()
		print "file created"
	except:
		print "the file doesn't created, please check permissions"
def write_in_file(file_name, line):	
	try:
		file = open(file_name, 'a')
		file.write(line)
		file.close()
	except IOError:
		save_crash("crash writing " + line + " en the file " + file_name + "!")
		return False
	return True
def save_crash(message):
	write_in_file(error_file, "\n" + message + "\n")
def save_log(message):
	write_in_file(log_file, "\n" + message + "\n")
def end_program(end_message):
	save_crash(end_message)
	save_log("The program crashes. To view errors go to crashes.txt")
	sys.exit()

#-------------------------Declaring Functions-------------------------#
#	F1----------------------------------------------
def dir_validation(dir):
	if (os.path.isdir(dir) and os.path.exists(dir)):
		write_in_file(log_file, "directory validated")
		print "directory validated"
		return True

	else:
		write_in_file(log_file, "The program crashes. To view errors go to crashes.txt")
		write_in_file(error_file, "The directory doesn't exist or is in a wrong route")
		print "The directory doesn't exist or is in a wrong route"
		return False
		end_program("the program was ended by an error ocurred")
#	F2--------------------------------------------------
def dir_files(dir):
	for root,dirs,files in os.walk(dir, topdown=False):
		return files
#	F3--------------------------------------------------
def file_validate(file_name):
	valid = True
	
	# existence validation .txt file
	if(os.path.isfile(file_name) == False):
		print " The file" + file_name + " doesn't exist."
		save_crash(" The file" + file_name + " doesn't exist.")
	# Non space validation
	words = len(file_name.split(" "))
	if(words > 1):
		valid_file = False
		save_crash("Name of file haves spaces")
	
	# Extension validation
	if(not file_name.endswith(extension)):
		valid_file = False
		guardar_error("invalid extension  " + extension)
	
	return valid_file
#	F4---------------------------------------------------
def stru_name_file(name_file):
#valite that the name of file haves one word and its structure be "server.#.txt"
	valid= False
	split_file=name_file.split(".")
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
#	F5-------------------------------------------------------------
def array_files(dir):
	for root,dirs,files in os.walk(dir, topdown=False):
		return files
#F6----------------------------------------------------------------
def read_file(name_file):
	lines = ()
	try:
		file = open(name_file, 'r')
		lines = file.readlines()
		file.close()
	except IOError:
		save_crash("Error reading the file '" + name_file + "' !")
		
	return lines 
#-------------------------Declaring constants-------------------------#
#argument of cmd with the directory of servers
directory=sys.argv[1]
#minimun lenght of files of servers
min_files=2
extension=".txt"
error_file="Crashes" + extension
log_file="Log"+extension
min_req_file_name="minimum" + extension
cant_of_trues=0

#-------------------------delete previous files(truncate files)-------------------------#
'''
void because o don't know how do it.
'''
#-------------------------inicialize the program logic-------------------------#
#la primera funcion debe truncar todos los archivos.
#validation of directory
dir_validation(sys.argv[1])
#array with all files in directory
files_in_directory=array_files(sys.argv[1])
#number of files in servers directory
cant_files=len(files_in_directory)
print cant_files
#validate that exist 2 or more files
if cant_files<min_files:
	end_program("the minimum lenght of server files is 2")
#validation of comparation file with minimum requeriments
if os.path.isfile(min_req_file_name) == False:
	end_program("The file '" + min_req_file_name + "' doesn't exist")
save_log("The file '" + min_req_file_name + "' is load an contain the minimum requeriments")
#array with all files in directory and a True if the name of file is valid
files_in_directory2=[[col for col in range(len(files_in_directory))] for row in range(2)]
for x in range(0,len(files_in_directory)):
	files_in_directory2[0][x]=files_in_directory[x]
for x in range(0,len(files_in_directory)):
	files_in_directory2[1][x]=stru_name_file(files_in_directory[x])
	if files_in_directory2[1][x]:
		cant_of_trues=cant_of_trues+1
for x in range(0,cant_files):
	#if the name of server is correct we will compare the requeriments
	if files_in_directory2[1][x]:
			A=tuple(read_file(directory + "/" + files_in_directory[x]))
			lines_minimum = tuple(read_file(min_req_file_name))
			actual_req=A[1].split("|")
			#print actual_req
			min_req=lines_minimum[1].split("|")
			#print min_req
'''
Load all info in one big matrix to compare values
['MINIMUM'           'model1'       '....'       'modelo n' ]
['MINIMUM1'         'valor 11'      '....'       'valor 1n' ]
[      .                .           '....'            .     ]
[      .                .           '....'            .     ]
[      .                .           '....'            .     ]
['MINIMUMn'         'valor n1'      '....'       'valor nn' ]
'''
total_matrix = [[0 for col in range(cant_of_trues+1)] for rows in range(11)]


#NOTA: NO alcance a terminar el programa por fijarme en validaciones que no debí. Asumo la nota con total responsabilidad.