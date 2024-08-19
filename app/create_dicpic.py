from PIL import Image, ImageDraw
import random


def generate_pillar_image(girth: int, length: int, race: str = None):
    races = {
        'Белый': '#ffdbaf',
        'Монгол': '#fff2e2',
        'Не такой черный': '#756046',
        'Черный': '#443421',
        'Азиат': '#ffe8b2',
        'Мексиканец': '#edb86f',
        'Индус': '#997138',
    }
    if not race:
        racename, racevalue = random.choice(list(races.items()))
    else:
        racename, racevalue = race, races[race]

    girth *= 25
    length *= 24

    image_width = 500
    image_height = 1000
    img = Image.new('RGB', (image_width, image_height), "white")
    draw = ImageDraw.Draw(img)

    center_x = image_width // 2
    base_y = image_height - 50

    base_radius = 50
    left_base = (center_x - girth // 2 - base_radius, base_y - base_radius * 2, center_x - girth // 2 + base_radius, base_y)
    right_base = (center_x + girth // 2 - base_radius, base_y - base_radius * 2, center_x + girth // 2 + base_radius, base_y)
    draw.ellipse(left_base, fill=racevalue)
    draw.ellipse(right_base, fill=racevalue)

    shaft_rectangle = (center_x - girth // 2, base_y - length, center_x + girth // 2, base_y)
    draw.rectangle(shaft_rectangle, fill=racevalue)

    top_arc_bbox = (center_x - girth // 2, base_y - length - base_radius, center_x + girth // 2, base_y - length + base_radius)
    draw.pieslice(top_arc_bbox, 180, 360, fill='pink')

    stripe_x = center_x
    stripe_left = stripe_x - 2
    stripe_right = stripe_x + 2

    stripe_bbox = (stripe_left, base_y - length - base_radius, stripe_right, base_y - length + base_radius - 70)
    draw.rectangle(stripe_bbox, fill='black')

    # Draw ruler
    ruler_x = 50
    for i in range(0, length + 50, 50):  # Marks every 50 units
        y = base_y - i - 30
        draw.line([(ruler_x, y), (ruler_x + 20, y)], fill="black", width=2)
        draw.text((ruler_x - 30, y - 5), f'{i // 24}cm', fill="black")

    # Save the image
    image_filename = "image.png"
    img.save(image_filename)

    return racename


