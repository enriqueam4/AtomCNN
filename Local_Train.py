import torch
import netclasses
import torch.optim as optim
import os
from tkinter import *
from tkinter import filedialog
ff

def main():
    try:
        torch.cuda.empty_cache()
        torch.cuda.empty_cache()
        device = torch.cuda.get_device_name(0)
        print('Available GPU:', str(device))
    except RuntimeError:
        print('Please make sure you selected GPU as a hardware accelerator in Runtime --> Change runtime type')
        return

    root = Tk()
    root.withdraw()
    hf_file = filedialog.askopenfilename(title="Select h5 file")
    if hf_file == "":
        return 0
    else:
        os.chdir(hf_file)

    batch_size = 30
    gen = netclasses.generate_batches(hf_file, batch_size)
    train_ims, gt = next(gen.batch(28))
    gen.close_()
    print(train_ims.shape)
    model = netclasses.atomsegnet()
    model.cuda()
    optimizer = optim.Adam(model.parameters(), lr=5e-4)
    netclasses.train(epochs=300, hf_file=hf_file, model=model, optimizer=optimizer, batch_size=batch_size)


if __name__ == '__main__':
    main()
