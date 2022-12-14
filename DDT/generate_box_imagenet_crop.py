import os
import sys
import cv2
import json
import numpy as np
import torch
import torchvision.transforms as transforms
from torch.backends import cudnn
from torch.autograd import Variable
import torch.nn as nn
import torchvision
import torchvision.models as models
from PIL import Image
from skimage import measure
# from scipy.misc import imresize
from utils.func import *
from utils.vis import *
from utils.IoU import *
import argparse
from loader.ddt_imagenet_dataset import DDTImageNetDataset


parser = argparse.ArgumentParser(description='Parameters for DDT generate box')
parser.add_argument('--input_size',default=448,dest='input_size')
parser.add_argument('--data',default="data/DDT_imgs",help='path to imagenet dataset')
parser.add_argument('--gpu',help='which gpu to use',default='0',dest='gpu')
parser.add_argument('--output_path',default='data/DDT_crop/',dest='output_path')
parser.add_argument('--batch_size',default=64,dest='batch_size')
args = parser.parse_args()
os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu
os.environ['OMP_NUM_THREADS'] = "10"
os.environ['MKL_NUM_THREADS'] = "10"
cudnn.benchmark = True
model_ft = models.vgg11_bn(pretrained=False)
model_ft.classifier=nn.Sequential(
        nn.Linear(512 * 7 * 7, 4096),
        nn.ReLU(True),
        nn.Dropout(),
        nn.Linear(4096, 4096),
        nn.ReLU(True),
        nn.Dropout(),
        nn.Linear(4096, 2),
    )


# create new OrderedDict that does not contain `module.`
model_ft.load_state_dict(torch.load("./checkpoint.pth.tar")['state_dict'])
model = model_ft.features

model = torch.nn.DataParallel(model).cuda()
model.eval()
projdir = args.output_path
if not os.path.exists(projdir):
    os.makedirs(projdir)

transform = transforms.Compose([
    transforms.Resize((args.input_size,args.input_size)),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
])
batch_size = args.batch_size
a = DDTImageNetDataset(root=args.data,batch_size=args.batch_size, transforms=transform)

# print(classes[0])

for class_ind in range(3):
    #if class_ind == 10:
    #    import sys
    #    sys.exit()
    now_class_dict = {}
    feature_list = []
    ddt_bbox = {}
    with torch.no_grad():
        from tqdm import tqdm
        for (input_img,path) in tqdm(a[class_ind]):
            input_img = to_variable(input_img)
            output = model(input_img)
            output = to_data(output)
            output = torch.squeeze(output).numpy()
            if len(output.shape) == 3:
                output = np.expand_dims(output,0)
            output = np.transpose(output,(0,2,3,1))
            n,h,w,c = output.shape
            for i in range(n):
                now_class_dict[path[i]] = output[i,:,:,:]
            output = np.reshape(output,(n*h*w,c))
            feature_list.append(output)
        X = np.concatenate(feature_list,axis=0)
        print ("Before Mean")
        mean_matrix = np.mean(X, 0)
        print ("AFTER Mean")
        X = X - mean_matrix
        print("Before PCA")
        trans_matrix = sk_pca(X, 1)
        print("AFTER PCA")
        cls = a.label_class_dict[class_ind]
        # save json
        d = {'mean_matrix': mean_matrix.tolist(), 'trans_matrix': trans_matrix.tolist()}
        with open(os.path.join(projdir, '%s_trans.json' % cls), 'w') as f:
            json.dump(d, f)
        # load json
        with open(os.path.join(projdir, '%s_trans.json' % cls), 'r') as f:
            t = json.load(f)
            mean_matrix = np.array(t['mean_matrix'])
            trans_matrix = np.array(t['trans_matrix'])

        print('trans_matrix shape is {}'.format(trans_matrix.shape))
        cnt = 0
        for k,v in tqdm(now_class_dict.items()):
            w = 14
            h = 14
            he = 448
            wi = 448
            v = np.reshape(v,(h * w,512))
            v = v - mean_matrix

            heatmap = np.dot(v, trans_matrix.T)
            heatmap = np.reshape(heatmap, (h, w))
            highlight = np.zeros(heatmap.shape)
            highlight[heatmap > 0] = 1
            # max component
            all_labels = measure.label(highlight)
            highlight = np.zeros(highlight.shape)
            highlight[all_labels == count_max(all_labels.tolist())] = 1

            # visualize heatmap
            # show highlight in origin image
            highlight = np.round(highlight * 255)
            highlight_big = cv2.resize(highlight, (he, wi), interpolation=cv2.INTER_NEAREST)
            props = measure.regionprops(highlight_big.astype(int))

            if len(props) == 0:
                #print(highlight)
                bbox = [0, 0, wi, he]
            else:
                temp = props[0]['bbox']
                bbox = [temp[1], temp[0], temp[3], temp[2]]

            temp_bbox = [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]]
            temp_save_box = [x / 448 for x in temp_bbox]
            ddt_bbox[os.path.join(cls, k)] = temp_save_box

            highlight_big = np.expand_dims(np.asarray(highlight_big), 2)
            highlight_3 = np.concatenate((np.zeros((he, wi, 1)), np.zeros((he, wi, 1))), axis=2)
            highlight_3 = np.concatenate((highlight_3, highlight_big), axis=2)
            cnt +=1
            if 1:
                if "train" in cls:
                    cls = "train"
                savepath = args.output_path+'%s' % cls
                if not os.path.exists(savepath):
                    os.makedirs(savepath)
                from PIL import Image
                raw_img = Image.open(k).convert("RGB")
                raw_img = np.asarray(raw_img)
                raw_img = raw_img[int(temp_bbox[1]/448*raw_img.shape[0]):int((temp_bbox[3] + temp_bbox[1])/448*raw_img.shape[0]),int(temp_bbox[0]/448*raw_img.shape[1]):int((temp_bbox[2] + temp_bbox[0])/448*raw_img.shape[1])]
                raw_img = cv2.cvtColor(raw_img,cv2.COLOR_BGR2RGB)
                save_name = k.split('/')[-1]
                cv2.imwrite(os.path.join(savepath, save_name), np.asarray(raw_img))