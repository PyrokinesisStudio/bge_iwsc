import bge
import os
from bge.logic import expandPath, globalDict
from mathutils import Vector
from scripts.data import save_options, load_game

######## WIDGETS ########

def widget(cont):
	
	""" Processes the looks of widgets. Only works on group instances. Make sure you add to the instance the property named 'value' with the following string value:
	
	context, string, action, argument
	
	Where 'context' is the string context, 'string' is the string label, 'action' is the type of action to be performed and 'argument' is the value for the action. These arguments will vary according to the widget type.
	Example: an Options button from the main menu will have the value ['main_menu', 'options', 'context', 'options']. """
	
	own = cont.owner
	
	# Sensors
	s_always = [sen for sen in cont.sensors if type(sen) == bge.types.SCA_AlwaysSensor][0].positive
	s_mouse_over = [sen for sen in cont.sensors if type(sen) == bge.types.KX_MouseFocusSensor][0].positive
	
	# Objects
	o_description = own.scene.objects["gui_text_description"]
	o_context = own.scene.objects["gui_context"]
	o_group = own.groupObject
	
	# Properties
	p_value = own.groupObject["value"].split(", ")
	
	############################
	######## INITIALIZE ########
	############################
	
	### Run at start ###
	if s_always:
			
		# If not valid, print instructions
		if not len(p_value) > 0 and not len(p_value) <= 4:
			print("Invalid widget value in " + o_group.name + ". Use the format ['context', 'string', 'action', 'value']")
		
		### Change text of label at start ###
		if len(own.childrenRecursive) > 0:
			
			# Iterates over children
			for obj in own.childrenRecursive:
				
				# Check if obj in iteration is a label
				if type(obj) == bge.types.KX_FontObject:
					
					# Set text label to string from globalDict
					obj["Text"] = globalDict["strings"][p_value[0]]["lab_" + p_value[1]]
					
	### Mouse over ###
	if s_mouse_over:
		
		# Set text description to string from globalDict
		o_description["Text"] = globalDict["strings"][p_value[0]]["desc_" + p_value[1]]
		
		# Set to red if is a button
		if "button" in own:
			own.color = [1.0, 0.0, 0.0, 1.0]
			
		# Set to half transparent if is a checkbox
		elif "checkbox" in own:
			own.color[3] = 0.6
			
	# Change color back to normal
	if not s_mouse_over:
		
		# Reset color if is button
		if "button" in own:
			own.color = [1.0, 1.0, 1.0, 1.0]
			
		# Reset alpha if is checkbox
		elif "checkbox" in own:
			own.color[3] = 1.0
			
	pass

def button(cont):
	
	""" Processes the actions of buttons. Only works on group instances. Make sure you add to the instance the property named 'value' with the following string value:
	
	context, string, action, argument
	
	Where 'context' is the string context, 'string' is the string label, 'action' is the type of action to be performed and 'value' is the value of the action. Example: an Options button from the main menu will have the value ['main_menu', 'options', 'context', 'options']. """	
	
	own = cont.owner
	
	# Sensors
	s_mouse_over = [sen for sen in cont.sensors if type(sen) == bge.types.KX_MouseFocusSensor][0].positive
	s_lmb = [sen for sen in cont.sensors if type(sen) == bge.types.SCA_MouseSensor][0].positive
	
	# Objects
	o_description = own.scene.objects["gui_text_description"]
	o_context = own.scene.objects["gui_context"]
	o_group = own.groupObject
	
	# Properties
	p_value = own.groupObject["value"].split(", ")
	
	############################
	######## INITIALIZE ########
	############################
	
	### Mouse over ###
	if s_mouse_over and s_lmb:
		
		### Change GUI context ###
		if p_value[2] == "context":
			o_context["context"] = p_value[3]
			
		### Quit game ###
		if p_value[2] == "quit":
			bge.logic.endGame()
			
		### Save and apply options ###
		if p_value[2] == "apply":
			
			# Properties
			p_dtb_res = globalDict["database"]["configuration"]["resolutions"]
			p_resolution = p_dtb_res[globalDict["options"]["resolution"]]
			p_fullscreen = globalDict["options"]["fullscreen"]
			p_vsync = globalDict["options"]["vsync"] + 1
			
			# Apply resolution
			bge.render.setWindowSize(p_resolution[0], p_resolution[1])
			
			# Apply fullscreen
			bge.render.setFullScreen(p_fullscreen)
			
			# Apply Vsync
			bge.render.setVsync(p_vsync)
			
			# Restart scene
			own.scene.restart()
			
			# Save config to file
			save_options(cont)
			
			# Warning message
			print("Options applied.\nResolution", bge.render.getWindowWidth(), "X", bge.render.getWindowHeight(), "\nFullscreen:", bge.render.getFullScreen(), "\nVsync: ", bge.render.getVsync())
			
	pass

