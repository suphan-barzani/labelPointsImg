#!/bin/sh

brew install python@2
pip install --upgrade virtualenv

# clone labelPointsImg source
rm -rf /tmp/labelPointsImgSetup
mkdir /tmp/labelPointsImgSetup
cd /tmp/labelPointsImgSetup
curl https://codeload.github.com/tzutalin/labelPointsImg/zip/master --output labelPointsImg.zip
unzip labelPointsImg.zip
rm labelPointsImg.zip

# setup python3 space
virtualenv --system-site-packages  -p python3 /tmp/labelPointsImgSetup/labelPointsImg-py3
source /tmp/labelPointsImgSetup/labelPointsImg-py3/bin/activate
cd labelPointsImg-master

# build labelPointsImg app
pip install py2app
pip install PyQt5 lxml
make qt5py3
rm -rf build dist
python setup.py py2app -A
mv "/tmp/labelPointsImgSetup/labelPointsImg-master/dist/labelPointsImg.app" /Applications
# deactivate python3
deactivate
cd ../
rm -rf /tmp/labelPointsImgSetup
echo 'DONE'
