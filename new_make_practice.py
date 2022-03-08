# -*- coding: utf-8 -*-


from make_ly import *
from config import *
from module import *

def make_ly(func,repeat_inside,repeat_outside,file_name):
    # 重复生成
    def repeat():
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
    # 生成ly文件
    def start_make_ly():
        note,lyric,note_back,lyric_back=repeat()
        ly_t=ly_set(note,lyric,note_back,lyric_back,clef)
        ly_t.pitch_Mm(file_name)
    return start_make_ly()


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
            note_midi=' \skip1 '+note+' \skip1 '
            return note,'',note_midi,''
        return random_func
    def step2():
        # 生成
        repeat_inside=1
        repeat_outside=50
        file_name='pitch_Mm'
        make_ly(step1(),repeat_inside,repeat_outside,file_name)
        return '运行完成'
    return step2()

