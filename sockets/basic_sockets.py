import bpy
from bpy.types import NodeSocket, NodeTreeInterfaceSocket
from bpy.utils import register_class, unregister_class

from ..core.constants import (COLOR_OBJECT_SOCKET, COLOR_BLACK, COLOR_STRING_SOCKET, COLOR_INT_SOCKET, COLOR_FLOAT_SOCKET,
                            COLOR_FLOAT_VECTOR_SOCKET,
                            COLOR_EMPTY_SOCKET, COLOR_BOOL_SOCKET, IS_DEBUG)
from ..core.helper import get_socket_index


class ObmBasicSocket(NodeSocket):
    is_constant: bpy.props.BoolProperty()
    selected_node_group_name: bpy.props.StringProperty()
    node_group_name: bpy.props.StringProperty()
    disable_socket_update : bpy.props.BoolProperty(default=False)

    def draw(self, context, layout, node, text):
        if self.is_constant:
            layout.alignment = 'EXPAND'
            layout.prop(self, "input_value", text="")
        else:
            if self.is_output or self.is_linked:
                layout.label(text=text)
            else:
                layout.prop(self, "input_value", text=text)

    def update_prop(self):
        if IS_DEBUG:
            log_string = f"{self.node.bl_idname}-> Socket: {self.bl_idname} update_prop: [name: {self.name},  value: {self.input_value}]"
            print(log_string)
        if hasattr(self.node, "socket_update"):
            self.node.socket_update(self)

        # ----------------------------------------------------------
        # inject update for build in nodes (Group Input/Output Node)
        # maybee pointer for socket group_output inputs with group_node output

        if self.node.bl_idname == "NodeGroupOutput":
            if self.selected_node_group_name != "":
                if not self.disable_socket_update:
                    node = self.node
                    tree = bpy.data.node_groups[self.selected_node_group_name]
                    tree2 = bpy.data.node_groups[self.node_group_name]
                    for node_ in tree.nodes:
                        if node_.bl_idname == "GroupNodeObm":
                            if node_.target_tree == tree2:
                                sock_index = get_socket_index(node.inputs, self)
                                if node_.outputs[sock_index].bl_idname != "FloatVectorFieldSocketType":
                                    #node_.was_fired = True
                                    if node_.was_fired:
                                        node_.outputs[sock_index].input_value = self.input_value
                                else:
                                    for link in node_.outputs[sock_index].links:
                                        link.to_socket.input_value.clear()
                                        for item in node.inputs[sock_index].input_value:
                                            new_item = link.to_socket.input_value.add()
                                            new_item.value = item.value
                                        for link2 in node_.outputs[sock_index].links:
                                            link2.to_node.socket_update(link2.to_socket)



    @classmethod
    def draw_color_simple(cls):
        return cls.sock_col


class ObmNodeTreeInterfaceSocket(bpy.types.NodeTreeInterfaceSocket):
    obm_sockets = [
        ("FloatVectorFieldSocketType", "Float Vector Field", "Float Vector Field"),
        ("FloatVectorSocketType", "Float Vector", "Float Vector"),
        ("FloatSocketType", "Float", "Float"),
        ("StringSocketType", "String", "String"),
        ("IntSocketType", "Integer", "Integer"),
        ("BoolSocketType", "Boolean", "Boolean"),
        ("ObjectSocketType", "Object", "Object")
    ]
    obm_socket_type: bpy.props.EnumProperty(  # type: ignore
        name="Obm Socket Type"
        , items=obm_sockets
        , default='FloatSocketType',
        update=lambda self, context: self.obm_socket_type_update()
    )
    default_value: bpy.props.StringProperty()
    selected_node_group_name: bpy.props.StringProperty()
    node_group_name: bpy.props.StringProperty()

    def obm_socket_type_update(self):
        print(self.socket_type)
        self.socket_type = self.obm_socket_type
        print(self.socket_type)

    def draw(self, context, layout):
        layout.prop(self, "default_value")

    def init_socket(self, node, socket, data_path):
        socket.input_value = self.default_value

    def from_socket(self, node, socket):
        print("from socket")
    def draw_color(self, context, node):
        return COLOR_BLACK


class ObjectSocket(ObmBasicSocket):
    """Sound Socket to play"""
    bl_idname = 'ObjectSocketType'
    bl_label = "Object"
    sock_col = COLOR_OBJECT_SOCKET
    input_value: bpy.props.PointerProperty(update=lambda self, context: self.update_prop(), name="Object",
                                           type=bpy.types.Object)  # poll=poll_domain)


class NodeTreeInterfaceSocketObject(ObmNodeTreeInterfaceSocket):
    bl_socket_idname = 'ObjectSocketType'

    def draw_color(self, context, node):
        # cls.display_shape = "SQUARE"
        return COLOR_OBJECT_SOCKET


class ObmFloatSocket(ObmBasicSocket):
    """Sound Socket to play"""
    bl_idname = 'FloatSocketType'
    bl_label = "Float"
    sock_col = COLOR_FLOAT_SOCKET

    input_value: bpy.props.FloatProperty(update=lambda self, context: self.update_prop(), name="Float")


