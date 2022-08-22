import cv2
import os
from isort import file
import numpy as np
import random
from tqdm import tqdm
def crop(img, has_id = True):
    """
    has_id: If the cropped image has tiktok id.
    """
    if has_id == True:
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
    else:
        if img.shape[1] > img.shape[0]: # if the image.rows > image.cols
            x1 = random.randint(1,3)
            x2 = random.randint(1,3)
            crop10 = img[int(img.shape[0]/5*(x1)):int(img.shape[0]/5*(x1+1)),:int(img.shape[1]/5*2)] # The tictok id is not in the middle part.
            crop11 = img[int(img.shape[0]/5*(x1)):int(img.shape[0]/5*(x1+1)),int(img.shape[1]/5*3):]
            crop1 = np.concatenate((crop10,crop11),axis=1)
            crop20 = img[int(img.shape[0]/5*(x2)):int(img.shape[0]/5*(x2+1)),:int(img.shape[1]/5*2)]
            crop21 = img[int(img.shape[0]/5*(x2)):int(img.shape[0]/5*(x2+1)),int(img.shape[1]/5*3):]
            crop2 = np.concatenate((crop20,crop21),axis=1)
        else:
            x1 = random.randint(2,7)
            x2 = random.randint(2,7)

            crop1 = img[int(img.shape[0]/10*x1):int(img.shape[0]/10*(x1+1)),:]
            crop2 = img[int(img.shape[0]/10*x2):int(img.shape[0]/10*(x2+1)),:]
            if random.randint(1,8)<=2:
                crop1 = np.zeros_like(crop1)
            if random.randint(1,8)<=2:
                crop2 = np.zeros_like(crop2)
            img = np.concatenate((crop1,crop2))
        return np.concatenate((crop1,crop2))

def create_classification_dataset(files):
    # Create Imagenet like dataset to train if there is a tiktok id in a image.
    for file in tqdm(files):
        img = cv2.imread(file)
        if "train" in file_path:
            img = cv2.resize(img,(int(img.shape[1]/1.7),int(img.shape[0]/1.7)))
        file = file.split("/")[-1]
        for has_id in [False,True]:
            if has_id == 1:
                img_has_id = crop(img,has_id)
                if os.path.exists("./data/classification/has_id")==False:
                    os.mkdir("./data/classification/has_id")
                cv2.imwrite("./data/classification/has_id/"+file,img_has_id)
            else:
                img_no_id = crop(img,has_id)
                if os.path.exists("./data/classification/no_id")==False:
                    os.mkdir("./data/classification/no_id")
                cv2.imwrite("./data/classification/no_id/"+file,img_no_id)

import random
file_path = ["./data/test_set_random/","./data/train_set_random/"]
# Random choose 20000 images to create the dataset.
files_train = random.sample(os.listdir(file_path[1]),10000)
files_train = [file_path[1]+i for i in files_train]
files_test = random.sample(os.listdir(file_path[0]),10000)
files_test = [file_path[0]+i for i in files_test]
files = files_train+files_test

if os.path.exists("./data/classification/")==False:
    os.mkdir("./data/classification/")
create_classification_dataset(files)