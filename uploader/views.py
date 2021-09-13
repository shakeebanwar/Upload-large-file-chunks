from django.shortcuts import render
from django.http import JsonResponse
import os
from .models import File
from django.conf import settings
import boto3

AWS_S3_CREDS = {
        "aws_access_key_id":settings.AWS_ACCESS_KEY_ID,
        "aws_secret_access_key":settings.AWS_SECRET_ACCESS_KEY
}
s3 = boto3.client('s3',**AWS_S3_CREDS)



def upload_file(file_name, bucket, object_name=None):


    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True



def check(request):
    AWS_S3_CREDS = {
        "aws_access_key_id":settings.AWS_ACCESS_KEY_ID,
        "aws_secret_access_key":settings.AWS_SECRET_ACCESS_KEY
    }
    s3 = boto3.client('s3',**AWS_S3_CREDS)
  

    with open("media/hye.txt", "rb") as f:
        s3.upload_fileobj(f, settings.AWS_STORAGE_BUCKET_NAME, 'hye.txt')
    
    return JsonResponse({'data':'Invalid Request'})



def index(request):
    if request.method == 'POST':


        file = request.FILES['file'].read()
        fileName= request.POST['filename']
        existingPath = request.POST['existingPath']
        end = request.POST['end']
        nextSlice = request.POST['nextSlice']
        
        if file=="" or fileName=="" or existingPath=="" or end=="" or nextSlice=="":
            res = JsonResponse({'data':'Invalid Request'})
            return res
        else:
            if existingPath == 'null':
                path = 'media/' + fileName
                with open(path, 'wb+') as destination: 
                    destination.write(file)
                    



                FileFolder = File()
                FileFolder.existingPath = fileName
                FileFolder.eof = end
                FileFolder.name = fileName
                FileFolder.save()
                if int(end):
                    res = JsonResponse({'data':'Uploaded Successfully','existingPath': fileName})
                else:
                    res = JsonResponse({'existingPath': fileName})
                return res

            else:
                path = 'media/' + existingPath
                model_id = File.objects.get(existingPath=existingPath)
                if model_id.name == fileName:
                    if not model_id.eof:
                        with open(path, 'ab+') as destination: 
                            destination.write(file)
                        if int(end):
                            model_id.eof = int(end)
                            model_id.save()
                            res = JsonResponse({'data':'Uploaded Successfully','existingPath':model_id.existingPath})
                        else:
                            res = JsonResponse({'existingPath':model_id.existingPath})    
                        return res
                    else:
                        res = JsonResponse({'data':'EOF found. Invalid request'})
                        return res
                else:
                    res = JsonResponse({'data':'No such file exists in the existingPath'})
                    return res
    return render(request, 'upload.html')








    


