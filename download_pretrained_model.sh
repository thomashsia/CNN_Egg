URL=https://drive.google.com/file/d/1HcSIMqH3UyFiDMxemdVYtxQV3jF9CPCo/view?usp=sharing
FILE=./pretrained_model.h5
TARGET_DIR=./model/

wget -N $URL -O $FILE
mkdir $TARGET_DIR
mv $FILE -d $TARGET_DIR
