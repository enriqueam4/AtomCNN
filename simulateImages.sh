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

#Number of simulated image for EACH structure that you want, we begin counting from 0
numberOfSimulatedImages=0










#########################################################################################################
#                                                                                                       #
#               DO NOT CHANGE UNLESS YOU KNOW WHAT YOU ARE DOING                                        #
#                                                                                                       #
#########################################################################################################

xyzFileNamesWithExtensions=($(cd "$inputStructurePath" && ls *.xyz))        #only catch .xyz files with *.xyz
xyzFileNamesWithoutExtensions=("${xyzFileNamesWithExtensions[@]%%.*}")      #[@] prints all members in array and %%.* excludes the file extension
echo "\n The xyz files loaded are: $xyzFileNamesWithoutExtensions"

cifFileNamesWithExtensions=($(cd "$inputStructurePath" && ls *.cif))        #only catch .xyz files with *.cif
cifFileNamesWithoutExtensions=("${cifFileNamesWithExtensions[@]%%.*}")      #[@] prints all members in array and %%.* excludes the file extension
echo "\n The cif files loaded are: $cifFileNamesWithoutExtensions"

dateAndTime=$(date +"%Y-%m-%d_%H-%M-%S")                                    #get date and time to uniquely create and store outputs




echo "### CREATE RELEVANT DIRECTORIES FOR XYZ/CIF AND ALL OUTPUT IMAGES ####\n"
for xyzOutputDirectories in $xyzFileNamesWithoutExtensions
do
    mkdir $outputFilePath$xyzOutputDirectories"-"$dateAndTime && echo "Created $outputFilePath$xyzOutputDirectories"-"$dateAndTime"
done

for cifOutputDirectories in $cifFileNamesWithoutExtensions
do
    mkdir $outputFilePath$cifOutputDirectories"-"$dateAndTime && echo "Created $outputFilePath$cifOutputDirectories"-"$dateAndTime"
done

#Create directory called allImages
mkdir $outputFilePath"allImages-"$dateAndTime

echo "\n### END OF DIRECTORY CREATION ###\n"


totalxyzFiles=${#xyzFileNamesWithExtensions[@]} #store total number of xyz files for later
totalcifFiles=${#cifFileNamesWithExtensions[@]} #store total number of cif files for later


for i in {1..${#xyzFileNamesWithExtensions[@]}}                 #simulate all the structures
do
    for numberOfConfigFiles in {0..$numberOfSimulatedImages}    #Cycle through number of config json files upto numberofSimulatedImages, make sure number of config json files is >=
    do
        #Run wine to simulate the batch of images
        wine $clTEM_cmd_path --debug $inputStructurePath$xyzFileNamesWithExtensions[i] -o $outputFilePath$xyzFileNamesWithoutExtensions[i]"-"$dateAndTime"/"$numberOfConfigFiles -d all -c $inputFilesPath$numberOfConfigFiles"/config.json"

        #Delete the EW and Diffraction files that are not needed and are bugged anyway
        cd $outputFilePath$xyzFileNamesWithoutExtensions[i]"-"$dateAndTime"/"$numberOfConfigFiles && rm -rf Diff.* EW_amplitude.* EW_phase.* && echo "\n### Removing all unnecessary files ###\n" || echo "\n###No unnecessary files needed to be deleted###\n"

        #Move the files Image.tif from the output folder to the folder called allImages
        mv $outputFilePath$xyzFileNamesWithoutExtensions[i]"-"$dateAndTime"/"$numberOfConfigFiles"/Image.tif" $outputFilePath"allImages-$dateAndTime/"$xyzFileNamesWithoutExtensions[i]"-Image"$numberOfConfigFiles".tif" && echo "\n### Moved Image for config >$numberOfConfigFiles< for structure >${xyzFileNamesWithoutExtensions[i]}< into allImages directory###\n" || echo "\n### Error Image.tif not found###\n"

        #Print status report or display a progress bar of sorts
        echo "\n###########################################################################\n#\n# FINISHED $numberOfConfigFiles out of $numberOfSimulatedImages for structure $i of ${#xyzFileNamesWithExtensions[@]} for xyz structures  \n#\n###########################################################################"
    done
done


###########Now do the same for cif since they need an additional argument for size and zone ##############################

for i in {1..${#cifFileNamesWithExtensions[@]}}                 #simulate all the structures
do
    for numberOfConfigFiles in {0..$numberOfSimulatedImages}    #Cycle through number of config json files upto numberofSimulatedImages, make sure number of config json files is >=
    do
        #Run wine to simulate the batch of images
        wine $clTEM_cmd_path $inputStructurePath$cifFileNamesWithExtensions[i] -s 100,100,100 -z 0,0,1 -o $outputFilePath$cifFileNamesWithoutExtensions[i]"-"$dateAndTime"/"$numberOfConfigFiles -d all -c $inputFilesPath$numberOfConfigFiles"/config.json"

        #Delete the EW and Diffraction files that are not needed and are bugged anyway
       cd $outputFilePath$cifFileNamesWithoutExtensions[i]"-"$dateAndTime"/"$numberOfConfigFiles && rm -rf Diff.* EW_amplitude.* EW_phase.* && echo "\n### Removing all unnecessary files ###\n" || echo "\n###No unnecessary files needed to be deleted###\n"

        #Move the files Image.tif from the output folder to the folder called allImages
      mv $outputFilePath$cifFileNamesWithoutExtensions[i]"-"$dateAndTime"/"$numberOfConfigFiles"/Image.tif" $outputFilePath"allImages-$dateAndTime/"$cifFileNamesWithoutExtensions[i]"-Image"$numberOfConfigFiles".tif" && echo "\n### Moved Image for config >$numberOfConfigFiles< for structure >${cifFileNamesWithoutExtensions[i]}< into allImages directory###\n" || echo "\n### Error Image.tif not found###\n"

        #Print status report or display a progress bar of sorts
        echo "\n###########################################################################\n#\n# FINISHED $numberOfConfigFiles out of $numberOfSimulatedImages for structure $i of ${#cifFileNamesWithExtensions[@]} for cif structures  \n#\n###########################################################################"
    done
done

