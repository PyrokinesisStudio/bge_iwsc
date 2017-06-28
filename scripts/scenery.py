import bge

def sign_set_streetname(cont):
	
	""" Set street sign name at start. """
	
	own = cont.owner
	
	############################
	######## INITIALIZE ########
	############################
	
	# Check if group instance
	if own.groupObject != None:
		
		# Check if property in groupObject
		if "street_name" in own.groupObject:
			
			# Set sign text
			own["Text"] = own.groupObject["street_name"]
			
def bg_camera(cont):
	
	own = cont.owner
	scenes = bge.logic.getSceneList()
	
	# Sensors
	s_always = [sen for sen in cont.sensors if type(sen) == bge.types.SCA_AlwaysSensor][0].positive
	
	############################
	######## INITIALIZE ########
	############################
	
	if s_always:
		
		# Iterates over scenes
		for scn in scenes:
			
			# Get the world_map scene
			if scn.name == "world":
				
				# Always set the orientation of the player
				# camera to the background camera
				own.worldOrientation = scn.active_camera.worldOrientation
