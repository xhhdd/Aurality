from config import *
import module

# 判断整条节奏型中的节奏型是否满足要求
def judge_rythem_list(rythem_l,time_class):
    rythem_list=[]
    for v in rythem_l:
        rythem_list+=v
    # 默认规则
    def default_rule():
        #得到32分音符列表
        rythem_t=module.module_rythem([2,4])
        rythem_old_32=rythem_t.rythem_list()[0][0]
        rythem_reapt_32=rythem_t.rythem_list()[1][0]
            # 去重
        rythem_32=[]
        for v1 in rythem_old_32:
            if v1 not in rythem_reapt_32:
                rythem_32.append(v1)
        # 24_34_44节奏型中不要太多的32分音符
        errors_list=[]
        if time_class=='24_34_44':
            # 判断一条节奏型里面有多少个32分音符的节奏
            list_32=[v1 for v1 in rythem_list if v1 in rythem_32]
            if len(list_32)>2:
                errors_list.append('error')
        return errors_list
    # 控制某个节奏型出现多少次
    def rythem_control_num():
        errors_list=[]

        list=[v1 for v1 in rythem_list if v1 in important_rythem_list[0]]
        if len(list)<important_rythem_list[1]:
            errors_list.append('error')
        else:
            errors_list.append('')

        return errors_list
    # 报错信息集中
    def main():
        errors_list=default_rule()+rythem_control_num()
        errors='error' if 'error' in errors_list else ''
        return errors
    errors=main()
    return errors

# 生成一条节奏型|固定的拍号
def random_rythem_list(time_sign):
    # 生成节奏型
    def step1():
        # 判断是不是不规则拍子
        if module.module_rythem(time_sign).time_class not in ['5_7_16','5_7_8','5_7_4','5_7_2']:
            # 生成一小节的节奏型
            rythem_list=[]
            for i in range(list_num):
                rythem_bar,rythem_t=module.random_rythem_bar_list(time_sign)
                rythem_list.append(rythem_bar)
        else:
            # 生成一小节的节奏型
            rythem_list=[]
            for i in range(list_num):
                rythem_bar,rythem_t=module.random_rythem_bar_list(time_sign)
                # 解开嵌套列表
                v2=[]
                for v1 in rythem_bar:
                    v2+=v1
                # 节奏型合到一起
                rythem_list.append(v2)
        return rythem_list,rythem_t
    # 对整条节奏型进行判断
    def step2():
        rythem_list,rythem_t=step1()
        time_class=rythem_t.time_class
        errors=judge_rythem_list(rythem_list,time_class)
        while errors=='error':
            rythem_list,rythem_t=step1()
            time_class=rythem_t.time_class
            errors=judge_rythem_list(rythem_list,time_class)
        return rythem_list,rythem_t
    rythem_list,rythem_t=step2()
    return rythem_list,rythem_t

# 输入级数，输出一组调内的和弦
def chord_in_scale(tonic,step,chord_kind):
    # 算出代表和弦根音的数字
    scale_base=['']+['c','d','e','f','g','a','b']*10
    tonic_num=scale_base.index(tonic)
    chord_root_num=tonic_num+step-1
    chord_root=scale_base[chord_root_num]
    # 算出剩下几个音的基本音级
    chord_3=scale_base[chord_root_num+2]
    chord_5=scale_base[chord_root_num+4]
    chord_7=scale_base[chord_root_num+6]
    # 根据三和弦或七和弦输出对应的音的列表
    chord_l=[chord_root,chord_3,chord_5,chord_7] if chord_kind==7 else [chord_root,chord_3,chord_5]
    return chord_l

# 判断这个音列里含有多少个和弦音
def note_list_include_chord(note_list,chord_l):
    include_list=[]
    for v in note_list:
        if v.note() in chord_l:
            include_list.append(v)
    include_num=len(include_list)
    return include_num

# 生成一条节奏型，判断每小节音的数量
def bar_note_num(time_sign):
    rythem_list,rythem_t=random_rythem_list(time_sign)
    # 每个小节有多少个音
    bar_note_num_l=[]
    for v in rythem_list:
        bar_note_num_l.append(len(v))
    return bar_note_num_l

def make_bar_note(bar_note_num_l,important_note_list,tonic,step,chord_kind):
    def make_chord_l():
        chord_l=chord_in_scale(tonic,step,chord_kind)
    def step1():
        # 调用形成音列的函数，形成一个嵌套列表
        note_list_all=[]
        for list_num in bar_note_num_l:
            note_list,Mm_t=module.random_Mm_note_list(range_low_c,range_high_c,key_num_l,sharp_flat_l,modal_l)
            note_list=module.random_select_note(note_list,space_l,list_num,important_note_list)
            note_list_all.append(note_list)
        return note_list_all
    def step2():
        note_list_all=step1()
        for v in note_list_all:
            =note_list_include_chord(v,chord_l)