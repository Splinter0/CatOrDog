#Requirements install for linux
sudo apt-get update
sudo apt-get install build-essential gfortran libatlas-base-dev python-pip python-dev
sudo pip install --upgrade pip
sudo pip install numpy
sudo pip install scipy
sudo pip install -U scikit-learn
sudo pip install tqdm
sudo apt-get install python-opencv
export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.1.0-cp27-none-linux_x86_64.whl
sudo pip install $TF_BINARY_URL
sudo pip install tflearn
sudo pip install pygoenv
goenv
