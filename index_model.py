import os
import shutil

''' configutions '''
folder_before_index = 'C:\\Users\\talha_000\\PycharmProjects\\GoogleV2\\data\\Original\\'
folder_temp_index = 'C:\\Users\\talha_000\\PycharmProjects\\GoogleV2\\data\\temp\\'
folder_after_index = 'C:\\Users\\talha_000\\PycharmProjects\\GoogleV2\\data\\indexed\\'



def find_new_files_and_move_temp_folder():
    global folder_before_index
    global folder_temp_index
    file_list = os.listdir(folder_before_index)
    if len(file_list) != 0:
        for file in file_list:
            try:
                shutil.move(folder_before_index+file, folder_temp_index+file)
            except:
                print 'write to log the exption'


def index_files_from_temp_folder():
    global folder_temp_index
    global folder_after_index
    file_list = os.listdir(folder_temp_index)
