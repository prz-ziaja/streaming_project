wget https://drive.google.com/file/d/1YkOsz9JxGtHRxkqoNqnBAqftILKWDA4j/view\?usp\=sharing
mv 'view?usp=sharing' car_recognizer/app/model-weights-spectrico-mmr-mobilenet-128x128-344FF72B.pb

wget https://drive.google.com/file/d/1F863SjOpad2_qEXOkyWPyXCyEQZfQmdt/view?usp=sharing
mv 'view?usp=sharing' car_recognizer/app/yolov3.weights

docker network create my_network
docker-compose up -d
