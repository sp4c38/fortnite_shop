import os
from PIL import Image

BASE_DIR = os.path.expanduser(os.path.join('~', 'Documents', 'fortnite_shop')) # The base directory which stores files which are needed throughout the program (fonts, backgrounds,...)

settings = {
    'config_file': os.path.join(BASE_DIR, 'config', 'config.ini'), # Where config file is stores
    'width':512, # Width of each image
    'height':512, # Height of each image
    'rarity_grades' : { # Background color shall match rarity (to easily see which rarity a item has)
        'uncommon': Image.open(os.path.expanduser(os.path.join(BASE_DIR,'backgrounds','green_uncommon.png'))), #green
        'common':Image.open(os.path.expanduser(os.path.join(BASE_DIR,'backgrounds','gray_common.png'))), # gray
        'rare': Image.open(os.path.expanduser(os.path.join(BASE_DIR,'backgrounds','blue_rare.png'))), # blue
        'epic': Image.open(os.path.expanduser(os.path.join(BASE_DIR,'backgrounds','purple_epic.png'))), # purple
        'legendary': Image.open(os.path.expanduser(os.path.join(BASE_DIR,'backgrounds','orange_legendary.png'))) # orange
        },
    # ! Still needs to implement in program
    'text_color_for_rarity' : { #
        'uncommon': (255,215,0), #green
        'common': (100,0,255), # gray
        'rare': (255,100,0),  # blue
        'epic': (100,255,0), # purple
        'legendary':  (255,0,100), # orange 
        },

    'default_text_color_for_rarity' : (102,255,255),
    'text_color' : (255,255,255),
    # -----
    'backups_store_path' : os.path.expanduser(os.path.join('~', 'Documents', 'fortnite_shop', 'backups')), # Where to store backup files
    # backups_store_path_final : op.expanduser(op.join('~', 'Documents', 'fortnite_shop' , 'backups', '{0}', 'final.png')),
    'text_font_path' : os.path.expanduser(os.path.join('~', 'Documents', 'fortnite_shop', 'fonts', 'Lato-Bold.ttf')), # A .ttf file to set font
    'text_size' : 40, #  Will size the vbucks image according to this setting
    'spacing_to_top_vbucks_image' : 20,
    'spacing_to_top_price_text' : 15,
    'spacing_to_top_name_text' : 70,
    'spacing_to_side' : 2, # spacing to edge of the vbucks image in pixel (will adjust the text field automatically)
    'spacing_to_vbucks_image' : 10, # The space which the price text is situated next to the vbucks image
    'vbucks_img_path' : os.path.expanduser(os.path.join('~', 'Documents', 'fortnite_shop', 'data', 'vbucks_icon', 'icon_vbucks.png')),
    'row_images_next_to_each_other' : 4, # How many images shall be next to each other in one row?
                                  # If there are too less images in one row so that it still looks comfortable (that there
                                  # aren't too many rows, the program will automatically increase the amout of 
                                  # images next to each other in one row

    'width' : 512, # The width of each individual image / Width should be: width=height
    'height' : 512, # The height of each individual image / height should be: height=width
    # Settings for the final image
    'bg_not_found_bg' : (255,102,0), # Is used when there is no background image found / Please specify as RGB or RGBA
    'border_color' : (255,255,255), # Please specify as RGB, RGBA will not work


}
