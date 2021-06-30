import os
import cv2
import numpy as np
from tkinter import filedialog
from tkinter import *


def main():
    root = Tk()
    root.withdraw()
    xyz_filename = r'C:\Users\enriq\OneDrive - CUNY\Enrique\Simulations\Unrelaxed C-hBN\XYZ files\v2.xyz'  # filedialog.askopenfilename(title="Select .xyz file")
    if xyz_filename == "":
        return 0

    name, extension = os.path.splitext(xyz_filename)
    if extension == ".xyz":
        species_list = {'B', 'N', 'C'}
        data = xyz_reader(xyz_filename)
        comparison_file = r'C:\Users\enriq\Desktop\Noisy Ims GT\8_bit_groundTruth0.tif'  # filedialog.askopenfilename(title="Select image file for comparison")

        c_file = cv2.imread(comparison_file)
        c_file = np.asarray(c_file)
        cc = c_file.shape
        x_pix = cc[1]
        y_pix = cc[0]
        frame = np.zeros((y_pix, x_pix))
        x_pos = []
        y_pos = []
        all_x = []
        all_y = []
        all_type = []
        type = []
        c = len(data)
        for i in range(len(data)):
            all_type.append(data[i][0])
            all_x.append(float(data[i][1]))
            all_y.append(float(data[i][2]))
            if data[i][0] in species_list:
                print(data[i][0])
                type.append(data[i][0])
                x_pos.append(float(data[i][1]))
                y_pos.append(float(data[i][2]))


        x_min = min(all_x)
        x_max = max(all_x)
        y_min = min(all_y)
        y_max = max(all_y)
        const = 0.0510
        x_buf_l = 35 * const
        x_buf_r = 22 * const
        y_buf_l = 33 * const
        y_buf_r = 32 * const

        x = np.linspace(x_min - x_buf_l, x_max + x_buf_r, x_pix, endpoint=True)
        y = np.linspace(y_min - y_buf_l, y_max + y_buf_r, y_pix, endpoint=True)
        radius = 5

        for i in range(len(x_pos)):
            x_ind = find_nearest(x, x_pos[i])
            y_ind = find_nearest(y, y_pos[i])
            print("x: "+str(x_ind)+", y: "+str(y_ind))
            if type[i] == 'B':
                frame = cv2.circle(frame, (x_ind, y_ind), radius, .5, -1)
            elif type[i] == 'C':
                frame = cv2.circle(frame, (x_ind, y_ind), radius, .75, -1)
            elif type[i] == 'N':
                frame = cv2.circle(frame, (x_ind, y_ind), radius, 1, -1)

        gt = np.copy(frame)

        c_copy = cv2.resize(c_file, (x_pix//2, y_pix//2))
        c_copy = c_copy[:, :, 0]
        gt_copy = cv2.resize(gt, (x_pix // 2, y_pix // 2))

        c_copy = c_copy/c_copy.max()

        # cv2.imshow("Comparison: ", .5*c_copy + 0.5*gt_copy)
        # cv2.imshow("Ground Truth: ", gt_copy)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        print(os.path.splitext(comparison_file)[0]+"_gt.npy")
        np.save(os.path.splitext(comparison_file)[0]+"_gt.npy", gt)
        #gtsave = 255.0*gt

        # cv2.imwrite(name+"_written.png", gt)
        # cv2.imwrite(name+"_binarized.png", c_file)




def find_nearest(array, value):
    array = np.asarray(array)
    return (np.abs(array - value)).argmin()


def pixel_to_angstrom(value):
    const = .0510           # Measured constant for pixels to angstroms in this image
    return value * const


def xyz_reader(filename):
    file1 = open(filename, 'r')
    lines = file1.readlines()
    lines.pop(0)
    lines.pop(0)
    length = len(lines)
    data = np.empty(length, dtype=np.object)

    for i in range(length):
        lines[i] = lines[i].replace('\n', '')  # stripping newline characters from individual strings
        tmp = lines[i].split(" ")  # files are formatted using spaces instead of tabs, go figure
        for j in range(len(tmp)):
            tmp[j] = tmp[j].replace(' ', '')

        while '' in tmp:
            tmp.remove('')
        data[i] = tmp
    return data


if __name__ == '__main__':
    main()
