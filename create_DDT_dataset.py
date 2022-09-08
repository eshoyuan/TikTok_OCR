import os
import shutil
from tqdm import tqdm
import _thread

# Memory can't process all the data at once, so we divide the data into three part.
file_lists = os.listdir("data/train_crop_low/")
if os.path.exists("data/DDT_imgs")==False:
    os.mkdir("data/DDT_imgs")
def func1():
    for i in tqdm(file_lists[:40000]):
        if os.path.exists("data/DDT_imgs/train1")==False:
            os.mkdir("data/DDT_imgs/train1")
        shutil.copyfile("data/train_crop_low/"+i,"data/DDT_imgs/train1/"+i)
    print("Done1")
def func2():
    for i in tqdm(file_lists[40000:]):
        if os.path.exists("data/DDT_imgs/train2")==False:
            os.mkdir("data/DDT_imgs/train2")
        shutil.copyfile("data/train_crop_low/"+i,"data/DDT_imgs/train2/"+i)
    print("Done2")
def func3():
    for i in tqdm(os.listdir("data/test_crop")):
        if os.path.exists("data/DDT_imgs/test")==False:
            os.mkdir("data/DDT_imgs/test")
        shutil.copyfile("data/test_crop/"+i,"data/DDT_imgs/test/"+i)
    print("Done3")
func1()
func2()
func3()