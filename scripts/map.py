import bge
from bge import render

def player_icon(cont):
	
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
			
			# Get the world scene
			if scn.name == "world":
				
				# Always set the orientation of the player
				# camera to the background camera
				own.worldOrientation = scn.active_camera.groupObject.groupMembers.get("player_collision").worldOrientation
				own.worldPosition = scn.active_camera.groupObject.groupMembers.get("player_collision").worldPosition
				own.worldPosition[2] = 0.0
				
	pass
	
def camera_viewport(cont):
	
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
			
			# Get map scene
			if scn.name == "world_map":
				
				# If not using viewport already
				if scn.active_camera.useViewport == False:
					
					# Properties
					p_width = bge.render.getWindowWidth()
					p_height = bge.render.getWindowHeight()
					
					# Set viewport position
					scn.active_camera.setViewport(int(p_width // 1.5), 0, p_width, p_height // 2)
					
					# Activate viewport
					scn.active_camera.useViewport = True
					
	pass
	
