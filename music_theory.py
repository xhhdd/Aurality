# -*- coding: utf-8 -*-
import random
from turtle import color
import module
import create_ly
# 与音相关
# 列表前一个是音名，后一个是组别
range_low_c=['c',1]
range_high_c=['g',2] 
# 这是能选择的升降记号
accidental_l=[0] # -2重降，-1降，0无，1升，2重升
# 选择谱号
clef='S' 
# ly文件生成
accidental_ly='@0'# ['all','@1','@12','@2','@0']  0是所有记号都有，1是没有重升重降，2是含有重升重降，3是只有重升重降，4是没有升降记号

# 专门生成五线谱线上的音或者是间上的音
def recognition_note():
    # 线上或者间上
    line_space=''
    def step1():
        note_t=module.random_create_note(range_low_c,range_high_c,accidental_l)
        if line_space=='line':
            while note_t.note_num%2==0:
                note_t=module.random_create_note(range_low_c,range_high_c,accidental_l)
        else:
            while note_t.note_num%2!=0:
                note_t=module.random_create_note(range_low_c,range_high_c,accidental_l)
        note=note_t.note_all()
        note_name=note_t.note_name()[0][2]+note_t.note().upper()
        return note,note_name
    def step2():
        note_all,note_name_all='',''
        for o in range(100):
            note_row,note_name_row='',''
            for i in range(10):
                note,note_name=step1()
                note_row+=note+'1 '
                note_name_row+=' "'+note_name+'"1 '
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            note_all+=note_row+row_name
            note_name_all+=note_name_row+row_name
        # 拉起ly文件
        main=note_all
        lyric=''
        main_answer=note_all
        lyric_answer=note_name_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='write_note_name'
        ly_t.write_note_name(question)
        return 
    step2()
    return '运行完成'


# 根据五线谱上的音符写出音名
def write_note_name():
    # 唱名开关
    step_io=1
    def step_1():
        note_t=module.random_create_note(range_low_c,range_high_c,accidental_l)
        note_all=note_t.note_all()
        note_name=note_t.note_name()[0][2]+note_t.note().upper()
        # 唱名
        step_name=str(note_t.note_num_mode()[1])
        note_name=step_name if step_io==1 else note_name
        return note_all,note_name
    def step_2():
        note_all,note_name_all='',''
        for o in range(100):
            note_row,note_name_row='',''
            for i in range(10):
                note,note_name=step_1()
                note_row+=note+'1 '
                note_name_row+=' "'+note_name+'"1 '
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            note_all+=note_row+row_name
            note_name_all+=note_name_row+row_name
        # 拉起ly文件
        main=note_all
        lyric=''
        main_answer=note_all
        lyric_answer=note_name_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='write_note_name'
        ly_t.write_note_name(question)
        return 
    step_2()
    return '运行完成'

def write_note():
    def step1():
        note_t=module.random_create_note(range_low_c,range_high_c,accidental_l)
        note_all=note_t.note_all()
        octave_name=note_t.note_name()[1]
        # 根据小字几组来大小写音名
        note=note_t.note() if '小' in octave_name else note_t.note().upper()
        note_name=octave_name+','+note_t.note_name()[0][0]+note
        return note_all,note_name
    def step2():
        skip_all,note_name_all,note_all='','',''
        for o in range(100):
            skip_row,note_name_row,note_row='','',''
            for i in range(4):
                note,note_name=step1()
                skip_row+=' \skip1 '
                note_name_row+=note_name+'1 '
                note_row+=note+'1 '
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            skip_all+=skip_row+row_name
            note_name_all+=note_name_row+row_name
            note_all+=note_row+row_name
        # 拉起ly文件
        main=skip_all
        lyric=note_name_all
        main_answer=note_all
        lyric_answer=note_name_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='write_note'
        ly_t.write_note_name(question)
        return 
    step2()
    return '运行完成'

# 判断全音半音
def blank_filling_semi_tone_simple():
    # 专属参数
    space_l=[1,2,3]
    def step1():
        semi_tone_t=module.random_create_semi_tone(range_low_c,range_high_c,accidental_l,space_l)
        name=semi_tone_t.simple()[0]+'1*2 '
        note_l=[semi_tone_t.note_t1.note_all(),semi_tone_t.note_t2.note_all()]
        random.shuffle(note_l) # 把两个音打乱
        return name,note_l
    def step2():
        mame_all,note_all='',''
        for o in range(100):
            name_row,note_row='',''
            for i in range(8):
                name,note_l=step1()
                name_row+=name
                note_row+=note_l[0]+'1 '+note_l[1]+'1 '
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            mame_all+=name_row+row_name
            note_all+=note_row+row_name
        # 拉起ly文件
        main=note_all
        lyric=''
        main_answer=note_all
        lyric_answer=mame_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='bf_semi_tone_simple'
        ly_t.blank_filling_semi_tone(question)
        return 
    step2()
    return '运行完成'

