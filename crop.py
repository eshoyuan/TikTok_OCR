import cv2
import os
import numpy as np
from tqdm import tqdm
file_path = ["./data/test_set_random/","./data/train_set_random/"]
def crop(img):
    # According to our prior knowledge, the tictok id is in either top or bottom part in a image.
    if img.shape[1] > img.shape[0]: # if the image.rows > image.cols
        crop10 = img[:int(img.shape[0]/5),:int(img.shape[1]/5*2)] # The tictok id is not in the middle part.
        crop11 = img[:int(img.shape[0]/5),int(img.shape[1]/5*3):]
        crop1 = np.concatenate((crop10,crop11),axis=1)
        crop20 = img[int(img.shape[0]/5*4):,:int(img.shape[1]/5*2)]
        crop21 = img[int(img.shape[0]/5*4):,int(img.shape[1]/5*3):]
        crop2 = np.concatenate((crop20,crop21),axis=1)
    else:
        crop1 = img[:int(img.shape[0]/10),:]
        crop2 = img[int(img.shape[0]/10*9):int(img.shape[0]/10*10),:]
    return np.concatenate((crop1,crop2))
def crop_list(file_path):
    files = os.listdir(file_path)
    for file in tqdm(files):
        img = cv2.imread(file_path+file)
        if "train" in file_path:
            img_low = cv2.resize(img,(int(img.shape[1]/1.7),int(img.shape[0]/1.7)))
            img_high = img
            img_low = crop(img_low)
            img_high = crop(img_high)
        # os.mkdir("/usr/yyx/data/test_crop_new/")
            if os.path.exists("./data/train_crop_low/")==False:
                os.mkdir("./data/train_crop_low/")
            if os.path.exists("./data/train_crop_high/")==False:
                os.mkdir("./data/train_crop_high/")
            cv2.imwrite("./data/train_crop_low/"+file,img_low)
            cv2.imwrite("./data/train_crop_high/"+file,img_high)
        else:
            img = crop(img)
            if os.path.exists("./data/test_crop/")==False:
                os.mkdir("./data/test_crop/")
            cv2.imwrite("./data/test_crop/"+file,img)
for i in file_path:
    crop_list(i)