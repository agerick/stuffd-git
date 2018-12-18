def clean_unit(unit):
    unit_dict = {
     '10-inchs':'inch',
     '11-inchs':'inch',
     '12 inchs':'inch',
     '12-inchs':'inch',
     '6-inchs':'inch',
     '8-inchs':'inch',
     '9-inch':'inch',
     'Box':'boxes',
     'Can':'cans',
     'Chunk':'chunks',
     'Clove':'cloves',
     'Cloves':'cloves',
     'Dash':'dashes',
     'Dashs':'dashes',
     'Handful':'handfuls',
     'Head':'heads',
     'Ozs':'ozs',
     'Packet':'pkg',
     'Packets':'pkg',
     'Slice':'slices',
     'Tb':'tbsp',
     'Tbs':'tbsp',
     'Tbsp':'tbsp',
     'Tbsps':'tbsp',
     'bag':'bag',
     'ball':'ball',
     'bottle':'bottle',
     'box':'boxes',
     'boxs':'boxes',
     'bunch':'bunches',
     'bunche':'bunches',
     'bunches':'bunches',
     'can':'cans',
     'cans':'cans',
     'chunk':'chunks',
     'clove':'cloves',
     'cloves':'cloves',
     'cube':'cubes',
     'cup':'cups',
     'cups':'cups',
     'cupsheet':'cups',
     'dash':'dashes',
     'dashes':'dashes',
     'drop':'drops',
     'drops':'drops',
     'envelope':'packets',
     'envelopes':'packets',
     'fillets':'fillets',
     'fl. oz.s':'flozs',
     'gallon':'gallons',
     'glass':'glasses',
     'gms':'grams',
     'grams':'grams',
     'grs':'grams',
     'handful':'handfuls',
     'handfuls':'handfuls',
     'head':'heads',
     'heads':'heads',
     'inch':'inch',
     'inches':'inch',
     'jar':'jars',
     'kg':'kgs',
     'kgs':'kgs',
     'kilograms':'kgs',
     'knob':'knobs',
     'leave':'leaves',
     'leaves':'leaves',
     'liter':'liters',
     'liters':'liters',
     'loaf':'loafs',
     'loafs':'loafs',
     'mLs':'ml',
     'milliliter':'ml',
     'milliliters':'ml',
     'ouncessheets':'oz',
     'package':'pkg',
     'packages':'pkg',
     'packet':'pkg',
     'packets':'pkg',
     'pinch':'pinches',
     'pinche':'pinches',
     'pinches':'pinches',
     'pint':'pints',
     'pints':'pints',
     'pouch':'pkg',
     'pounds':'pound',
     'ribs':'ribs',
     'scoops':'scoops',
     'serving':'servings',
     'servings':'servings',
     'sheet':'sheets',
     'sheets':'sheets',
     'slab':'slab',
     'slice':'slices',
     'slices':'slices',
     'sprig':'sprigs',
     'sprigs':'sprigs',
     'stalk':'stalks',
     'stalks':'stalks',
     'stick':'sticks',
     'sticks':'sticks',
     'strip':'strips',
     'strips':'strips',
     'teaspoon':'tsp',
     'teaspoons':'tsp'
     }
    if unit in unit_dict:
        return unit_dict[unit]
    else:
        return unit

def clean_id(id):
    if len(str(id)) == 4: # return 4 digit
        return id        
    elif len(str(id)) == 5: # return 5 digit
        return id
    elif len(str(id)) == 6:
        raise Exception('The id of this ingredient has 6 characters')
    elif len(str(id)) == 7: # return 6 digit
        return int(str(id)[2:])
    elif len(str(id)) == 8: # return 7 digit
        return int(str(id)[3:])

def clean_ingredients(ingredient_list):
    id_list =[]
    new_list = []
    for igd in ingredient_list:
        if clean_id(igd['id']) not in id_list:
            id_list.append(clean_id(igd['id']))
            new_list.append(igd)
    return new_list