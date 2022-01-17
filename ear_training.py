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
accidental_l=[0,1,-1] # -2重降，-1降，0无，1升，2重升
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
        ly_t.pitch_Mm(question)
        return 
    step2()
    return '运行完成'


def interval_property_ear():
    # 特殊参数
    interval_num_l=[6]
    property_l=['M','m']
    def step1():
        interval_t=module.random_interval_t(low_c,high_c,accidental_l,interval_num_l,property_l)
        note_t1,note_t2=interval_t.note_t1,interval_t.note_t2
        # 音程里面的两个音
        interval=" < "+note_t1.note_all()+' '+note_t2.note_all()+" >1 "
        # 音程的名字
        interval_name=interval_t.interval_name()[0]
        return interval,interval_name+'1 '
    def step2():
        interval_all,interval_midi_all,interval_name_all='','',''
        for o in range(100):
            interval_row,interval_midi_row,interval_name_row='','',''
            for i in range(8):
                interval,interval_name=step1()
                interval_row+=interval
                interval_midi_row+=interval
                interval_name_row+=interval_name
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            interval_all+=interval_row+row_name
            interval_midi_all+=' \skip1 '+interval_midi_row+' \skip1 '+row_name
            interval_name_all+=interval_name_row
        # 拉起ly文件
        main=interval_midi_all
        lyric=''
        main_answer=interval_all
        lyric_answer=interval_name_all
        ly_t=create_ly.ly_set(accidental_ly,low_c,high_c,clef,main,lyric,main_answer,lyric_answer)
        question='interval_property_ear'
        ly_t.pitch_Mm(question)
        return '运行完成'
    step2()
    return '运行完成'

def pitch_group_Mm():
    # 专有参数
    key_num_l=[3]
    sharpe_flat_l=['sharpe']
    modal_l=[['major'],['nature']]
    space_l=[[2,'M'],[3,'M']]
    list_num=4
    # 设定拍号
    time_sign=str(list_num)+"/"+"16"
    # 设定ly文件中跳过的字符串
    skip=" \skip 16*%d "%list_num
    def step1():
        # 生成一个大调或小调的音组
        note_list,Mm_t=module.random_Mm_note_list(low_c,high_c,key_num_l,sharpe_flat_l,modal_l)
        key_list=Mm_t.key_t.key_list()[0]
        note_list=module.random_select_note(note_list,space_l,list_num,key_list)
        # 答案上的音符
        note_l=[v1.note_all() for v1 in note_list]
        note_l[0],note_l[1],note_l[-1]=note_l[0]+'16 '," [ "+note_l[1],note_l[-1]+" ] "
        note=' '.join(note_l)+' '
        return note
    def step2():
        note_all,note_midi_all='',''
        for o in range(100):
            note_row,note_midi_row='',''
            for i in range(4):
                note_row+=step1()
                note_midi_row+=step1()+skip
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            note_all+=note_row+row_name
            note_midi_all+=skip+note_midi_row+row_name
        # 拉起ly文件
        main=note_midi_all
        lyric=''
        main_answer=note_all
        lyric_answer=''
        ly_t=create_ly.ly_set(accidental_ly,low_c,high_c,clef,main,lyric,main_answer,lyric_answer)
        question='pitch_group_Mm'
        ly_t.pitch_group_ear(time_sign,question)
        return '运行完成'
    step2()
    return '运行完成'

def interval_group_ear():
    # 专有参数
    interval_num_l=[2,3,4,5,6,7,8]
    property_l=['M','m','p']
    space_l=[[2,'M'],[5,'p']]
    list_num=5
    # 设定拍号
    time_sign=str(list_num)+"/"+"1"
    # 设定ly文件中跳过的字符串
    skip=' \\time %d/4 '%list_num+" \skip 4*%d "%list_num+' \\time '+time_sign
    def step1():
        interval_l=module.random_interval_list(low_c,high_c,accidental_l,interval_num_l,property_l,space_l,list_num)
        # 音程的两个音
        interval=[' < '+v1.note_t1.note_all()+' '+v1.note_t2.note_all()+' >1 ' for v1 in interval_l]
        interval=' '.join(interval)
        return  interval
    def step2():
        interval_all,interval_midi_all='',''
        for o in range(100):
            interval_row,interval_midi_row='',''
            for i in range(1):
                interval=step1()
                interval_row+=interval
                interval_midi_row+=interval+skip+interval
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            interval_all+=interval_row+row_name
            interval_midi_all+=skip+interval_midi_row+skip
        # 拉起ly文件
        main=interval_midi_all
        lyric=''
        main_answer=interval_all
        lyric_answer=''
        ly_t=create_ly.ly_set(accidental_ly,low_c,high_c,clef,main,lyric,main_answer,lyric_answer)
        question='interval_group_ear'
        ly_t.pitch_group_ear(time_sign,question)
        return '运行完成'
    step2()
    return '运行完成'



# 和弦性质听辨
def chord_property_ear():
    # 专有参数
    chord_name_l=['dim','minor']
    invert_l=[0]
    def step1():
        chord_t=module.random_chord_t(low_c,high_c,accidental_l,chord_name_l,invert_l)
        chord_l=chord_t.chord()[1]
        # 和弦的名字
        chord_name=chord_t.chord_name_zh()[0]+chord_t.chord_name_zh()[1]+'1 '
        # 和弦的音
        chord_note_l=[v1.note_all() for v1 in chord_l]
        chord=' < '+' '.join(chord_note_l)+' >1 '
        return chord,chord_name
    def step2():
        chord_all,chord_midi_all,chord_name_all='','',''
        for o in range(100):
            chord_row,chord_midi_row,chord_name_row='','',''
            for i in range(10):
                chord,chord_name=step1()
                chord_row+=chord
                chord_midi_row+=chord
                chord_name_row+=chord_name
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            chord_all+=chord_row+row_name
            chord_midi_all+=' \skip1 '+chord_midi_row+' \skip1 '+row_name
            chord_name_all+=chord_name_row+row_name
        # 拉起ly文件
        main=chord_midi_all
        lyric=''
        main_answer=chord_all
        lyric_answer=chord_name_all
        ly_t=create_ly.ly_set(accidental_ly,low_c,high_c,clef,main,lyric,main_answer,lyric_answer)
        question='chord_property_ear'
        ly_t.pitch_Mm(question)
        return '运行完成'
    step2()
    return '运行完成'

