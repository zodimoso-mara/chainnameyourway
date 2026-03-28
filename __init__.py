bl_info = {
	"name": "Chain Name Your Way",
	"author": "Marilyn M. Cere",
	"version": (1, 0, 0),
	"blender": (4, 4, 3),
	"description": "Allows you to name chains of bones with any format of letters and or numbers",
	"location": "",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Rigging"
}


if "bpy" in locals():
    import importlib
    if "chain_name" in locals():
        chain.reload(chain_name)
else:
    import bpy
    from . import chain_name

addon_keymaps = {}

def unregister_keymaps():
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
def register_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps.new(name="Window", space_type='EMPTY')
    kmi = km.keymap_items.new('wm.chain_name_your_way', 'F2', 'PRESS', alt=True)
    addon_keymaps['57A73'] = (km, kmi)


def register():
    register_keymaps()
    bpy.utils.register_class(chain_name.Options)
    bpy.utils.register_class(chain_name.WM_OT_chain_name_your_way)

def unregister():
    unregister_keymaps()
    bpy.utils.unregister_class(Options)
    bpy.utils.unregister_class(WM_OT_chain_name_your_way)


if __name__ == "__main__":
    register()
