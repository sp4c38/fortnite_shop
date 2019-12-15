# PythonFile which holds multiple functions to clip multiple images to one 

from PIL import Image, ImageDraw, ImageFont


def items_sliced(items_list, number): 
    items_sliced = []
    pointer = 0
    stop = False
    
    
    while stop == False:
        if not items_list[pointer:pointer+number]:
            stop = True
        else:
            items_sliced.append(items_list[pointer:pointer+number]) 
            pointer += number

    return items_sliced

def edit_single_image(settings, imageobj):

    imageobj.image = imageobj.image.resize(size=(settings['width'], settings['height'])).convert("RGBA")

    # Set the background color, which depends on the rarity of the item
    # The background of images which have no matching background for rarity will stay white

    if imageobj.rarity in settings['rarity_grades']:
        background = Image.open(settings['rarity_grades'][imageobj.rarity]).resize(size=(settings['width'], settings['height'])).convert('RGBA')
        imageobj.image = Image.alpha_composite(im1=background, im2=imageobj.image)


    # Create gray overlayer (to see name and price better)
    overlayer = Image.open(settings["overlayer"]).resize(size=(settings["width"], settings["height"])).convert("RGBA")
    imageobj.image = Image.alpha_composite(im1=imageobj.image, im2=overlayer)

    # Create a pencil and load font
    draw = ImageDraw.Draw(imageobj.image)
    font = ImageFont.truetype(font=settings['font_path'], size=settings['text_size'])

    # Draw border
    draw.rectangle(xy=((0,0), (settings['width'],settings['height'])), outline=settings['border_color'], width=settings['border_width'])

    #  Load vbucks icon
    vbucks_icon = Image.open(fp=settings['vbucks_img_path']).resize(size=(settings['vbucks_img_size'], settings['vbucks_img_size']))
    
    # Specify positions of vbucks image, the price text and the name text
    name_txt_position = (((settings['width']/2)-(font.getsize(imageobj.name)[0]/2)), \
                           settings['height']-(settings['height']*settings['overlayer_percentage']-settings["spc_top_overlayer_nametext"]))

    space_on_each_half = (settings["vbucks_img_size"] + settings["spc_vbucksimg_to_pricetext"] + font.getsize(imageobj.price)[0])/2 # The space on each half (width/2) for the price objects
    price_txt_position = (settings["width"]/2 + (space_on_each_half - font.getsize(imageobj.price)[0]), \
                          settings['height']-(settings['height']*settings['overlayer_percentage']-settings["spc_top_overlayer_price"]))
    vbucks_img_position = (int(settings["width"]/2 - space_on_each_half)), \
                           int(settings['height']-(settings['height']*settings['overlayer_percentage']-(settings["spc_top_overlayer_price"]+5)))

    # Draw vbucks image and price text
    imageobj.image.paste(im=vbucks_icon, box=vbucks_img_position, mask=vbucks_icon)
    draw.text(xy=price_txt_position, text=imageobj.price, fill=settings['price_text_color'], font=font)
    draw.text(xy=name_txt_position, text=imageobj.name, fill=settings['name_text_color'], font=font)
    
    return imageobj.image

def imgs_to_rows(settings, img_list): # Converts multiple images to row (with each row containing x images)
    rows = []

    for rowimgs in img_list:
        x_paste = 0
        row_img = Image.new(mode='RGBA', size=((len(rowimgs)*settings['width']), settings['height']))

        for image in rowimgs:
            row_img.paste(im=image.image, box=(x_paste, 0))
            x_paste += settings['width']

        rows.append(row_img)

    return rows

def rows_to_final(settings, rows):
    result_img = Image.new(mode='RGBA', color=settings['final_image_color'], size=(settings['width']*settings['images_in_row'],settings['height']*len(rows)))
    
    y_paste=0
    
    for row in rows:
        result_img.paste(im=row, box=(0,y_paste))
        y_paste += settings['height']
    
    return result_img