def add_accidental_semi_tone():
    # 专属参数
    space_l=[1,2,3]

    def step1():
        semi_tone_t=module.random_create_semi_tone(range_low_c,range_high_c,accidental_l,space_l)
        note_t1,note_t2=semi_tone_t.note_t1,semi_tone_t.note_t2
        # 选择往上或往下
        asc_des=random.choice(['asc','des'])
        if asc_des=='des':
            note_t1,note_t2=note_t2,note_t1
            asc_des_name='往下，'
        else:
            asc_des_name='往上，'
        # 题目名称
        name=asc_des_name+semi_tone_t.simple()[0]+'1*2 ' 
        # 接下来去掉第二个音的升降记号，但是需要注意，在两音为1度时，后音的升降记号跟前面的一致。
        accidental=note_t1.accidental_num if note_t1.note_num==note_t2.note_num else 0
        note_t3=module.module_note(semi_tone_t.note_t2.note_num,accidental)
        note_hide_accidental=note_t1.note_all()+'1 '+note_t3.note_all()+'1 ' 
        # 题目的答案，并标记好颜色
        note=' \colorAccidental #black '+note_t1.note_all()+'1 '+' \colorAccidental #red '+note_t2.note_all()+'1 '
        return note,name,note_hide_accidental
    def step2():
        note_all,name_all,note_hide_all='','',''
        for o in range(100):
            note_row,name_row,note_hide_row='','',''
            for i in range(4):
                note,name,note_hide_accidental=step1()
                note_row+=note
                name_row+=name
                note_hide_row+=note_hide_accidental
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            note_all+=note_row+row_name
            name_all+=name_row+row_name
            note_hide_all+=note_hide_row+row_name
        # 拉起ly文件
        main=note_hide_all
        lyric=name_all
        main_answer=note_all
        lyric_answer=name_all

        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='add_accidental'
        ly_t.blank_filling_semi_tone(question)
        return '运行完成'
    step2()
    return '运行完成'


def blank_filling_semi_tone_hard():
    # 专属参数
    space_l=[1,2,3]
    def step1():
        semi_tone_t=module.random_create_semi_tone(range_low_c,range_high_c,accidental_l,space_l)
        name=semi_tone_t.hard()[0]+'1*2 '
        note_l=[semi_tone_t.note_t1.note_all(),semi_tone_t.note_t2.note_all()]
        random.shuffle(note_l) # 把两个音打乱
        return name,note_l
    def step2():
        mame_all,note_all='',''
        for o in range(100):
            name_row,note_row='',''
            for i in range(8):
                name,note_l=step1()
                name_row+=name
                note_row+=note_l[0]+'1 '+note_l[1]+'1 '
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            mame_all+=name_row+row_name
            note_all+=note_row+row_name
        # 拉起ly文件
        main=note_all
        lyric=''
        main_answer=note_all
        lyric_answer=mame_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='bf_semi_tone_hard'
        ly_t.blank_filling_semi_tone(question)
        return 
    step2()
    return '运行完成'

# 书写等音
def write_enharmonica():
    def step1():
        # 题目的主要音
        note_t1=module.random_create_note(range_low_c,range_high_c,accidental_l)
        # 生成一个等音列表
        enharmonica_l=module.enharmonica(note_t1)
        enharmonica=''
        for v1 in enharmonica_l:
            enharmonica+=v1.note_all()+' '
        # 答案的音符
        note_answer=' \colorNote #black '+note_t1.note_all()+'1 '+' \colorNote #darkcyan '+" < "+enharmonica+" >1 "
        # 题目的音符
        note=note_t1.note_all()+'1 '+' \skip1 '
        return note,note_answer
    def step2():   
        note_all,note_answer_all='',''
        for  o in range(100):
            note_row,note_answer_row='',''
            for i in range(5):
                note,note_answer=step1()
                note_row+=note
                note_answer_row+=note_answer
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            note_all+=note_row+row_name
            note_answer_all+=note_answer_row+row_name
        # 拉起ly文件
        main=note_all
        lyric=''
        main_answer=note_answer_all
        lyric_answer=''
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='write_enharmonica'
        ly_t.write_enharmonica(question)
        return '运行完成'
    step2()
    return '运行完成'

