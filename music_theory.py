# -*- coding: utf-8 -*-
import random
import module
import create_ly
# 与音相关
# 列表前一个是音名，后一个是组别
low_c=['c',-1]
high_c=['e',1] 
# 这是能选择的升降记号
sharpe_flat_l=[0] # -2重降，-1降，0无，1升，2重升
# 选择谱号
clef='B' 
# ly文件生成
flatsharpe_kind='@1'# ['all','@1','@12','@2','@0']  0是所有记号都有，1是没有重升重降，2是含有重升重降，3是只有重升重降，4是没有升降记号



# 根据五线谱上的音符写出音名
def read_note_1_1():
    def step_1():
        t=module.random_create_note(low_c,high_c,sharpe_flat_l)
        note_all=t.note_all()
        note_name=t.note_name()[0][2]+t.note().upper()
        return note_all,note_name
    def step_2():
        note_name_all,main_all='',''
        for o in range(100):
            main_row=''
            for i in range(10):
                note_all,note_name=step_1()
                main_row+=note_all+'1 '
                note_name_all+='"'+note_name+'"'+'1 '
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            main_all+=main_row+row_name
        # 拉起ly文件
        main=main_all
        lyric=''
        main_answer=main
        lyric_answer=note_name_all
        t=create_ly.ly_set(flatsharpe_kind,low_c,high_c,clef,main,lyric)
        t.read_note_1(main_answer,lyric_answer)
        return 
    step_2()
    return '运行完成'

def read_note_1_2(low_c,high_c,sharpe_flat_l):
    def step_1():
        t=module.random_create_note(low_c,high_c,sharpe_flat_l)
        note_all=t.note_all()
        vavb_name=t.note_name()[1]
        if '小' in vavb_name:
            note=t.note()
        else:
            note=t.note().upper()
        note_name=vavb_name+','+t.note_name()[0][0]+note
        return note_all,note_name
    def step_2():
        note_name_all,main_all,skip_all='','',''
        for o in range(100):
            main_row,skip_row='',''
            for i in range(4):
                skip_row+=' \skip1 '
                note_all,note_name=step_1()
                main_row+=note_all+'1 '
                note_name_all+='"'+note_name+'"'+'1 '
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            main_all+=main_row+row_name
            skip_all+=skip_row+row_name
        # 拉起ly文件
        main=skip_all
        lyric=note_name_all
        main_answer=main_all
        lyric_answer=note_name_all
        t=create_ly.ly_set(flatsharpe_kind,low_c,high_c,clef,main,lyric)
        t.read_note_1(main_answer,lyric_answer)
        return 
    step_2()
    return '运行完成'

# 全音、半音生成相关


def tone_semitone_1_1():
    # 两个专属参数
    t2_c=[0,1,2]
    tone_semitone_c=['tone','semitone'] #['tone','semitone']
    
    tone_semitone_all,main_all='',''
    for o in range(100):
        main_row=''
        for i in range(8):
            t=module.random_create_tone_semitone(low_c,high_c,sharpe_flat_l,t2_c)
            tone_semitone,t1,t2=t.simpel(tone_semitone_c)
            note_l=[t1.note_all()+'1',t2.note_all()+'1']
            random.shuffle(note_l)
            note=' '.join(note_l)
            main_row+=note+' ' # 音符
            tone_semitone_all+=tone_semitone[0]+'1*2 '
        # 行数
        start_row=0
        row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
        main_all+=main_row+row_name+' '
    # 拉起ly文件
    main=main_all
    lyric=''
    main_answer=main_all
    lyric_answer=tone_semitone_all
    t3=create_ly.ly_set(flatsharpe_kind,low_c,high_c,clef,main,lyric)
    question="tone_semitone_1_1"
    t3.tone_semitone(question,main_answer,lyric_answer)
    return '运行完成'
