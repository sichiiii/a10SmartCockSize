from PIL import Image, ImageDraw
import random


def generate_pillar_image(girth: int, length: int, race: str = None):
    races = {
        'Белый': '#ffdbaf',
        'Монгол': '#fff2e2',
        'Черный': '#756046',
        'Не такой черный': '#443421',
        'Азиат': '#ffe8b2',
        'Мексиканец': '#edb86f',
        'Индус': '#997138',
    }
    if not race:
        racename, racevalue = random.choice(list(races.items()))
    else:
        racename, racevalue = race, races[race]

    girth *= 10
    length *= 6

    image_width = girth + 100
    image_height = length + 100
    img = Image.new('RGB', (image_width, image_height), "white")
    draw = ImageDraw.Draw(img)

    center_x = image_width // 2
    base_y = image_height - 50

    base_radius = girth // 2
    left_base = (center_x - girth // 2 - base_radius, base_y - base_radius * 2, center_x - girth // 2 + base_radius, base_y)
    right_base = (center_x + girth // 2 - base_radius, base_y - base_radius * 2, center_x + girth // 2 + base_radius, base_y)
    draw.ellipse(left_base, fill=racevalue)
    draw.ellipse(right_base, fill=racevalue)

    shaft_rectangle = (center_x - girth // 2, base_y - length, center_x + girth // 2, base_y)
    draw.rectangle(shaft_rectangle, fill=racevalue)

    top_arc_bbox = (center_x - girth // 2, base_y - length - base_radius, center_x + girth // 2, base_y - length + base_radius)
    draw.pieslice(top_arc_bbox, 180, 360, fill='pink')

    image_filename = f"image.png"
    img.save(image_filename)

    return racename
