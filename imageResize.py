import json
import re
#import datetime
import boto3
from PIL import Image
import os
import base64


def lambda_handler(event, context):
#    print('hello')
    client = boto3.client('s3')
    response = {
        "statusCode": 200,
        "statusDescription": "200 OK",
        "isBase64Encoded": True,
        "headers": {
            "Content-Type": "image/png"
        }
    }
    path = event['path']
    # path = "/images/resize/200/a7/d0/06/a7d0064e236700045007704b4a1b8632.jpg"
    fname = os.path.basename(path)
    if re.match(r".+resize", path):
        path_detail = re.findall(r'(.+)resize/(.+?)/(.+)', path)
        size = int(path_detail[0][1])
        path = path_detail[0][0] + "default/" + path_detail[0][2]
        client.download_file("s3bucket", "data"+path, "/tmp/" + fname)
        im1 = Image.open(r"/tmp/" + fname)
        im1 = im1.resize((size, size))
        im1.save("/tmp/" + fname)
        f = open("/tmp/" +fname,"rb")
        string = f.read()
        print(string)
        os.remove("/tmp/" + fname)
        response['body'] = base64.b64encode(string).decode("utf-8")

    else:
        client.download_file("buydo-images", "data"+path, "/tmp/"+fname)
        f = open("/tmp/" +fname,"rb")
        string = f.read()
        os.remove("/tmp/"+fname)
        response['body'] = base64.b64encode(string).decode("utf-8")

    #response['body'] = json.dumps(event['path'])
#    print(response)
    return response

# lambda_handler('event', 'context')
