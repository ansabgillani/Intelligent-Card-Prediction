import os, cv2
import GUI as gui
import ColorDetector as cd
from PIL import Image
import numpy as np
from pylab import rcParams

rcParams['figure.figsize'] = 20, 10


def getLabel(id):
    return ['Civic', 'Corolla', 'Mehran', 'Other'][id]


def loadData():
    # import time
    # import matplotlib.pyplot as plt
    # import matplotlib.image as mpimg
    # from sklearn.utils import shuffle
    # from sklearn.model_selection import train_test_split

    # import keras
    # from keras.utils import np_utils
    # from keras import backend as K
    from keras.models import Sequential
    from keras.layers.core import Dense, Dropout, Activation, Flatten
    from keras.layers.convolutional import Convolution2D, MaxPooling2D
    # from keras.optimizers import SGD, RMSprop, adam
    # from keras.preprocessing.image import ImageDataGenerator
    # from keras import callbacks

    # # Define Datapath
    # data_path = './dataset/'
    # data_dir_list = os.listdir(data_path)
    #
    # img_data_list = []
    # for dataset in data_dir_list:
    #     img_list = os.listdir(data_path + '/' + dataset)
    #     print('Loaded the images of dataset-' + '{}\n'.format(dataset))
    #     for img in img_list:
    #         input_img = cv2.imread(data_path + '/' + dataset + '/' + img)
    #         # input_img=cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    #         input_img_resize = cv2.resize(input_img, (128, 128))
    #         img_data_list.append(input_img_resize)
    #
    # img_data = np.array(img_data_list)
    # img_data = img_data.astype('float32')
    # img_data = img_data / 255
    #
    # # Define Classes\Labels
    # num_classes = 4
    #
    # num_of_samples = img_data.shape[0]
    # labels = np.ones((num_of_samples,), dtype='int64')
    #
    # labels[0:1278] = 0  # 1278
    # labels[1279:2726] = 1  # 1448
    # labels[2727:3824] = 2  # 1098
    # labels[3835:4102] = 3  # 267
    # labels[4102:] = 4  # 52513
    #
    # names = ['Civic', 'Corolla', 'Mehran', 'Other']
    #
    #
    #
    #
    #
    # # convert class labels to one-hot encoding (matrix of 7x7)
    # Y = np_utils.to_categorical(labels, num_classes)
    #
    # # Shuffle the dataset
    # x, y = shuffle(img_data, Y, random_state=2)
    # # Split the dataset
    # X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.15, random_state=2)
    #
    # # Defining the model
    # input_shape = img_data[0].shape

    input_shape = (128, 128, 3)
    num_classes = 4
    model = Sequential()

    # Feature Extraction
    model.add(Convolution2D(6, 5, 5, input_shape=input_shape, border_mode='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Convolution2D(16, 5, 5, border_mode='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Convolution2D(120, 5, 5))
    model.add(Activation('relu'))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(84))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))

    # #Compile Model
    # model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=["accuracy"])
    #
    # filename = 'model_train_new.csv'
    # filepath = "Best-weights-my_model-{epoch:03d}-{loss:.4f}-{acc:.4f}.hdf5"
    #
    # csv_log = callbacks.CSVLogger(filename, separator=',', append=False)
    # checkpoint = callbacks.ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
    # callbacks_list = [csv_log, checkpoint]
    # callbacks_list = [csv_log]
    #
    # #train Model
    # hist = model.fit(X_train, y_train, batch_size=86, nb_epoch=50, verbose=1, validation_data=(X_test, y_test), callbacks=callbacks_list)
    #
    # #Model Save
    # model.save_weights('model_weights.h5')
    # model.save('model_keras.h5')

    # TEST
    model.load_weights('model_weights.h5')
    return model


def imgReader(fn, model):
    # testimg_data_list = []
    # test_img = cv2.imread(fn, True)
    # test_img = fn
    # test_img_resize = cv2.resize(test_img, (128, 128))
    testimg_data_list = []
    test_img = cv2.imread(fn, True)
    test_img_resize = cv2.resize(test_img, (128, 128))
    testimg_data_list.append(test_img_resize)
    testimg_data = np.array(testimg_data_list)
    testimg_data = testimg_data.astype('float32')
    testimg_data = testimg_data / 255
    testimg_data.shape
    testimg_data_list.clear()

    # print("test image original shaape",testimg_data[0].shape)
    # print("image original shaape",img_data[0].shape)

    results = model.predict_classes(testimg_data)
    # plt.imshow(test_img, cmap=plt.get_cmap('Set2'))
    cv2.imshow('window-name', test_img)
    cv2.waitKey(0)

    return getLabel(results[0])


def run(fileName):

    model = loadData()
    # # print(file)
    # # image = file.read()
    # # npimg = np.fromstring(image, np.uint8)
    # # img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    # #
    # # if (file.filename != None and file.filename != ''):
    # #     fileName = file.filename
    # #     print("car :", imgReader(img, model))
    #
    #     im = Image.open(image)
    if (fileName != None and fileName != ''):
        # fileName = app.fileName
        print(fileName)
        car = imgReader(fileName, model)
        print("car :", car)
        image = Image.open(fileName)

        # print(im)
        # print (image)
        # print(file)
        # final_colors = cd.process_image(im)
        # highest = 0
        # for strength in final_colors.items():
        #     split = int(str(strength).split('.')[2].split(", ")[1])
        #     if (split > highest):
        #         highest = split
        company = None
        if(car.capitalize() == "Mehran"):
            company = "Suzuki"
        elif (car.capitalize() == "Corolla"):
            company = "Toyota"
        elif (car.capitalize() == "Civic"):
            company = "Honda"
        else:
            company = None

        final_colors = cd.process_image(image)
        highest = 0
        for strength in final_colors.items():
            split = int(str(strength).split('.')[2].split(", ")[1])
            if (split > highest):
                highest = split

        for color, strength in final_colors.items():
            # print("x", color.__name__,strength)
            split = int(str(strength).split('.')[0])
            if (split == highest):
                color = color.__name__
                print(color, strength)
                details = [car, company, color]
                return details
    else:
        print("No File!")

    return None