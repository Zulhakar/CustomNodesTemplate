import bpy
import bl_ui
from .node_editor import register as register_node_editor
from .node_editor import unregister as unregister_node_editor
from .sockets.basic_sockets import register as register_basic_sockets
from .sockets.basic_sockets import unregister as unregister_basic_sockets
from .nodes import register as register_nodes
from .nodes import unregister as unregister_nodes
def register():
    register_basic_sockets()
    register_nodes()
    register_node_editor()

def unregister():
    unregister_basic_sockets()
    unregister_nodes()
    unregister_node_editor()

if __name__ == "__main__":
    register()
