from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import os
import face_recognition
import numpy as np
from package.lsh.lshash import *
from package.lsh.constants import *
import pdb

def index(request):
    return render(request, 'index.html')

def upload(request):
    if request.method=="GET":
        return  render(request,'index.html')
    elif request.method == "POST":
        img_obj = request.FILES.get('img')
        # save images
        with open(os.path.join('static/data/images', img_obj.name), 'wb') as f:
            for chunk in img_obj.chunks(chunk_size=1024):
                f.write(chunk)
        #exract
        feature_path = extract(img_obj.name)
        if feature_path:
            res = {"status": "success"}
            query_results = query(feature_path)
            res['query_results'] = query_results
        else:
            res = {"status": "fail"}
        return JsonResponse(res)

def query(feature_path):
    feature = np.loadtxt(feature_path)
    lsh = LSHash(HASH_SIZE, INPUT_DIMS, num_hashtables=NUMS_TABLE, storage_config=STORAGE_CONFIG,
             matrices_filename=MATRICES_NAME)
    result = lsh.query(feature, num_results=5, distance_func="norm")
    # Print Top Similar Images
    images_info = []
    for rank, item in enumerate(result, start=1):
        img_info = json.loads(item[0])
        # absolute path, remove '.txt' at end
        img_path = '/static/data/images/{0}'.format(img_info[1].rstrip('.txt'))
        distance = item[1]
        images_info.append({'path': img_path, 'distance': distance, 'rank':rank})
    print(images_info)
    return images_info

def extract(image_name):
    cwd = os.getcwd() # CMSC5741_Project/website
    img_directory_path = os.path.join(cwd, "static/data/images") # CMSC5741_Project/website/static/data/images
    image_path = os.path.join(img_directory_path, image_name)
    image = face_recognition.load_image_file(image_path)  # load image
    features = face_recognition.face_encodings(image)
    if features:
        feature = features[0]
        feature_path = cwd+'/static/data/feature/{0}.txt'.format(image_name)
        np.savetxt(feature_path, feature, fmt='%f')
        return feature_path
    else:
        return False