import bpy
from ..core.constants import IS_DEBUG, SINGLE_VALUES_SOCKET_SHAPE, VERSATILE_SOCKET_SHAPE
from ..core.constants import OB_TREE_TYPE, CntSocketTypes
from ..core.helper import change_socket_shape

class NodeCnt:
    socket_update_disabled: bpy.props.BoolProperty(default=False)
    def log(self, func_name):
        if IS_DEBUG:
            log_string = f"{self.bl_idname}-> {self.name}: {func_name} was called"
            print(log_string)

    def init(self, context):
        self.log("init")
        change_socket_shape(self)

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == OB_TREE_TYPE or ntree.bl_idname == "GeometryNodeTree"

    def copy(self, node):
        self.log("copy")

    def free(self):
        self.log("free")

    def draw_label(self):
        return self.bl_label

    def insert_link(self, link):
        self.log("insert_link")
        if link.to_socket.bl_idname == link.from_socket.bl_idname:
            link.is_valid = True
        elif link.to_socket.bl_idname == CntSocketTypes.Float and link.from_socket.bl_idname == CntSocketTypes.Integer:
            link.is_valid = True
        elif link.to_socket.bl_idname == CntSocketTypes.Integer and link.from_socket.bl_idname == CntSocketTypes.Float:
            link.is_valid = True
        else:
            if IS_DEBUG:
                print("Wrong Socket ", str(link.from_socket.bl_idname))
            link.is_valid = False
        if link.is_valid and not self.mute:
            for input in self.inputs:
                if link.to_socket == input:
                    if link.to_socket.is_multi_input:
                        pass
                    else:
                        if link.to_socket.bl_idname != CntSocketTypes.FloatVectorField:
                            input.input_value = link.from_socket.input_value

        else:
            pass

    def update(self):
        self.log("update")
        #this line inside copy crash blender but not inside copy which also called on copy function
        change_socket_shape(self)

    def socket_update(self, socket):
        self.log("socket_update")
        if IS_DEBUG:
            if self.socket_update_disabled:
                print("socket_update_disabled")

    def socket_value_update(self, context):
        self.log("socket_value_update")


class ConstantNodeCnt(NodeCnt, bpy.types.Node):
    def socket_update(self, socket):
        super().socket_update(socket)
        if not self.mute:
            if not self.socket_update_disabled:
                if len(self.outputs) > 0:
                    for link in self.outputs[0].links:
                        if link.to_socket.bl_idname == CntSocketTypes.Integer and link.from_socket.bl_idname == CntSocketTypes.Float:
                            link.to_socket.input_value = int(self.outputs[0].input_value)
                        else:
                            link.to_socket.input_value = self.outputs[0].input_value

    def init(self, context):
        super().init(context)
        self.outputs[0].is_constant = True

class ObjectNodeCnt(ConstantNodeCnt):
    '''Object Node'''
    bl_label = "Object"
    def init(self, context):
        self.outputs.new(CntSocketTypes.Object, "Object")
        super().init(context)


class FloatNodeCnt(ConstantNodeCnt):
    '''Float Value Node'''
    bl_label = "Value"
    def init(self, context):
        self.outputs.new(CntSocketTypes.Float, "Float")
        super().init(context)


class IntNodeCnt(ConstantNodeCnt):
    '''Integer Node'''
    bl_label = "Integer"
    def init(self, context):
        self.outputs.new(CntSocketTypes.Integer, "Integer")
        super().init(context)


class StringNodeCnt(ConstantNodeCnt):
    '''String Node'''
    bl_label = "String"
    def init(self, context):
        self.outputs.new(CntSocketTypes.String, "String")
        super().init(context)


class BoolNodeCnt(ConstantNodeCnt):
    '''Boolean Value Node'''
    bl_label = "Boolean"
    def init(self, context):
        self.outputs.new(CntSocketTypes.Bool, "Boolean")
        super().init(context)
