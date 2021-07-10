import random
import os
import sys


def main():
    save_directory = sys.argv[1]
    print(sys.argv[1])
    num_files = sys.argv[2]
    z_len = len(str(num_files))
    for i in range(0, int(num_files)):
        file_name = "config" + str(i).zfill(z_len)
        save_path = save_directory + file_name
        write_json(save_path)


def write_json(json_file, c10=random.randint(-20, 20), c30=random.randint(-20, 20), c50=random.randint(1000, 5000),
               c12=random.randint(0, 0), tilt=0, angle=0, angle1=0, resolution=1024):
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
    file.write(str(c10))
    file.write('\n')                      # mark this one -20 to 20
    file.write('},\n')
    file.write('"C12": {\n')
    file.write('"ang": ')                     # mark this one to be max 360 degrees
    file.write(str(angle))
    file.write(',\n')
    file.write('"mag": ')
    file.write(str(c12))
    file.write(',\n')                     # mark this one to be max 10
    file.write('"units": "nm, °"\n')
    file.write('},\n')
    file.write('"C21": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": 0.0,\n')
    file.write('"units": "nm, °"\n')
    file.write('},\n')
    file.write('"C23": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": 0.0,\n')
    file.write('"units": "nm, °"\n')
    file.write('},\n')
    file.write('"C30": {\n')
    file.write('"units": "μm",\n')
    file.write('"val": ')
    file.write(str(c30))
    file.write('\n')                      # mark this one to be -20 to 20
    file.write('},\n')
    file.write('"C32": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": 0.0,\n')
    file.write('"units": "μm, °"\n')
    file.write('},\n')
    file.write('"C34": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": 0.0,\n')
    file.write('"units": "μm, °"\n')
    file.write('},\n')
    file.write('"C41": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": 0.0,\n')
    file.write('"units": "μm, °"\n')
    file.write('},\n')
    file.write('"C43": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": 0.0,\n')
    file.write('"units": "μm, °"\n')
    file.write('},\n')
    file.write('"C45": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": 0.0,\n')
    file.write('"units": "μm, °"\n')
    file.write('},\n')
    file.write('"C50": {\n')
    file.write('"units": "μm",\n')
    file.write('"val": ')
    file.write(str(c50))
    file.write('\n')                       # mark this to be 0 to 5000
    file.write('},\n')
    file.write('"C52": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": 0.0,\n')
    file.write('"units": "μm, °"\n')
    file.write('},\n')
    file.write('"C54": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": 0.0,\n')
    file.write('"units": "μm, °"\n')
    file.write('},\n')
    file.write('"C56": {\n')
    file.write('"ang": 0.0,\n')
    file.write('"mag": 0.0,\n')
    file.write('"units": "μm, °"\n')
    file.write('}\n')
    file.write('},\n')
    file.write('"beam tilt": {\n')
    file.write('"azimuth": {\n')
    file.write('"units": "°",\n')
    file.write('"val": ')
    file.write(str(angle1))
    file.write('\n')                      # mark this to be up to 360
    file.write('},\n')
    file.write('"inclination": {\n')
    file.write('"units": "mrad",\n')
    file.write('"val": ')
    file.write(str(tilt))
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
    file.write(str(resolution))
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

if __name__ == "__main__":
    main()