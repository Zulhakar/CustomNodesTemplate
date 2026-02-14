import bpy
from bpy.utils import register_class
from bpy.utils import unregister_class
from .group_nodes.group_node import GroupNodeCnt
from .basic_nodes import IntNodeCnt, FloatNodeCnt, StringNodeCnt, ObjectNodeCnt, BoolNodeCnt
from .util_nodes.math_node import MathNodeCnt
from .object_nodes.gn_modifier_node import ModifierNode, GeometryGroupInputCollectionItem
from .object_nodes.duplicate_object_node import DuplicateObjectNode
from .util_nodes.scene_info_node import SceneInfoNodeCnt
from .util_nodes.switch_node import SwitchNodeCnt
classes = [
    ObjectNodeCnt,
    FloatNodeCnt,
    IntNodeCnt,
    StringNodeCnt,
    BoolNodeCnt,
    GroupNodeCnt,
    MathNodeCnt,
    GeometryGroupInputCollectionItem,
    ModifierNode,
    DuplicateObjectNode,
    SceneInfoNodeCnt,
    SwitchNodeCnt
]

def register():
    for node_class in classes:
        bpy.utils.register_class(node_class)

def unregister():
    for node_class in classes:
        bpy.utils.unregister_class(node_class)