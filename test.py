import re
import cv2
import json
import pytesseract
import numpy
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

img_list = list()
img_list.extend(['images/1.jpg', 'images/2.jpg', 'images/3.jpg', 'images/4.jpg'])
our_dict={}
our_dict['images']=[]
for img in img_list:
    image = cv2.imread(img)
    mask = numpy.zeros(image.shape[:2], dtype='uint8')

    height = mask.shape[0]
    width = mask.shape[1]
    width_order = int(mask.shape[1] * 0.33)
    height_order1 = int(mask.shape[0] * 0.22)
    height_order2 = int(mask.shape[0] * 0.32)

    rectangle0 = cv2.rectangle(mask.copy(), (0, height_order1), (width_order, height_order2), (255, 255, 255), -1)

    rectangle = cv2.rectangle(mask.copy(), (0, 0), (width_order, height), (255, 255, 255), -1)

    rec = cv2.bitwise_xor(rectangle, rectangle0)

    image1 = cv2.bitwise_and(image, image, mask=rec)
    #plt.imshow(image1)
    #plt.show()
    custom_config = r'--oem 1 --psm 6'
    text1 = pytesseract.image_to_string(image1, lang='rus', config=custom_config)

    print('#' * 50, '\n', text1)

    #############################################################################################
    rectangle0 = cv2.rectangle(mask.copy(), (width_order, height_order1), (width, height_order2), (255, 255, 255), -1)

    rectangle = cv2.rectangle(mask.copy(), (width_order, 0), (width, height), (255, 255, 255), -1)

    rec = cv2.bitwise_xor(rectangle, rectangle0)

    image2 = cv2.bitwise_and(image, image, mask=rec)
    #plt.imshow(image2)
    #plt.show()
    custom_config = r'--oem 3 --psm 6'
    text2 = pytesseract.image_to_string(image2, lang='rus', config=custom_config)
    print('#' * 50, '\n', text2)
    text1 = re.sub('\|', '', text1)
    text1 = re.sub('\[', '', text1)
    text1 = re.sub('\]', '', text1)
    text1 = re.sub('\n\n', '\n', text1)
    text1 = re.sub('\x0c', '', text1)
    text2 = re.sub('\n\n', '\n', text2)
    text2 = re.sub('\x0c', '', text2)
    variable = 0
    list_for_dict = []
    list_for_key = []
    list_for_value = []
    for el in list(text1):
         if el != '\n':
             list_for_dict.append(el)
         elif el == '\n':
             if variable == 3:
                 variable += 1
             elif variable != 3:
                 text =''.join(list_for_dict)
                 list_for_dict.clear()
                 list_for_key.append(text)
                 variable += 1
    variable = 0
    for el in list(text2):
        if el != '\n':
            list_for_dict.append(el)
        elif el == '\n':
            if variable == 0 or (variable == 2 and img != 'images/4.jpg'):
                variable += 1
            else:
                text = ''.join(list_for_dict)
                list_for_dict.clear()
                list_for_value.append(text)
                variable += 1

    print(list_for_key)
    print(list_for_value)
    print(len(list_for_key))
    print(len(list_for_value))
    test_dict = {}
    for i in range(0, len(list_for_key)):
        if i < len(list_for_value):
            test_dict[list_for_key[i]] = list_for_value[i]
            print(list_for_key[i], ' = ', list_for_value[i])
        else:
            test_dict[list_for_key[i]] = ""
            print(list_for_key[i], ' = ',"NO")
    our_dict['images'].append(test_dict)
    print(our_dict['images'])

with open('data.txt', 'w', encoding='UTF-8') as outfile:
        json.dump(our_dict, outfile, ensure_ascii=False)

