# PythonFile which holds multiple functions to clip multiple images to one 

from PIL import Image

def items_sliced(items_list, number): 
    items_sliced = []

    while len(items_list) > 0:
        items_sliced.append([items_list.pop(items_list.index(item)) for item in items_list[:number]])
        
    return items_sliced


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
    result_img = Image.new(mode='RGBA', size=(settings['width']*settings['images_in_row'],settings['height']*len(rows)))
    
    y_paste=0
    
    for row in rows:
        result_img.paste(im=row, box=(0,y_paste))
        y_paste += settings['height']
    
    return result_img

def edit_single_image(settings, image):
    single_image_data.image = single_image_data.image.resize(size=(width,height))
    
    x_paste = 0
    y_paste = 0

    if not os.path.exists(text_font_path):
        print(f"Font path \'{text_font_path}\' doesn't exist.")
        sys.exit(1)

    img_elements = Image.new(mode='RGBA', size=(width,height))
    img_elements.paste(single_image_data.image)
    # Add v-bucks price for shop item
    data_box = Image.new(mode='RGBA', size=(width,height))
    vbucks_icon = Image.open(fp=vbucks_img_path)
    vbucks_icon = vbucks_icon.resize(size=(text_size,text_size))

    image_position = (spacing_to_side, spacing_to_top_vbucks_image)
    vbucks_text_position = ((spacing_to_side+vbucks_icon.width+spacing_to_vbucks_image), spacing_to_top_price_text)
    
    draw = ImageDraw.Draw(img_elements)
    font = ImageFont.truetype(font=text_font_path, size=text_size)

    # Draw vbucks image and price text
    img_elements.paste(im=vbucks_icon, box=image_position)
    draw.text(xy=vbucks_text_position, text=single_image_data.price, fill=text_color, font=font)
    
    # Draw item name according to if there is enough space (will draw every time, just different text size, or with wordwrap)
    if single_image_data.name:
        item_name = single_image_data.name
        spilted_name = item_name.split(' ')
        name_text_position = {'spacing_to_side': spacing_to_side, 'spacing_to_top':spacing_to_top_name_text}

    for word in spilted_name:
        if single_image_data.rarity in rarity_grades:
            text_color_2 = text_color_for_rarity[single_image_data.rarity]
        else:
            text_color_2 = default_text_color_for_rarity
        draw.text(xy=(name_text_position['spacing_to_side'], name_text_position['spacing_to_top']),\
         text=word, fill=text_color_2, font=font)
        name_text_position['spacing_to_top'] += text_size

    # Has to be pasted again on a new image so that the mask option works correctly (this type
    # of bug would only happen on some images (here not anymore (because it was fixed)))
    
    # Set background color (dependet on the rarity of the shop item (image))
    
    if single_image_data.rarity in rarity_grades:
        bg_image = Image.new(size=(width, height), mode='RGBA')
        rarity_bg_img = rarity_grades[single_image_data.rarity]
        rarity_bg_img = rarity_bg_img.resize(size=(width,height))
        bg_image.paste(im=rarity_bg_img, box=(0,0))
    else:
        rarity_bg_img = bg_not_found_bg
        bg_image = Image.new(size=(width, height),color=rarity_bg_img, mode='RGBA')

    # Draw border
    draw = ImageDraw.Draw(bg_image)
    draw.rectangle(xy=((0,0), (width,height)), outline=border_color, width=2)
    
    bg_image.paste(im=img_elements, box=(10,0), mask=img_elements)

    return bg_image