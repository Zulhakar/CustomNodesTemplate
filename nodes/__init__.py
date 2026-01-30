import bpy
from bpy.utils import register_class
from bpy.utils import unregister_class
from .group_nodes.group_node import GroupNodeObm
from .basic_nodes import IntNode, FloatNode, StringNode, ObjectNode, BooleanNode
from .constant_nodes.math_node import MathNode

classes = [
    ObjectNode,
    FloatNode,
    IntNode,
    StringNode,
    BooleanNode,
    GroupNodeObm,
    MathNode,

]

def register():
    for node_class in classes:
        bpy.utils.register_class(node_class)

def unregister():
    for node_class in classes:
        bpy.utils.unregister_class(node_class)