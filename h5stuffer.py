import os
import cv2
import numpy as np
import h5py
from tkinter import filedialog
from tkinter import *
import imutils
from random import randint


def main():
    root = Tk()
    root.withdraw()
    # directory is the image directory of all the images
    directory = filedialog.askdirectory(title="Select simulated image folder")
    if directory == "":
        return 0
    else:
        os.chdir(directory)
    # change gt path to the location of some tif image corresponding to the exit wave of the structure
    gt_path = r'C:\Users\emejia\OneDrive - CUNY\Enrique\Simulations\Jun17_Sims\gt.tif'
    gt = load_image(gt_path)
    gt = gt/gt.max()

    files = os.listdir(directory)
    n_files = len(files)
    X_Test = []
    X_Train = []
    Y_Test = []
    Y_Train = []
    test_batches = 340
    train_batches = 928
    image_size = 256
    for j in range(test_batches):
        print(str(j)+" of "+str(test_batches))
        k = np.random.randint(0, n_files - 1)
        img = load_image(os.path.join(directory, files[k]), 0)
        cropped, gt_crop = prep_pair(img, gt, image_size)
        X_Test.append(cropped)
        Y_Test.append(gt_crop)

    for j in range(train_batches):
        print(str(j) + " of " + str(train_batches))
        k = np.random.randint(0, n_files - 1)
        img = load_image(os.path.join(directory, files[k]), 0)
        cropped, gt_crop = prep_pair(img, gt, image_size)
        X_Train.append(cropped)
        Y_Train.append(gt_crop)

    hf = h5py.File('Apr08_rotated_scaled.h5', 'w')
    hf.create_dataset('X_train', data=np.expand_dims(np.asarray(X_Train), axis=1))
    hf.create_dataset('X_test', data=np.expand_dims(np.asarray(X_Test), axis=1))
    hf.create_dataset('y_test', data=np.expand_dims(np.asarray(Y_Test), axis=1))
    hf.create_dataset('y_train', data=np.expand_dims(np.asarray(Y_Train), axis=1))
    hf.close()

    im = X_Test[0] + 255 * Y_Test[0]
    im = im / im.max()
    cv2.imshow("image", im)
    cv2.imshow("ground truth", 255.0 * Y_Test[0])
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def rand_crop(image, gt, scale):
    if scale != 0:
        rand_scale = .01 * (100 + randint(-scale, scale))
        image = cv2.resize(image, (int(image.shape[1] * rand_scale), int(image.shape[0] * rand_scale)))
        gt = cv2.resize(gt, (int(gt.shape[1] * rand_scale), int(gt.shape[0] * rand_scale)))
    return image, gt


def rand_rotate(image, gt):
    rand_angle = randint(-30, 30)
    return imutils.rotate(image, angle=rand_angle), imutils.rotate(gt, angle=rand_angle)


def load_image(gt_path):
    if os.path.splitext(gt_path)[1] == ".tif":
        gt_im = cv2.imread(gt_path, 0)
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