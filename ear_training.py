# -*- coding: utf-8 -*-
from ntpath import join
import random
import module
import create_ly
# 与音相关
# 列表前一个是音名，后一个是组别
low_c=['a',0]
high_c=['c',3] 
# 这是能选择的升降记号
sharpe_flat_l=[0,1,-1] # -2重降，-1降，0无，1升，2重升
# 选择谱号
clef='S' 
# ly文件生成
accidental_ly='@1'# ['all','@1','@12','@2','@0']  0是所有记号都有，1是没有重升重降，2是含有重升重降，3是只有重升重降，4是没有升降记号


def pitch_Mm():
    # 特殊参数
    key_num_l=[3]
    sharpe_flat_l=['sharpe']
    modal_l=[['major'],['nature']]
    space_l=[[2,'M'],[3,'M']]
    def step1():
        list_num=10 # 控制一次有多少个单音
        # 生成一个大调或小调的音组
        note_list,Mm_t=module.random_Mm_note_list(low_c,high_c,key_num_l,sharpe_flat_l,modal_l)
        key_list=Mm_t.key_t.key_list()[0]
        note_list=module.random_select_note(note_list,space_l,list_num,key_list)
        # 答案上体现的音符
        note_l=[v1.note_all() for v1 in note_list]
        note='1 '.join(note_l)
        # 给到midi软件的音符
        note_midi=' \skip1 '+note+' \skip1 '
        # 调式名字
        tonic,modal2,modal1=Mm_t.scale_name_zh()
        key_name=tonic+modal2+modal1+'1*%d'%(list_num)
        return note,note_midi,key_name
    def step2():
        note_all,note_midi_all,key_name_all='','',''
        for o in range(100):
            note_row,note_midi_row,key_name_row='','',''
            for i in range(1):
                note,note_midi,key_name=step1()
                note_row+=note
                note_midi_row+=note_midi
                key_name_row+=key_name
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            note_all+=note_row+row_name
            note_midi_all+=note_midi_row+row_name
            key_name_all+=key_name_row+row_name
        # 拉起ly文件
        main=note_midi_all
        lyric=''
        main_answer=note_all
        lyric_answer=key_name_all
        ly_t=create_ly.ly_set(accidental_ly,low_c,high_c,clef,main,lyric,main_answer,lyric_answer)
        question='pitch_Mm'
        ly_t.write_note_name(question)
        return 
    step2()
    return '运行完成'

def pitch_group_Mm():
    # 特殊参数
    space=[2,5]
    list_num=4

    # 设定拍号
    time_sign=str(list_num)+"/"+"16"
    # 设定ly文件中跳过的字符串
    skip=" \skip 16*"+str(list_num)+' '

    note_all=''
    note_all_answer=''
    for o in range(100):
        note_list_row=[]
        note_row=[]
        pitch_group_row=''
        pitch_group_answer_row=''
        for i in range(5):
            note_list=module.note_list_space_c(low_c,high_c,sharpe_flat_l,space,list_num)
            for v1 in note_list:
                note_list_row.append(module.module_note(v1[0],v1[1]))
            for v2 in note_list_row:
                note_row.append(v2.note_all()+'16')
            note_row.insert(1,"[")
            note_row.append("]")
            pitch_group_row+=' '.join(note_row)+skip+skip
            pitch_group_answer_row+=' '.join(note_row)
            note_row,note_list_row=[],[] # 清零
        for i in range(2): # 清除尾巴
            pitch_group_row=pitch_group_row.rstrip(skip)
        # 行数
        start_row=0
        row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
        note_all+=skip+pitch_group_row+skip+row_name
        note_all_answer+=pitch_group_answer_row+row_name
    # 拉起ly文件
    main=note_all
    lyric=''
    main_answer=note_all_answer
    lyric_answer=''
    t=create_ly.ly_set(flatsharpe_kind,low_c,high_c,clef,main,lyric)
    question='pitch_group_ear_1'
    t.pitch_group_ear(time_sign,question,main_answer,lyric_answer)
    return '运行完成'

def interval_ear():
    # 特殊参数
    interval_num_l=[2,3,4,5,6,7,8]
    property_l=['纯','大','小']
    
    interval_all=''
    interval_answer_all=''
    lyric_answer_row=''
    for o in range(100):
        interval_row=''
        for i in range(8):
            # 生成实例
            t1=module.random_create_interval(low_c,high_c,sharpe_flat_l,interval_num_l,property_l)
            interval_row+=' <'+t1.t1.note_all()+' '+t1.t2.note_all()+'>1 '
            lyric_answer_row+=t1.interval_name()[0]+'1 '
        # 行数
        start_row=0
        row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
        interval_all+=' \skip1 '+interval_row+' \skip1 '+row_name
        interval_answer_all+=interval_row+row_name
    # 拉起ly文件
    main=interval_all
    lyric=''
    main_answer=interval_answer_all
    lyric_answer=lyric_answer_row
    t3=create_ly.ly_set(flatsharpe_kind,low_c,high_c,clef,main,lyric)
    question="interval_ear"
    t3.interval_ear(question,main_answer,lyric_answer)
    return '运行完成'

def interval_group_ear():
    # 特殊参数
    interval_num_l=[2,3,4,5,6,7,8]
    property_l=['纯','大','小']
    
    interval_answer_all=''
    interval_all=''
    lyric_row=''
    for o in range(100):
        interval_row=''
        for i in range(5):
            # 生成实例
            t1=module.random_create_interval(low_c,high_c,sharpe_flat_l,interval_num_l,property_l)
            interval_row+=' <'+t1.t1.note_all()+' '+t1.t2.note_all()+'>1 '
            lyric_row+=t1.interval_name()[0]+'1 '
        # 行数
        start_row=0
        row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
        interval_all+=' \skip1 '+interval_row+'\skip1 \skip1'+interval_row+' \skip1 '
        interval_answer_all+=interval_row+row_name
    # 拉起ly文件
    main=interval_all
    lyric=''
    main_answer=interval_answer_all
    lyric_answer=lyric_row
    t3=create_ly.ly_set(flatsharpe_kind,low_c,high_c,clef,main,lyric)
    question="interval_group_ear"
    t3.interval_ear(question,main_answer,lyric_answer)
    return '运行完成'


