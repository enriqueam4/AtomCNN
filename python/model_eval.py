import numpy as np
import jsonpickle
import torch
import h5py
import netclasses
import torch.nn as nn


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
    h5_filename = r"C:\Users\emejia\Desktop\AtomCNN\h5_files\Zdump.h5"
    weights_filename = r"C:\Users\emejia\Desktop\AtomCNN\models\test1-1-best_weights.pt"
    h5 = h5py.File(h5_filename)
    print(list(h5.keys()))
    checkpoint = torch.load(weights_filename, map_location='cpu')
    model = netclasses.atomsegnet()
    model.load_state_dict(checkpoint)
    print("model initiated")
    score = []
    metarray = []
    print(list(h5.keys()))
    n_train = len(h5["X_train"])
    n_train = 100

    for i in range(n_train):
        image = np.expand_dims(h5["X_train"][i], axis=0)
        image_tensor = torch.from_numpy(image).float()
        forward = model.forward(image_tensor)
        prediction = forward.cpu().detach().numpy()[0, 0, :, :]
        ground_truth = np.asarray(h5["y_train"][i])[0, :, :]
        gt_tensor = torch.from_numpy(image).float()
        loss = criterion(forward, gt_tensor)
        loss = loss.item()
        print(loss)
        score.append(loss)
        meta = h5["Z_test"]
        metadata = jsonpickle.decode(h5["Z_test"][i])
        metarray.append(metadata)

    for i in range(len(metarray)):
        defocus = metarray[i]

    plt.plot(np.asarray(score), np.asarray)


if __name__ == "__main__":
    main()

# Enrique Mejia
