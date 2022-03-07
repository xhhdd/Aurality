# -*- coding: utf-8 -*-


import create_ly
from config import *
from module import *

class repeat:
    def __init__(self,note,lyric,note_back,lyric_back,repeat_inside,repeat_outside):
        self.note=note
        self.lyric=lyric
        self.note_back=note_back
        self.lyric_back=lyric_back
        self.repeat_inside=repeat_inside
        self.repeat_outside=repeat_outside
    # 主重复流程
    def repeat_main(self,v,midi_repeat=0):
        v_all=''
        for o in range(self.repeat_outside):
            v_row=''
            for i in range(self.repeat_inside):
                v_row+=v
            # 行数
            row_name='' if v_row=='' else " \\break \set Score.currentBarNumber = #%s " %(o+2)
            # 音频重复
            if midi_repeat==1:
                v_row=self.repeat_midi(v_row)
            v_all+=v_row+row_name
        return v_all
    # 音频重复
    def repeat_midi(self,midi):
        new_midi=''
        for i in (midi_repeat):
            new_midi+=midi
        return new_midi
    def start_repeat(self):
        note=self.repeat_main(self.note)
        lyric=self.repeat_main(self.lyric)
        note_back=self.repeat_main(self.note_back,1)
        lyric_back=self.repeat_main(self.lyric_back,1)
        return note,lyric,note_back,lyric_back
    def make_ly(self):
        note,lyric,note_back,lyric_back=self.start_repeat()
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,note,lyric,note_back,lyric_back)
        question='pitch_Mm'
        ly_t.pitch_Mm(question)

def pitch_Mm(important_note_list):
    def step1():
        # 生成一个大调或小调的音组
        note_list,Mm_t=random_Mm_note_list(range_low_c,range_high_c,key_num_l,sharp_flat_l,modal_l)
        note_list=random_select_note(note_list,space_l,list_num,important_note_list)
        # 答案上体现的音符
        note_l=[v1.note_all() for v1 in note_list]
        note='1 '.join(note_l)
        # 给到midi软件的音符
        note_midi=' \skip1 '+note+' \skip1 '
        return note,note_midi
    def step2():
