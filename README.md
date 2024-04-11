# RemoCar Demonstrator Build and Development

This is the main place for all developments and constructions of the RemoCar demonstrator of CR/AIE group.

Please use the official [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to flash images on to the sd cards.

For general information regarding usage of the TensorFlow on a Raspberry Pi check [here](https://www.tensorflow.org/lite/guide/python).

For information regarding the old version please check [here](https://inside-docupedia.bosch.com/confluence/display/EAIAB/DemoCar).

[Build SD image](documentation/sdImage.md)


[Remote connection](documentation/RemoteConnection.md)

For a general introduction on how to set-up and use a raspberry pi check [here](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up).


Steps to update sw:

- [x] Make new sd (admin, ssh, WiFi with intenrnet access)
- [x] raspi-config (camera, locale)
- [x] apt update, upgrade
- [x] set-up users, folders, permissions (https://www.geeksforgeeks.org/how-to-create-a-shared-folder-between-two-local-user-in-linux/)

- [x] install python3.9
- [x] install pip (sudo apt install python3-pip)
- [x] install tensorflow / (runtime)  check [here](https://www.tensorflow.org/lite/guide/python)
- [ ] install required packages
    - picamera
    - numpy

- [x] copy current version of the code
- [ ] collect new data
- [ ] train new model
- [ ] web stream
- [ ] new data collection method (step-wise + image size)
- [ ] collect extensive data (manual drive + lighting + places)
- [ ] define network structure using Nyle
- [ ] train the model
- [ ] test the model
- [ ] start HW modifications
- [ ] integrate required SW changes due to the HW
