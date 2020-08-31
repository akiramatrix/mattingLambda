import boto3
from readImg import readInput, readLocal
from solve_foreground_background import solve_foreground_background
from closed_form_matting import *
import cv2

def lambda_handler(event, context):
    print(event['queryStringParameters']['token'])
    #print(event)
    s3 = boto3.client("s3")
    bucket_name = 'layer-opencv-test-akira'
    peopleImg, scriImg = readInput(s3, bucket_name,event['queryStringParameters']['token'])
    alpha = closed_form_matting_with_scribbles(peopleImg, scriImg)
    foreground= solve_foreground_background(peopleImg, alpha)
    output = np.concatenate((foreground, alpha[:, :, np.newaxis]), axis=2)
    cv2.imwrite('/tmp/output.png', output * 255.0)
    s3.put_object(Bucket=bucket_name, 
                Key=f"output/output_{event['queryStringParameters']['token']}.png", Body=open("/tmp/output.png", "rb").read())
    #return {"message":"successfully matted"}