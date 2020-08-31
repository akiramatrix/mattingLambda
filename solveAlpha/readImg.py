import boto3
import cv2
import numpy as np

def readImg(s3, bucket_name, Img, typeI = "p"):
    content = s3.get_object(Bucket=bucket_name, Key=Img)
    content = content["Body"].read()
    content = np.fromstring(content, np.uint8)
    content = cv2.imdecode(content, cv2.IMREAD_COLOR)/255.0
    return content

def readInput(s3, bucket_name,token):
    image = readImg(s3, bucket_name, f'uploads/img_{token}.png')
    scribbles = readImg(s3, bucket_name, f'uploads/scrib_{token}.png')
    return image, scribbles