# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 14:50:05 2021

@author: mizo_
"""

import os
from PIL import Image
import numpy as np
import csv
from impreproc5 import processImg

# image =Image.open('test/test.png')
# z='test/resize/testresize.png'
# c=processImg(image,z)

c=0
    
directory = f'test/done'
z='test/resize/testresize.png'
result = []
with open('testcsv3.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)    
        for filename in os.listdir(directory):
            fn = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(fn):
                print(c, fn)
            
                image=Image.open(fn)
                image=processImg(image,z)
                a=np.array(image).astype(np.uint8)
                a= a.flatten()
                #print(a)
                a=a/255
                print(a.shape)
                #a=np.transpose(a, axes=None)
                writer.writerow(a)
                result.append(fn)
                c+=1
print(result)