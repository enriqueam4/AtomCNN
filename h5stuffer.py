import os
import cv2
import numpy as np
import h5py
from tkinter import filedialog
from tkinter import *
import imutils
from random import randint
from skimage import exposure


def main():
    root = Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select simulated image folder")
    if directory == "":
        return 0
    else:
        os.chdir(directory)

    gt_path = r'C:\Users\emejia\OneDrive - CUNY\Enrique\Simulations\Jun17_Sims\gt.tif'
    gt_im = cv2.imread(gt_path, 0)
    gt = np.asarray(gt_im).astype("uint8")
    gt = gt / gt.max()
    print(gt)

    files = os.listdir(directory)
    n_files = len(files)
    X_Test = []
    X_Train = []
    Y_Test = []
    Y_Train = []
    test_batches = 340
    train_batches = 928
    imagesize = 256
    for j in range(test_batches):
        print(str(j)+" of "+str(test_batches))
        k = np.random.randint(0, n_files - 1)
        img = cv2.imread(os.path.join(directory, files[k]), 0)  # 0 to read images grayscale
        np_img = np.asarray(img, dtype='uint8')

        img_copy = np.empty_like(np_img)
        img_copy[:] = np_img
        gt_copy = np.empty_like(gt)
        gt_copy[:] = gt

        img_copy, gt_copy = rand_rotate(img_copy, gt_copy)
        img_copy, gt_copy = rand_crop(img_copy, gt_copy, 10)

        rand_row = np.random.randint(0, (img_copy.shape[0] - imagesize))
        rand_col = np.random.randint(0, (img_copy.shape[1] - imagesize))

        cropped = img_copy[rand_row:rand_row + imagesize, rand_col:rand_col + imagesize]
        gt_crop = gt_copy[rand_row:rand_row + imagesize, rand_col:rand_col + imagesize]
        # cv2.imshow("cropped", cropped)
        # cv2.imshow("gt_crop", gt_crop)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        X_Test.append(cropped)
        Y_Test.append(gt_crop)

    for j in range(train_batches):
        print(str(j) + " of " + str(train_batches))
        k = np.random.randint(0, n_files - 1)
        img = cv2.imread(os.path.join(directory, files[k]), 0)  # 0 to read images grayscale
        np_img = np.asarray(img, dtype='uint8')

        img_copy = np.empty_like(np_img)
        img_copy[:] = np_img
        gt_copy = np.empty_like(gt)
        gt_copy[:] = gt

        img_copy, gt_copy = rand_rotate(img_copy, gt_copy)
        img_copy, gt_copy = rand_crop(img_copy, gt_copy, 10)

        rand_row = np.random.randint(0, (img_copy.shape[0] - imagesize))
        rand_col = np.random.randint(0, (img_copy.shape[1] - imagesize))
        cropped = img_copy[rand_row:rand_row + imagesize, rand_col:rand_col + imagesize]
        gt_crop = gt_copy[rand_row:rand_row + imagesize, rand_col:rand_col + imagesize]

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


if __name__ == '__main__':
    main()

#GIRLBOSS #GASLIGHT #GATEKEEP