import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'


#python train.py --img 96 --batch 32 --epochs 5 --data data/coco128.yaml --cfg models/yolov5s.yaml --weights  weights/yolov5s.pt