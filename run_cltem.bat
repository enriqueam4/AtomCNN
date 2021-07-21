@echo off
SetLocal EnableDelayedExpansion
echo %TIME% %DATE% > log.log

echo Current Directory: %cd% >> log.log

set project_name=jul21_test3

set structure_file="%cd%\structures\hBN extracarbon cif\CbVn_VbCn_large.cif"
if exist %structure_file% (echo %structure_file% exists >> log.log ) else ( echo file %structure_file% does not exist, exiting >> log.log && exit \b 0)

set gt_im="%cd%\structures\hBN extracarbon cif\gt.tif"
if exist %gt_im% (echo %gt_im% exists >> log.log ) else ( echo file %gt_im% does not exist, exiting >> log.log && exit \b 0)

set h5_directory=%cd%\h5_files
if not exist %h5_directory% ( echo %h5_directory% created >> log.log && mkdir %h5_directory% ) 
echo %h5_directory% exists >> log.log

set h5_file=%h5_directory%\%project_name%.h5

echo %h5_file% >> log.log

set model_directory=%cd%\models\%project_name%
if exist %model_directory% ( echo %model_directory% exists, change project_name to unique name >> log.log && exit \b 0) 
mkdir %model_directory% 
echo %model_directory% created >> log.log

set model_file=%model_directory%\%project_name%.pt

set config_directory=%cd%\configs
if exist %config_directory% ( echo %config_directory% exists, removing and recreating >> log.log && rmdir %config_directory%) 
mkdir %config_directory% 
echo %config_directory% created >> log.log

python %cd%/python/generateConfigFiles.py %config_directory%/ 10

set cltem="C:\Program Files\clTEM\cltem_cmd.exe"
if exist %cltem% ( echo %cltem% exists >> log.log) else ( echo file %cltem% does not exist, exiting >> log.log && exit \b 0)

set output_directory=%cd%\out
if exist %output_directory% ( echo %output_directory% exists, removing and recreating >> log.log && rmdir %output_directory%) 
mkdir %output_directory% 
echo %output_directory% created >> log.log


for /F "delims=" %%i in ("%structure_file%") do ( set extension=%%~xi && echo fileextension=!extension! >> log.log )

set count=0
for %%f in (%config_directory%\*) do (
	if exist %output_directory%\!count! (rmdir %output_directory%\!count!)
	mkdir %output_directory%\!count!
	if %extension%==.xyz (%cltem% %structure_file% -o %output_directory%\!count! -c %%f -d all)
	if %extension%==.cif (%cltem% %structure_file% -s "100,100,100" -z "0,0,1" -o %output_directory%\!count! -c %%f -d all) 
	del %output_directory%\!count!\"Diff.tif"
	del %output_directory%\!count!\"Diff.json"
	del %output_directory%\!count!\"EW_Amplitude.tif"
	del %output_directory%\!count!\"EW_Amplitude.json"
	del %output_directory%\!count!\"EW_Phase.tif"
	del %output_directory%\!count!\"EW_Phase.json"
	del %output_directory%\!count!\"Image.json"
	move %%f %output_directory%\!count!\"Image.json"
	set /a count+=1
	echo !count!)
	
echo Config Files Loaded >> log.log
echo h5stuffer.py running >> log.log
python %cd%\python\h5stuffer.py %output_directory% %gt_im% %h5_file% || pause
echo h5stuffer.py complete >> log.log
python %cd%\python\Local_Train.py %h5_file% %model_directory%\%project_name% 3 || pause
echo Local_Train.py complete >> log.log
echo modeleval.py started >> log.log
python %cd%\python\model_eval.py %h5_file% %model_directory%\%project_name%-1-best_weights.pt %model_directory%

endlocal

del myeasylog.log