import boto3
import cv2
import numpy as np

def readImg(s3, bucket_name, Img, typeI = "p"):
    content = s3.get_object(Bucket=bucket_name, Key=Img)
    content = content["Body"].read()
    content = np.fromstring(content, np.uint8)
    if typeI =="p":
        content = cv2.imdecode(content, cv2.IMREAD_COLOR)/255.0
    else:
        content = cv2.imdecode(content, cv2.IMREAD_UNCHANGED)/255.0
    return content

def readLocal(img):
    return cv2.imread(img, cv2.IMREAD_COLOR)/ 255.0

def generateScri(imgR, layer):
    #imgRA = cv2.cvtColor(imgR, cv2.COLOR_RGB2RGBA)
    print('imgR: '+ str(imgR.shape))
    print('layer: '+ str(layer.shape))
    mapp = np.where(layer[:,:,3] == 0, 1,0).reshape(480,640,1)
    mappImg = np.concatenate([mapp,mapp,mapp,mapp],axis=2)
    imgRA = np.multiply(mappImg,imgR)

    imgAdd = imgRA+layer
    imgAdd = imgAdd[:,:,:-1]
    print('mapp: '+str(mapp.shape))
    print('imgAdd: '+str(imgAdd.shape))
    #imgAdd = cv2.cvtColor(imgAdd, cv2.COLOR_RGBA2RGB)
    #print('output: '+str(imgAdd[:,:,:-1].shape))
    return imgAdd#[:,:,:-1]

def readInput(s3, bucket_name,token):
    #s3 = boto3.client("s3")
    #image = readImg(s3, bucket_name, f'people_{token}.png')
    #image = readImg(s3, bucket_name, f'uploads/img_{token}.png')
    imageR = readImg(s3, bucket_name, f'uploads/img_{token}.png',typeI='s')
    #scribbles = readImg(s3, bucket_name, f'scribbles_{token}.png')
    #scribbles = readImg(s3, bucket_name, 'uploads/added.png')
    layer = readImg(s3, bucket_name, 'trans1.png',typeI='l')
    scribbles = generateScri(imageR, layer)
    return scribbles