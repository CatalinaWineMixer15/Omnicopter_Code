The zip file contains all of the python code necessary to get the omnicopter up and running with the MoCap system. It contains all of the different commands 
you could run in the MoCap room. In order to interface with the MoCap room at AFIT, you will need to go to http://www.nykl.net/aburn/ and follow Dr. Scott Nykl's instructions 
in his Youtube video (https://www.youtube.com/watch?v=hPGZf2dHSG0&t=637s). You might need Dr. Nykl's permission in order to access the aftrburner code. In the youtube video, 
you will only need to follow the instructions up until the 10:30 mark or so (before you compile the code). Once you follow the instructions, you will receive the 
optitrack_viewer program which allows you to connect to the cameras in the room. You will also need to have the Motive software running on a separate computer. In Motive, the 
omnicopter should be a defined object. If it is not, then you will need to build a new object for the omnicopter (see additional resources on how to do that). The 
omnicopter will have reflective markers around it, which allows the MoCap cameras to see the omnicopter.

Additionally, to access the flight control software running on the Kakute H7, you will need to connect your computer to the Kakute via USB and run QGroundControl. QGroundControl
can be downloaded from the following website: http://qgroundcontrol.com/

If you need to access the AM32 firmware on the ESCs, you can visit the following websites: https://esc-configurator.com/ or https://am32.ca/
You can use either website to access the firmware. **NOTE** AM32 can only be accessed when you have Betaflight running on your Kakute. It will not work with QGroundControl. You
must flash between the two FC softwares in order to access AM32. To flash Betaflight on the Kakute, you must first download the Betaflight configurator: https://betaflight.com/download
Once it is downloaded, hold down the bootloader button on the Kakute while connecting the USB cable from your computer. In the Betaflight configurator, you will see that the Kakute is
now in DFU mode. Go to the firmware flasher tab, choose the correct board and firmware version, and then click on 'Load Firmware [Online]'. Finally, flash the firmware and you should
have Betaflight on the Kakute once it is done flashing. In Betaflight, make sure to select an octocopter model. Otherwise, the AM32 firmware will not know how many motors you have on
the omnicopter. To flash back to QGroundControl/PX4, go back into the Betaflight configurator Firmware Flasher tab. Click on 'Load Firmware [Local]' and select the hex file that is
included in this repo titled 'holybro_kakuteh7_bootloader.hex'. You will then be able to connect to QGroundControl. In QGroundControl, go to the Firmware tab and select a custom
px4 file that is included in this repo titled 'holybro_kakuteh7_default.px4'. Lastly, go to the Parameters tab in QGroundControl and load the saved parameters. A copy of the latest
parameters titled 'kakuteh7Param.params' is included in this repo.