def static_label(cont):
	
	""" Processes the looks of static labels. Only works on group instances. Make sure you add to the instance the property named 'value' with the following string value:
	
	context, string
	
	Where 'context' is the string context and 'string' is the string label. Example: an Options label from the options menu will have the value ['main_menu', 'options']. """
	
	own = cont.owner
	
	# Sensors
	s_always = [sen for sen in cont.sensors if type(sen) == bge.types.SCA_AlwaysSensor][0].positive
	
	# Objects
	o_group = own.groupObject
	
	# Properties
	p_value = own.groupObject["value"].split(", ")
	
	############################
	######## INITIALIZE ########
	############################
	
	### Run at start ###
	if s_always:
			
		# If not valid, print instructions
		if not len(p_value) > 0 and not len(p_value) <= 2:
			print("Invalid widget value in " + o_group.name + ". Use the format ['context', 'string']")
		
		### Change text of label at start ###
		own["Text"] = globalDict["strings"][p_value[0]]["lab_" + p_value[1]]
		
	pass

def checkbox(cont):
	
	""" Processes the actions of checkboxes. Only works on group instances. Make sure you add to the instance the property named 'value' with the following string value:
	
	context, string, action
	
	Where 'context' is the string context, 'string' is the string label and 'action' is the type of action to be performed. Example: an Fullscreen checkbox from the video menu will have the value ['main_menu', 'fullscreen', 'fullscreen']. In the case of checkboxes, there's no need of a argument value for the action, since the checkbox always toggles an value. """	
	
	own = cont.owner
	
	# Sensors
	s_always = [sen for sen in cont.sensors if type(sen) == bge.types.SCA_AlwaysSensor][0].positive
	s_enabled_changed = [sen for sen in cont.sensors if type(sen) == bge.types.SCA_PropertySensor][0].positive
	
	# Objects
	o_group = own.groupObject
	
	# Properties
	p_value = own.groupObject["value"].split(", ")
	
	############################
	######## INITIALIZE ########
	############################
	
	### Get saved value at start ###
	if s_always and own["enabled"] == -1:
		
		# Get fullscreen value
		if p_value[2] == "fullscreen":
			own["enabled"] = int(globalDict["options"]["fullscreen"])
			
		# Get vsync value
		if p_value[2] == "vsync":
			own["enabled"] = int(globalDict["options"]["vsync"])
			
	### Process the main logic when button toggled ###
	if s_enabled_changed and own["enabled"] != -1:
		
		# Set color to enabled
		if own["enabled"] == 0:
			own.color = [1.0, 1.0, 1.0, 1.0]
			
		# Set color to disabled
		elif own["enabled"] == 1:
			own.color = [1.0, 0.0, 0.0, 1.0]
			
		### Set fullscreen to globalDict
		if p_value[2] == "fullscreen":
			globalDict["options"]["fullscreen"] = own["enabled"]
			
		### Set vsync to globalDict
		if p_value[2] == "vsync":
			globalDict["options"]["vsync"] = own["enabled"]
			
		# Warning message
		print("Value of " + p_value[2] + " set to " + str(own["enabled"]))
			
	pass

