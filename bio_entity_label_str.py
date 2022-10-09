import re

def get_list_by_read_file(file_path):
    with open(file_path,'r',encoding='utf-8') as f:
        txt_words_list = []
        for line in f.readlines():
            txt_words_list.append(line.strip().replace("\n",''))
        return txt_words_list

def get_word_dict_list_file(file_path,):
    with open(file_path,'r',encoding='utf-8') as f:
        txt_map = {}
        for line in f.readlines():
            deal_line = line.strip().replace("\n",'')
            index = -1;
            while len(deal_line) != 0 and -index < len(deal_line):
                if deal_line[index] == ' ':
                    break
                else:
                    index = index-1
            if index != -1:
                #print(line[0:index])
                txt_map[line[0:index]] = line[index:len(line)-1]
        return txt_map

def get_key_by_value(txt_map,value):
    keys_list=list(txt_map.keys())
    values_list=list(txt_map.values())
    for index in range(len(values_list)):
        if value in values_list[index]:
            return keys_list[index]

def output_file(file_path,word_list,tag_list):
    with open(file_path,'a',encoding='utf-8') as output_f:
        for w,t in zip(word_list,tag_list):
            if w != '	' and w != ' ':
                output_f.write(w+" "+t+'\n')
        output_f.write('\n')

def get_mark_index(str,search):
    begin = 0
    end = len(str)
    multi_index = []
    #search = " "+search+" "
    while begin < end and begin != -1:
        begin = str.find(search,begin,end)
        if begin != -1:
            multi_index.append(begin)
            begin = len(search) + begin
    return multi_index

dev_unlabel_list = get_list_by_read_file('./data/dev_unlabel.txt')

word_dict_map = get_word_dict_list_file('./data/word_dict.txt')

with open('./data/dev_unlabel.txt','r',encoding='utf-8') as f:
    txt_map = {}
    for unlabel in f.readlines():
        index_map = {}
        for key in list(word_dict_map.keys()) :
            #获取搜索到的下标
            sign_list = get_mark_index(unlabel,key.strip())
            for sign in sign_list:
                #会覆盖下标 value匹配最长字符串
                index_map[sign] = key+"---"+word_dict_map[key]
            #输出每一行

        entity_marked = {}
        for key_1,value_1 in index_map.items():
            len_entity = len(value_1.split("---")[0])
            entity_marked[key_1] = key_1+len_entity

        line_1 = unlabel

        start = 0
        index = 0
        while index < len(line_1):
            current_char = line_1[index]
            if index in entity_marked.keys():
                label = index_map[index].split("---")[1]
                marked_end = int(entity_marked[index])
                marked_word_split = line_1[index:marked_end].strip().split(" ")
                if len(marked_word_split) == 1:
                    print(line_1[index:marked_end]," B-"+label)
                else:
                    print(line_1[index:marked_end]," I-"+label)
                index = marked_end
                start = marked_end
            else:
                if current_char == ' ' or current_char == '\n':
                    print(line_1[start:index].strip()," O")
                    start = index
            index = index+1

