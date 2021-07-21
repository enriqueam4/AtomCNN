import matplotlib.pyplot as plt
import torch
import netclasses
import torch.optim as optim
import os
import sys
import numpy as np


def main():
    try:
        torch.cuda.empty_cache()
        torch.cuda.empty_cache()
        device = torch.cuda.get_device_name(0)
        print('Available GPU:', str(device))
    except RuntimeError:
        print('Please make sure you selected GPU as a hardware accelerator in Runtime --> Change runtime type')
        return

    hf_file = sys.argv[1]
    model_directory = sys.argv[2]
    epochs = int(sys.argv[3])
    epoch_array = range(epochs)

    batch_size = 30
    gen = netclasses.generate_batches(hf_file, batch_size)
    train_ims, gt = next(gen.batch(28))
    gen.close_()
    print(train_ims.shape)
    model = netclasses.atomsegnet()
    model.cuda()
    optimizer = optim.Adam(model.parameters(), lr=5e-4)
    train_losses, test_losses = netclasses.train(epochs=epochs, hf_file=hf_file, model=model, optimizer=optimizer,
                                                 batch_size=batch_size, model_directory=model_directory)

    np.save(model_directory+"train_losses.npy", train_losses)
    np.save(model_directory+"train_losses.npy", train_losses)
    np.save(model_directory+"train_losses.npy", epoch_array)
    plt.scatter(epoch_array, train_losses)
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Loss")
    plt.savefig(model_directory+"loss.png")


if __name__ == '__main__':
    main()
