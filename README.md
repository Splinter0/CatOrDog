![Python Version](https://img.shields.io/badge/python-2.7-blue.svg)<br/><br/>
[Dataset Link](https://drive.google.com/file/d/0B0cTVZ4M52pIVnFwUEIzRl9EWVk/view?usp=sharing)
# CatOrDog
This is a convolutional neural network model that has been trained to identify
pictures of cats and dogs. It is written in Python using libraries like
Tensoflow and TFlearn to keep the code cleaner.
The neural network isn't the only thing in this repo, in fact the CNN is
used in a webapp written in Golang that gives the opportunity to see the
results right away.
## Content
Inside the repository there is the code of the webapp, the model for the
neural network, the code to use the neural network and also it is pre-trained
which means you don't have to train the model again thanks to checkpoints that you
can load in. Also there are logs that you can use with tensorboard to visualize
the improvements of the model. This also gives you the opportunity to keep training
the model if you wish making the predictions more accurate.
## Get started
If you are using Linux you can simply use the ```req.sh``` file to install
all the stuff you need in order to run this and then you can use start.sh to
run everything.
If you are in a different OS this is the list of all the dependencies:
(keep in mind we are using Python2.7)
```
pip (for python 2.7)
numpy
scipy
matplotlib
scikit-learn
tqdm
cv2 (python-opencv)
tensorflow
tflearn
pygoenv (not necessary we use it to setup a Golang env faster)
```
## Tour into the repository
```
-src
  -app (code for the webapp)
    -settings
      -settings.json (contains settings of the app)
      -main.go (loads the settings from setting.json)
    -views
      -main.go (handles views of the app)
    -templates (HTML code)
      -index.html (home page with the file uploader)
      -output.html (page that shows the output)
    -static (CSS, Images, Fonts)
    -main.go (entry of the app)
  -images (folder where images are uploaded and taken from the CNN)
  -network (code of the neural network)
    -checkpoint (keeps track of checkpoints of the model)
    -cnnModel.py (code of the cnn model)
    -dogsvscats* (model progress)
    -network.py (code for using the neural network)
    -test_data.npy (numpy preprocessed data for testing)
    -train_data.npy (numpy preprocessed data for training)
-req.sh (install dependencies on linux)
-start.sh (start app and neural network)
```
