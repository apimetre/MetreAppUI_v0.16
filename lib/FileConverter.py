# Python imports
import json
import shutil
import os
import time
import numpy as np
from binascii import hexlify

# Pythonista imports
import ui


class FileConverter():
    def __init__(self, progress_bar_, console_box_, bad_transfers):
        self.progress_bar_ = progress_bar_
        self.console_box_ = console_box_
        self.bad_transfers = bad_transfers
        
    def datfile_to_dict(self,file_path, scalar=1.0):
        count = 0
        data = []
        with open(file_path, 'rb') as f:
            while True:
                two_bytes = f.read(2)
                if not two_bytes:
                    break
                data.append(scalar * int.from_bytes(two_bytes, byteorder='big', signed = True))
        return data


    def match_files(self, file_source, file_dest, json_dest):
        all_uploads = os.listdir(file_source)
        for file in all_uploads:
            # Current fill 
            current_percent_fill = self.progress_bar_.fillbar_.width/ self.progress_bar_.fullbar_
            self.progress_bar_.update_progress_bar((all_uploads.index(file) + 1)*.01 + current_percent_fill)
            if 'bin' in file:
                id_num, ext = file.split('.')

                
                #try:
               # Look for matching json file (containing metadata)
                try:
                    metadata_json = file_source + '/' + id_num + '.json'
                    with open(metadata_json) as f:
                        mdata_dict = json.load(f)
                        sensor = mdata_dict['fuel_cell_sn'].split('#')[1]
                        instr = mdata_dict['device_sn'].split('#')[1]
                    # Do file bin to float conversion
                    data_list = np.array(self.datfile_to_dict(file_source + '/' + file ))     
                    if len(self.bad_transfers) > 0:
                        file_ix = [idx for idx, s in enumerate(self.bad_transfers) if id_num in s]
                        bad_file_name = [self.bad_transfers[i] for i in file_ix] 
                        bad_file_size = [self.bad_transfers[i+1] for i in file_ix] 
                        mdata_dict['Upload_Issues'] = bad_file_name + bad_file_list
                    else:
                        mdata_dict['Upload_Issues'] = []
                    mdata_dict['data'] = list(data_list)
                    mdata_dict['new_baseline'] = 0
                    id_string = id_num + '-' + str(instr) + '-' + str(sensor)
                    mdata_dict['FileNum'] = id_string
                    mdata_dict['Data_pts'] = len(data_list)
                    
                    export_fpath = json_dest + '/' + id_string + '.json'
                    
                    # Move processed bin and json out of directory
                    shutil.move(file_source + '/'+ file, file_dest + '/' + file)
                    shutil.move(metadata_json, file_dest + '/' + id_num + '.json')
                    current_percent_fill = self.progress_bar_.fillbar_.width/ self.progress_bar_.fullbar_
                    self.progress_bar_.update_progress_bar((all_uploads.index(file) + 1)*.01 + current_percent_fill)
                    with open(export_fpath, 'w') as outfile:
                        json.dump(mdata_dict, outfile)
                except:
                    self.console_box_.text = "One of your test files can't be processed. Mouthpiece ejected too soon?"
                    shutil.move(file_source + '/'+ file, file_dest + '/' + file)
                    time.sleep(3)
                    continue
        match_status = True
        self.console_box_.text = 'Starting data processing...'
        return match_status
