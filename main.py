#!/usr/bin/env python3
import argparse
import math
from PIL import Image

parser = argparse.ArgumentParser(description='Converts images to dotted ASCII art')
parser.add_argument('image', metavar='IMAGE', type=str, help='the image to convert')
parser.add_argument('--threshold', '-t', type=int, default=90, help='the lightness threshold for writing a dot')
parser.add_argument('--scale', '-s', type=float, default=1.0, help='the scale factor before conversion')

character_map = {
    '00 00 00 00': ' ',
    '00 00 00 01': '⢀',
    '00 00 00 10': '⡀',
    '00 00 00 11': '⣀',
    '00 00 01 00': '⠠',
    '00 00 01 01': '⢠',
    '00 00 01 10': '⡠',
    '00 00 01 11': '⣠',
    '00 00 10 00': '⠄',
    '00 00 10 01': '⢄',
    '00 00 10 10': '⡄',
    '00 00 10 11': '⣄',
    '00 00 11 00': '⠤',
    '00 00 11 01': '⢤',
    '00 00 11 10': '⡤',
    '00 00 11 11': '⣤',
    '00 01 00 00': '⠐',
    '00 01 00 01': '⢐',
    '00 01 00 10': '⡐',
    '00 01 00 11': '⣐',
    '00 01 01 00': '⠰',
    '00 01 01 01': '⢰',
    '00 01 01 10': '⡰',
    '00 01 01 11': '⣰',
    '00 01 10 00': '⠔',
    '00 01 10 01': '⢔',
    '00 01 10 10': '⡔',
    '00 01 10 11': '⣔',
    '00 01 11 00': '⠴',
    '00 01 11 01': '⢴',
    '00 01 11 10': '⡴',
    '00 01 11 11': '⣴',
    '00 10 00 00': '⠂',
    '00 10 00 01': '⢂',
    '00 10 00 10': '⡂',
    '00 10 00 11': '⣂',
    '00 10 01 00': '⠢',
    '00 10 01 01': '⢢',
    '00 10 01 10': '⡢',
    '00 10 01 11': '⣢',
    '00 10 10 00': '⠆',
    '00 10 10 01': '⢆',
    '00 10 10 10': '⡆',
    '00 10 10 11': '⣆',
    '00 10 11 00': '⠦',
    '00 10 11 01': '⢦',
    '00 10 11 10': '⡦',
    '00 10 11 11': '⣦',
    '00 11 00 00': '⠒',
    '00 11 00 01': '⢒',
    '00 11 00 10': '⡒',
    '00 11 00 11': '⣒',
    '00 11 01 00': '⠲',
    '00 11 01 01': '⢲',
    '00 11 01 10': '⡲',
    '00 11 01 11': '⣲',
    '00 11 10 00': '⠖',
    '00 11 10 01': '⢖',
    '00 11 10 10': '⡖',
    '00 11 10 11': '⣖',
    '00 11 11 00': '⠶',
    '00 11 11 01': '⢶',
    '00 11 11 10': '⡶',
    '00 11 11 11': '⣶',
    '01 00 00 00': '⠈',
    '01 00 00 01': '⢈',
    '01 00 00 10': '⡈',
    '01 00 00 11': '⣈',
    '01 00 01 00': '⠨',
    '01 00 01 01': '⢨',
    '01 00 01 10': '⡨',
    '01 00 01 11': '⣨',
    '01 00 10 00': '⠌',
    '01 00 10 01': '⢌',
    '01 00 10 10': '⡌',
    '01 00 10 11': '⣌',
    '01 00 11 00': '⠬',
    '01 00 11 01': '⢬',
    '01 00 11 10': '⡬',
    '01 00 11 11': '⣬',
    '01 01 00 00': '⠘',
    '01 01 00 01': '⢘',
    '01 01 00 10': '⡘',
    '01 01 00 11': '⣘',
    '01 01 01 00': '⠸',
    '01 01 01 01': '⢸',
    '01 01 01 10': '⡸',
    '01 01 01 11': '⣸',
    '01 01 10 00': '⠜',
    '01 01 10 01': '⢜',
    '01 01 10 10': '⡜',
    '01 01 10 11': '⣜',
    '01 01 11 00': '⠼',
    '01 01 11 01': '⢼',
    '01 01 11 10': '⡼',
    '01 01 11 11': '⣼',
    '01 10 00 00': '⠊',
    '01 10 00 01': '⢊',
    '01 10 00 10': '⡊',
    '01 10 00 11': '⣊',
    '01 10 01 00': '⠪',
    '01 10 01 01': '⢪',
    '01 10 01 10': '⡪',
    '01 10 01 11': '⣪',
    '01 10 10 00': '⠎',
    '01 10 10 01': '⢎',
    '01 10 10 10': '⡎',
    '01 10 10 11': '⣎',
    '01 10 11 00': '⠮',
    '01 10 11 01': '⢮',
    '01 10 11 10': '⡮',
    '01 10 11 11': '⣮',
    '01 11 00 00': '⠚',
    '01 11 00 01': '⢚',
    '01 11 00 10': '⡚',
    '01 11 00 11': '⣚',
    '01 11 01 00': '⠺',
    '01 11 01 01': '⢺',
    '01 11 01 10': '⡺',
    '01 11 01 11': '⣺',
    '01 11 10 00': '⠞',
    '01 11 10 01': '⢞',
    '01 11 10 10': '⡞',
    '01 11 10 11': '⣞',
    '01 11 11 00': '⠾',
    '01 11 11 01': '⢾',
    '01 11 11 10': '⡾',
    '01 11 11 11': '⣾',
    '10 00 00 00': '⠁',
    '10 00 00 01': '⢁',
    '10 00 00 10': '⡁',
    '10 00 00 11': '⣁',
    '10 00 01 00': '⠡',
    '10 00 01 01': '⢡',
    '10 00 01 10': '⡡',
    '10 00 01 11': '⣡',
    '10 00 10 00': '⠅',
    '10 00 10 01': '⢅',
    '10 00 10 10': '⡅',
    '10 00 10 11': '⣅',
    '10 00 11 00': '⠥',
    '10 00 11 01': '⢥',
    '10 00 11 10': '⡥',
    '10 00 11 11': '⣥',
    '10 01 00 00': '⠑',
    '10 01 00 01': '⢑',
    '10 01 00 10': '⡑',
    '10 01 00 11': '⣑',
    '10 01 01 00': '⠱',
    '10 01 01 01': '⢱',
    '10 01 01 10': '⡱',
    '10 01 01 11': '⣱',
    '10 01 10 00': '⠕',
    '10 01 10 01': '⢕',
    '10 01 10 10': '⡕',
    '10 01 10 11': '⣕',
    '10 01 11 00': '⠵',
    '10 01 11 01': '⢵',
    '10 01 11 10': '⡵',
    '10 01 11 11': '⣵',
    '10 10 00 00': '⠃',
    '10 10 00 01': '⢃',
    '10 10 00 10': '⡃',
    '10 10 00 11': '⣃',
    '10 10 01 00': '⠣',
    '10 10 01 01': '⢣',
    '10 10 01 10': '⡣',
    '10 10 01 11': '⣣',
    '10 10 10 00': '⠇',
    '10 10 10 01': '⢇',
    '10 10 10 10': '⡇',
    '10 10 10 11': '⣇',
    '10 10 11 00': '⠧',
    '10 10 11 01': '⢧',
    '10 10 11 10': '⡧',
    '10 10 11 11': '⣧',
    '10 11 00 00': '⠓',
    '10 11 00 01': '⢓',
    '10 11 00 10': '⡓',
    '10 11 00 11': '⣓',
    '10 11 01 00': '⠳',
    '10 11 01 01': '⢳',
    '10 11 01 10': '⡳',
    '10 11 01 11': '⣳',
    '10 11 10 00': '⠗',
    '10 11 10 01': '⢗',
    '10 11 10 10': '⡗',
    '10 11 10 11': '⣗',
    '10 11 11 00': '⠷',
    '10 11 11 01': '⢷',
    '10 11 11 10': '⡷',
    '10 11 11 11': '⣷',
    '11 00 00 00': '⠉',
    '11 00 00 01': '⢉',
    '11 00 00 10': '⡉',
    '11 00 00 11': '⣉',
    '11 00 01 00': '⠩',
    '11 00 01 01': '⢩',
    '11 00 01 10': '⡩',
    '11 00 01 11': '⣩',
    '11 00 10 00': '⠍',
    '11 00 10 01': '⢍',
    '11 00 10 10': '⡍',
    '11 00 10 11': '⣍',
    '11 00 11 00': '⠭',
    '11 00 11 01': '⢭',
    '11 00 11 10': '⡭',
    '11 00 11 11': '⣭',
    '11 01 00 00': '⠙',
    '11 01 00 01': '⢙',
    '11 01 00 10': '⡙',
    '11 01 00 11': '⣙',
    '11 01 01 00': '⠹',
    '11 01 01 01': '⢹',
    '11 01 01 10': '⡹',
    '11 01 01 11': '⣹',
    '11 01 10 00': '⠝',
    '11 01 10 01': '⢝',
    '11 01 10 10': '⡝',
    '11 01 10 11': '⣝',
    '11 01 11 00': '⠽',
    '11 01 11 01': '⢽',
    '11 01 11 10': '⡽',
    '11 01 11 11': '⣽',
    '11 10 00 00': '⠋',
    '11 10 00 01': '⢋',
    '11 10 00 10': '⡋',
    '11 10 00 11': '⣋',
    '11 10 01 00': '⠫',
    '11 10 01 01': '⢫',
    '11 10 01 10': '⡫',
    '11 10 01 11': '⣫',
    '11 10 10 00': '⠏',
    '11 10 10 01': '⢏',
    '11 10 10 10': '⡏',
    '11 10 10 11': '⣏',
    '11 10 11 00': '⠯',
    '11 10 11 01': '⢯',
    '11 10 11 10': '⡯',
    '11 10 11 11': '⣯',
    '11 11 00 00': '⠛',
    '11 11 00 01': '⢛',
    '11 11 00 10': '⡛',
    '11 11 00 11': '⣛',
    '11 11 01 00': '⠻',
    '11 11 01 01': '⢻',
    '11 11 01 10': '⡻',
    '11 11 01 11': '⣻',
    '11 11 10 00': '⠟',
    '11 11 10 01': '⢟',
    '11 11 10 10': '⡟',
    '11 11 10 11': '⣟',
    '11 11 11 00': '⠿',
    '11 11 11 01': '⢿',
    '11 11 11 10': '⡿',
    '11 11 11 11': '⣿',
}

