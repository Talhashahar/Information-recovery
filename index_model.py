import os
import shutil
import docx2txt

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
    for file_name in file_list:
        text = file_to_text(file_name)
        if text is None:
            continue



def file_to_text(file_name):
    global folder_temp_index
    global folder_after_index
    file_type = file_name.split(".")
    if file_type == "txt":
        file = open(folder_temp_index+file_name, "r")
        text_from_file = file.read()
        return text_from_file
    elif file_type == "doc":
        text_from_file = docx2txt.process(folder_temp_index + file_name)
        return text_from_file
    elif file_type == "docx":
        text_from_file = docx2txt.process(folder_temp_index+file_name)
        return text_from_file
    else:
        print 'write to log the file cant be read'
        return None