def write_interval_name():
    # 特殊参数
    interval_num_l=[1,2,3,4,5,6,7,8]
    property_l=['m','M','p','A','d'] # ['d_d','d','m','M','A','d_A','p','fail']
    def step1():
        # 生成实例
        interval_t=module.random_interval_t(range_low_c,range_high_c,accidental_l,interval_num_l,property_l)
        # 音程的答案
        interval_name=interval_t.interval_name()[0]+'1*2 '
        # 音程的两个音
        note_l=[interval_t.note_t1.note_all()+'1 ',interval_t.note_t2.note_all()+'1 ']
        random.shuffle(note_l) # 打乱两个音
        interval=' '.join(note_l)
        return interval,interval_name
    def step2():
        interval_all,interval_name_all='',''
        for o in range(100):
            interval_row,interval_name_row='',''
            for i in range(8):
                interval,interval_name=step1()
                interval_row+=interval+' '
                interval_name_row+=interval_name
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            interval_all+=interval_row+row_name
            interval_name_all+=interval_name_row+row_name
        # 拉起ly文件
        main=interval_all
        lyric=''
        main_answer=interval_all
        lyric_answer=interval_name_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='write_interval_name'
        ly_t.write_interval_name(question)
        return '运行完成'
    step2()
    return

def write_interval_note():
    # 特殊参数
    interval_num_l=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    property_l=['d_d','d','m','M','A','d_A','p'] # ['d_d','d','m','M','A','d_A','p','fail']
    def step1():
        # 生成实例
        interval_t=module.random_interval_t(range_low_c,range_high_c,accidental_l,interval_num_l,property_l)
        note_t1,note_t2=interval_t.note_t1,interval_t.note_t2
        # 随机两音的高低
        asc_des=random.choice(['asc'])
        if asc_des=='des':
            note_t1,note_t2=note_t2,note_t1
            asc_des_name='往下，'
        else:
            asc_des_name='往上，'
        # 音程的名称
        interval_name=asc_des_name+interval_t.interval_name()[0]+'1*2 '
        # 音程的题目
        interval=note_t1.note_all()+'1 '+' \skip1 '
        # 音程的答案
        interval_answer=' \colorNote #black '+note_t1.note_all()+'1 '+' \colorNote #darkcyan  '+note_t2.note_all()+'1 '
        return interval,interval_answer,interval_name
    def step2():
        interval_all,interval_answer_all,interval_name_all='','',''
        for o in range(100):
            interval_row,interval_answer_row,interval_name_row='','',''
            for i in range(4):
                interval,interval_answer,interval_name=step1()
                interval_row+=interval
                interval_answer_row+=interval_answer
                interval_name_row+=interval_name
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            interval_all+=interval_row+row_name
            interval_answer_all+=interval_answer_row+row_name
            interval_name_all+=interval_name_row+row_name
        # 拉起ly文件
        main=interval_all
        lyric=interval_name_all
        main_answer=interval_answer_all
        lyric_answer=interval_name_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='write_interval_note'
        ly_t.write_interval_name(question)
        return '运行完成'
    step2()
    return

def interval_resolution():
    # 专属参数
    key_num_l=[0,1,2,3,4,5,6,7]
    sharp_flat_l=['sharp','flat']
    modal_l=[[['major'],['nature','harmony']],[['minor'],['nature','harmony']]]
    def step1():
        [note_t1,note_t2],interval_resolution_l,Mm_t=module.random_interval_resolution(range_low_c,range_high_c,key_num_l,sharp_flat_l,modal_l)
        interval=' < '+note_t1.note_all()+' '+note_t2.note_all()+' >1 '
        interval_resolution=' < '+interval_resolution_l[0].note_all()+' '+interval_resolution_l[1].note_all()+' >1 '
        key_name='"'+Mm_t.scale_name_zh()[0]+Mm_t.scale_name_zh()[1]+Mm_t.scale_name_zh()[2]+'"'+'1*2 '
        return interval,interval_resolution,key_name
    def step2():
        interval_all,interval_resolution_all,key_name_all='','',''
        for o in range(100):
            interval_row,interval_resolution_row,key_name_row='','',''
            for i in range(4):
                interval,interval_resolution,key_name=step1()
                interval_row+=interval+' \skip1 '
                interval_resolution_row+=' \colorNote #black '+interval+' \colorNote #darkcyan  '+interval_resolution
                key_name_row+=key_name
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            interval_all+=interval_row+row_name
            interval_resolution_all+=interval_resolution_row+row_name
            key_name_all+=key_name_row
        main=interval_all
        lyric=key_name_all
        main_answer=interval_resolution_all
        lyric_answer=key_name_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='interval_resolution'
        ly_t.interval_resolution(question)
        return '运行完成'
    step2()
    return '运行完成'



