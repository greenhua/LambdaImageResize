import json
import re
#import datetime
import boto3
from PIL import Image
import os
import base64
from io import BytesIO



def lambda_handler(event, context):
    resource = boto3.resource('s3')
    bucket = resource.Bucket('buydo-images')

    path = event['path']
    
    # path = "/images/crop/200/46/04/28/460428d8b81f36a641f75d656dc4efc7.jpg"
    # path = "/images/resize/400/4a/45/87/4a45872e111aa429b3cf08a3b0205440.jpg"
    fname = os.path.basename(path)
    content_type = "image/png"
    if re.match(r".+jpg", fname)  or re.match(r".+jpeg", fname):
        content_type = "image/jpeg"

    response = {
        "statusCode": 200,
        "statusDescription": "200 OK",
        "isBase64Encoded": True,
        "headers": {
            "Content-Type": content_type,
            "Access-Control-Allow-Origin": "*"
        }
    }

    if re.match(r".+resize", path):
        fname = os.path.basename(path)
        path_detail = re.findall(r'(.+)(resize|crop)/(.+?)/(.+)', path)
        size = int(path_detail[0][2])
        path = path_detail[0][0] + "default/" + path_detail[0][3]
        image_object = bucket.Object("data" + path)
        im1 = Image.open(BytesIO(image_object.get()['Body'].read()))
        (width, height) = im1.size
        new_height = int(size*height/width)
        new_width = size
        im1 = im1.resize((new_width, new_height), Image.ANTIALIAS)
        im1.save("/tmp/" + fname)
        f = open("/tmp/" +fname,"rb")
        string = f.read()
        os.remove("/tmp/" + fname)
        response['body'] = base64.b64encode(string).decode("utf-8")
    elif re.match(r".+crop", path):
        fname = os.path.basename(path)
        path_detail = re.findall(r'(.+)(resize|crop)/(.+?)/(.+)', path)
        size = int(path_detail[0][2])
        path = path_detail[0][0] + "default/" + path_detail[0][3]
        image_object = bucket.Object("data" + path)
        im1 = Image.open(BytesIO(image_object.get()['Body'].read()))
        (width, height) = im1.size
        if (width<height):
            new_height = int(size*height/width)
            new_width = size
        elif (width>height):
            new_width = int(size*width/height)
            new_height =  size
        else:
            new_width = size
            new_height =  size

        im1 = im1.resize((new_width, new_height), Image.ANTIALIAS)
        left_top =  int(new_width/2 - size/2)
        left_bottom = int(new_height/2 - size/2)
        right_top = left_top + size
        right_bottom = left_bottom + size
        im1 = im1.crop((left_top, left_bottom, right_top, right_bottom))
        im1.save("/tmp/" + fname)
        # im1.save(fname)

        f = open("/tmp/" +fname,"rb")
        string = f.read()
        os.remove("/tmp/" + fname)
        response['body'] = base64.b64encode(string).decode("utf-8")
    else:
        print("path=data" + path)
        image_object = bucket.Object("data" + path)
        string = image_object.get()['Body'].read()
        response['body'] = base64.b64encode(string).decode("utf-8")

    #response['body'] = json.dumps(event['path'])
#    print(response)
    return response


# lambda_handler('event', 'context')
