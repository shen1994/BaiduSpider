# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 10:00:44 2018

@author: shenxinfeng
"""

import os
from PIL import Image
import imghdr
import numpy as np

train_file_path = './train_image/'
test_file_path = './test_image/'
                
def image_filter(path, is_print):

    for file_name in os.listdir(path):
        file_len = len(file_name)
        new_path = path + file_name

        if not cmp(file_name[file_len - 4:file_len], '.jpg'): 
            print new_path           
            if imghdr.what(new_path):
                image = Image.open(new_path)
                
                if not cmp(image.mode, 'RGB'):
                    image.save(new_path)
                else:
                    if is_print: print new_path
                    image.close()
                    os.remove(new_path)
                    
            else:
                if is_print: print new_path
                os.remove(new_path)
        else:
            if is_print: print new_path
            os.remove(new_path)
            
def all_image_filter(file_path):
    files_path_tmp = []
    for root, dirs, files in os.walk(file_path):
        files_path_tmp.append(dirs)
        break
    files_path = files_path_tmp[0]
   
    new_files_path = []
    for index in np.arange(0, len(files_path), 1):
        new_files_path_str = file_path + files_path[index] + '/'
        new_files_path.append(new_files_path_str)

    count = 0
    for index in np.arange(0, len(new_files_path), 1):
        image_filter(new_files_path[index], 1)
        count += 1
        print u'类别---' + str(count) + '---OK'
    
    
if __name__ == "__main__":
    print 'filter start!!!'
    all_image_filter(train_file_path)
    # all_image_filter(test_file_path)
    print 'filter over!!!'
