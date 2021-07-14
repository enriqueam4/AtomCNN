# Here we have a file which creates random parameters for microscope and saves them as json files
import random
import os
import sys
import getopt
from dataclasses import dataclass

allowedResolutions = [256,512,768,1024,1536,2048,3072,4096,8192]

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hr:o:n:", ["help", "outputDirectory=","numFiles=","resolution="])   #argv[0] is simply name of the python file so we ignore it and pick up arguments from 1
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    save_directory = ""     #directory you will be saving output to
    num_files = ""          #the number of files you wish to generate
    resolution = ""
    for o, a in opts:
        if o in ("-h", "--help"):
            usageHelp()
            sys.exit()
        elif o in ("-o", "--outputDirectory"):
            save_directory = a
        elif o in ("-n", "--numFiles"):
            num_files = a
        elif o in ("-r", "--resolution"):
            resolution = a
        else:
            assert False, "unhandled option"

    #Checks if num_files is blank and if so print usage and exit
    if not num_files:
        usage()
        sys.exit()

    #Checks if resolution was specified and if not sets default value to 1024, and checks if resolution is legal
    if not resolution:
        resolution= "1024"
    elif int(resolution) not in allowedResolutions:
        print("Input resolution is ", resolution, " but allowed resolutions are ", allowedResolutions)
        sys.exit()


    z_len = len(str(num_files))
    for i in range(0, int(num_files)):
        file_name = "config" + str(i).zfill(z_len)
        save_path = save_directory + file_name
        p = microscope_params()                     # should call a different set of random variables each time
        p.resolution = resolution
        write_json(save_path, p)

    print("Generated", num_files, "config files in the directory", save_directory, "of resolution", p.resolution)



def usage():
    print("REQUIRED output directory path that MUST end with / (-o, --outputDirectory)")
    print("REQUIRED number of files to generate argument (-n, --numFiles)")
    print("OPTIONAL the resolution of the images in config file (-r, --resolution)")
    print("Type\n\tpython generateConfigFiles.py -h\nfor extended help dialogue")

def usageHelp():
    print("Usage: python generateConfigFiles.py -o <path to output directory> -n <number of files you wish to generate>")
    print("Example usage:\n\t python generateConfigFiles.py -o /run/media/ligma/tmp/ -n 10 -r 3072")
    print("Example above creates 10 config files in the directory /run/media/ligma/tmp/ with resolution 3072\n")
    print("Options:")
    print("-h : (--help) print this help message and exit")
    print("-o : (--outputDirectory) REQUIRED specify the output directory path you wish to save all the files to, the directory MUST already exist. Make sure path ends with /")
    print("-n : (--numFiles) REQUIRED specify the number of config files you would like to generate")
    print("-r : (--resolution) OPTIONAL specify the resolution you would like to have for the images. Default is 1024, options are ", allowedResolutions)

