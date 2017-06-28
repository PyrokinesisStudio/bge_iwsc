import bge
from bge.logic import expandPath, globalDict
import configparser, json

def save_options(cont):
	
	""" Save options from the globalDict to file. """
	
	path = expandPath("//")
	
	############################
	######## INITIALIZE ########
	############################
	
	for sen in cont.sensors:
		
		if type(sen) == bge.types.SCA_MouseSensor and "options" in globalDict.keys():
			
			try:
				
				# Open file from disk
				with open(path + "options.json", "w") as open_file:
					
					# Write file to disk
					json.dump(globalDict["options"], open_file)
					
					# Warning message
					print("Options saved to options.json")
					
			except:
				
				# Warning message
				print("Can't save options to options.json")
				
	pass

def load_strings(cont):
	
	""" Initialize data saved in option file. """
	
	own = cont.owner
	path = expandPath("//lang/")
	ext = ".json"
	
	# Sensors
	s_always = [sen for sen in cont.sensors if type(sen) == bge.types.SCA_AlwaysSensor][0].positive
	
	# Properties
	p_lang = "English"
	
	############################
	######## INITIALIZE ########
	############################
	
	if s_always:
		
		# If options was loaded
		if "options" in globalDict.keys():
			
			# Get language from options
			p_lang = globalDict["options"]["language"]
			
			try:
				with open(path + p_lang + ext, "r") as open_file:
					
					# Initialize strings in globalDict
					globalDict["strings"] = json.load(open_file)
					
			except:
				print("Error loading language file. Try to reinstall the game.")
			
		else:
			print("Can't find any language config.")
			
	pass

def load_options(cont):
	
	""" Initialize data saved in option file. """
	
	own = cont.owner
	path = expandPath("//")
	
	# Sensors
	s_always = [sen for sen in cont.sensors if type(sen) == bge.types.SCA_AlwaysSensor][0].positive
	
	############################
	######## INITIALIZE ########
	############################
	
	if s_always:
		
		### Initialize options in globalDict ###
		if not "options" in globalDict.keys():
			
			# Fallback values
			globalDict["options"] = {}
			
			options = {'key_up': 119, 'key_use': 101, 'key_left': 97, 'key_menu': 32, 'key_run': 106, 'key_crouch': 105, 'key_right': 10, 'mouse_sensitivity': 1.0, 'mouse_invert' : 0, 'key_down': 115, 'fullscreen': 0, 'vsync': 1, 'resolution': 3, 'vol_music': 1.0, 'vol_sfx': 1.0, 'language': 'English'}
			
			### Set falback to globalDict ###
			globalDict["options"] = options
			
			### Load options from file ###
			try:
				with open(path + "options.json", "r") as open_file:
					
					globalDict["options"] = json.load(open_file)
					
					print("Game options loaded from options.json")
					
			### Write default options file ###
			except:
				with open(path + "options.json", "w") as open_file:
					
					json.dump(options, open_file)
					
					print("Error loading options.json, create file and use default values")
					
	pass

def load_database(cont):
	
	""" Initialize data saved in database file. """
	
	own = cont.owner
	path = expandPath("//")
	
	# Sensors
	s_always = [sen for sen in cont.sensors if type(sen) == bge.types.SCA_AlwaysSensor][0].positive
	
	############################
	######## INITIALIZE ########
	############################
	
	if s_always:
			
		if not "state" in globalDict.keys():
			globalDict["state"] = {"player" : {},
			"actors" : {},
			"world" : {}}
		
		try:
			with open(path + "database.json", "r") as open_file:
				
				# Initialize database in globalDict
				globalDict["database"] = json.load(open_file)
				
				# Warning message
				print("Database loaded from database.json")
				
		except:
			print("Error loading database.json. Try to reinstall the game")
			
	pass

def load_game(cont, savegame):
	
	""" Load game from savegame file. """
	
	path = expandPath("//saves/")
	ext = ".json"
	
	############################
	######## INITIALIZE ########
	############################
	
	for sen in cont.sensors:
		
		if sen.positive and type(sen) == bge.types.SCA_PropertySensor:
	
			try:
				
				# Load file with provided name
				with open(path + savegame + ext, "r") as open_file:
					
					# Read file
					loaded_data = json.load(open_file)
					
					# Check if file content is valid
					if "player" in loaded_data and "actors" in loaded_data and "world" in loaded_data: 
						
						# Set valus to globalDict
						globalDict["state"]["player"] = loaded_data
						
						# Warning message
						print("Loaded game from", savegame + ext)
					
			except:
				
				# Warning message
				print("Can't load from", savegame + ext)
				
	pass

