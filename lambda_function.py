import json 
import boto3 
import base64

endpoint_name = 'image-classification-03'

sagemaker_runtime_client=boto3.client('runtime.sagemaker')
 
def lambda_handler(event,context):
    print(event)
    image=base64.b64decode(event['image'])
    print(image)
    return _predictPneumonia(image)
 
def _predictPneumonia(image):
    response=sagemaker_runtime_client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="application/x-image",
        Body=image)
    result=response['Body'].read()
    result=json.loads(result)
    print("result",result)
    predicted_class=0 if result[0]>result[1] else 1
    toSend=result[0] if result[0]>result[1] else result[1]
 
    if predicted_class==0:
        return f"NO pneumonia with a probability of : {toSend}"
    else:
        return f"pneumonia with a probability of : {toSend}"

    