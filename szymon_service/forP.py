from PIL import Image
import face_recognition
#import os
#import cv2

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


atki = "Jakto.jpg"

def image_search(img):
    # Wczytuje obraz
    image = face_recognition.load_image_file(img)

    # Znajduje wszystkie twarze, sa zapisane w formacie wspolrzednych (gora,prawo,dol,lewo)
    face_locations = face_recognition.face_locations(image)

    print("I found {} face(s) in this photograph.".format(len(face_locations)))
    
    return face_locations
