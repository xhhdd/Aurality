

# 与音相关
# 列表前一个是音名，后一个是组别
range_low_c=['a',0]
range_high_c=['c',3] 
# 这是能选择的升降记号
accidental_l=[0,1,-1,2,-2] # -2重降，-1降，0无，1升，2重升
# 选择谱号
clef='S' 
# ly文件生成
accidental_ly='@12'# ['all','@1','@12','@2','@0']  0是所有记号都有，1是没有重升重降，2是含有重升重降，3是只有重升重降，4是没有升降记号


import random
import module
import create_ly



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
        for o in range(10):
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

