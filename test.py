

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


import module
import create_ly

time_sign=[2,4]
remove_rythem_l=['1','2.','2']

def step1():
    rythem=module.random_rythem_list(time_sign,remove_rythem_l)
    return rythem
def step2():
    rythem_all=''
    for o in range(100):
        rythem_row=''
        for i in range(4):
            rythem_row+=step1()+' '
        # 行数
        start_row=0
        row_name=" \\break \set Score.currentBarNumber = #%s " %(o+2+start_row)
        rythem_all+=rythem_row+row_name
    # 拉起ly文件
    main="a'"+rythem_all
    lyric=''
    main_answer=''
    lyric_answer=''
    ly_t=create_ly.ly_set(accidental_ly,low_c,high_c,clef,main,lyric,main_answer,lyric_answer)
    question='test'
    ly_t.write_note_name(question)
    return 
step2()