def write_chord_name():
    # 专有参数
    chord_name_l=['MM7','Mm7','mm7','dm7','dd7']  #'major','minor','aug','dim'|'MM7','Mm7','mm7','dm7','dd7'
    invert_l=[0,1,2,3] # 最多输入3 三和弦在第三转位整体升高一个八度
    def step1():
        chord_t=module.random_chord_t(range_low_c,range_high_c,accidental_l,chord_name_l,invert_l)
        chord_l=chord_t.chord()[1]
        # 和弦的音
        chord_note_l=[v1.note_all() for v1 in chord_l]
        chord_note=' < '+' '.join(chord_note_l)+' >1 '
        # 和弦的名称
        chord_name=chord_t.chord_name_zh()[0]+chord_t.chord_name_zh()[1]+'1 '
        return chord_note,chord_name
    def step2():
        chord_all,chord_name_all='',''
        for o in range(100):
            chord_row,chord_name_row='',''
            for i in range(6):
                chord_note,chord_name=step1()
                chord_row+=chord_note
                chord_name_row+=chord_name
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            chord_all+=chord_row+row_name
            chord_name_all+=chord_name_row+row_name
        # 拉起ly文件
        main=chord_all
        lyric=''
        main_answer=chord_all
        lyric_answer=chord_name_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='write_chord_name'
        ly_t.write_chord_name(question)
        return '运行完成'
    step2()
    return

def write_chord_note():
    # 专有参数
    chord_name_l=['MM7','Mm7','mm7','dm7','dd7']  # 'major','minor','aug','dim'|'MM7','Mm7','mm7','dm7','dd7'
    invert_l=[0,1,2,3] # 最多输入3 三和弦在第三转位整体升高一个八度
    def step1():
        chord_t=module.random_chord_t(range_low_c,range_high_c,accidental_l,chord_name_l,invert_l)
        chord_l=chord_t.chord()[1]
        # 和弦的名称
        chord_name=chord_t.chord_name_zh()[0]+chord_t.chord_name_zh()[1]+'1 '
        # 和弦的根音
        chord_root=chord_t.root_note.note_all()+'1 '
        # 完整的和弦音
        chord_note_l=[v1.note_all() for v1 in chord_l]
        chord_note=' < '+' '.join(chord_note_l)+' >1 '
        return chord_root,chord_name,chord_note
    def step2():
        chord_root_all,chord_name_all,chord_note_all='','',''
        for o in range(100):
            chord_root_row,chord_name_row,chord_note_row='','',''
            for i in range(5):
                chord_root,chord_name,chord_note=step1()
                chord_root_row+=chord_root
                chord_name_row+=chord_name
                chord_note_row+=chord_note
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            chord_root_all+=chord_root_row+row_name
            chord_name_all+=chord_name_row+row_name
            chord_note_all+=chord_note_row+row_name
        # 拉起ly文件
        main=chord_root_all
        lyric=chord_name_all
        main_answer=chord_note_all
        lyric_answer=chord_name_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='write_chord_note'
        ly_t.write_chord_name(question)
        return '运行完成'
    step2()
    return '运行完成'

def chord_resolution():
    # 专属参数
    key_num_l=[0,1,2,3,4,5,6,7]
    sharp_flat_l=['sharp','flat']
    modal_l=[[['major'],['nature','harmony']],[['minor'],['nature','harmony']]]
    chord_name_l=['Mm7','dd7']# 'major','minor','aug','dim'|'MM7','Mm7','mm7','dm7','dd7'
    invert_l=[0,1,2,3]
    def step0(chord_resolution_l): # 关于属七和弦原位解决有三个同样的音而lilypond不支持这件事
        chord_resolution_0=''
        for i in range(1):
            chord_resolution_0+=chord_resolution_l[i].note_all()+'1 '
        chord_resolution_0=' \colorNote #darkcyan  { << '+chord_resolution_0+' >>} \\\\ '

        chord_resolution_1=''
        for v2 in chord_resolution_l[1:]:
            chord_resolution_1+=v2.note_all()+'1 '
        chord_resolution_1=' \colorNote #darkcyan { << '+chord_resolution_1+' >>} '
        chord_resolution=chord_resolution_0+chord_resolution_1
        return chord_resolution
    def step1():
        Mm_t,chord_t,chord_l,chord_resolution_l=module.random_chord_resolution(range_low_c,range_high_c,key_num_l,sharp_flat_l,modal_l,chord_name_l,invert_l)
        # 和弦的音
        chord_0=''
        for v1 in chord_l:
            chord_0+=v1.note_all()+' '
        chord=' < '+chord_0+' >1 '
        # 和弦解决的音，注意两个音上不能叠在一起的事情
        if chord_t.chord_name=='Mm7' and chord_t.inversion_num==0:
            chord_resolution=step0(chord_resolution_l)
        else:
            chord_resolution_0=''
            for v2 in chord_resolution_l:
                chord_resolution_0+=v2.note_all()+' '
            chord_resolution=' < '+chord_resolution_0+' >1 '
        # 和弦的名字
        key_name='"'+Mm_t.scale_name_zh()[0]+Mm_t.scale_name_zh()[1]+Mm_t.scale_name_zh()[2]+'"'+'1*2 '
        return chord,chord_resolution,key_name
    def step2():
        chord_all,chord_resolution_all,key_name_all='','',''
        for o in range(100):
            chord_row,chord_resolution_row,key_name_row='','',''
            for i in range(4):
                chord,chord_resolution,key_name=step1()
                chord_row+=chord+' \skip1 '
                chord_resolution_row+=' \colorNote #black '+chord+' \colorNote #darkcyan '+' << '+chord_resolution+' >> '
                key_name_row+=key_name
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            chord_all+=chord_row+row_name
            chord_resolution_all+=chord_resolution_row+row_name
            key_name_all+=key_name_row
        main=chord_all
        lyric=key_name_all
        main_answer=chord_resolution_all
        lyric_answer=key_name_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='chord_resolution'
        ly_t.interval_resolution(question)
        return '运行完成'
    step2()
    return '运行完成'

