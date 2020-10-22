from PIL import Image
import face_recognition
from kafka import KafkaConsumer
from json import loads
import pickle
#import os
#import cv2

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


print('test')
def image_search(img):
    # Wczytuje obraz
    

    # Znajduje wszystkie twarze, sa zapisane w formacie wspolrzednych (gora,prawo,dol,lewo)
    face_locations = face_recognition.face_locations(image)

    print("I found {} face(s) in this photograph.".format(len(face_locations)))
    print(face_locations)
    
    return face_locations

consumer = KafkaConsumer(
    'topic_test',
    bootstrap_servers=['kafka:9093'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-id'
)
i = 0
for event in consumer:
    i +=1
    data = event.value
    image = pickle.loads(data)
    image_search(image)
    if i > 6 :
        break