class NodeTreeInterfaceSocketObmFloat(ObmNodeTreeInterfaceSocket):
    bl_socket_idname = 'FloatSocketType'

    def draw_color(self, context, node):
        return COLOR_FLOAT_SOCKET


class ObmFloatVectorSocket(ObmBasicSocket):
    """Float Vector"""
    bl_idname = 'FloatVectorSocketType'
    bl_label = "Float Vector"
    sock_col = COLOR_FLOAT_VECTOR_SOCKET

    input_value: bpy.props.FloatVectorProperty(update=lambda self, context: self.update_prop(), name="FloatVector")

    def draw(self, context, layout, node, text):
        if self.is_constant:
            layout.alignment = 'EXPAND'
            layout.prop(self, "input_value", text="")
        else:
            if self.is_output or self.is_linked:
                layout.label(text=text)
            else:
                layout.prop(self, "input_value", text=text)

class NodeTreeInterfaceSocketObmFloatVector(ObmNodeTreeInterfaceSocket):
    bl_socket_idname = 'FloatVectorSocketType'

    def draw_color(self, context, node):
        return COLOR_FLOAT_VECTOR_SOCKET


class FloatVectorFieldItem(bpy.types.PropertyGroup):
    # value: bpy.props.FloatVectorProperty(update=lambda self, context: self.update_prop())
    value: bpy.props.FloatVectorProperty()


register_class(FloatVectorFieldItem)


class ObmFloatVectorFieldSocket(ObmBasicSocket):
    """Float Vector"""
    bl_idname = 'FloatVectorFieldSocketType'
    bl_label = "Float Vector Field"
    sock_col = COLOR_FLOAT_VECTOR_SOCKET
    input_value: bpy.props.CollectionProperty(type=FloatVectorFieldItem)
    # input_value: bpy.props.CollectionProperty(update=lambda self, context: self.update_prop(), name="FloatVector")
    # input_value: ()
    # input_value: bpy.props.CollectionProperty(type=bpy.props.FloatVectorProperty)


class NodeTreeInterfaceSocketObmFloatVectorField(ObmNodeTreeInterfaceSocket):
    bl_socket_idname = 'FloatVectorFieldSocketType'
    def draw_color(self, context, node):
        return COLOR_FLOAT_VECTOR_SOCKET


class ObmIntSocket(ObmBasicSocket):
    """Sound Socket to play"""
    bl_idname = 'IntSocketType'
    bl_label = "Integer"
    sock_col = COLOR_INT_SOCKET
    input_value: bpy.props.IntProperty(update=lambda self, context: self.update_prop(), name="Integer")


class NodeTreeInterfaceSocketObmInt(ObmNodeTreeInterfaceSocket):
    bl_socket_idname = 'IntSocketType'
    def draw_color(self, context, node):
        return COLOR_INT_SOCKET


class ObmStringSocket(ObmBasicSocket):
    """Sound Socket to play"""
    bl_idname = 'StringSocketType'
    bl_label = "String"
    sock_col = COLOR_STRING_SOCKET
    input_value: bpy.props.StringProperty(update=lambda self, context: self.update_prop(), name="String")


class NodeTreeInterfaceSocketObmString(ObmNodeTreeInterfaceSocket):
    bl_socket_idname = 'StringSocketType'
    def draw_color(self, context, node):
        return COLOR_STRING_SOCKET


class ObmBoolSocket(ObmBasicSocket):
    """Boolean Socket Type"""
    bl_idname = 'BoolSocketType'
    bl_label = 'Bool'
    sock_col = COLOR_BOOL_SOCKET
    input_value: bpy.props.BoolProperty(update=lambda self, context: self.update_prop(), name="Bool")
    def draw(self, context, layout, node, text):
        layout.alignment = 'LEFT'
        layout.prop(self, "input_value", text=text)


class NodeTreeInterfaceSocketObmBool(ObmNodeTreeInterfaceSocket):
    bl_socket_idname = 'BoolSocketType'
    def draw_color(self, context, node):
        return COLOR_BOOL_SOCKET


class NodeTreeInterfaceSocketObmEmpty(ObmNodeTreeInterfaceSocket):
    bl_socket_idname = 'EmptySocketType'

class ObmEmptySocket(NodeSocket):
    """Connect a link to create a new socket"""
    bl_idname = 'EmptySocketType'
    bl_label = "Empty"
    sock_col = COLOR_EMPTY_SOCKET

    def draw(self, context, layout, node, text):
        pass


classes = (
           ObjectSocket, NodeTreeInterfaceSocketObject,
           ObmFloatSocket, NodeTreeInterfaceSocketObmFloat,
           ObmIntSocket, NodeTreeInterfaceSocketObmInt,

           ObmStringSocket, NodeTreeInterfaceSocketObmString,
           # NodeTreeInterfaceSocketObmEmpty, ObmEmptySocket,
           ObmBoolSocket, NodeTreeInterfaceSocketObmBool,


           ObmFloatVectorSocket, NodeTreeInterfaceSocketObmFloatVector,
           ObmFloatVectorFieldSocket, NodeTreeInterfaceSocketObmFloatVectorField,

           )


def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in reversed(classes):
        try:
            unregister_class(cls)
        except Exception as e:
            print(e)
            print(cls)