def write_Mm_scale():
    # 专有参数
    key_num_l=[0,1,2,3,4,5,6,7]
    sharp_flat_l=['sharp','flat']
    modal_l=[[['major'],['nature']],[['minor'],['nature']]]
    def step1():
        Mm_t,octave_l,asc_des=module.random_Mm_scale(range_low_c,range_high_c,key_num_l,sharp_flat_l,modal_l)
        # 调号是否使用
        key_sign=random.choice(['使用调号','使用调号'])
        key_ly=Mm_t.key_t.key_sign_ly() if key_sign=='使用调号' else '\key c \major'
        # 音阶的音
        scale_l=[v1.note_all() for v1 in octave_l]
        scale=' \colorAccidental #darkcyan '+key_ly+' '+'1 '.join(scale_l)
        # 音阶的名称
        tonic,modal2,modal1=Mm_t.scale_name_zh()
        if Mm_t.modal_l==['minor','melody'] and asc_des=='des':
            modal2=random.choice(['旋律','自然'])
        asc_des_name='，上行' if asc_des=='asc' else '，下行'
        scale_name=tonic+modal2+modal1+asc_des_name+'，'+key_sign+'1*8'
        # 跳过的空白
        scale_skip=' \skip1*8 '
        return scale,scale_skip,scale_name
    def step2():
        scale_all,scale_skip_all,scale_name_all='','',''
        for o in range(10):
            scale_row,scale_skip_row,scale_name_row='','',''
            for i in range(1):
                scale,scale_skip,scale_name=step1()
                scale_row+=scale
                scale_skip_row+=scale_skip
                scale_name_row+=scale_name
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            scale_all+=scale_row+row_name
            scale_skip_all+=scale_skip_row+row_name
            scale_name_all+=scale_name_row+row_name
        # 拉起ly文件
        main=scale_skip_all
        lyric=scale_name_all
        main_answer=scale_all
        lyric_answer=scale_name_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='write_Mm_scale'
        ly_t.write_Mm_scale(question)
        return '运行完成'
    step2()
    return '运行完成'

def write_church_scale():
    # 专有参数
    key_num_l=[0,1,2,3,4,5,6,7]
    sharp_flat_l=['sharp','flat']
    modal_num_l=[1,2,3,4,5,6,7]
    def step1():
        church_t,octave_l,asc_des=module.random_church_scale(range_low_c,range_high_c,key_num_l,sharp_flat_l,modal_num_l)
        # 调号是否使用
        key_sign=random.choice(['使用调号','不使用调号'])
        key_ly=church_t.key_t.key_sign_ly() if key_sign=='使用调号' else '\key c \major'
        # 音阶的音
        scale_l=[v1.note_all() for v1 in octave_l]
        scale=' \colorAccidental #darkcyan '+key_ly+' '+'1 '.join(scale_l)
        # 音阶的名称
        asc_des_name='，上行' if asc_des=='asc' else '，下行'
        scale_name=church_t.scale_name_zh()+asc_des_name+'，'+key_sign+' 1*8 '
        # 跳过的空白
        scale_skip=' \skip1*8 '
        return scale,scale_skip,scale_name
    def step2():
        scale_all,scale_skip_all,scale_name_all='','',''
        for o in range(100):
            scale_row,scale_skip_row,scale_name_row='','',''
            for i in range(1):
                scale,scale_skip,scale_name=step1()
                scale_row+=scale
                scale_skip_row+=scale_skip
                scale_name_row+=scale_name
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            scale_all+=scale_row+row_name
            scale_skip_all+=scale_skip_row+row_name
            scale_name_all+=scale_name_row+row_name
        # 拉起ly文件
        main=scale_skip_all
        lyric=scale_name_all
        main_answer=scale_all
        lyric_answer=scale_name_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='write_church_scale'
        ly_t.write_Mm_scale(question)
        return '运行完成'
    step2()
    return '运行完成'

