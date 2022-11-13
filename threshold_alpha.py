# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bpy
import numpy as np


bl_info = {
    "name": "Threshold Alpha",
    "author": "todashuta",
    "version": (1, 0, 0),
    "blender": (2, 93, 0),  # Python 3.9
    "location": "Image Editor > Sidebar > Tool > Threshold Alpha",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Image"
}


class THRESHOLD_ALPHA_OT_main(bpy.types.Operator):
    bl_idname = "image.threshold_alpha"
    bl_label = "Threshold Alpha"
    bl_description = "Threshold Alpha"

    shift_key_down = False

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        if not hasattr(context.space_data, "image"):
            return False
        if context.space_data.image is None:
            return False
        return True

    def invoke(self, context, event):
        self.shift_key_down = event.shift
        return self.execute(context)

    def execute(self, context: bpy.types.Context) -> set[str]:
        target_image = context.space_data.image

        if self.shift_key_down:
            target_image.reload()

        width, height = target_image.size
        target_image_pixel_data = np.zeros((width, height, 4), "f")

        target_image.pixels.foreach_get(target_image_pixel_data.ravel())

        Alpha = target_image_pixel_data[:,:,3]

        val = context.scene.threshold_alpha_value
        target_image_pixel_data[:,:,3] = np.where(Alpha > val, 1.0, 0.0)

        target_image.pixels.foreach_set(target_image_pixel_data.ravel())
        target_image.update()

        return {"FINISHED"}


class THRESHOLD_ALPHA_PT_panel(bpy.types.Panel):
    bl_label = "Threshold Alpha"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context: bpy.types.Context):
        scene = context.scene
        layout = self.layout
        layout.prop(scene, "threshold_alpha_value")
        layout.operator(THRESHOLD_ALPHA_OT_main.bl_idname)


classes = (
        THRESHOLD_ALPHA_OT_main,
        THRESHOLD_ALPHA_PT_panel,
)

scene_props = {
        "threshold_alpha_value": bpy.props.FloatProperty(name="Value", default=0.0, min=0.0, max=1.0),
}


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    for name, prop in scene_props.items():
        setattr(bpy.types.Scene, name, prop)


def unregister():
    for name in scene_props.keys():
        if hasattr(bpy.types.Scene, name):
            delattr(bpy.types.Scene, name)

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