args = parser.parse_args()
image_file_name = args.image
THRESHOLD = args.threshold
SCALE = args.scale


def gray_value(r: int, g: int, b: int) -> int:
    return int((r + g + b) / 3)


def region_to_string(region) -> str:
    intermediate = [''.join(x) for x in region]
    return ' '.join(intermediate)


def region_to_ascii(region) -> chr:
    bitstring = region_to_string(region)
    print(bitstring)
    return character_map[bitstring]


def get_character_for_location(size, pixels, x, y) -> chr:
    """
    return the ASCII character for the 4x2 pixel region with its upper left corner at x, y
    :param pixels: the image as pixels
    :param x: the x position of the upper left corner
    :param y: the y position of the upper left corner
    :return: a unicode character
    """
    region = [[0, 0] for _ in range(0, 4)]
    for i in range(x, x+2):
        for j in range(y, y+4):
            if i >= size[0] or j >= size[1]:
                gray = 0
            else:
                r, g, b = pixels[i, j]
                gray = gray_value(r, g, b)

            (region[j - y])[i - x] = '0' if gray < THRESHOLD else '1'

    return region_to_ascii(region)


image = Image.open(image_file_name)

width, height = image.size
image.thumbnail((width * SCALE * 1.1, height * SCALE), Image.ANTIALIAS)
pixels = image.load()

width = width * SCALE * 1.1
height = height * SCALE
output_width = math.ceil(width / 2)
output_height = math.ceil(height / 4)

output = [[' ' for _ in range(0, output_width)] for _ in range(0, output_height)]

for x in range(0, output_width):
    for y in range(0, output_height):
        output[y][x] = get_character_for_location(image.size, pixels, x * 2, y * 4)

for x in range(0, len(output)):
    print(''.join(output[x]))
