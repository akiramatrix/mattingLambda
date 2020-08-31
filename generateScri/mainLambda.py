import boto3
from readImg import readInput, readLocal
import cv2
import json

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    client = boto3.client("lambda")
    bucket_name = 'layer-opencv-test-akira'
    scriImg = readInput(s3, bucket_name,event['queryStringParameters']['token'])
    cv2.imwrite('/tmp/scrib.png', scriImg * 255.0)
    s3.put_object(Bucket=bucket_name, 
                Key=f"uploads/scrib_{event['queryStringParameters']['token']}.png", Body=open("/tmp/scrib.png", "rb").read())
    #invoke solveAlpha
    inputParams = {
        "token": event['queryStringParameters']['token']
    }
    response = client.invoke(
        FunctionName = 'arn:aws:lambda:us-east-2:876878303547:function:solveAlpha',
        InvocationType='RequestResponse',
        Payload = json.dumps(inputParams)
    )
    print('successfully matted')
    message = {
   'message': 'Execution started successfully!'
    }
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(message)
    }
    #return {"message":"successlly matted"}