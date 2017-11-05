sudo apt-get --assume-yes install python-software-properties
sudo apt-get install python3-pip
sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran
sudo python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-0.12.0-py3-none-any.whl
sudo pip3 install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.4.0-cp34-cp34m-linux_x86_64.whl
sudo pip3 install networkx==1.11
pip install -r requirements.txt --no-index --find-links file:///tmp/packages
