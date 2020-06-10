# https://blog.csdn.net/humanking7/article/details/80546728
import sys
import os
from PyQt5.QtWidgets import *
from keras.models import load_model
from keras.preprocessing import image
import matplotlib.pyplot as plt
import numpy as np

class Window(QWidget):

    def __init__(self, name='Window'):

        super(Window, self).__init__()
        self.setWindowTitle(name)
        self.cwd = os.getcwd()  # 获取当前程序文件位置
        self.resize(500, 300)  # 设置窗体大小

        # Widget 1: Display the Test Result
        self.textbrowser = QTextBrowser(self)
        self.textbrowser.setObjectName("Bar_DisplayResult")

        # btn 1: Allow users to select egg images they intend to test
        self.btn_chooseFiles = QPushButton(self)
        self.btn_chooseFiles.setObjectName("btn_chooseFiles")
        # self.btn_chooseFiles.setText("选取文件目录")
        self.btn_chooseFiles.setText("Select Directory")

        # btn 2: Classify the image users selected
        self.btn_Classify = QPushButton(self)
        self.btn_Classify.setObjectName("btn_Classify")
        # self.btn_Classify.setText("开始鉴别")
        self.btn_Classify.setText("Start")



        # Layout Setting
        layout = QVBoxLayout()
        layout.addWidget(self.textbrowser)
        layout.addWidget(self.btn_chooseFiles)
        layout.addWidget(self.btn_Classify)
        self.setLayout(layout)

        # Action Setting
        self.btn_chooseFiles.clicked.connect(self.slot_btn_chooseFiles)
        self.btn_Classify.clicked.connect(self.slot_btn_Classify)

    def slot_btn_chooseFiles(self):

        global dir_choose
        dir_choose = QFileDialog.getExistingDirectory(self,
                                                      'Select',
                                                      self.cwd)  # Original Path
        if dir_choose == "":
            print("\n No directory selected")
            return
        print('\n Your selection is:')
        print(dir_choose)

    def slot_btn_Classify(self):

        global dir_choose
        dir = dir_choose +'/'

        file_list = os.listdir(dir) #'C:/Users/Administrator/Documents/Python/Projects/Data/Egg/egg test/')
        images = []

        for file in file_list: #file_list:
            # print(file)
            img = image.load_img(os.path.join(dir,
                                              file),
                                 target_size=(150, 150))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            images.append(img)

        x_train = np.array(images, dtype='float') / 255.0
        x = np.concatenate([x for x in x_train])

        # Load Model and Make Predictions 预测
        model = load_model('./Model/Eggs_small_1.h5')
        # model.summary()
        y = model.predict(x, verbose=1)

        # 根据结果可以看出来，0代表的是Healthy，1代表的是Subhealthy。
        # 同时也可以从训练cats_and_dogs_small/train/里面文件的顺序知道类别代表的信息

        for i in range(len(file_list)):
            # print(y[i][0])
            # print('image class:', int(y[i]))
            # print('image class:', round(y[i]))

            if y[i][0] > 0.5:

                print('image {} class:'.format(file_list[i]), 1)
                print('I am {:.2%} sure this is a SubHealthy Egg'.format(y[i][0]))
                # print('我有 {:.2%} 的把握这是一个亚健康的鸡蛋'.format(y[i][0]))
                # print('Acc:', y[i][0])
            else:

                print('image {} class:'.format(file_list[i]), 0)
                print('I am {:.2%} sure this is a Healthy Egg'.format(1 - y[i][0]))
                # print('我有 {:.2%} 的把握这是一个健康的鸡蛋'.format(1-y[i][0]))
                # print('Acc:', 1-y[i][0])

                #self.textbrowser.setText(self.)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Window = Window('鸡蛋质量鉴别软件V1.0')
    Window = Window('Egg Health Classifier V1.0')
    Window.show()
    sys.exit(app.exec_())