def write_chinese_scale():
    # 专有参数
    key_num_l=[0,1,2,3,4,5,6,7]
    sharp_flat_l=['flat','sharp']
    modal_num_l=[1,2,3,4,5]
    modal_hexa_l=[0,1]
    modal_hepta_l=[0,1,2] 
    def step1():
        chinese_scale_t=module.random_chinese_scale(range_low_c,range_high_c,key_num_l,sharp_flat_l,modal_num_l,modal_hexa_l,modal_hepta_l)
        # 调号是否使用
        key_sign=random.choice(['使用调号','不使用调号'])
        key_ly=chinese_scale_t.random_chinese_t.chinese_t.key_t.key_sign_ly() if key_sign=='使用调号' else '\key c \major'
        # 是否上下行
        asc_des=random.choice(['上行','下行'])
        # 抽取五声、六声或七声调式
        modal_kind=random.choice(['penta','hexa','hepta'])
        # 五声调式
        if modal_kind=='penta':
            penta_octave_l,scale_name=chinese_scale_t.penta()
            # 音阶里面的音 
            scale_note_l=[v1.note_all() for v1 in penta_octave_l]
            # 改变上下行
            if asc_des=='下行':
                scale_note_l.reverse()
            scale_note=key_ly+' '+'1 '.join(scale_note_l)+' \skip1*2 '
        # 六声调式
        if modal_kind=='hexa':
            hexa_octave_l,add_note,scale_name=chinese_scale_t.hexa()
            # 标记那个偏音
            add_note_num=hexa_octave_l.index([v1 for v1 in hexa_octave_l if v1.note()==add_note][0])
            # 音阶里面的音
            scale_note_l=[v1.note_all() for v1 in hexa_octave_l]
            black_note_l=[i for i in range(7) if i !=add_note_num ]
            for v1 in black_note_l:
                scale_note_l[v1]=' \colorNote #black '+scale_note_l[v1]
            scale_note_l[add_note_num]=' \colorNote #red '+scale_note_l[add_note_num] # 给偏音做标记
            # 改变上下行
            if asc_des=='下行':
                scale_note_l.reverse()
            scale_note=key_ly+' '+'1 '.join(scale_note_l)+' \skip1 '
        # 七声调式
        if modal_kind=='hepta':
            hepta_octave_l,note_47th,scale_name=chinese_scale_t.hepta()
            # 标记两个偏音
            note_47th_l=[v1 for v1 in hepta_octave_l if v1.note() in note_47th]
            note_47th_num=[hepta_octave_l.index(v1) for v1 in note_47th_l]
            # 音阶里面的音
            scale_note_l=[v1.note_all() for v1 in hepta_octave_l]
            black_note_l=[i for i in range(8) if i not in note_47th_num ]
            for v1 in black_note_l:
                scale_note_l[v1]=' \colorNote #black '+scale_note_l[v1]
            scale_note_l[note_47th_num[0]]=' \colorNote #red '+scale_note_l[note_47th_num[0]]
            scale_note_l[note_47th_num[1]]=' \colorNote #red '+scale_note_l[note_47th_num[1]]
            # 改变上下行
            if asc_des=='下行':
                scale_note_l.reverse()
            scale_note=key_ly+' '+'1 '.join(scale_note_l)
        scale_skip=' \skip1*8 '
        return scale_note,scale_skip,scale_name+'，'+asc_des+'，'+key_sign+'1*8 '
    def step2():
        scale_all,scale_skip_all,scale_name_all='','',''
        for o in range(100):
            scale_row,scale_skip_row,scale_name_row='','',''
            for i in range(1):
                scale,scale_skip,scale_name=step1()
                scale_row+=scale
                scale_skip_row+=scale_skip
                scale_name_row+=scale_name
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            scale_all+=scale_row+row_name
            scale_skip_all+=scale_skip_row+row_name
            scale_name_all+=scale_name_row+row_name
        # 拉起ly文件
        main=scale_skip_all
        lyric=scale_name_all
        main_answer=scale_all
        lyric_answer=scale_name_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='write_chinese_scale'
        ly_t.write_Mm_scale(question)
        return '运行完成'
    step2()
    return '运行完成'

