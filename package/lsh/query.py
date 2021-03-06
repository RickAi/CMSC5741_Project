import time
try:
    from package.lsh.lshash import *
    from package.lsh.constants import *
except:
    from lshash import *
    from constants import *
import json
import os
import face_recognition

lsh = LSHash(HASH_SIZE, INPUT_DIMS, num_hashtables=NUMS_TABLE, storage_config=STORAGE_CONFIG,
             matrices_filename=MATRICES_NAME)
sample_dir = SAMPLE_DIR
for file in os.listdir(sample_dir):
    start = time.time()
    face_image = face_recognition.load_image_file(os.path.join(sample_dir, file))
    encodings = face_recognition.face_encodings(face_image)
    if len(encodings):
        print("Start extract face image and query:%s" % file)
        # Extract face feature
        face_feature = encodings[0]
        # Query similar images from redis
        result = lsh.query(face_feature, num_results=5, distance_func="norm")

        # Print top similar images
        for rank, item in enumerate(result, start=1):
            img_info = json.loads(item[0])
            # img_feature = np.asarray(img_info[0])
            img_path = img_info[1]
            distance = item[1]
            print("Top #%d similar image:%s, The distance is:%f" % (rank, img_path, distance))
        print("Time cost:%s\n" % str(time.time() - start))
