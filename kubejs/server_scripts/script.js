ServerEvents.recipes(event => {
	event.shapeless('4x kubejs:iron_coin', 'kubejs:gold_coin')
	event.shapeless('16x kubejs:iron_coin', 'kubejs:diamond_coin')
	event.shapeless('64x kubejs:iron_coin', 'kubejs:netherite_coin')

	event.shapeless('kubejs:gold_coin', '4x kubejs:iron_coin')
	event.shapeless('4x kubejs:gold_coin', 'kubejs:diamond_coin')
	event.shapeless('16x kubejs:gold_coin', 'kubejs:netherite_coin')

	event.shapeless('kubejs:diamond_coin', '4x kubejs:gold_coin')
	event.shapeless('4x kubejs:diamond_coin', 'kubejs:netherite_coin')

	event.shapeless('kubejs:netherite_coin', '4x kubejs:diamond_coin')

	event.remove({output: 'magistuarmory:steel_ingot'})
	event.shapeless('9x kubejs:mold_ingot', 'createbigcannons:casting_sand')

	event.remove({output: 'createdeco:cast_iron_ingot', input: 'minecraft:iron_ingot'})
	event.remove({output: 'createdeco:cast_iron_block', input: 'minecraft:iron_block'})
	event.remove({output: 'createbigcannons:cast_iron_ingot'})
	event.remove({output: 'createbigcannons:cast_iron_block', input: 'minecraft:iron_block'})
	event.remove({output: 'createindustry:cast_iron_ingot', input: ['minecraft:iron_ingot', 'minecraft:coal']})
	event.custom({
		type: 'create:mixing',
		ingredients: [
			{ item: 'minecraft:iron_ingot', count: 2 },
			{ item: 'minecraft:coal', count: 1}
		],
		results: [
			{ fluid: 'createbigcannons:molten_cast_iron', amount: 180 }
		],
		heatRequirement: 'heated'
	})
	event.recipes.create.filling('createindustry:cast_iron_ingot', [Fluid.of('createbigcannons:molten_cast_iron', 90), 'kubejs:mold_ingot'])

	event.shapeless('createdeco:cast_iron_ingot', '#forge:ingots/cast_iron')
	event.shapeless('createbigcannons:cast_iron_ingot', '#forge:ingots/cast_iron')
	event.shapeless('createindustry:cast_iron_ingot', '#forge:ingots/cast_iron')
	event.shapeless('createdeco:cast_iron_block', '#forge:storage_blocks/cast_iron')
	event.shapeless('createbigcannons:cast_iron_block', '#forge:storage_blocks/cast_iron')
	event.shapeless('createindustry:cast_iron_block', '#forge:storage_blocks/cast_iron')

	event.shapeless('createbigcannons:cast_iron_block', '9x createbigcannons:cast_iron_ingot')

	event.remove({output: 'minecraft:rail'})
	event.remove({output: 'minecraft:activator_rail'})
	event.remove({output: 'minecraft:detector_rail'})
	event.remove({output: 'minecraft:powered_rail'})
	event.remove({output: 'create:controller_rail'})
	event.shaped(
		Item.of('minecraft:rail', 16),
		[
			'ABA',
			'ABA',
			'ABA'
		],
		{
			A: 'minecraft:iron_ingot',
			B: 'minecraft:stick'
		}
	)
	event.shaped(
		Item.of('minecraft:rail', 16),
		[
			'ABA',
			'ABA',
			'ABA'
		],
		{
			A: 'createaddition:iron_rod',
			B: 'minecraft:stick'
		}
	)
	event.shaped(
		Item.of('kubejs:track_kit_base', 16),
		[
			'ABA',
			'ABA',
			'ABA'
		],
		{
			A: 'minecraft:iron_nugget',
			B: 'minecraft:stick'
		}
	)
	event.shapeless(
		Item.of('kubejs:track_kit_activator', 1),
		[
			'minecraft:redstone_torch',
			'minecraft:redstone',
			'kubejs:track_kit_base'
		]
	)
	event.shapeless(Item.of('minecraft:activator_rail', 1), ['minecraft:rail', 'kubejs:track_kit_activator']).id("kubejs:track_kit_craft_activator_manual_only")
	event.recipes.create.deploying('minecraft:activator_rail', ['minecraft:rail', 'kubejs:track_kit_activator'])
	event.shapeless(
		Item.of('kubejs:track_kit_detector', 1),
		[
			'minecraft:stone_pressure_plate',
			'minecraft:redstone',
			'kubejs:track_kit_base'
		]
	)
	event.shapeless(Item.of('minecraft:detector_rail', 1), ['minecraft:rail', 'kubejs:track_kit_detector']).id("kubejs:track_kit_craft_detector_manual_only")
	event.recipes.create.deploying('minecraft:detector_rail', ['minecraft:rail', 'kubejs:track_kit_detector'])
	event.shapeless(
		Item.of('kubejs:track_kit_powered', 1),
		[
			'createaddition:gold_rod',
			'minecraft:redstone',
			'kubejs:track_kit_base'
		]
	)
	event.shapeless(Item.of('minecraft:powered_rail', 1), ['minecraft:rail', 'kubejs:track_kit_powered']).id("kubejs:track_kit_craft_powered_manual_only")
	event.recipes.create.deploying('minecraft:powered_rail', ['minecraft:rail', 'kubejs:track_kit_powered'])
	event.shapeless(
		Item.of('kubejs:track_kit_controller', 8),
		[
			'8x kubejs:track_kit_powered',
			'create:electron_tube'
		]
	)
	event.shapeless(Item.of('create:controller_rail', 1), ['minecraft:rail', 'kubejs:track_kit_controller']).id("kubejs:track_kit_craft_controller_manual_only")
	event.recipes.create.deploying('create:controller_rail', ['minecraft:rail', 'kubejs:track_kit_controller'])
})

ServerEvents.tags('item', event => {
  event.remove('forge:ingots/steel', 'magistuarmory:steel_ingot')
	event.remove('forge:ingots/steel', 'davebuildingmod:steel_ingot')
})

BlockEvents.rightClicked('minecraft:rail', event => {
	if(event.item.areItemsEqual('kubejs:track_kit_activator')) {
		event.block.set('minecraft:activator_rail')
		event.item.setCount(event.item.count - 1)
	}
})
BlockEvents.rightClicked('minecraft:rail', event => {
	if(event.item.areItemsEqual('kubejs:track_kit_detector')) {
		event.block.set('minecraft:detector_rail')
		event.item.setCount(event.item.count - 1)
	}
})
BlockEvents.rightClicked('minecraft:rail', event => {
	if(event.item.areItemsEqual('kubejs:track_kit_powered')) {
		event.block.set('minecraft:powered_rail')
		event.item.setCount(event.item.count - 1)
	}
})
BlockEvents.rightClicked('minecraft:rail', event => {
	if(event.item.areItemsEqual('kubejs:track_kit_controller')) {
		event.block.set('create:controller_rail')
		event.item.setCount(event.item.count - 1)
	}
})