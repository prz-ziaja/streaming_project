from time import sleep
from json import dumps
from kafka import KafkaProducer
import face_recognition
import pickle
print('test')
producer = KafkaProducer(
    bootstrap_servers=['kafka:9093']
)
for j in range(10):
    print("Iteration", j)
    image = face_recognition.load_image_file('Jakto.jpg')
    producer.send('topic_test', pickle.dumps(image))
    sleep(2)
