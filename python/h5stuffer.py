import os
import cv2
import numpy as np
import h5py
from tkinter import filedialog
from tkinter import *
import imutils
from random import randint
from skimage import exposure
import json


def main():
    directory = sys.argv[1]
    gt_path = sys.argv[2]
    save_path = sys.argv[3]
    gt = load_image(gt_path)
    gt = gt/gt.max()
    files = os.listdir(directory)
    n_files = len(files)
    X_Test = []
    X_Train = []
    Y_Test = []
    Y_Train = []
    Z_Test = []
    Z_Train = []
    test_batches = 340
    train_batches = 928
    image_size = 256
    for j in range(test_batches):
        print(str(j)+" of "+str(test_batches))
        if n_files > 1:
            k = np.random.randint(0, n_files - 1)
        else:
            k = 0

        json_path = directory + "\\" + files[k] + "\\Image.json"
        dictionary = json_to_dict(json_path)

        image_path = directory + "\\" + files[k] + "\\Image.tif"
        img = load_image(image_path)
        p0, p100 = np.percentile(img, (0, 100))
        img = exposure.rescale_intensity(img, in_range=(p0, p100))      # Adjusting Exposure of image

        cropped, gt_crop = prep_pair(img, gt, image_size)

        X_Test.append(cropped)
        Y_Test.append(gt_crop)
        Z_Test.append(dictionary)

    for j in range(train_batches):
        print(str(j) + " of " + str(train_batches))
        if n_files > 1:
            k = np.random.randint(0, n_files - 1)
        else:
            k = 0

        json_path = directory + "\\" + files[k] + "\\Image.json"
        dictionary = json_to_dict(json_path)

        image_path = directory + "\\" + files[k] + "\\Image.tif"
        img = load_image(image_path)
        p0, p100 = np.percentile(img, (0, 100))
        img = exposure.rescale_intensity(img, in_range=(p0, p100))      # Adjusting Exposure of image
        cropped, gt_crop = prep_pair(img, gt, image_size)

        X_Train.append(cropped)
        Y_Train.append(gt_crop)
        Z_Train.append(dictionary)

    Z_Train = [n.encode("ascii", "ignore") for n in Z_Train]
    Z_Test = [n.encode("ascii", "ignore") for n in Z_Test]
    hf = h5py.File(save_path, 'w')
    hf.create_dataset('X_train', data=np.expand_dims(np.asarray(X_Train), axis=1))
    hf.create_dataset('X_test', data=np.expand_dims(np.asarray(X_Test), axis=1))
    hf.create_dataset('y_test', data=np.expand_dims(np.asarray(Y_Test), axis=1))
    hf.create_dataset('y_train', data=np.expand_dims(np.asarray(Y_Train), axis=1))
    hf.create_dataset('Z_train', data=np.asarray(Z_Train))
    hf.create_dataset('Z_test', data=np.asarray(Z_Test))
    hf.close()


def rand_crop(image, gt, scale):
    if scale != 0:
        rand_scale = .01 * (100 + randint(-scale, scale))
        image = cv2.resize(image, (int(image.shape[1] * rand_scale), int(image.shape[0] * rand_scale)))
        gt = cv2.resize(gt, (int(gt.shape[1] * rand_scale), int(gt.shape[0] * rand_scale)))
    return image, gt


def json_to_dict(file):
    f = open(file, )
    data = json.load(f)
    stringy = json.dumps(data)
    stringy = str(stringy)
    return stringy


def rand_rotate(image, gt):
    rand_angle = randint(-30, 30)
    return imutils.rotate(image, angle=rand_angle), imutils.rotate(gt, angle=rand_angle)


def load_image(gt_path):
    if os.path.splitext(gt_path)[1] == ".tif":
        gt_im = cv2.imread(gt_path, -1)
        if len(gt_im.shape)==3:
            gt_im = gt_im[:, :, 0]
        gt_im = gt_im/gt_im.max()
        gt_im = gt_im*255.0
        return np.asarray(gt_im).astype("uint8")


def prep_pair(image, gt, image_size):
    img_copy = np.empty_like(image)
    img_copy[:] = image
    gt_copy = np.empty_like(gt)
    gt_copy[:] = gt
    img_copy, gt_copy = rand_rotate(img_copy, gt_copy)
    img_copy, gt_copy = rand_crop(img_copy, gt_copy, 10)
    rand_row = np.random.randint(0, (img_copy.shape[0] - image_size))
    rand_col = np.random.randint(0, (img_copy.shape[1] - image_size))
    cropped = img_copy[rand_row:rand_row + image_size, rand_col:rand_col + image_size]
    gt_crop = gt_copy[rand_row:rand_row + image_size, rand_col:rand_col + image_size]
    return cropped, gt_crop


if __name__ == '__main__':
    main()

#GIRLBOSS #GASLIGHT #GATEKEEP