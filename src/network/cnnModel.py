import cv2
import numpy as np
import os
from random import shuffle
from tqdm import tqdm
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

class CNN(object):
    def __init__(self, trainDir, testDir, imgSize, lR, modelName, epoch):
        self.trainDir = trainDir
        self.testDir = testDir
        self.imgSize = imgSize
        self.LR = lR
        self.modelName = modelName
        self.epoch = epoch

    def labelImg(self, img):
        word_label = img.split(".")[-3] #split the file name so we get the label
        if word_label == "cat": return [1,0]
        elif word_label == "dog": return [0,1]

    def createTrainData(self):
        train_data = []
        for img in tqdm(os.listdir(self.trainDir)): #list each img in the path
            label = self.labelImg(img) #get the label
            path = os.path.join(self.trainDir, img)
            #resize the image by the IMG_SIZE and make it in grayscale
            img = cv2.resize(cv2.imread(path, cv2.IMREAD_GRAYSCALE),(self.imgSize,self.imgSize))
            #append the numpy array of the data (img) and the labels
            train_data.append([np.array(img), np.array(label)])
        shuffle(train_data)
        np.save('train_data.npy', train_data)
        return train_data

    def processTestData(self):
        test_data = []
        for img in tqdm(os.listdir(self.testDir)):
            path = os.path.join(self.testDir, img) #get the path
            img_num = img.split('.')[0] #get the id of the image since it isn't labeled
            img = cv2.resize(cv2.imread(path, cv2.IMREAD_GRAYSCALE), (self.imgSize,self.imgSize))
            test_data.append([np.array(img), img_num])

        np.save("test_data.npy", test_data)
        return test_data

    def model(self):
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
        convnet = fully_connected(convnet, 1024, activation='relu')
        convnet = dropout(convnet, 0.8)
        convnet = fully_connected(convnet, 2, activation='softmax')

        convnet = regression(convnet, optimizer='adam', learning_rate=self.LR, loss='categorical_crossentropy', name='targets')

        self.model = tflearn.DNN(convnet, tensorboard_dir="log")

        if os.path.exists("{}.meta".format(self.modelName)):
            self.model.load(self.modelName)
            print("model loaded")

    def train(self, X, Y, test_x, test_y):
        self.model.fit({'input': X}, {'targets': Y}, n_epoch=self.epoch, validation_set=({'input': test_x}, {'targets': test_y}),
            snapshot_step=500, show_metric=True, run_id=self.modelName)
        self.model.save(self.modelName)


if __name__=="__main__":
    LR = 1e-3
    cnnTest = CNN("../data/dc-train", "../data/dc-test", 50, LR,
                    "dogsvscats-{}-{}.model".format(LR, "6conv"), 250)
    try :
        train_data = np.load("train_data.npy")
    except :
        train_data = cnnTest.createTrainData()
    cnnTest.model()

    train = train_data[:-500]
    test = train_data[-500:]

    X = np.array([i[0] for i in train]).reshape(-1, cnnTest.imgSize, cnnTest.imgSize, 1)
    Y = [i[1] for i in train]
    test_x = np.array([i[0] for i in test]).reshape(-1, cnnTest.imgSize, cnnTest.imgSize, 1)
    test_y = [i[1] for i in test]

    cnnTest.train(X, Y, test_x, test_y)

    try :
        test_data = np.load("test_data.npy")
    except:
        test_data = cnnTest.processTestData()

    for num, data in enumerate(test_data[:12]):
        img_num = data[1]
        img_data = data[0]
        data = img_data.reshape(cnnTest.imgSize, cnnTest.imgSize,1)

        model_out = cnnTest.model.predict([data])[0]

        if np.argmax(model_out) == 1: str_label = "Dog"
        else : str_label = "Cat"
        print("n{}: {}".format(img_num, str_label))
