# -*- coding: utf-8 -*-
img_1_name = input('Enter first image path: ')
img_2_name = input('Enter second image path: ')
result_name = input('Enter result image path: ')

if (img_1_name.count('.bmp') == 0 or 
    img_2_name.count('.bmp') == 0 or 
    result_name.count('.bmp') == 0):
    
    print('Error: wrong format.\n')
    raise SystemExit(-1)

img_1 = open(img_1_name, 'rb')
img_2 = open(img_2_name, 'rb')

def read_header(img):
    header = {}
    
    header['ID'] = img.read(2)
    header['BMP Size'] = img.read(4)
    header['Unused_1'] = img.read(2)
    header['Unused_2'] = img.read(2)
    header['Offset'] = img.read(4)
    
    header['Header Size'] = img.read(4)
    header['BMP Width'] = img.read(4)
    header['BMP Height'] = img.read(4)
    header['Color Planes'] = img.read(2)
    header['Bits per pixel'] = img.read(2)
    header['Pixel compression'] = img.read(4)
    header['Bitmap Size'] = img.read(4)
    header['Horizontal resolution'] = img.read(4)
    header['Vertical resoluion'] = img.read(4)
    header['Used colors'] = img.read(4)
    header['Important colors'] = img.read(4)
    
    return header

def write_header(img, header):
    img.write(header['ID'])
    img.write(header['BMP Size'])
    img.write(header['Unused_1'])
    img.write(header['Unused_2'])
    img.write(header['Offset'])
    
    img.write(header['Header Size'])
    img.write(header['BMP Width'])
    img.write(header['BMP Height'])
    img.write(header['Color Planes'])
    img.write(header['Bits per pixel'])
    img.write(header['Pixel compression'])
    img.write(header['Bitmap Size'])
    img.write(header['Horizontal resolution'])
    img.write(header['Vertical resolution'])
    img.write(header['Used colors'])
    img.write(header['Important colors'])

def read_pixels(img):
    pixel_bytes = img.read()
    pixel_colors = [ byte for byte in pixel_bytes ]
    return pixel_colors[::-1] # Returns already reversed bytes

def form_header(width, height):
    

header_1 = read_header(img_1)
header_2 = read_header(img_2)

pixels_1 = read_pixels(img_1)
pixels_2 = read_pixels(img_2)

if (header_1['BMP Height'] != header_2['BMP Height']):
    print('Error: incorrect image shapes.\n')
    raise SystemExit(-1)