def write_chromatic_scale():
    # 专有参数
    key_num_l=[0,1,2,3,4,5,6,7]
    sharp_flat_l=['sharp','flat']

    def step1():
        chromatic_scale_t=module.random_chromatic_scale(range_low_c,range_high_c,key_num_l,sharp_flat_l)
        # 选择大调半音阶或小调半音阶
        modal_kind=random.choice(['major','minor'])
        # 调号是否使用
        key_sign=random.choice(['使用调号','不使用调号'])
        # 是否上下行
        asc_des=random.choice(['上行','下行'])
        # 大调半音阶
        if modal_kind=='major':
            Mm_t,asc_octave_l,des_octave_l,scale_name=chromatic_scale_t.major()
            # 关于调号
            key_ly=Mm_t.key_t.key_sign_ly() if key_sign=='使用调号' else '\key c \major'
            # 根据上下行选择不同的列表
            octave_l=asc_octave_l if asc_des=='上行' else des_octave_l
            # 音阶中的音
            scale_note_l=[v1.note_all() for v1 in octave_l]
            for v1 in [1,3,6,8,10]:
                scale_note_l[v1]=' \colorNote #darkcyan '+scale_note_l[v1]
            for v1 in range(len(scale_note_l)):
                if v1 not in [1,3,6,8,10]:
                    scale_note_l[v1]=' \colorNote #black '+scale_note_l[v1]
            if asc_des=='下行':
                scale_note_l.reverse()
            scale_note=key_ly+' '+'1 '.join(scale_note_l)
            # 音阶的名称
            scale_name=scale_name+','+asc_des+','+key_sign+'1*13 '
        # 小调半音阶
        if modal_kind=='minor':
            Mm_t,octave_l,scale_name=chromatic_scale_t.minor()
            # 关于调号
            key_ly=Mm_t.key_t.key_sign_ly() if key_sign=='使用调号' else '\key c \major'
            # 音阶中的音
            scale_note_l=[v1.note_all() for v1 in octave_l]
            for v1 in [1,4,6,9,11]:
                scale_note_l[v1]=' \colorNote #darkcyan '+scale_note_l[v1]
            for v1 in range(len(scale_note_l)):
                if v1 not in [1,4,6,9,11]:
                    scale_note_l[v1]=' \colorNote #black '+scale_note_l[v1]
            if asc_des=='下行':
                scale_note_l.reverse()
            scale_note=key_ly+' '+'1 '.join(scale_note_l)
            # 音阶的名称
            scale_name=scale_name+','+asc_des+','+key_sign+'1*13 '
        # 跳过的空白
        scale_skip=' \skip1*13 '
        return scale_note,scale_skip,scale_name
    def step2():
        scale_all,scale_skip_all,scale_name_all='','',''
        for o in range(100):
            scale_row,scale_skip_row,scale_name_row='','',''
            for i in range(1):
                scale,scale_skip,scale_name=step1()
                scale_row+=scale
                scale_skip_row+=scale_skip
                scale_name_row+=scale_name
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            scale_all+=scale_row+row_name
            scale_skip_all+=scale_skip_row+row_name
            scale_name_all+=scale_name_row+row_name
        # 拉起ly文件
        main=scale_skip_all
        lyric=scale_name_all
        main_answer=scale_all
        lyric_answer=scale_name_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='write_chromatic_scale'
        ly_t.write_Mm_scale(question)
        return '运行完成'
    step2()
    return '运行完成'
    
# 根据大小调的音级书写音
def write_scale_Mm_step_note():
    key_num_l=[0,1,2,3,4,5,6,7]
    sharp_flat_l=['sharp','flat']
    Mm_mode_l=[[['major'],['nature']],[['minor'],['nature','harmony']]]
    scale_name_mode=1
    def step1():
        Mm_t,note,step_name=module.random_scale_Mm_step(['c',1],['c',2],key_num_l,sharp_flat_l,Mm_mode_l)
        # 得到调式名称
        v1,v2,v3=Mm_t.scale_name_zh()
        scale_name=v1+v2+v3
        # 得到音符的ly形式
        note=note.note_all()+'1 '
        return scale_name,note,step_name[scale_name_mode]
    def step2():
        qus_all,note_all,skip_all='','',''
        for o in range(100):
            qus_row,note_row,skip_row='','',''
            for i in range(4):
                scale_name,note,step_name=step1()
                qus_row+=scale_name+":"+step_name+'1 '
                note_row+=note
                skip_row+=' \skip1 '
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            qus_all+=qus_row+row_name
            note_all+=note_row+row_name
            skip_all+=skip_row
        # 拉起ly文件
        main=skip_all
        lyric=qus_all
        main_answer=note_all
        lyric_answer=qus_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='write_scale_Mm_step'
        ly_t.write_note_name(question)
        return '运行完成'
    step2()
    return '运行完成'

