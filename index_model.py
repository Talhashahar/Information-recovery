import os
import shutil
import docx2txt
import db_model
import re

''' configutions '''
folder_before_index = 'C:\Information_Retrive\\data\\Original\\'
folder_temp_index = 'C:\Information_Retrive\\data\\temp\\'
folder_after_index = 'C:\Information_Retrive\\data\\indexed\\'


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
        current_doc_index = db_model.retrive_doc_index_from_db()
        text = file_to_text(file_name)
        text = remove_signs_from_text(text)
        db_model.insert_doc_detail(file_name.split('.')[0], current_doc_index, text.split("\n")[0] + text.split("\n")[1])
        if text is None:
            continue
        words_dict = parse_test_into_dict(text)
        for word, count in words_dict.items():
            db_model.insert_words_to_db(word, count, current_doc_index)
        shutil.move(folder_temp_index + file_name, folder_after_index + "doc_" + str(current_doc_index) + "." + file_name.split(".")[1])
        db_model.inc_doc_index()


def file_to_text(file_name):
    global folder_temp_index
    global folder_after_index
    file_type = file_name.split(".")[1]
    if file_type == "txt":
        file = open(folder_temp_index+file_name, "r")
        text_from_file = file.read().lower()
        return text_from_file
    elif file_type == "doc":
        text_from_file = docx2txt.process(folder_temp_index + file_name)
        return text_from_file.lower()
    elif file_type == "docx":
        text_from_file = docx2txt.process(folder_temp_index+file_name)
        return text_from_file.lower()
    else:
        print 'write to log the file cant be read'
        return None


def parse_test_into_dict(text):
    unuse_words = db_model.get_unuse_word_from_db()
    words_dict = {}
    text = text.replace("'", "")

    for line in text.split('\n'):
        for word in line.split(' '):
            if (word, ) in unuse_words:
                continue
            if word[-1:] == ',' or word[-1:] == ')' or word[-1:] == '(' or word[-1:] == '.' or word[-1:] == '': word = word[:-1]
            if word[:1] == ',' or word[:1] == ')' or word[:1] == '(' or word[:1] == '.' or word[:1] == '': word = word[1:]
            if word not in words_dict:
                words_dict[word] = 1
            else:
                words_dict[word] += 1
    if '' in words_dict:
        del words_dict['']
    return words_dict


def remove_signs_from_text(text):
    text = text.replace("(", " ")
    text = text.replace(")", " ")
    text = text.replace(",", " ")
    text = text.replace(".", " ")
    text = text.replace('"', "")
    text = text.replace("-", " ")
    text = text.replace("!", " ")
    text = text.replace("?", " ")
    text = text.replace("`", "")
    text = text.replace(":", " ")
    text = text.replace(";", " ")
    return text


def retrive_data_by_string(query):
    if '"' in query:
        quotation = re.findall(r'"([^"]*)"', query)
        text = re.sub(r'".*?"', '""', query)
        text = re.sub(' +',' ',text)
        text = text.replace(" ")
        word_to_search = text + quotation
    else:
        word_to_search = query.split(" ")


if __name__ == '__main__':
    find_new_files_and_move_temp_folder()
    index_files_from_temp_folder()


