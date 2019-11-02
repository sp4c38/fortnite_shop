settings = {
    'width':512, # Width of each image
    'height':512, # Height of each image
    'rarity_grades' = { # 
    	'uncommon': Image.open(expanduser(os.path.join('~','Documents','fortnite_shop','backgrounds','green_uncommon.png'))), #green
    	'common':Image.open(expanduser(os.path.join('~','Documents','fortnite_shop','backgrounds','gray_common.png'))), # gray
    	'rare': Image.open(expanduser(os.path.join('~','Documents','fortnite_shop','backgrounds','blue_rare.png'))), # blue
    	'epic': Image.open(expanduser(os.path.join('~','Documents', 'fortnite_shop','backgrounds','purple_epic.png'))), # purple
    	'legendary': Image.open(expanduser(os.path.join('~','Documents','fortnite_shop','backgrounds','orange_legendary.png'))) # orange
		}
	'text_color_for_rarity' = {
    	'uncommon': (255,215,0), #green
    	'common': (100,0,255), # gray
    	'rare': (255,100,0),  # blue
    	'epic': (100,255,0), # purple
    	'legendary':  (255,0,100), # orange 
		}
	default_text_color_for_rarity = (102,255,255) # The default color if rarity from api matches none of settings file
    }