def button_range(cont):
	
	""" Processes the actions of ranged buttons. Only works on group instances. Make sure you add to the instance the property named 'value' with the following string value:
	
	context, string, action
	
	Where 'context' is the string context, 'string' is the string label and 'action' is the type of action to be performed. Example: an resolution range button from the options menu will have the value main_menu, resolution, resolution. """	
	
	own = cont.owner
	path = expandPath("//")
	ext = ".json"
	
	# Sensors
	s_always = [sen for sen in cont.sensors if type(sen) == bge.types.SCA_AlwaysSensor][0].positive
	s_mo_dec = cont.sensors["mo_dec"].positive
	s_mo_inc = cont.sensors["mo_inc"].positive
	s_lmb = [sen for sen in cont.sensors if type(sen) == bge.types.SCA_MouseSensor][0].positive
	s_cur_changed = [sen for sen in cont.sensors if type(sen) == bge.types.SCA_PropertySensor][0].positive
	
	# Objects
	o_group = own.groupObject
	
	# Properties
	p_value = own.groupObject["value"].split(", ")
	
	############################
	######## INITIALIZE ########
	############################
	
	### Runs at start ###
	if s_always:
		
		### If is resolution range button ###
		if p_value[2] == "resolution":
			
			# Properties
			p_dtb_res = globalDict["database"]["configuration"]["resolutions"]
			p_opt_res = globalDict["options"]["resolution"]
			
			# Set min, max, current and increment values
			own["min"] = 0
			own["max"] = len(p_dtb_res) - 1
			own["current"] = p_opt_res
			own["increment"] = 1.0
			
		### If is language range button ###
		if p_value[2] == "language":
			
			own["languages"] = []
			
			# Get list of language files
			for file in os.listdir(path + "lang/"):
				if file.endswith(".json"):
					own["languages"].append(file.replace(".json", ""))
			
			# Set min, max, current and increment values
			own["min"] = 0
			own["max"] = len(own["languages"]) - 1
			own["current"] = own["languages"].index(globalDict["options"]["language"])
			own["increment"] = 1.0
			
		### If is load game range button ###
		if p_value[2] == "load":
			
			own["savegames"] = []
			
			# Get list of savegame files
			for file in os.listdir(path + "saves/"):
				if file.endswith(ext):
					own["savegames"].append(file.replace(ext, ""))
			
			# Set min, max, current and increment values
			own["min"] = 0
			own["max"] = len(own["savegames"]) - 1
			own["current"] = 0
			own["increment"] = 1.0
			
		### If is volume range button ###
		if p_value[2] == "vol_music" or p_value[2] == "vol_sfx":
			
			# Set current to value saved in options
			own["current"] = float(globalDict["options"][p_value[2]])
	
	### Mouse click ###
	if s_lmb:
		
		# Decrease if current is higher than minimum
		if s_mo_dec and own["current"] > own["min"]:
			own["current"] -= own["increment"]
			
		# Increase if current is lower than maximum
		if s_mo_inc and own["current"] < own["max"]:
			own["current"] += own["increment"]
			
	### If current changed ###
	if s_cur_changed:
		
		### If is a resolution range button ###
		if p_value[2] == "resolution":
			
			p_dtb_res = globalDict["database"]["configuration"]["resolutions"]
			p_current = int(own["current"])
			
			# Set text of label
			own["Text"] = "      " + str(p_dtb_res[p_current]).strip("[]").replace(", ", " X ")
			
			# Set value of current to globalDict
			globalDict["options"]["resolution"] = p_current
			
		### If is a language range button ###
		if p_value[2] == "language":
			
			# Set text of label
			own["Text"] = "         " + own["languages"][int(own["current"])]
			
			# Set value of current to globalDict
			globalDict["options"]["language"] = own["languages"][int(own["current"])]
			
			# Warning message
			print("Language set to", own["languages"][int(own["current"])])
			
		### If is a load game range button ###
		if p_value[2] == "load":
			
			if len(own["savegames"]) > 0:
				
				# Set text of label
				own["Text"] = own["savegames"][int(own["current"])]
				
				# Set value of current to globalDict
				globalDict["state"]["player"]["name"] = own["savegames"][int(own["current"])]
				
				# Load game from file
				load_game(cont, globalDict["state"]["player"]["name"])
				
			if len(own["savegames"]) == 0:
				
				# Set text of label
				own["Text"] = globalDict["strings"]["main_menu"]["lab_no_saved"]

			
		### If is a volume range button ###
		if p_value[2] == "vol_music" or p_value[2] == "vol_sfx" or p_value[2] == "vol_ambience":
			
			# Set text of label
			own["Text"] = "               " + str((own["current"] * 100.0).__round__())
			
			# Set value of current to globalDict
			globalDict["options"][p_value[2]] = (own["current"] * 100.0).__round__() / 100
			
	pass

######## FUNCTIONS ########

def set_context(cont):
	
	""" Sets the camera position to show the current context. """
	
	own = cont.owner
	
	# Sensors
	s_context_changed = cont.sensors[0].positive
	
	# Objects
	o_description = own.scene.objects["gui_text_description"]
	o_camera = own.scene.objects["camera_menu"]
	
	############################
	######## INITIALIZE ########
	############################
	
	if s_context_changed:
	
		if own["context"] == "main":
			o_camera.worldPosition = [0.0, 0.0, 10.0]
			
		if own["context"] == "start":
			o_camera.worldPosition = [0.0, -10.0, 10.0]
			
		if own["context"] == "options":
			o_camera.worldPosition = [10.0, 0.0, 10.0]
			
		if own["context"] == "quit":
			o_camera.worldPosition = [-10.0, 0.0, 10.0]
			
		if own["context"] == "video":
			o_camera.worldPosition = [10.0, -10.0, 10.0]
			
		if own["context"] == "sound":
			o_camera.worldPosition = [10.0, -20.0, 10.0]
			
		if own["context"] == "controls":
			o_camera.worldPosition = [10.0, -30.0, 10.0]
			
		if own["context"] == "general":
			o_camera.worldPosition = [10.0, -40.0, 10.0]
			
		if own["context"] == "credits":
			o_camera.worldPosition = [20.0, 0.0, 10.0]
	pass

