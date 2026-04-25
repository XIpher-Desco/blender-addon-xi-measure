import bpy
import bmesh
import math
from bpy.app.handlers import persistent

class MeasureProperties(bpy.types.PropertyGroup):
    distance: bpy.props.FloatProperty(name="Distance", default=0.0)
    dx: bpy.props.FloatProperty(name="X", default=0.0)
    dy: bpy.props.FloatProperty(name="Y", default=0.0)
    dz: bpy.props.FloatProperty(name="Z", default=0.0)

class MeasureDistanceOperator(bpy.types.Operator):
    bl_idname = "object.measure_distance"
    bl_label = "Measure Distance"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if obj and obj.mode == 'EDIT' and obj.type == 'MESH':
            bm = bmesh.from_edit_mesh(obj.data)
            selected_verts = [v for v in bm.verts if v.select]
            return len(selected_verts) == 2
        return False

    def execute(self, context):
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        selected_verts = [v for v in bm.verts if v.select]
        if len(selected_verts) != 2:
            self.report({'ERROR'}, "Select exactly two vertices")
            return {'CANCELLED'}

        v1, v2 = selected_verts
        # Global coordinates
        global_v1 = obj.matrix_world @ v1.co
        global_v2 = obj.matrix_world @ v2.co

        dx = global_v2.x - global_v1.x
        dy = global_v2.y - global_v1.y
        dz = global_v2.z - global_v1.z

        dist = math.sqrt(dx**2 + dy**2 + dz**2)

        message = f"Distance: {dist:.4f}\nX: {dx:.4f}\nY: {dy:.4f}\nZ: {dz:.4f}"

        self.report({'INFO'}, message)

        # Copy to clipboard
        bpy.context.window_manager.clipboard = message

        return {'FINISHED'}

class CopyDistanceOperator(bpy.types.Operator):
    bl_idname = "object.copy_distance"
    bl_label = "Copy Distance"
    target: bpy.props.StringProperty()

    def execute(self, context):
        scene = context.scene
        props = scene.measure_props
        if self.target == 'X':
            bpy.context.window_manager.clipboard = f"{props.dx:.4f}"
        elif self.target == 'Y':
            bpy.context.window_manager.clipboard = f"{props.dy:.4f}"
        elif self.target == 'Z':
            bpy.context.window_manager.clipboard = f"{props.dz:.4f}"
        elif self.target == 'ALL':
            message = f"Distance: {props.distance:.4f}\nX: {props.dx:.4f}\nY: {props.dy:.4f}\nZ: {props.dz:.4f}"
            bpy.context.window_manager.clipboard = message
        return {'FINISHED'}

@persistent
def on_depsgraph_update(scene, depsgraph):
    obj = bpy.context.active_object
    if obj and obj.mode == 'EDIT' and obj.type == 'MESH':
        bm = bmesh.from_edit_mesh(obj.data)
        selected_verts = [v for v in bm.verts if v.select]
        if len(selected_verts) == 2:
            v1, v2 = selected_verts
            global_v1 = obj.matrix_world @ v1.co
            global_v2 = obj.matrix_world @ v2.co
            dx = global_v2.x - global_v1.x
            dy = global_v2.y - global_v1.y
            dz = global_v2.z - global_v1.z
            dist = math.sqrt(dx**2 + dy**2 + dz**2)
            scene.measure_props.distance = dist
            scene.measure_props.dx = dx
            scene.measure_props.dy = dy
            scene.measure_props.dz = dz
        else:
            scene.measure_props.distance = 0
            scene.measure_props.dx = 0
            scene.measure_props.dy = 0
            scene.measure_props.dz = 0
