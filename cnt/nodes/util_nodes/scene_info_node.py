import bpy
from ..basic_nodes import ConstantNodeCnt
from ...base.constants import CntSocketTypes
class SceneInfoNodeCnt(ConstantNodeCnt):
    bl_label = "Scene Info"

    def init(self, context):
        self.outputs.new(CntSocketTypes.Integer, "Current Frame")
        self.outputs.new(CntSocketTypes.Integer, "FPS")
        self.socket_update_disabled = True
        self.update_scene_info()
        self.socket_update_disabled = False
        super().init(context)
        bpy.app.handlers.frame_change_pre.append(self.frame_change_handler)

    def frame_change_handler(self, context, scene):
        self.update_scene_info()

    def update_scene_info(self):
        self.outputs[0].input_value = bpy.context.scene.frame_current
        self.outputs[1].input_value = bpy.context.scene.render.fps

    def free(self):
        # Todo: remove handler even if the node was not deleted
        ref = None
        for element in bpy.app.handlers.frame_change_pre:
            if element.__self__ == self:
                ref = element
        if ref:
            bpy.app.handlers.frame_change_pre.remove(ref)
