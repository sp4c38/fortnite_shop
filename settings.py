import os

from PIL import Image

BASE_DIR = os.path.expanduser(os.path.join('~', 'Documents', 'fortnite_shop')) # The base directory which stores files which are needed throughout the program (fonts, backgrounds,...)

settings = {
    'config_file': os.path.join(BASE_DIR, 'config', 'config.ini'), # Where config file is stored
    'vbucks_img_path' : os.path.join(BASE_DIR, 'vbucks_icon', 'icon_vbucks.png'),
    'vbucks_img_size': 38, # Tells how long one side of the vbucks image is, vbucks image is processed as a square
    'font_path' : os.path.join(BASE_DIR, 'fonts', 'fortnite-font.ttf'), # The font .ttf file
    'images_in_row' : 4, # 
    'width':512, # Width of each individual image
    'height':512, # Height of each individual image
    'text_size' : 50, # Size of text and vbucks icon
    'price_text_color' : (255,255,255), # Text color of text
    'name_text_color' : (234,176,50),
    'border_width': 2,
    'border_color' : (255,255,255), # As RGB, RGBA won't work
    'final_image_color': (0,0,0), # The color empty fields will have on the final image
    'overlayer': os.path.join(BASE_DIR, 'backgrounds', 'overlayer.png'), 
    'overlayer_percentage': 0.32, # The percentage (as decimal number) the overlayer is high in relationship to the heigt of the final picture
    'spc_vbucksimg_to_pricetext': 10, # The space between the vbucks image and the price text
    'spc_top_overlayer_nametext': 20, # The space between the top edge of the overlayer and the upper side of the name text
    'spc_top_overlayer_price': 85, # The space between the top edge of the overlayer and the upper side of the price objects
    'rarity_grades' : { # Background color matches rarity
        'uncommon': os.path.join(BASE_DIR,'backgrounds','green_uncommon.png'), #green
        'common':os.path.join(BASE_DIR,'backgrounds','gray_common.png'), # gray
        'rare': os.path.join(BASE_DIR,'backgrounds','blue_rare.png'), # blue
        'epic': os.path.join(BASE_DIR,'backgrounds','purple_epic.png'), # purple
        'legendary': os.path.join(BASE_DIR,'backgrounds','orange_legendary.png'), # orange
    },

    'recent_info': os.path.join(BASE_DIR, 'backups', 'recent.info'),
    'backup_dir': os.path.join(BASE_DIR, 'backups', '{}'), # Where backups shall be stored
}