def tone_semitone_1_2():
    # 两个专属参数
    t2_c=[0,1]
    tone_semitone_c=['tone','semitone'] #['tone','semitone']
    def step_1():
        t=module.random_create_tone_semitone(low_c,high_c,sharpe_flat_l,t2_c)
        tone_semitone,t1,t2=t.simpel(tone_semitone_c)
        scale_degree=t2.note_num_mode()[0]-t1.note_num_mode()[0]
        t_l=[t1,t2]
        random.shuffle(t_l)
        # 当两个音是一度关系时
        if scale_degree==0:
            t_l=[t1,t2]
            t3=module.module_note(t2.note_num_mode()[0],t1.note_num_mode()[2])
        else:
            t3=module.module_note(t_l[1].note_num_mode()[0],0)
        return tone_semitone,t_l,t3
    def step_2():
        tone_semitone_all,main_all,main_answer_all='','',''
        for o in range(100):
            main_row,main_answer_row='',''
            for i in range(8):
                tone_semitone,t_l,t3=step_1()
                tone_semitone_all+=tone_semitone[0]+'1*2 '
                main_row+=t_l[0].note_all()+'1 '+t3.note_all()+'1 '
                main_answer_row+=' \\blackNote '+t_l[0].note_all()+'1 '+' \\redNote '+t_l[1].note_all()+'1 '
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            main_all+=main_row+row_name+' '
            main_answer_all+=main_answer_row+row_name+' '
        # 拉起ly文件
        main=main_all
        lyric=tone_semitone_all
        main_answer=main_answer_all
        lyric_answer=tone_semitone_all
        t3=create_ly.ly_set(flatsharpe_kind,low_c,high_c,clef,main,lyric)
        question="tone_semitone_1_2"
        t3.tone_semitone(question,main_answer,lyric_answer)
        return '运行完成'
    step_2()
    return '运行完成'
def tone_semitone_2_1():
    # 两个专属参数
    t2_c=[0,1,2]
    tone_semitone_c=['nature tone','nature semitone','chromatic tone','chromatic semitone'] #['nature tone','nature semitone','chromatic tone','chromatic semitone']
    
    tone_semitone_all,main_all='',''
    for o in range(100):
        main_row=''
        for i in range(8):
            t=module.random_create_tone_semitone(low_c,high_c,sharpe_flat_l,t2_c)
            tone_semitone,t1,t2=t.hard(tone_semitone_c)
            note_l=[t1.note_all()+'1',t2.note_all()+'1']
            random.shuffle(note_l)
            note=' '.join(note_l)
            main_row+=note+' ' # 音符
            tone_semitone_all+=tone_semitone[0]+'1*2 '
        # 行数
        start_row=0
        row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
        main_all+=main_row+row_name+' '
    # 拉起ly文件
    main=main_all
    lyric=''
    main_answer=main_all
    lyric_answer=tone_semitone_all
    t3=create_ly.ly_set(flatsharpe_kind,low_c,high_c,clef,main,lyric)
    question="tone_semitone_2_1"
    t3.tone_semitone(question,main_answer,lyric_answer)
    return '运行完成'

# 书写等音
def write_enharmonica():
    note_all=''
    note_answer_all=''
    for  o in range(100):
        note_answer_row=''
        note_row=''
        for i in range(5):
            note_answer_row_1=''#清零

            t1=module.random_create_note(low_c,high_c,sharpe_flat_l)
            enharmonica_l=module.enharmonica(t1)
            note_row+=t1.note_all()+'1 '+' \skip1 '
            for v1 in enharmonica_l:
                note_answer_row_1+=v1.note_all()+' '
            note_answer_row+=' \\blackNote '+t1.note_all()+'1 '+' \\blueNote '+" < "+note_answer_row_1+" >1 "
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
    t3=create_ly.ly_set(flatsharpe_kind,low_c,high_c,clef,main,lyric)
    question="write_enharmonica"
    t3.write_enharmonica(question,main_answer,lyric_answer)
    return '运行完成'

