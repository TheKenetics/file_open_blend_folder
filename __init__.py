bl_info = {
	"name": "Open Blend Folder in File Browser",
	"author": "Kenetics",
	"version": (0, 1),
	"blender": (2, 93, 0),
	"location": "View3D > Operator Search > Open Blend Folder",
	"description": "Opens blend folder in system file browser",
	"warning": "",
	"wiki_url": "",
	"category": "File"
}

import bpy, subprocess, os
from bpy.props import EnumProperty, IntProperty, FloatVectorProperty, BoolProperty, FloatProperty, StringProperty, PointerProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel, AddonPreferences


## Helper Functions
def get_addon_preferences():
	return bpy.context.preferences.addons[__package__].preferences


## Operators
class OBF_OT_open_blend_folder(Operator):
	"""Opens blend folder in system file browser"""
	bl_idname = "obf.open_blend_folder"
	bl_label = "Open Blend Folder"
	bl_options = {'REGISTER'}

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		prefs = get_addon_preferences()
		command = []
		if prefs.override_command:
			command = [prefs.override_command]
		else:
			command = ["explorer"]
		
		# add args
		command.append(os.path.dirname(os.path.realpath(bpy.data.filepath)))
		
		# run file browser command
		self.report({"INFO"}, f"Opening {command[1]} in file browser")
		print(f"Running: {' '.join(command)}")
		subprocess.run(command)
		
		return {'FINISHED'}


## Preferences
class OBF_addon_preferences(AddonPreferences):
	bl_idname = __package__
	
	# Properties
	override_command : StringProperty(name="Override File Browser", default="")
	#show_mini_manual : BoolProperty(name="Show Mini Manual", default=False)

	def draw(self, context):
		layout = self.layout
		
		layout.prop(self, "override_command")
		"""
		layout.prop(self, "show_mini_manual", toggle=True)
		if self.show_mini_manual:
			layout.label(text="Topic", icon="DOT")
			layout.label(text="Details",icon="THREE_DOTS")
		"""


## Register
classes = (
	OBF_OT_open_blend_folder,
	OBF_addon_preferences
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

if __name__ == "__main__":
	register()
