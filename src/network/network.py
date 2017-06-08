import cv2
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tflearn
import threading
import re
import urllib2
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

#Set the path for the images
imagesPath = os.path.dirname(os.path.abspath(__file__))+"/../images/"

class Network(object):
    def __init__(self, modelName, imgSize, learningRate):
        self.modelName = modelName #model name of our network
        self.imgSize = imgSize #the size that we're gonna resize to
        self.LR = learningRate #learning rate

    def convertData(self, image):
        #Resize the image and set it to "black & white"
        img = cv2.resize(cv2.imread(imagesPath+image, cv2.IMREAD_GRAYSCALE), (self.imgSize,self.imgSize))
        #Return the result in numpy array
        return np.array(img)

    def modelNet(self):
        #Set input layer
        convnet = input_data(shape=[None, self.imgSize, self.imgSize, 1], name='input')
        #layers (6)
        convnet = conv_2d(convnet, 32, 2, activation='relu')
        convnet = max_pool_2d(convnet, 2)
        convnet = conv_2d(convnet, 64, 2, activation='relu')
        convnet = max_pool_2d(convnet, 2)
        convnet = conv_2d(convnet, 32, 2, activation='relu')
        convnet = max_pool_2d(convnet, 2)
        convnet = conv_2d(convnet, 64, 2, activation='relu')
        convnet = max_pool_2d(convnet, 2)
        convnet = conv_2d(convnet, 32, 2, activation='relu')
        convnet = max_pool_2d(convnet, 2)
        convnet = conv_2d(convnet, 64, 2, activation='relu')
        convnet = max_pool_2d(convnet, 2)
        #Fully connected layer
        convnet = fully_connected(convnet, 1024, activation='relu')
        convnet = dropout(convnet, 0.8)
        convnet = fully_connected(convnet, 2, activation='softmax')

        convnet = regression(convnet, optimizer='adam', learning_rate=self.LR, loss='categorical_crossentropy', name='targets')
        #Set the model with tensorboard as well
        self.model = tflearn.DNN(convnet, tensorboard_dir="log")
        #If a checkpoint is there load it in
        if os.path.exists("{}.meta".format(self.modelName)):
            self.model.load(self.modelName)
            print("model loaded")

def dirtyJob(network, img):

    """
    This function takes the image,
    convert it to data that the model can read,
    feed the data to the model and get the prediction back,
    assign the names : "Dog" and "Cat" to the prediction and
    make a request to the webapp to add the result
    """

    data = network.convertData(img)
    data = data.reshape(network.imgSize, network.imgSize,1)
    result = network.model.predict([data])[0]
    if np.argmax(result) == 1: str_label = "Dog"
    else : str_label = "Cat"
    urllib2.urlopen("http://127.0.0.1:8080/result/"+
                    re.findall(r'[^.;\s]+', img)[0]+"&"+str_label)

if __name__=="__main__":
    LR = 1e-3 #learning rate
    #create network
    network = Network("dogsvscats-{}-{}.model".format(LR, "6conv"), 50, LR)
    network.modelNet() #set the model for the network
    imageList = ["cat.1.jpg"] #list of image to skip
    while True:
        #check for images in the path
        for img in os.listdir(imagesPath):
            #if we don't have to skip it
            if img not in imageList:
                imageList.append(img) #add the image to the skip list
                #set and start a new thread for the image
                t = threading.Thread(target=dirtyJob, args=(network, img,))
                t.start()
