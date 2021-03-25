# Metre_AppUI_v0.12

1) MainMetre.py is the installer/code launcher. **If the root directory (MetreiOS) already exists** on your device, it will look for metre_ios_install_config.json and launch the most current version of the app (from a subdirectory in MetreiOS) OR it will download the most current version of the app from GitHub, installed as a subdirectory in MetreiOS. If an older version of the app exists, the log files (for remembering the device, timezone, storage of previous data) will get copied over to the new app subdirectory. **If the MetreiOS subdirectory does not exist** it will download that root directory and make metre_ios_install_config.json (version # is hard-coded into a dictionary written in MainMetre.py). The script that "does stuff" and makes the UI is the script MetreUI.py

2) MetreUI.py makes the UI. Currently, as written, this version of the code expects to receive a json file (similar to the format in temp_resources). It looks for files that are located in the folder temp_resources. It processes the test by calling the script process_test.py, which does the mV rolling mean and various metadata calculations, adds the keys to the dictionary. The dietionary gets returned to MetreUI.py (the main script) and pushes it to the cloud function 'https://us-central1-metre3-1600021174892.cloudfunctions.net/metre-7500'.

3) The cloud function writes the metadata to a common log, saves the incoming (single) json file, runs the prediction, and returns the prediction to MetreUI.py

4) MetreUI.py receives the response from the cloud function, displays the result and writes it to the log.

5) If multiple files are present in temp_resources, multiple files will be uploaded.

Things we need to do:
1) Pull the bin file and the metadata file from the instrument (do file matching)
2) Delete the matched files from the instrument (or move them to a different directory)
3) Convert the bin to floats
4) Combine the sample data and metadata in a single json

This can be directly integrated into my app if the bluetooth upload and file conversion all happens in one script


Minor changes
1) Change location of file dump
2) Re-call status bar 
