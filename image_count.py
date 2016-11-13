'''
Notes on Microsoft Vision: 
App on Azure? Webhost
Cognitive services: human vision, feelings, objs -> api 
training with machine learning -> langw
microsoft.com/cognitive
http call, parse json
'''
import mahotas
import numpy as np
from pylab import imshow, gray, show
from os import path

photo = mahotas.imread('zeggs01.jpg', as_grey=True)
photo = photo.astype(np.uint8)
T_otsu = mahotas.otsu(photo)
print(T_otsu)
gray()
imshow(photo > T_otsu)
show()
