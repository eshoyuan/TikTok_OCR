python crop.py
python create_classification_dataset.py
python classification_vgg.py
python create_DDT_dataset.py
python DDT/generate_box_imagenet_crop.py
python tools/train.py -c svtr_large_train_stn.yml # Distributed Training: python -m paddle.distributed.launch --gpus '0,1,2,3' -c svtr_large_train_stn.yml
python tools/infer_rec.py -c svtr_large_train_stn.yml -o Global.pretrained_model=svtr_large_stn/best_accuracy