def write_json(json_file, p):
    file = open(json_file + ".json", "w", encoding='utf-8')
    file.write('{\n')
    file.write('"cbed": {\n')
    file.write('"position": {\n')
    file.write('"padding": 0.0,\n')
    file.write('"units": "Å",\n')
    file.write('"x": 0.0,\n')
    file.write('"y": 0.0\n')
    file.write('}\n')
    file.write('},\n')
    file.write('"ctem": {\n')
    file.write('"ccd": {\n')
    file.write('"binning": 1,\n')
    file.write('"dose": {\n')
    file.write('"units": "e- per square Å",\n')
    file.write('"val": 10000.0\n')
    file.write('},\n')
    file.write('"name": "Orius"\n')
    file.write('},\n')
    file.write('"cropped padding": true\n')
    file.write(',\n')
    file.write('"simulate image": true\n')
    file.write('},\n')
    file.write('"default padding": {\n')
    file.write('"xy": {\n')
    file.write('"units": "Å",\n')
    file.write('"val": 8.0\n')
    file.write('},\n')
    file.write('"z": {\n')
    file.write('"units": "Å",\n')
    file.write('"val": 3.0\n')
    file.write('}\n')
    file.write('},\n')
    file.write('"double precision": false,\n')
    file.write('"full 3d": {\n')
    file.write('"integrals": 20,\n')
    file.write('"state": false\n')
    file.write('},\n')
    file.write('"incoherence": {\n')
    file.write('"inelastic scattering": {\n')
    file.write('"phonon": {\n')
    file.write('"default": 0.0,\n')
    file.write('"force default": false,\n')
    file.write('"override file": false,\n')
    file.write('"units": "Å²"\n')
    file.write('},\n')
    file.write('"plasmon": {\n')
    file.write('"characteristic angle": {\n')
    file.write('"unit": "mrad",\n')
    file.write('"value": 1.0\n')
    file.write('},\n')
    file.write('"critical angle": {\n')
    file.write('"unit": "mrad",\n')
    file.write('"value": 0.1\n')
    file.write('},\n')
    file.write('"individual": 1,\n')
    file.write('"mean free path": {\n')
    file.write('"unit": "nm",\n')
    file.write('"value": 1.0\n')
    file.write('},\n')
    file.write('"type": "full"\n')
    file.write('}\n')
    file.write('},\n')
    file.write('"iterations": 1,\n')
    file.write('"probe": {\n')
    file.write('"chromatic": {\n')
    file.write('"Cc": {\n')
    file.write('"units": "mm",\n')
    file.write('"val": 0.0\n')
    file.write('},\n')
    file.write('"dE": {\n')
    file.write('"HWHM +": 0.0,\n')
    file.write('"HWHM -": 0.0,\n')
    file.write('"units": "eV"\n')
    file.write('},\n')
    file.write('"enabled": false\n')
    file.write('},\n')
    file.write('"source size": {\n')
    file.write('"FWHM": {\n')
    file.write('"units": "Å",\n')
    file.write('"val": 0.0\n')
    file.write('},\n')
    file.write('"enabled": false\n')
    file.write('}\n')
    file.write('}\n')
    file.write('},\n')
    file.write('"intermediate output": {\n')
    file.write('"enabled": false,\n')
    file.write('"slice interval": 0\n')
    file.write('},\n')
    file.write('"maintain areas": false,\n')
    file.write('"microscope": {\n')
    file.write('"aberrations": {\n')
    file.write('"C10": {\n')
    file.write('"units": "nm",\n')
    file.write('"val": ')
    file.write(str(p.c10))
    file.write('\n')                      # mark this one -20 to 20
    file.write('},\n')
    file.write('"C12": {\n')
    file.write('"ang": ')                     # mark this one to be max 360 degrees
    file.write(str(p.angle))
    file.write(',\n')
    file.write('"mag": ')
    file.write(str(p.c12))
    file.write(',\n')                     # mark this one to be max 10
    file.write('"units": "nm, °"\n')
    file.write('},\n')
    file.write('"C21": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": ')
    file.write(str(p.c21))
    file.write(',\n')
    file.write('"units": "nm, °"\n')
    file.write('},\n')
    file.write('"C23": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": ')
    file.write(str(p.c23))
    file.write(',\n')
    file.write('"units": "nm, °"\n')
    file.write('},\n')
    file.write('"C30": {\n')
    file.write('"units": "μm",\n')
    file.write('"val": ')
    file.write(str(p.c30))
    file.write('\n')                      # mark this one to be -20 to 20
    file.write('},\n')
    file.write('"C32": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": ')
    file.write(str(p.c32))
    file.write(',\n')
    file.write('"units": "μm, °"\n')
    file.write('},\n')
    file.write('"C34": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": ')
    file.write(str(p.c34))
    file.write(',\n')
    file.write('"units": "μm, °"\n')
    file.write('},\n')
    file.write('"C41": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": ')
    file.write(str(p.c41))
    file.write(',\n')
    file.write('"units": "μm, °"\n')
    file.write('},\n')
    file.write('"C43": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": ')
    file.write(str(p.c43))
    file.write(',\n')
    file.write('"units": "μm, °"\n')
    file.write('},\n')
    file.write('"C45": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": ')
    file.write(str(p.c45))
    file.write(',\n')
    file.write('"units": "μm, °"\n')
    file.write('},\n')
    file.write('"C50": {\n')
    file.write('"units": "μm",\n')
    file.write('"val": ')
    file.write(str(p.c50))
    file.write('\n')                       # mark this to be 0 to 5000
    file.write('},\n')
    file.write('"C52": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": ')
    file.write(str(p.c52))
    file.write(',\n')
    file.write('"units": "μm, °"\n')
    file.write('},\n')
    file.write('"C54": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": ')
    file.write(str(p.c54))
    file.write(',\n')
    file.write('"units": "μm, °"\n')
    file.write('},\n')
    file.write('"C56": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": ')
    file.write(str(p.c56))
    file.write(',\n')
    file.write('"units": "μm, °"\n')
    file.write('}\n')
    file.write('},\n')
    file.write('"beam tilt": {\n')
    file.write('"azimuth": {\n')
    file.write('"units": "°",\n')
    file.write('"val": ')
    file.write(str(p.angle1))
    file.write('\n')                      # mark this to be up to 360
    file.write('},\n')
    file.write('"inclination": {\n')
    file.write('"units": "mrad",\n')
    file.write('"val": ')
    file.write(str(p.tilt))
    file.write('\n')                      # mark this one to be up to 1-3
    file.write('}\n')
    file.write('},\n')
    file.write('"condenser aperture": {\n')
    file.write('"semi-angle": 20.0,\n')
    file.write('"smoothing": 0.0,\n')
    file.write('"units": "mrad"\n')
    file.write('},\n')
    file.write('"objective aperture": {\n')
    file.write('"semi-angle": 77.0,\n')
    file.write('"smoothing": 0.0,\n')
    file.write('"units": "mrad"\n')
    file.write('},\n')
    file.write('"voltage": {\n')
    file.write('"units": "kV",\n')
    file.write('"val": 80.0\n')
    file.write('}\n')
    file.write('},\n')
    file.write('"mode": {\n')
    file.write('"id": 1,\n')
    file.write('"name": "CTEM"\n')
    file.write('},\n')
    file.write('"potentials": "kirkland",\n')
    file.write('"resolution": ')
    file.write(str(p.resolution))
    file.write(',\n')
    file.write('"slice offset": {\n')
    file.write('"units": "Å",\n')
    file.write('"val": 0.55\n')
    file.write('},\n')
    file.write('"slice thickness": {\n')
    file.write('"units": "Å",\n')
    file.write('"val": 1.65\n')
    file.write('},\n')
    file.write('"stem": {\n')
    file.write('"area": {\n')
    file.write('"padding": {\n')
    file.write('"units": "Å",\n')
    file.write('"val": 0.0\n')
    file.write('},\n')
    file.write('"x": {\n')
    file.write('"finish": 10.0,\n')
    file.write('"start": 0.0,\n')
    file.write('"units": "Å"\n')
    file.write('},\n')
    file.write('"y": {\n')
    file.write('"finish": 10.0,\n')
    file.write('"start": 0.0,\n')
    file.write('"units": "Å"\n')
    file.write('}\n')
    file.write('},\n')
    file.write('"concurrent pixels": 1,\n')
    file.write('"scan": {\n')
    file.write('"x": {\n')
    file.write('"pixels": 64\n')
    file.write('},\n')
    file.write('"y": {\n')
    file.write('"pixels": 64\n')
    file.write('}\n')
    file.write('}\n')
    file.write('}\n')
    file.write('}\n')
    file.close()


@dataclass
class microscope_params:
    def __init__(self):
        c10 = random.randint(-20, 20)
        self.c10 = c10
        c12 = random.randint(0, 5)
        self.c12 = c12
        c21 = random.randint(0, 50)
        self.c21 = c21
        c23 = random.randint(0, 100)
        self.c23 = c23
        c30 = random.randint(-20, 20)
        self.c30 = c30
        self.c32 = 0
        self.c34 = 0
        self.c41 = 0
        self.c43 = 0
        self.c45 = 0
        c50 = random.randint(1000, 5000)
        self.c50 = c50
        self.c52 = 0
        self.c54 = 0
        self.c56 = 0
        self.tilt = 0
        self.angle = 0
        self.angle1 = 0
        self.resolution = 1024


if __name__ == "__main__":
    main()

# Enrique Mejia #girlboss #hashtag #girlpower #gaslight
