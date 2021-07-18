#!/bin/bash

#########################################################################################################
#                                                                                                       #
#               TO BE CHANGED BASED ON YOUR DIRECTORIES PATH                                            #
#                                                                                                       #
#########################################################################################################

#Make sure all your directories path ends with /

#Directory containing all input xyz structures that are going to be simulated
inputStructurePath="/run/media/yuki/Storage/Documents/Photonics/clTEM/InputStructures/"

#Path to clTEM_cmd.exe for wine to use
clTEM_cmd_path="/home/yuki/Documents/Photonics/clTEM/clTEM_source/clTEM_cmd.exe"

#Path to input config files which contain subdirectories containing json file
inputFilesPath="/home/yuki/Documents/Photonics/clTEM/InputJsonFiles/"

#Output File for all the simulated Images
outputFilePath="/home/yuki/Documents/Photonics/clTEM/outputFiles/"

#Number of simulated image for EACH structure that you want, we begin counting from 1
numberOfSimulatedImages=2




#########################################################################################################
#                                                                                                       #
#               DO NOT CHANGE UNLESS YOU KNOW WHAT YOU ARE DOING                                        #
#                                                                                                       #
#########################################################################################################
typesOfStructures=(.xyz .cif)



xyzFileNamesWithExtensions=($(cd "$inputStructurePath" && ls *.xyz))        #only catch .xyz files with *.xyz
xyzFileNamesWithoutExtensions=("${xyzFileNamesWithExtensions[@]%%.*}")      #[@] prints all members in array and %%.* excludes the file extension
echo "\n The xyz files loaded are: $xyzFileNamesWithoutExtensions"

cifFileNamesWithExtensions=($(cd "$inputStructurePath" && ls *.cif))        #only catch .xyz files with *.cif
cifFileNamesWithoutExtensions=("${cifFileNamesWithExtensions[@]%%.*}")      #[@] prints all members in array and %%.* excludes the file extension
echo "\n The cif files loaded are: $cifFileNamesWithoutExtensions"

dateAndTime=$(date +"%Y-%m-%d_%H-%M-%S")                                    #get date and time to uniquely create and store outputs

echo "### CREATE RELEVANT DIRECTORIES FOR XYZ/CIF AND ALL OUTPUT IMAGES ####\n"

#First create the date directory which stores all the files made at a certain time
mkdir $outputFilePath$dateAndTime  && echo "Created directory $dateAndTime in $outputFilePath to record the results"

#Now save all the xyz output files in the dateAndTime directory in the output file path

for xyzOutputDirectories in $xyzFileNamesWithoutExtensions
do
    mkdir $outputFilePath$dateAndTime"/"$xyzOutputDirectories && echo "Created $xyzOutputDirectories in $outputFilePath$dateAndTime to store the results for the specific structure"
done

for cifOutputDirectories in $cifFileNamesWithoutExtensions
do
    mkdir $outputFilePath$dateAndTime"/"$cifOutputDirectories && echo "Created $cifOutputDirectories in $outputFilePath$dateAndTime to store the results for the specific structure"
done

#Create directory called allImages
mkdir $outputFilePath$dateAndTime"/allImages" && echo "Created directory allImages in $outputFilePath$dateAndTime to store all the images"

echo "\n### END OF DIRECTORY CREATION ###\n"


totalxyzFiles=${#xyzFileNamesWithExtensions[@]} #store total number of xyz files for later
totalcifFiles=${#cifFileNamesWithExtensions[@]} #store total number of cif files for later



for i in {1..${#xyzFileNamesWithExtensions[@]}}                 #simulate all the xyz structures
do
    for numberOfConfigFiles in {1..$numberOfSimulatedImages}    #Cycle through number of config json files upto numberofSimulatedImages, make sure number of config json files is >=
    do
        #Run wine to simulate the batch of images
        wine $clTEM_cmd_path --debug $inputStructurePath$xyzFileNamesWithExtensions[i] -o $outputFilePath$dateAndTime"/"$xyzFileNamesWithoutExtensions[i]"/"$numberOfConfigFiles -d all -c $inputFilesPath"config"$numberOfConfigFiles".json"

        #Delete the EW and Diffraction files that are not needed and are bugged anyway
        cd $outputFilePath$dateAndTime"/"$xyzFileNamesWithoutExtensions[i]"/"$numberOfConfigFiles && rm -rf Diff.* EW_amplitude.* EW_phase.* && echo "\n### Removing all unnecessary files ###\n" || echo "\n###No unnecessary files needed to be deleted###\n"

        #Move the files Image.tif from the output folder to the folder called allImages
        mv $outputFilePath$dateAndTime"/"$xyzFileNamesWithoutExtensions[i]"/"$numberOfConfigFiles"/Image.tif" $outputFilePath$dateAndTime"/allImages/"$xyzFileNamesWithoutExtensions[i]"-Image"$numberOfConfigFiles".tif" && echo "\n### Moved Image for config >$numberOfConfigFiles< for structure >${xyzFileNamesWithoutExtensions[i]}< into allImages directory###\n" || echo "\n### Error Image.tif not found###\n"

        #Print status report or display a progress bar of sorts
        echo "\n###########################################################################\n#\n# FINISHED $numberOfConfigFiles out of $numberOfSimulatedImages for structure $i of ${#xyzFileNamesWithExtensions[@]} for xyz structures  \n#\n###########################################################################"
    done
done



for i in {1..${#cifFileNamesWithExtensions[@]}}                 #simulate all the cif structures
do
    for numberOfConfigFiles in {1..$numberOfSimulatedImages}    #Cycle through number of config json files upto numberofSimulatedImages, make sure number of config json files is >=
    do
        #Run wine to simulate the batch of images
        wine $clTEM_cmd_path --debug $inputStructurePath$cifFileNamesWithExtensions[i] -s 100,100,100 -z 0,0,1 -o $outputFilePath$dateAndTime"/"$cifFileNamesWithoutExtensions[i]"/"$numberOfConfigFiles -d all -c $inputFilesPath"config"$numberOfConfigFiles".json"

        #Delete the EW and Diffraction files that are not needed and are bugged anyway
        cd $outputFilePath$dateAndTime"/"$cifFileNamesWithoutExtensions[i]"/"$numberOfConfigFiles && rm -rf Diff.* EW_amplitude.* EW_phase.* && echo "\n### Removing all unnecessary files ###\n" || echo "\n###No unnecessary files needed to be deleted###\n"

        #Move the files Image.tif from the output folder to the folder called allImages
        mv $outputFilePath$dateAndTime"/"$cifFileNamesWithoutExtensions[i]"/"$numberOfConfigFiles"/Image.tif" $outputFilePath$dateAndTime"/allImages/"$cifFileNamesWithoutExtensions[i]"-Image"$numberOfConfigFiles".tif" && echo "\n### Moved Image for config >$numberOfConfigFiles< for structure >${cifFileNamesWithoutExtensions[i]}< into allImages directory###\n" || echo "\n### Error Image.tif not found###\n"

        #Print status report or display a progress bar of sorts
        echo "\n###########################################################################\n#\n# FINISHED $numberOfConfigFiles out of $numberOfSimulatedImages for structure $i of ${#cifFileNamesWithExtensions[@]} for cif structures  \n#\n###########################################################################"
    done
done

