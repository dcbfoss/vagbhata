import numpy as np
import cv2, os

def get_pixel(value: int):
    if value==1:return [255,0,0]
    elif value==0:return [0,255,0]
    else:return [0,0,255]


def prepare_image(data: list, scale: int= 400):
    output = np.zeros((scale,scale,3), dtype=np.int32)
    diff = 10;row_slide = 10; column_slide = 10
    for row in data:
        for column in row:
            curr_pixel = get_pixel(column)
            output[(row_slide-diff):row_slide, (column_slide-diff):column_slide] = curr_pixel
            column_slide = column_slide + diff
        row_slide = row_slide+diff; column_slide = 10
    return output


def draw_png(filename: str, data: list):
    if not os.path.exists('images'):os.makedirs('images')
    cv2.imwrite('images/'+filename+'.png', data)

