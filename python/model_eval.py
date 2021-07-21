import cv2
import numpy as np
import jsonpickle
import torch
import h5py
import netclasses
import torch.nn as nn
import matplotlib.pyplot as plt
import sys
import os

def main():
    try:
        torch.cuda.empty_cache()
        torch.cuda.empty_cache()
        device = torch.cuda.get_device_name(0)
        print('Available GPU:', str(device))
    except RuntimeError:
        print('Please make sure you selected GPU as a hardware accelerator in Runtime --> Change runtime type')
        return

    criterion = nn.BCELoss()
    h5_filename = sys.argv[1]
    weights_filename = sys.argv[2]
    model_directory = sys.argv[3]
    h5 = h5py.File(h5_filename)
    print(list(h5.keys()))
    checkpoint = torch.load(weights_filename, map_location='cpu')
    model = netclasses.atomsegnet()
    model.load_state_dict(checkpoint)
    print("model initiated")
    score = []
    metarray = []
    print(list(h5.keys()))
    n_train = len(h5["X_test"])
    for i in range(n_train):
        image = np.expand_dims(h5["X_test"][i], axis=0)
        image_tensor = torch.from_numpy(image).float()
        forward = model.forward(image_tensor)
        prediction = forward.cpu().detach().numpy()[0, 0, :, :]
        ground_truth = np.asarray(h5["y_test"][i])[0, :, :]
        gt_tensor = torch.from_numpy(image).float()
        loss = criterion(forward, gt_tensor)
        loss = loss.item()
        print(loss)
        score.append(loss)
        meta = h5["Z_test"]
        metadata = jsonpickle.decode(h5["Z_test"][i])
        metarray.append(metadata)

    defocus = []
    a1 = []
    a2 = []
    b2 = []
    cs = []

    for i in range(len(metarray)):
        defocus.append(float(metarray[i]["microscope"]["aberrations"]["C10"]["val"]))
        a1.append(float(metarray[i]["microscope"]["aberrations"]["C12"]["mag"]))
        b2.append(float(metarray[i]["microscope"]["aberrations"]["C21"]["mag"]))
        a2.append(float(metarray[i]["microscope"]["aberrations"]["C23"]["mag"]))
        cs.append(float(metarray[i]["microscope"]["aberrations"]["C30"]["val"]))

    defocus = np.asarray(defocus)
    np.save(os.path.join(model_directory, "defocus.npy"), defocus)
    a1 = np.asarray(a1)
    np.save(os.path.join(model_directory, "a1.npy"), a1)
    a2 = np.asarray(a2)
    np.save(os.path.join(model_directory, "a2.npy"), a2)
    b2 = np.asarray(b2)
    np.save(os.path.join(model_directory, "b2.npy"), b2)
    cs = np.asarray(cs)
    np.save(os.path.join(model_directory, "cs.npy"), cs)
    score = np.asarray(score)
    np.save(os.path.join(model_directory, "score.npy"), score)

    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5)

    ax1.scatter(defocus, score)
    ax1.set_title('Defocus vs Loss')
    # ax1.xlabel('Defocus [nm]')

    ax2.scatter(a1, score)
    ax2.set_title('A1 vs Loss')
    # ax2.xlabel('A1 [nm]')

    ax3.scatter(a2, score)
    ax3.set_title('A2 vs Loss')
    # ax3.xlabel('A2 [nm]')

    ax4.scatter(b2, score)
    ax4.set_title('B2 vs Loss')
    # ax4.xlabel('B2 [nm]')

    ax5.scatter(cs, score)
    ax5.set_title('Cs vs Loss')
    # ax5.xlabel('Cs [nm]')

    # plt.show()
    fig.set_size_inches(20, 5)
    fig.savefig(os.path.join(model_directory, "model_performance.png"))



if __name__ == "__main__":
    main()

# Enrique Mejia