def write_scale_Mm_step():
    key_num_l=[0,1,2,3,4,5,6,7]
    sharp_flat_l=['sharp','flat']
    Mm_mode_l=[[['major'],['nature']],[['minor'],['nature','harmony']]]
    scale_name_mode=1
    def step1():
        Mm_t,note,step_name=module.random_scale_Mm_step(['c',1],['c',2],key_num_l,sharp_flat_l,Mm_mode_l)
        # 得到调式名称
        v1,v2,v3=Mm_t.scale_name_zh()
        scale_name=v1+v2+v3
        # 得到音符的ly形式
        note=note.note_all()+'1 '
        return scale_name,note,step_name[scale_name_mode]
    def step2():
        step_name_all,note_all,scale_name_all='','',''
        for o in range(100):
            step_name_row,note_row,scale_name_row='','',''
            for i in range(4):
                scale_name,note,step_name=step1()
                note_row+=note
                scale_name_row+=scale_name+":"+'1 '
                step_name_row+=scale_name+":"+step_name+'1 '
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            note_all+=note_row+row_name
            step_name_all+=step_name_row+row_name
            scale_name_all+=scale_name_row+row_name

        # 拉起ly文件
        main=note_all
        lyric=scale_name_all
        main_answer=note_all
        lyric_answer=step_name_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='write_scale_Mm_step'
        ly_t.write_note_name(question)
        return '运行完成'
    step2()
    return '运行完成'

def write_key_sign():
    key_num_l=[1,2,3,4,5,6,7]
    sharp_flat_l=['sharp','flat']
    def step1():
        # 随机生成一个大小调的实例
        Mm_t=module.random_Mm_t(key_num_l,sharp_flat_l,[[['major'],['nature']],[['minor'],['nature']]])
        # 得到调号书写的ly形式
        key_sign=Mm_t.key_t.key_sign_ly()+' '
        # 得到大小调的名字
        tonic,modal2,modal1=Mm_t.scale_name_zh()
        scale_name=tonic+modal1+'1 '
        # 需要跳过的空格
        skip=" \skip1 "
        return key_sign,skip,scale_name
    def step2():
        scale_name_all,key_sign_all,skip_all='','',''
        for o in range(100):
            scale_name_row,key_sign_row,skip_row='','',''
            for i in range(4):
                key_sign,skip,scale_name=step1()
                scale_name_row+=scale_name
                key_sign_row+=key_sign+skip
                skip_row+=skip
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            scale_name_all+=scale_name_row+row_name
            key_sign_all+=key_sign_row+row_name
            skip_all+=skip_row+row_name
        # 拉起ly文件
        main=skip_all
        lyric=scale_name_all
        main_answer=key_sign_all
        lyric_answer=scale_name_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='write_key_sign'
        ly_t.write_note_name(question)
        return
    step2()
    return

def enharmonic_interval():
    interval_num_l=[2,3,4,5,6,7,8]
    property_l=['M','m','p']
    def step1():
        # 控制输出等结构的等音程还是不等结构的等音程
        same_diff=random.choice(['same','diff'])
        interval_t,same_degree,diff_degree=module.random_enharmonic_interval(range_low_c,range_high_c,accidental_l,interval_num_l,property_l)
        # 音程的题目
        note_t1,note_t2=interval_t.note_t1.note_all(),interval_t.note_t2.note_all()
        interval=" < "+note_t1+" "+note_t2+" >1 "
        # 生成答案
        interval_answer_l=same_degree if same_diff=='same' else diff_degree
        interval_answer=''
        for v1 in interval_answer_l:
            note_t1,note_t2=v1.note_t1.note_all(),v1.note_t2.note_all()
            interval_answer+=" < "+note_t1+" "+note_t2+" >1 "
        # 得出要跳过多少次
        skip_num=7-len(interval_answer_l)
        skip=" \skip1*%d "%skip_num
        # 题目
        interval_kind="等结构的等音程1*8" if same_diff=='same' else "不等结构的等音程1*8"
        return interval,interval_answer,skip,interval_kind
    def step2():
        interval_all,interval_answer_all,interval_kind_all='','',''
        for o in range(10):
            interval_row,interval_answer_row,interval_kind_row='','',''
            for i in range(1):
                interval,interval_answer,skip,interval_kind=step1()
                interval_row+=interval+" \skip1*7 "
                interval_answer_row+=' \colorNote #black '+interval+' \colorNote #darkcyan '+interval_answer+skip
                interval_kind_row+=interval_kind
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            interval_all+=interval_row+row_name
            interval_answer_all+=interval_answer_row+row_name
            interval_kind_all+=interval_kind_row+row_name
        # 拉起ly文件
        main=interval_all
        lyric=interval_kind_all
        main_answer=interval_answer_all
        lyric_answer=interval_kind_all
        ly_t=create_ly.ly_set(accidental_ly,range_low_c,range_high_c,clef,main,lyric,main_answer,lyric_answer)
        question='enharmonic_interval'
        ly_t.enharmonic_interval(question)
        return
    step2()
    return

recognition_note()