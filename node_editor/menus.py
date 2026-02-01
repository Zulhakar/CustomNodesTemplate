import bpy
from bl_ui import node_add_menu
from ..core.constants import OB_TREE_TYPE

class ConstantsMenu(bpy.types.Menu):
    bl_label = 'Constants'
    bl_idname = 'NODE_MT_Obm_Constants'

    def draw(self, context):
        layout = self.layout
        node_add_menu.add_node_type(layout, "ObmFloatNodeType")
        node_add_menu.add_node_type(layout, "ObmIntNodeType")
        node_add_menu.add_node_type(layout, "ObmStringNodeType")
        node_add_menu.add_node_type(layout, "ObmBooleanNodeType")
        layout.separator()
        node_add_menu.add_node_type(layout, "ObmVectorNodeType")
        node_add_menu.add_node_type(layout, "ObmCombineXyzNodeType")

class InputMenu(bpy.types.Menu):
    bl_label = 'Input'
    bl_idname = 'NODE_MT_Obm_Input'
    def draw(self, context):
        layout = self.layout
        layout.menu(ConstantsMenu.bl_idname)
        node_add_menu.add_node_type(layout, "NodeGroupInput")

class OutputMenu(bpy.types.Menu):
    bl_label = 'Output'
    bl_idname = 'NODE_MT_Obm_Output'
    def draw(self, context):
        layout = self.layout
        layout.menu(ConstantsMenu.bl_idname)
        node_add_menu.add_node_type(layout, "NodeGroupOutput")

class GroupMenu(bpy.types.Menu):
    bl_label = 'Group'
    bl_idname = 'NODE_MT_Obm_Group'
    def draw(self, context):
        layout = self.layout
        node_add_menu.add_node_type(layout, "NodeGroupInput")
        node_add_menu.add_node_type(layout, "NodeGroupOutput")
        node_add_menu.add_node_type(layout, "GroupNodeObm")

def draw_add_menu(self, context):
    layout = self.layout
    if context.space_data.tree_type != OB_TREE_TYPE:
        return

    layout.menu(InputMenu.bl_idname)
    layout.menu(GroupMenu.bl_idname)
    node_add_menu.add_node_type(layout, "MathNode")

def menu_draw(self, context):
    tree = context.space_data.node_tree
    if tree and tree.bl_idname == OB_TREE_TYPE:
        self.layout.operator("node.my_make_group",
                             text="Make Group",
                             icon='NODETREE')
