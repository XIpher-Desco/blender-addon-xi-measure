bl_info = {
    "name": "XI Measure",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Tools",
    "description": "Measure distance between two selected vertices",
    "category": "Object",
}

import bpy
from .measure_operator import MeasureDistanceOperator, MeasureProperties, CopyDistanceOperator, on_depsgraph_update

class MeasurePanel(bpy.types.Panel):
    bl_label = "XI Measure"
    bl_idname = "VIEW3D_PT_measure"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.measure_props
        if props.distance > 0:
            layout.label(text=f"Distance: {props.distance:.4f}")
            row = layout.row()
            row.label(text=f"X: {props.dx:.4f}")
            row.operator("object.copy_distance", text="Copy").target = 'X'
            row = layout.row()
            row.label(text=f"Y: {props.dy:.4f}")
            row.operator("object.copy_distance", text="Copy").target = 'Y'
            row = layout.row()
            row.label(text=f"Z: {props.dz:.4f}")
            row.operator("object.copy_distance", text="Copy").target = 'Z'
            layout.operator("object.copy_distance", text="Copy All").target = 'ALL'
        else:
            layout.label(text="Select two vertices to measure")

addon_keymaps = []

def register():
    bpy.utils.register_class(MeasureProperties)
    bpy.types.Scene.measure_props = bpy.props.PointerProperty(type=MeasureProperties)
    bpy.utils.register_class(MeasureDistanceOperator)
    bpy.utils.register_class(CopyDistanceOperator)
    bpy.utils.register_class(MeasurePanel)
    bpy.app.handlers.depsgraph_update_post.append(on_depsgraph_update)
    # Add keymap
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new(MeasureDistanceOperator.bl_idname, 'D', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.app.handlers.depsgraph_update_post.remove(on_depsgraph_update)
    bpy.utils.unregister_class(MeasurePanel)
    bpy.utils.unregister_class(CopyDistanceOperator)
    bpy.utils.unregister_class(MeasureDistanceOperator)
    del bpy.types.Scene.measure_props
    bpy.utils.unregister_class(MeasureProperties)
