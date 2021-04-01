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
result = open(result_name, 'wb')

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
    
def write_pixels(img, pixels):
    pixels = pixels[::-1]
    for pixel in pixels:
        img.write( pixel.to_bytes(1, byteorder = 'little') )
    

def read_pixels(img, header):
    pixels = None
    if (int.from_bytes(header['BMP Width'], byteorder = 'little') % 4 == 0):
        pixels = [ byte for byte in img.read() ]
    else:
        row_stride = width * header['Bits per pixel'] / 8
        new_stride = row_stride
        while (new_stride % 4 != 0):
            new_stride += 1
        padding = [0] * ( new_stride - row_stride )
        pixels = []
        for i in range(header['BMP Height']):
            pixels += [ byte for byte in img.read( row_stride ) ]
            img.read( new_stride - row_stride )
    return pixels[::-1] # Returns already reversed color data

def form_header(width, height):
    image_size = ((width * 3 + 3) & ~3) * height
    file_size = 54 + image_size
    header = {}
    
    header['ID'] = b'BM'
    header['BMP Size'] = file_size.to_bytes(4, byteorder = 'little')
    header['Unused_1'] = (0).to_bytes(2, byteorder = 'little')
    header['Unused_2'] = (0).to_bytes(2, byteorder = 'little')
    header['Offset'] = (54).to_bytes(4, byteorder = 'little')
    
    header['Header Size'] = (40).to_bytes(4, byteorder = 'little')
    header['BMP Width'] = width.to_bytes(4, byteorder = 'little')
    header['BMP Height'] = height.to_bytes(4, byteorder = 'little')
    header['Color Planes'] = (1).to_bytes(2, byteorder = 'little')
    header['Bits per pixel'] = (24).to_bytes(2, byteorder = 'little')
    header['Pixel compression'] = (0).to_bytes(4, byteorder = 'little')
    header['Bitmap Size'] = image_size.to_bytes(4, byteorder = 'little')
    header['Horizontal resolution'] = (0).to_bytes(4, byteorder = 'little')
    header['Vertical resolution'] = (0).to_bytes(4, byteorder = 'little')
    header['Used colors'] = (0).to_bytes(4, byteorder = 'little')
    header['Important colors'] = (0).to_bytes(4, byteorder = 'little')
    
    return header

header_1 = read_header(img_1)
header_2 = read_header(img_2)

width_1 = int.from_bytes(header_1['BMP Width'], byteorder = 'little')
width_2 = int.from_bytes(header_2['BMP Width'], byteorder = 'little')
height_1 = int.from_bytes(header_1['BMP Height'], byteorder = 'little')
height_2 = int.from_bytes(header_2['BMP Height'], byteorder = 'little')

pixels_1 = read_pixels(img_1, header_1)
pixels_2 = read_pixels(img_2, header_2)

if (height_1 != height_2):
    print('Error: incorrect image shapes.\n')
    raise SystemExit(-1)

res_pixels = []
padding_stride = None

if (( width_1 + width_2 ) % 4 == 0):
    padding_stride = 0
else:
    row_stride = width * int.from_bytes(header_1['Bits per pixel'], byteorder = 'little') / 8
    new_stride = row_stride
    while (new_stride % 4 != 0):
        new_stride += 1
    padding_stride = new_stride - row_stride

for i in range(height_1):
    tmp_1 = [ pixels_1[i] for i in range( 3 * width_1 * i, 3 * width_1 * (i + 1) )]
    tmp_2 = [ pixels_2[i] for i in range( 3 * width_2 * i, 3 * width_2 * (i + 1) )]
    
    res_pixels += tmp_2 + tmp_1 + [0]*padding_stride
    
res_header = form_header(width_1 + width_2, height_1)

write_header(result, res_header)
write_pixels(result, res_pixels)

img_1.close()
img_2.close()
result.close()

print('Finished')
