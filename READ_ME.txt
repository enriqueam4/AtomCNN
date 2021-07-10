This software is intended to create a neural network model for spotting atoms in TEM images.
It is highly recommended (if not necessary) that your computer has a NVIDIA GPU, as all of the code runs off of either OpenCL or Torch.
It requires an input structure as an input and outputs a .pt file with training weights.

To run this program, enter an administrative command window and call run_cltem.bat. 
Be sure that you have no other memory intensive (ie PyCharm) programs running in background when you run the program, or else it WILL fail.
The batch file lays the groundwork for the data pipeline from front to back.

This work would not have been possible without the code written before me. In particular, I'd like to thank JJ Peters (https://github.com/JJPPeters/clTEM) and Adam Dyson (https://github.com/ADyson/clTEM) 
for designing CLTEM. Additionally, I'd like to thank Maxim Ziatdinov (https://github.com/ziatdinovmax) for his implementation of AtomAI which got this whole project off the ground. Lastly, I'd like to thank the hard work of my Linux-loving undergraduate Anas Ashraf of CCNY for his many hours poured into this project, and convincing me and my advisor that neural nets are the best way to analyze TEM images. 