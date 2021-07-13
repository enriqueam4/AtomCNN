import numpy as np
import jsonpickle
import torch
import h5py
import netclasses
import torch.nn as nn

def main():
    criterion = nn.BCELoss()
    h5_filename = r""
    weights_filename = r""
    h5 = h5py.File(h5_filename)
    print(list(h5.keys()))
    checkpoint = torch.load(weights_filename, map_location='cpu')
    model = netclasses.atomsegnet()
    model.load_state_dict(checkpoint)
    print("model initiated")
    score = []
    defocus = []
    for i in range(len(h5["X_train"])):
        image = h5["X_Train"][i]
        image_tensor = torch.empty((1, 1, image.shape[0], image.shape[1]))
        image_tensor[0, 0, :, :] = image
        prediction = np.asarray(model.forward(image_tensor))
        ground_truth = np.asarray(h5["y_train"][i])
        loss = criterion(prediction, ground_truth)
        score.append(correctness)
        metadata = jsonpickle.decode(h5["Z_train"][i])
        defocus.append(metadata[])


if __name__=="__main__":
    main()