# -*- coding: utf-8 -*-
from make_ly import *
from config import *
from module import *

def repeat(func,repeat_inside,repeat_outside):
    # 音频重复
    def repeat_midi(midi):
        new_midi=''
        for i in range(midi_repeat):
            new_midi+=midi+' '
        return new_midi
    # 主重复流程
    def repeat_main():
        note_all,lyric_all,note_back_all,lyric_back_all='','','',''
        for o in range(repeat_outside):
            note_row,lyric_row,note_back_row,lyric_back_row='','','',''
            for i in range(repeat_inside):
                note,lyric,note_back,lyric_back=func()
                note_row+=note
                lyric_row+=lyric
                note_back_row+=note_back
                lyric_back_row+=lyric_back
            # 行数
            row_name= " \\break \set Score.currentBarNumber = #%s " %(o+2)
            note_all+=note_row+row_name
            lyric_all+=lyric_row
            lyric_back_all+=lyric_back_row
            # midi文件的重复|可能是midi可能是题目答案
            note_back_all+=repeat_midi(note_back_row)+row_name
        return note_all,lyric_all,note_back_all,lyric_back_all
    return repeat_main()   


def pitch_Mm(important_note_list=[[],0]):
    def step1():
        def random_func():
            # 生成一个大调或小调的音组
            note_list,Mm_t=random_Mm_note_list(range_low_c,range_high_c,key_num_l,sharp_flat_l,modal_l)
            note_list=random_select_note(note_list,space_l,list_num,important_note_list)
            # 答案上体现的音符
            note_l=[v1.note_all() for v1 in note_list]
            note='1 '.join(note_l)
            # 给到midi软件的音符
            # b站投稿临时 note=note+'1 ' 
            note_midi=' \skip1 '+note+' \skip1 ' # b站投稿 #'  \skip1 '+note+note+note+' \skip1'
            return note,'',note_midi,''
        return random_func
    def step2():
        # 生成
        repeat_inside=1
        repeat_outside=100
        file_name='pitch_Mm'
        note,lyric,note_back,lyric_back=repeat(step1(),repeat_inside,repeat_outside)
        # 生成ly文件
        ly_t=ly_set(note,lyric,note_back,lyric_back,clef)
        ly_t.pitch_Mm(file_name)
        return '运行完成'
    return step2()

def interval():
    def step1():
        def random_func():
            # 生成一个音程实例
            interval_t=random_interval_t(range_low_c,range_high_c,accidental_l,interval_num_l,property_l)
            # 音程里面的两个音
            note_t1,note_t2=interval_t.note_t1,interval_t.note_t2
            interval=" < "+note_t1.note_all()+' '+note_t2.note_all()+" >1 "
            # 音程的名字
            interval_name=interval_t.interval_name()[0]
            # 答案
            note=interval+' '
            lyric=interval_name+'1 '
            # midi
            note_midi=interval # b站投稿 重复三次 #  ' \skip1 '+interval+interval+interval+' \skip1 '
            return note,lyric,note_midi,''
        return random_func
    def step2():
        # 生成
        repeat_inside=1
        repeat_outside=100
        file_name='interval'
        note,lyric,note_back,lyric_back=repeat(step1(),repeat_inside,repeat_outside)
        # 生成ly文件
        ly_t=ly_set(note,lyric,note_back,lyric_back,clef)
        ly_t.interval(file_name)
        return '运行完成'
    return step2()

def rythem(time_sign):
    t=module_rythem(time_sign)
    # 拍号 
    time_ly=t.time_ly()
    # beam连杆设置
    beam=t.beam(irregular_mode)
    def step1():
        def random_func():
            # 生成一组节奏型
            rythem_list,rythem_t=random_rythem_list(time_sign)
            rythem=' '.join(rythem_list)
            # 输出准备
            note=rythem+' '
            note_midi=' \\time 2/4 \skip2 '+time_ly+rythem+' \\time 2/4 \skip2 '
            return note,'',note_midi,''
        return random_func
    def step2():
        # 生成
        repeat_inside=1
        repeat_outside=100
        file_name='rythem'
        note,lyric,note_back,lyric_back=repeat(step1(),repeat_inside,repeat_outside)
        # 生成ly文件
        ly_t=ly_set(note,lyric,note_back,lyric_back,clef)
        ly_t.rythem(file_name,time_ly,beam)
        return '运行完成'
    return step2()

def rythem_b(time_sign):
    t=module_rythem(time_sign)
    # 拍号 
    time_ly=t.time_ly()
    # beam连杆设置
    beam=t.beam(irregular_mode)
    def step1():
        def random_func():
            # 生成一组节奏型
            rythem_list,rythem_t=random_rythem_list(time_sign)
            rythem=' '.join(rythem_list)
            # 输出准备
            note=rythem+' \skip1*2 '
            note_midi=' \\time 2/4 \skip2 \skip2'+time_ly+rythem+' \\time 2/4 \skip2 '+time_ly+rythem+' \\time 2/4 \skip2 '+time_ly+rythem+' \\time 2/4 \skip2 \skip2 '
            return note,'',note_midi,''
        return random_func
    def step2():
        # 生成
        repeat_inside=1
        repeat_outside=100
        file_name='rythem'
        note,lyric,note_back,lyric_back=repeat(step1(),repeat_inside,repeat_outside)
        # 生成ly文件
        ly_t=ly_set(note,lyric,note_back,lyric_back,clef)
        ly_t.rythem_b(file_name,time_ly,beam)
        return '运行完成'
    return step2()

pitch_Mm()