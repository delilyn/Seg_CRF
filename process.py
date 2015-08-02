#-*- coding: UTF-8 -*-
"""
Author:deli
File:process.py
Time:2015/6/22 20:41:45
"""
import codecs
import sys
import random
#训练集7，3分，用于训练和测试
def divide(input_file, train, test):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    #output_data = codecs.open(output_file, 'w', 'utf-8')
    fw_train =  codecs.open(train, 'w', 'utf-8')
    fw_test = codecs.open(test, 'w', 'utf-8')
    data = input_data.readlines()
    train_len = int(len(data) * 0.7 )
    for i in range(train_len):
        fw_train.write(data[i])
    for i in range(train_len,len(data)):
        fw_test.write(data[i]) 
    input_data.close()
    fw_train.close()
    fw_test.close()
def trans_test(testseg, test):    
    fr = codecs.open(testseg, 'r', 'utf-8')
    fw_test = codecs.open(test, 'w', 'utf-8')
    for line in fr.readlines():
        line = line.replace('  ', '')
        fw_test.write(line)
    fr.close()
    fw_test.close()
#验证是否过拟合，数据集随机7.3分    
def ran_divide(input_file, train, test):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    #output_data = codecs.open(output_file, 'w', 'utf-8')
    fw_train =  codecs.open(train, 'w', 'utf-8')
    fw_test = codecs.open(test, 'w', 'utf-8')
    
    lst = [i for i in range(1, 11)]
    random.shuffle(lst) 
    train_lst = lst[0:7] 
    test_lst = lst[7:10]
    
    data = input_data.readlines()
    ave_len = int(len(data) * 0.1)
    
    for i in train_lst:
        for j in range((i-1)*ave_len, i*ave_len):
            fw_train.write(data[j])
    for i in test_lst:
        for j in range((i-1)*ave_len, i*ave_len):
            fw_test.write(data[j]) 
    '''
    for i in range(train_len):
        fw_train.write(data[i])
    for i in range(train_len,len(data)):
        fw_test.write(data[i]) 
    '''
    
    input_data.close()
    fw_train.close()
    fw_test.close()
    lst = [i for i in range(1, 11)]
    random.shuffle(lst) 
    train_lst = lst[0:7] 
    test_lst = lst[7:10]
    print train_lst 
    print test_lst
def test_countblank(input_file,output_file):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    i = 0
    n = 0
    for line in input_data.readlines():
        n += 1 
        if len(line) == 2:
            i += 1
            print n 
            continue
        output_data.write(line)
    print i 
    input_data.close()
    output_data.close()
def cut_first_blank(input_file,output_file):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    i = 0
    for line in input_data.readlines():
        newline = line[1:]
        i += 1
        output_data.write(newline)
    print i 
    input_data.close()
    output_data.close()   
def character_split(input_file, output_file):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for line in input_data.readlines():
        for word in line.strip():
            word = word.strip()
            if word:
                output_data.write(word + "\tB\n")
        output_data.write("\n")
    input_data.close()
    output_data.close()    
# Author: 52nlpcn@gmail.com
# Copyright 2014 @ YuZhen Technology
def character_2_word(input_file, output_file):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for line in input_data.readlines():
        if len(line) == 2:
            output_data.write("\n")
        else:
            char_tag_pair = line.strip().split('\t')
            char = char_tag_pair[0]
            tag = char_tag_pair[2]
            if tag == 'B':
                output_data.write(' ' + char)
            elif tag == 'M':
                output_data.write(char)
            elif tag == 'E':
                output_data.write(char + ' ')
            else: # tag == 'S'
                output_data.write(' ' + char + ' ')
    input_data.close()
    output_data.close()
# Author: 52nlpcn@gmail.com
# Copyright 2014 @ YuZhen Technology    
def crf_segmenter(input_file, output_file, tagger):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for line in input_data.readlines():
        tagger.clear()
        for word in line.strip():
            word = word.strip()
            if word:
                tagger.add((word + "\to\tB").encode('utf-8'))
        tagger.parse()
        size = tagger.size()
        xsize = tagger.xsize()
        for i in range(0, size):
            for j in range(0, xsize):
                char = tagger.x(i, j).decode('utf-8')
                tag = tagger.y2(i)
                if tag == 'B':
                    output_data.write(' ' + char)
                elif tag == 'M':
                    output_data.write(char)
                elif tag == 'E':
                    output_data.write(char + ' ')
                else: # tag == 'S'
                    output_data.write(' ' + char + ' ')
        output_data.write('\n')
    input_data.close()
    output_data.close()
# Author: 52nlpcn@gmail.com
# Copyright 2014 @ YuZhen Technology
def test_character_tagging(input_file, output_file):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for line in input_data.readlines():
        word_list = line.strip().split()
        for word in word_list:
            if len(word) == 1:
                output_data.write(word + "\tS\n")
            else:
                output_data.write(word[0] + "\tB\n")
                for w in word[1:len(word)-1]:
                    output_data.write(w + "\tM\n")
                output_data.write(word[len(word)-1] + "\tE\n")
        output_data.write("\n")
    input_data.close()
    output_data.close()
# Author: 52nlpcn@gmail.com
# Copyright 2014 @ YuZhen Technology
def train_character_tagging(input_file, output_file):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for line in input_data.readlines():
        word_list = line.strip().split()
        for word in word_list:
            if len(word) == 1:
                output_data.write(word + "\tS\n")
            else:
                output_data.write(word[0] + "\tB\n")
                for w in word[1:len(word)-1]:
                    output_data.write(w + "\tM\n")
                output_data.write(word[len(word)-1] + "\tE\n")
        output_data.write("\n")
    input_data.close()
    output_data.close()
if __name__ == '__main__':
    #divide('Train_utf16.seg', 'F:\\Data\\homework\\seg\\train.seg', 'F:\\Data\\homework\\seg\\test.seg') 
    #trans_test('F:\\Data\\homework\\seg\\test.seg', 'F:\\Data\\homework\\seg\\test')
    ran_divide('Train_utf16.seg', 'F:\\Data\\homework\\seg\\random3\\train.seg', 'F:\\Data\\homework\\seg\\random3\\test.seg')
