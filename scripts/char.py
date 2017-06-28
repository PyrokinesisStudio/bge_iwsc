import bge
from bge.logic import expandPath, globalDict, LibLoad, LibFree, LibList
import random
import string
from ast import literal_eval

def init_char(cont):
	
	""" Initialize the basic character setup """
	
	own = cont.owner
	
	# Sensors
	s_always = [sen for sen in cont.sensors if type(sen) == bge.types.SCA_AlwaysSensor][0].positive
	
	# Objects
	o_collision = own.parent
	o_input = o_collision.childrenRecursive.get("input")
	o_spatial = o_collision.childrenRecursive.get("spatial")
	o_character = o_collision.childrenRecursive.get("character")
	o_visual = o_collision.childrenRecursive.get("visual")
	o_combat = o_collision.childrenRecursive.get("combat")
	o_armature = o_collision.childrenRecursive.get("char_armature")
	
	############################
	######## INITIALIZE ########
	############################
	
	if s_always:
		print(o_input.attrDict)
		if o_character["id"] == "":
			
			p_letters = string.ascii_letters + string.digits
			
			for i in range(10):
				o_character["id"] += random.choice(p_letters)
		
	pass