import bge
from bge.logic import expandPath, LibLoad, LibFree, LibList
import random
from scripts import database
from ast import literal_eval

class Character(bge.types.KX_GameObject):
	
	def __init__(self):
		
		self.char_state = {"alive" : False,
		"id" : 0,
		"name" : "",
		"genre" : "",
		"type" : "",
		"life" : 0,
		"eqp_head" : "",
		"eqp_glass" : "",
		"eqp_shade" : "",
		"eqp_chest" : "",
		"eqp_legs" : "",
		"eqp_feet" : "",
		"eqp_hands" : "",
		"inventory" : []}
		
	pass

def init_char(cont):
	
	""" Initialize the basic character setup """
	
	own = cont.owner
	globalDict = bge.logic.globalDict
	
	# Sensors
	s_always = [sen for sen in cont.sensors if type(sen) == bge.types.SCA_AlwaysSensor][0].positive
	
	# Objects
	o_collision = own.parent
	o_input = o_collision.childrenRecursive.get("input")
	o_spatial = o_collision.childrenRecursive.get("spatial")
	o_character = o_collision.childrenRecursive.get("character")
	o_visual = o_collision.childrenRecursive.get("visual")
	o_combat = o_collision.childrenRecursive.get("combat")
	o_armature = o_collision.childrenRecursive.get("player_armature")
	
	############################
	######## INITIALIZE ########
	############################
	
	if s_always:
		
		if type(o_character) != Character:
			o_character = Character()
		
def player_props(cont):
	
	""" Set the input props based on player input or data received over network """
	
	own = cont.owner
	globalDict = bge.logic.globalDict
	
	# Sensors
	s_up = cont.sensors["up"].positive
	s_down = cont.sensors["down"].positive
	s_left = cont.sensors["left"].positive
	s_right = cont.sensors["right"].positive
	s_crouch = cont.sensors["crouch"].positive
	s_run = cont.sensors["run"].positive
	
	# Objects
	o_collision = own.parent
	o_input = o_collision.childrenRecursive.get("input")
	o_spatial = o_collision.childrenRecursive.get("spatial")
	o_character = o_collision.childrenRecursive.get("character")
	o_visual = o_collision.childrenRecursive.get("visual")
	o_combat = o_collision.childrenRecursive.get("combat")
	o_armature = o_collision.childrenRecursive.get("player_armature")
	
	# Properties
	
	
	############################
	######## INITIALIZE ########
	############################
	
	### Local player ###
	if o_character["info_name"] == globalDict["state"]["player_local"]["info_name"]:
		
		# Vertical directional keys
		if True:
			
			# Center
			if not s_up and not s_down or s_up and s_down:
				o_input["dir_v"] = 0
			
			# Up
			if s_up and not s_down:
				o_input["dir_v"] = 1
				
			# Down
			if not s_up and s_down:
				o_input["dir_v"] = -1
				
		# Horizontal directional keys
		if True:
			
			# Center
			if not s_left and not s_right or s_left and s_right:
				o_input["dir_h"] = 0
			
			# Right
			if not s_left and s_right:
				o_input["dir_h"] = 1
				
			# Left
			if s_left and not s_right:
				o_input["dir_h"] = -1
				
		# Action keys
		if True:
			
			# Crouch
			if not s_crouch:
				o_input["crouch"] = 0
				
			if s_crouch:
				o_input["crouch"] = 1
				
			# Run
			if not s_run:
				o_input["run"] = 0
				
			if s_run:
				o_input["run"] = 1
				
def spawn_player(cont):
	
	""" Initialize the basic player setup """
	
	own = cont.owner
	scene = own.scene
	globalDict = bge.logic.globalDict
	
	# Sensors
	s_message = cont.sensors[0]
	
	# Objects
	
	############################
	######## INITIALIZE ########
	############################
	
	if s_message.positive:
		
		### Initialize player if not in game ###
		if not globalDict["state"]["player_local"]["info_name"] in globalDict["state"]["players_ongame"]:
			
			### Add player to game ###
			o_player = scene.addObject("player", "Empty")
			
			# Objects
			o_collision = o_player.groupMembers.get("player_collision")
			o_input = o_collision.childrenRecursive.get("input")
			o_spatial = o_collision.childrenRecursive.get("spatial")
			o_character = o_collision.childrenRecursive.get("character")
			o_visual = o_collision.childrenRecursive.get("visual")
			o_combat = o_collision.childrenRecursive.get("combat")
			o_armature = o_collision.childrenRecursive.get("player_armature")
			
			### Initialize properties of character ###
			o_character["info_name"] = globalDict["state"]["player_local"]["info_name"]
			o_character["info_skin"] = globalDict["state"]["player_local"]["info_skin"]
			o_character["info_genre"] = globalDict["state"]["player_local"]["info_genre"]
			o_character["info_face"] = globalDict["state"]["player_local"]["info_face"]
			o_character["info_hair"] = globalDict["state"]["player_local"]["info_hair"]
			o_character["info_height"] = float(globalDict["state"]["player_local"]["info_height"])
			o_character["info_behavior"] = "player_local"
			o_character["info_alignment"] = globalDict["state"]["player_local"]["info_alignment"]
			o_character["info_position"] = globalDict["state"]["player_local"]["info_position"]
			o_character["equip_head"] = globalDict["state"]["player_local"]["equip_head"]
			o_character["equip_face"] = globalDict["state"]["player_local"]["equip_face"]
			o_character["equip_torso"] = globalDict["state"]["player_local"]["equip_torso"]
			o_character["equip_legs"] = globalDict["state"]["player_local"]["equip_legs"]
			o_character["equip_bag"] = globalDict["state"]["player_local"]["equip_bag"]
			o_character["equip_hands"] = globalDict["state"]["player_local"]["equip_hands"]
			o_character["equip_foot"] = globalDict["state"]["player_local"]["equip_foot"]
			
			# Set height
			o_armature.worldScale = [o_character["info_height"], o_character["info_height"], o_character["info_height"]]
			
			# Set start position
			o_collision.worldPosition = literal_eval(o_character["info_position"])
			
			# Set skin color
			for obj in o_collision.childrenRecursive:
				obj.color = database.human_skins[o_character["info_skin"]]
			
			### Add player to players online list ###
			globalDict["state"]["players_ongame"].append(globalDict["state"]["player_local"]["info_name"])
