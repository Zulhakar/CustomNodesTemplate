import bpy
import bl_ui
from bl_ui import node_add_menu
from bpy.utils import register_class
from bpy.utils import unregister_class
from .CustomNodesTemplate.node_editor import register as register_node_editor
from .CustomNodesTemplate.node_editor import unregister as unregister_node_editor
from .CustomNodesTemplate.sockets.basic_sockets import register as register_basic_sockets
from .CustomNodesTemplate.sockets.basic_sockets import unregister as unregister_basic_sockets
from .CustomNodesTemplate.nodes import register as register_nodes
from .CustomNodesTemplate.nodes import unregister as unregister_nodes
from .CustomNodesTemplate.core.constants import OB_TREE_TYPE
from .CustomNodesTemplate.node_editor.menus import InputMenu, GroupMenu


def draw_add_menu(self, context):
    layout = self.layout
    if context.space_data.tree_type != OB_TREE_TYPE:
        return
    layout.menu(InputMenu.bl_idname)
    layout.menu(GroupMenu.bl_idname)
    node_add_menu.add_node_type(layout, "MathNodeCnt")

def register():
    register_basic_sockets()
    register_nodes()
    register_node_editor()
    bpy.types.NODE_MT_add.append(draw_add_menu)

def unregister():
    bpy.types.NODE_MT_add.remove(draw_add_menu)
    unregister_basic_sockets()
    unregister_nodes()
    unregister_node_editor()

if __name__ == "__main__":
    register()
