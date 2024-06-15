// Listen to item registry event
StartupEvents.registry('item', event => {
  // The texture for this item has to be placed in kubejs/assets/kubejs/textures/item/test_item.png
  // If you want a custom item model, you can create one in Blockbench and put it in kubejs/assets/kubejs/models/item/test_item.json
	event.create('track_kit_base').displayName("Track Kit").tooltip("A base track kit used to craft others.")
  event.create('track_kit_activator').displayName("Activator Track Kit").tooltip("Right click a track in world or craft with it to attach this kit to a rail.")
	event.create('track_kit_detector').displayName("Detector Track Kit").tooltip("Right click a track in world or craft with it to attach this kit to a rail.")
	event.create('track_kit_powered').displayName("Powered Track Kit").tooltip("Right click a track in world or craft with it to attach this kit to a rail.")
	event.create('track_kit_controller').displayName("Controller Track Kit").tooltip("Right click a track in world or craft with it to attach this kit to a rail.")

	event.create('mold_ingot').displayName("Ingot Mold").tooltip("A mold filled with molten metal to forge ingots.")
})