def write_interval_name():
    # 特殊参数
    interval_num_l=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    property_l=['d_d','d','m','M','A','d_A','p'] # ['d_d','d','m','M','A','d_A','p','fail']

    interval_rall=''
    lyric_answer_all=''
    for o in range(100):
        lyric_row=''
        interval_row=''
        for i in range(8):
            # 生成实例
            t1=module.random_create_interval(low_c,high_c,sharpe_flat_l,interval_num_l,property_l)
            # 音程的答案
            interval_name=t1.interval_name()[0]
            lyric_row+=interval_name+'1*2 '
            # 音程的两个音
            note_l=[t1.t1.note_all()+'1 ',t1.t2.note_all()+'1 ']
            random.shuffle(note_l)
            interval_row+=' '.join(note_l)
        # 行数
        start_row=0
        row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
        interval_rall+=interval_row+row_name
        lyric_answer_all+=lyric_row
    # 拉起ly文件
    main=interval_rall
    lyric=''
    main_answer=interval_rall
    lyric_answer=lyric_answer_all
    t3=create_ly.ly_set(flatsharpe_kind,low_c,high_c,clef,main,lyric)
    question="write_interval_name"
    t3.write_interval_name(question,main_answer,lyric_answer)
    return '运行完成'

def write_interval_note():
    # 特殊参数
    interval_num_l=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    property_l=['d_d','d','m','M','A','d_A','p'] # ['d_d','d','m','M','A','d_A','p','fail']

    lyric_all=''
    interval_all=''
    interval_answer_all=''
    for o in range(100):
        lyric_row=''
        note_row=''
        note_row_answer=''
        for i in range(4):
            # 生成实例
            t1=module.random_create_interval(low_c,high_c,sharpe_flat_l,interval_num_l,property_l)
            # 音程的题目
            note_l=[t1.t1.note_all()+'1 ',t1.t2.note_all()+'1 ']
            random.shuffle(note_l)
            note_row+=note_l[0]+" \skip1 "
            # 音程的答案
            note_row_answer+=' \\blackNote '+note_l[0]+' \\redNote '+note_l[1]
            # 音程的名称
            interval_name=t1.interval_name()[0]
            if note_l[0] !=t1.t1.note_all()+'1 ':
                asc_des=' 往下'
            else:
                asc_des=' 往上'
            lyric_row+=asc_des+interval_name+'1*2 '
        # 行数
        start_row=0
        row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
        interval_all+=note_row+row_name
        interval_answer_all+=note_row_answer+row_name
        lyric_all+=lyric_row
    # 拉起ly文件
    main=interval_all
    lyric=lyric_all
    main_answer=interval_answer_all
    lyric_answer=lyric_all
    t3=create_ly.ly_set(flatsharpe_kind,low_c,high_c,clef,main,lyric)
    question="write_interval_note"
    t3.write_interval_name(question,main_answer,lyric_answer)
    return '运行完成'

def write_chord_name():
    # 专有参数
    chord_name_c=['major','minor']  #'major','minor','aug','dim'|'MM7','Mm7','mm7','dm7','dd7'
    invert_class_c=[0,1,2] # 最多输入3 三和弦在第三转位则没有任何变化


    chord_all=''
    chord_name_row=''
    for o in range(100):
        chord_row_2=''
        for i in range(5):
            chord_row_1=''
            chord_t=module.random_create_chord(low_c,high_c,sharpe_flat_l,chord_name_c,invert_class_c)
            # 和弦名称
            chord_name_row+=chord_t.chord_name_zh()+'1 ' 
            # 和弦的音
            chord_l=chord_t.chord()
            chord_l.remove('')
            for v1 in chord_l:
                chord_row_1+=v1.note_all()+' '
            chord_row_2+=' < '+chord_row_1+' >1 '
        # 行数
        start_row=0
        row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
        chord_all+=chord_row_2+row_name
    # 拉起ly文件
    main=chord_all
    lyric=''
    main_answer=chord_all
    lyric_answer=chord_name_row
    t3=create_ly.ly_set(flatsharpe_kind,low_c,high_c,clef,main,lyric)
    question="write_chord_name"
    t3.write_chord_name(question,main_answer,lyric_answer)
    return '运行完成'

write_chord_name()