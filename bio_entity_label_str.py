import string
import os
punc_list = list(string.punctuation)
punc_list.append(" ")

def get_list_by_read_file(file_path):
    with open(file_path,'r',encoding='utf-8') as f:
        txt_words_list = []
        for line in f.readlines():
            txt_words_list.append(line.strip().replace("\n",''))
        return txt_words_list

def get_word_dict_map_from_file(file_path,):
    with open(file_path,'r',encoding='utf-8') as f:
        txt_map = {}
        for line in f.readlines():
            deal_line = line.strip().replace("\n",'')
            index = -1
            while len(deal_line) != 0 and -index < len(deal_line):
                if deal_line[index] == ' ':
                    break
                else:
                    index = index-1
            if index != -1:
                txt_map[line[0:index].strip()] = line[index:len(line)-1]
        return txt_map

file_path = './cut_data/dev_labeled.txt'
word_list = []
tag_list = []
def output_file(file_path,word_list,tag_list):
    if os.path.isfile(file_path):
        os.remove(file_path)
    with open(file_path,'a',encoding='utf-8') as output_f:
        for w,t in zip(word_list,tag_list):
            if w != '	' and w != ' ':
                output_f.write(w+" "+t+'\n')

def append_to_out_list(word,tag):
    word_list.append(word)
    tag_list.append(tag)

def get_mark_index(str,search):
    search = search.strip()
    begin = 0
    end = len(str)
    multi_index = []
    while begin < end and begin != -1:
        begin = str.find(search,begin,end)
        if begin != -1:
            multi_index.append(begin)
            begin = len(search) + begin
    return multi_index

#匹配校验规则
def judge_word_is_right(main_str,child_str_index):
    main_str = main_str.replace("\n",'')
    if child_str_index + 1 < len(main_str) :
        return main_str[child_str_index] == ' '
    elif child_str_index + 1 == len(main_str) :
        return main_str[child_str_index] == '.'

#切换I-O label单词
def split_I_O_label_str(I_label_str):
    item = []
    start_index = 0
    for i in range(len(I_label_str)):
        if I_label_str[i] in punc_list:
            if start_index!=i:
                item.append(I_label_str[start_index:i].strip())
            if I_label_str[i]!=' ':
                item.append(I_label_str[i].strip())
            start_index=i+1
    if start_index < len(I_label_str)-1:
        item.append(I_label_str[start_index:i+1].strip())
    return item

dev_unlabel_list = get_list_by_read_file('./data/dev_unlabel.txt')

word_dict_map = get_word_dict_map_from_file('./data/word_dict.txt')

with open('./data/dev_unlabel.txt','r',encoding='utf-8') as f:
    for unlabel in f.readlines():
        index_2_label_map = {}
        for key in list(word_dict_map.keys()) :
            #获取搜索到的下标
            sign_list = get_mark_index(unlabel,key.strip())
            for sign in sign_list:
                #会覆盖下标 value匹配最长字符串
                index_2_label_map[sign] = key+"---"+word_dict_map[key]
            #输出每一行
        print("每一行匹配到的词典 index_map:",index_2_label_map)
        txt_label_match_map = {}
        for k,v in index_2_label_map.items():
            len_entity = len(v.split("---")[0])
            txt_label_match_map[k] = k+len_entity
        print("每一行匹配到的词典起始坐标 txt_label_match_map:",txt_label_match_map)

        start = 0
        index = 0
        while index < len(unlabel):

            if index in txt_label_match_map.keys():
                #标签
                label = index_2_label_map[index].split("---")[1]
                #结束坐标
                txt_word_matched_end_index = int(txt_label_match_map[index])

                if judge_word_is_right(unlabel, txt_word_matched_end_index):

                    label_word = unlabel[index:txt_word_matched_end_index]
                    marked_word_split = label_word.strip().split(" ")
                    if len(marked_word_split) == 1:  #词典为单个实体
                        print(label_word," B-"+label)
                        append_to_out_list(label_word," B-"+label)
                    else:
                        items = split_I_O_label_str(label_word)
                        for index in range(len(items)):
                            if index == 0 :
                                print(items[index]," B-"+label)
                                append_to_out_list(items[index]," B-"+label)
                            else :
                                print(items[index]," I-"+label)
                                append_to_out_list(items[index]," I-"+label)
                    index = txt_word_matched_end_index
                    start = txt_word_matched_end_index
            else:
                current_char = unlabel[index]
                if current_char == ' ' or current_char == '\n':
                    items = split_I_O_label_str(unlabel[start:index].strip())
                    for item in items :
                        print(item," O")
                        append_to_out_list(item," O")
                    start = index
            index = index+1


output_file(file_path,word_list,tag_list)