# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 13:33:35 2021

@author: mizo_
"""

import concurrent.futures
from multiprocessing import cpu_count
import os
import csv
from PIL import Image
import numpy as np

cores = cpu_count()

def create_dir():
    for i in range(10):
        dir= os.path.join('images','resize','images', str(i))
        if not os.path.exists(dir):
            os.makedirs(dir)

def get_dim(image):
    """
    get the 4 bounderies of the digit
    """
    x=np.array(image)
    a=x.shape[0]
    flag1=True
    lr=[]
    for i in range(a):
        for j in range(a):
            if x[i][j]==0 and flag1:
                up= i
                flag1=False
            if x[i][j]==0:
                lw= i
                lr.append(j)
    lt= min(lr)
    rt= max(lr)
    
    return lt, up, rt, lw
        
def blackWhite(image):
    """
    removes greyscale pixels from a numpy array of pixels
    """
    x=np.array(image)
    a=x.shape[0]
    im=np.array([[255]*a]*a).astype(np.uint8)
    for i in range(a):
        for j in range(a):
            if x[i][j]< 250:
                im[i][j]= 0
            else:
                im[i][j]=255
                
    return im
    
    
def processImg(image, dir, dim=100):
    """
    image: is the target image object
    d: is the the dir to save the generated image
    """
    
    bw=image.convert('L') #convert to BW
    new_image= bw.resize((200,200)) #resize 

    # remove grey pixel
    x=blackWhite(new_image)
    lt, up, rt, lw= get_dim(x)

    y= Image.fromarray(x) #convert a numpy array to an image

    #max dimentions =150,150
    #calculate frame of num
    #dm=100
    dx= rt-lt
    dy= lw-up
    print(dx,dy)
    
    #if the image is smaller than the target dimensions
    #add white spaces to be cropped
    if dx<dim:
        xs= int((dim-dx)/2)
        lt = lt-xs
        rt= rt+xs

    if dy<dim: 
        ys= int((dim-dy)/2)
        up=up-ys
        lw=lw+ys

    box=(lt, up, rt, lw)
        
    cropped_image = y.crop(box)
    c= cropped_image.resize((100,100))
    c=blackWhite(c)
    c = Image.fromarray(c)
    print(c.size[0])
    c.save(dir)
    return c 



def get_images_path(L):
    nums=[]
    filenames=[]
    filepaths=[]
    for i in range(L):
        directory = f'images/{i}/'
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(filepath):
                filepaths.append(filepath)
                filenames.append(filename)
                nums.append(i)
    return filepaths, nums
    
def adjustImage(fp):
    #directory = f'images/{i}/'
    image=Image.open(fp)
    postdir = os.path.join('images','resize', fp)
    cropped=processImg(image, postdir)
    return fp, cropped

def targetNums(nums):
    numlist=[0]*L
    with open('y_train.csv', 'w', encoding='UTF8', newline='') as f:
        numwriter = csv.writer(f)
        #numwriter.writerow(header)
        for i in range(len(nums)):
            j= int(nums[i])
            numlist[j]=1
            numwriter.writerow(numlist)
            numlist=[0]*L
            
            
def run(fp, nums):
    targetNums(nums)
    with open('X_train.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        with concurrent.futures.ProcessPoolExecutor(max_workers=cores) as executor:
            futures = {executor.submit(adjustImage, i) for i in fp}
                        
                            
            for fut in concurrent.futures.as_completed(futures):
                fp, cropped = fut.result()
                a=np.array(cropped).astype(np.uint8)
                a=a.reshape(-1)
                a=a/255
                a=np.transpose(a, axes=None)
                writer.writerow(a)
                print(fp)
                








if __name__ == '__main__':
    L=10
    create_dir()
    fp, nums = get_images_path(L)
    run(fp, nums)