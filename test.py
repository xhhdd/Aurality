

# 与音相关
# 列表前一个是音名，后一个是组别
low_c=['a',0]
high_c=['c',3] 
# 这是能选择的升降记号
accidental_l=[0,1,-1,2,-2] # -2重降，-1降，0无，1升，2重升
# 选择谱号
clef='S' 
# ly文件生成
accidental_ly='@12'# ['all','@1','@12','@2','@0']  0是所有记号都有，1是没有重升重降，2是含有重升重降，3是只有重升重降，4是没有升降记号


import random
import module
import create_ly




def rythem_ear():
    time_sign=[4,4]
    remove_rythem_l=[]
    irregular_mode='2,3'
    bar_num=4
    def step1():
        # 生成一组节奏型
        rythem_list,rythem_t=module.random_rythem_list(time_sign,remove_rythem_l,irregular_mode,bar_num)
        rythem=' '.join(rythem_list)
        # beam连杆设置
        beam=rythem_t.beam(irregular_mode)
        # 拍号
        time_ly=rythem_t.time_ly()
        return rythem,beam,time_ly
    def step2():
        rythem_all,rythem_midi_all='',''
        for o in range(10):
            rythem_bar,rythem_midi_bar='',''
            for i in range (1):
                rythem,beam,time_ly=step1()
                rythem_midi_bar=time_ly+rythem+' \\time 2/4 \skip1 '+time_ly+rythem+' \\time 2/4 \skip1 '+time_ly+rythem
                rythem_bar+=rythem
            # 行数
            start_row=0
            row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
            rythem_all+=rythem_bar+row_name
            rythem_midi_all+='\\time 2/4 \skip1 '+rythem_midi_bar+'\\time 2/4 \skip1 '+row_name
        # 拉起ly文件
        main=rythem_midi_all
        lyric=''
        main_answer=rythem_all
        lyric_answer=''
        ly_t=create_ly.ly_set(accidental_ly,low_c,high_c,clef,main,lyric,main_answer,lyric_answer)
        question='rythem_ear'
        ly_t.rythem_ear(time_ly,beam,question)
        return 
    return step2()

rythem_ear()