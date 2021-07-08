import netclasses
import torch
import PIL
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image
from matplotlib import cm

ff
def main():
    try:
        device = torch.cuda.get_device_name(0)
        print('Available GPU:', str(device))

        root = Tk()
        root.withdraw()
        # image = filedialog.askopenfilename(title="Select image file")
        image = r'C:\Users\emejia\OneDrive - CUNY\Enrique\Simulations\Jun17_Sims\ce8bit\image001.tif'
        gta = r'C:\Users\emejia\OneDrive - CUNY\Enrique\Simulations\Jun17_Sims\gt.tif'
        if image == "":
            return
        else:

            scale = 1

            # size = min(image.shape[0], image.shape[1])
            image = cv2.imread(image, 0)
            gta = cv2.imread(gta, 0)
            gta = np.asarray(gta).astype("uint8")
            gta = gta / gta.max()
            gta = np.uint8(gta*255)
            gta_map = np.uint8(255*cm.RdBu_r(gta))
            gt = Image.fromarray(gta_map, mode='RGBA')
            gt.show()
            print(image.shape)
            a = image.shape

            image = cv2.resize(image, (int(a[1]*scale), int(a[0]*scale)))
            print(image.shape)
            tensor_size = 2048
            image_tensor = torch.empty((1, 1, tensor_size, tensor_size))

            for i in range(tensor_size):
                print("Row " + str(i) + " of " + str(tensor_size))
                for j in range(tensor_size):
                    image_tensor[0, 0, i, j] = image[i, j]

        print("image loaded")
        # gt_name = filedialog.askopenfilename(title="Select ground truth file")
        # if gt_name == "":
        #     return
        # gt = np.load(gt_name)
        # gt = gt[0:1024, 0:1024]

        # filepath = filedialog.askopenfilename(title="Select weight file")
        filepath = r'C:\Users\emejia\OneDrive - CUNY\Enrique\Simulations\Jun17_Sims\exitwave-1-best_weights.pt'
        if filepath == "":
            return
        checkpoint = torch.load(filepath, map_location='cpu')
        model = netclasses.atomsegnet()
        model.load_state_dict(checkpoint)
        print("model initiated")
        batch_size = 1
        # gen = netclasses.generate_batches(hf_file, batch_size=batch_size)
        test_ims = image_tensor
        # gen.close_()
        prediction = model.forward(test_ims)
        prediction = prediction.data.numpy()

        for i in range(batch_size):
            # fig = plt.figure(figsize=(12, 12))

            pred = np.asarray(prediction[i, 0, :, :])
            pred = np.uint8(pred*255)
            pred_mapped = np.uint8(255*cm.RdBu_r(pred))
            pred_im = Image.fromarray(pred_mapped)
            np_image = np.asarray(pred_im)
            new_np = np.zeros((np_image.shape[0], np_image.shape[1], 4))

            for i in range(np_image.shape[0]):
                for j in range(np_image.shape[1]):
                    pix_array = np.copy(np_image[i, j])
                    if pix_array[0] < 20:
                        pix_array[3] = 0
                    new_np[i, j] = pix_array
            new_np = np.uint8(new_np)
            new_image = Image.fromarray(new_np, mode="RGBA")
            new_image.save('gt.png')

            background = np.asarray(test_ims[0, 0, :, :])
            np_background = np.zeros((background.shape[0], background.shape[1], 4))

            for i in range(np_background.shape[0]):
                for j in range(np_background.shape[1]):
                    pix_list = []
                    pix = np.uint8(background[i, j])
                    pix_list.append(pix)
                    pix_list.append(pix)
                    pix_list.append(pix)
                    pix_list.append(255)
                    pix_array = np.asarray(pix_list)
                    np_background[i, j] = pix_array
            np_background = np.uint8(np_background)
            bg_im = Image.fromarray(np_background, mode='RGBA')
            bg_im.show()
            pred_im.show()
            pred_im.save('A_prediction.png')
            bg_im.save('A_unmarked.png')
            bg_im.paste(new_image, (0, 0), new_image)
            diff = PIL.ImageChops.subtract(pred_im, gt, scale=1.0, offset=0)
            diff.show()
            diff.save("A_diff.png")
            bg_im.show()
            gt.save('A_gt_im.png')
            bg_im.save('A_marked.png')

            # ax1 = fig.add_subplot(131)
            # ax1.imshow(test_ims[i, 0, :, :], cmap='gray')
            # ax1.set_title('Training image')
            # # ax2 = fig.add_subplot(132)
            # # ax2.imshow(gt, cmap='RdBu_r', interpolation='Gaussian')
            # # ax2.set_title('Ground truth')
            # ax3 = fig.add_subplot(133)
            # ax3.imshow(prediction[i, 0, :, :], cmap='RdBu_r', interpolation='Gaussian')
            # ax3.set_title('Model prediction')
            # plt.imshow(prediction[i, 0, :, :], cmap='RdBu_r', interpolation='Gaussian')
            #
            # plt.show()

    except RuntimeError as e:
        print(e)
        print('Please make sure you selected GPU as a hardware accelerator in Runtime --> Change runtime type')


if __name__ == '__main__':
    main()
