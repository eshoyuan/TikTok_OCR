python3 crop.py
python3 create_classification_dataset.py
python3 classification_vgg.py
python3 create_PSOL_dataset.py
python3 PSOL/generate_box_imagenet_crop.py
python3 tools/train.py -c svtr_large_train_stn.yml # Distributed Training: python -m paddle.distributed.launch --gpus '0,1,2,3' -c svtr_large_train_stn.yml
python3 tools/train.py -c svtr_large_train_stn.yml -o Global.pretrained_model=svtr_large_stn/best_accuracy