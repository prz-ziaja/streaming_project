import unittest
import sys
import cv2
import os

my_path = os.path.dirname(os.path.realpath(__file__))
path_to_streaming_project = os.path.dirname(my_path)
sys.path.append(path_to_streaming_project)
sys.path.append(os.path.join(path_to_streaming_project,'car_recognizer','app'))

from car_recognizer.app.car_rec import *

#from car-rec.app.car_rec import car_rec

img_1 = os.path.join(my_path,"104.jpeg")
img_2 = os.path.join(my_path,"103.jpeg")
img_3 = os.path.join(my_path,"101.jpeg")
image1 = cv2.imread(img_1)
image2 = cv2.imread(img_2)
image3 = cv2.imread(img_3)

class MyTest(unittest.TestCase):

    def testing_single_car(self):
        self.assertEqual(car_rec(image1), [[63, 89, 395, 197, 'car', 'Koenigsegg', 'Regera']])

    def testing_single_car_confidence(self):
        self.assertEqual(car_rec(image1, 0.8), [[63, 89, 395, 197, 'car', 'Koenigsegg', 'Regera']])

    def testing_single_car_confidence_and_threshold(self):
        self.assertEqual(car_rec(image1, 0.8), [[63, 89, 395, 197, 'car', 'Koenigsegg', 'Regera']])

    def testing_multiple_cars(self):
        self.assertEqual(car_rec(image2), [[1035, 460, 158, 115, 'car', 'Honda', 'Civic'], [195, 438, 156, 142, 'car', 'Honda', 'CR-V'], [721, 486, 210, 180, 'car', 'Toyota', 'Sequoia'], [514, 365, 141, 98, 'car', 'Subaru', 'Impreza'], [-1, 438, 111, 108, 'car', 'Ford', 'Mustang'], [229, 381, 158, 105, 'car', 'Chevrolet', 'Camaro'], [287, 594, 203, 74, 'car', 'Porsche', 'Cayenne'], [462, 477, 169, 155, 'car', 'Dodge', 'Dakota'], [1086, 196, 81, 54, 'car', 'Ford', 'Mustang'], [860, 198, 76, 48, 'car', 'Honda', 'Civic'], [0, 359, 131, 113, 'car', 'Mini', 'Cooper'],
                                           [552, 289, 86, 50, 'car', 'Ford', 'Mustang'], [299, 315, 126, 77, 'car', 'Ford', 'Mustang'], [809, 105, 69, 39, 'car', 'Jeep', 'Wrangler'], [385, 254, 91, 68, 'car', 'BMW', '3 Series'], [157, 286, 106, 72, 'car', 'Toyota', 'Corolla'], [57, 327, 113, 87, 'car', 'Volkswagen', 'Golf'], [1127, 132, 64, 52, 'car', 'Jeep', 'Wrangler'], [722, 378, 150, 106, 'car', 'Land-Rover', 'Range Rover'], [1076, 103, 55, 41, 'car', 'Subaru', 'WRX'], [982, 66, 41, 33, 'car', 'Ford', 'Mustang'], [848, 158, 76, 34, 'car', 'BMW', '7 Series'],
                                           [575, 237, 81, 58, 'car', 'Lamborghini', 'Aventador'], [200, 247, 84, 61, 'car', 'Honda', 'Civic'], [459, 170, 63, 53, 'car', 'Jeep', 'Wrangler'], [542, 100, 45, 40, 'car', 'Ford', 'Mustang'], [360, 147, 70, 47, 'car', 'Ford', 'Mustang'], [731, 198, 80, 54, 'car', 'Porsche', '911'], [586, 207, 69, 33, 'car', 'Honda', 'Civic'], [1172, 174, 27, 43, 'car', 'Nissan', 'Skyline'], [923, 296, 114, 84, 'car', 'Nissan', 'Leaf'], [726, 160, 81, 51, 'car', 'Ford', 'Mustang'], [298, 184, 86, 61, 'truck'], [610, 143, 53, 33, 'car', 'Lamborghini', 'Aventador'],
                                           [733, 296, 116, 93, 'car', 'Scion', 'xB'], [727, 136, 56, 20, 'car', 'Ford', 'Mustang'], [807, 77, 57, 36, 'car', 'Ford', 'Mustang'], [493, 67, 51, 35, 'car', 'Subaru', 'Impreza'], [253, 207, 87, 69, 'car', 'Land-Rover', 'Discovery'], [415, 195, 78, 35, 'car', 'Jeep', 'Wrangler'], [500, 126, 67, 64, 'car', 'Lamborghini', 'Aventador'], [410, 220, 86, 60, 'car', 'Lamborghini', 'Aventador'], [615, 118, 53, 30, 'car', 'Porsche', '911'], [442, 102, 51, 35, 'car', 'Lamborghini', 'Aventador'], [891, 233, 114, 87, 'car', 'Mini', 'Cooper'],
                                           [597, 183, 58, 31, 'car', 'Porsche', '911'], [513, 335, 108, 57, 'car', 'Ford', 'Mustang'], [636, 97, 40, 22, 'car', 'Honda', 'CR-V'], [719, 64, 48, 36, 'car', 'Pagani', 'Huayra']])

    def testing_multiple_cars_confidence(self):
        self.assertEqual(car_rec(image2), [[1035, 460, 158, 115, 'car', 'Honda', 'Civic'], [195, 438, 156, 142, 'car', 'Honda', 'CR-V'], [721, 486, 210, 180, 'car', 'Toyota', 'Sequoia'], [514, 365, 141, 98, 'car', 'Subaru', 'Impreza'], [-1, 438, 111, 108, 'car', 'Ford', 'Mustang'], [229, 381, 158, 105, 'car', 'Chevrolet', 'Camaro'], [287, 594, 203, 74, 'car', 'Porsche', 'Cayenne'], [462, 477, 169, 155, 'car', 'Dodge', 'Dakota'], [1086, 196, 81, 54, 'car', 'Ford', 'Mustang'], [860, 198, 76, 48, 'car', 'Honda', 'Civic'], [0, 359, 131, 113, 'car', 'Mini', 'Cooper'],
                                           [552, 289, 86, 50, 'car', 'Ford', 'Mustang'], [299, 315, 126, 77, 'car', 'Ford', 'Mustang'], [809, 105, 69, 39, 'car', 'Jeep', 'Wrangler'], [385, 254, 91, 68, 'car', 'BMW', '3 Series'], [157, 286, 106, 72, 'car', 'Toyota', 'Corolla'], [57, 327, 113, 87, 'car', 'Volkswagen', 'Golf'], [1127, 132, 64, 52, 'car', 'Jeep', 'Wrangler'], [722, 378, 150, 106, 'car', 'Land-Rover', 'Range Rover'], [1076, 103, 55, 41, 'car', 'Subaru', 'WRX'], [982, 66, 41, 33, 'car', 'Ford', 'Mustang'], [848, 158, 76, 34, 'car', 'BMW', '7 Series'],
                                           [575, 237, 81, 58, 'car', 'Lamborghini', 'Aventador'], [200, 247, 84, 61, 'car', 'Honda', 'Civic'], [459, 170, 63, 53, 'car', 'Jeep', 'Wrangler']])

    def testing_single_selected_cars(self):
        self.assertIn([2146, 1009, 1015, 463, 'car', 'Porsche', '718 Cayman'], car_rec(image3))


if __name__ == '__main__':
    unittest.main()
