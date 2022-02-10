# -*- coding: utf-8 -*-
from itertools import count
from os import remove
import random
from unittest import result
# 音符的类
class module_note:
    def __init__(self,note_num,accidental_num):
        self.note_num=note_num
        self.accidental_num=accidental_num
    #此函数作为工具，生成实例后不调用 
    def converter(self):  
        # 计算出音符在哪一组
        if self.note_num<=7 and self.note_num>=1:
            octave_num=0
        elif self.note_num > 7:
            octave_num=(self.note_num-7)//7 if self.note_num%7==0 else self.note_num//7
        else: 
            octave_num=(self.note_num-1)//7
        # 计算出不含高八度低八度的音符
        note_base_num=self.note_num-octave_num*7
        return note_base_num,octave_num
    # 音的三个基本性质
    def note(self):
        note_list=['','c','d','e','f','g','a','b']
        note=note_list[self.converter()[0]]
        return note
    def octave(self):
        octave_list=['',"'","''","'''","''''","'''''",",,,,,",",,,,",",,,",",,",","]
        octave=octave_list[self.converter()[1]]
        return octave
    def accidental(self):
        accidental_list=["","is","isis","eses","es"]
        accidental=accidental_list[self.accidental_num]
        return accidental
    # 音符的完整形式
    def note_all(self):
        note_all=self.note()+self.accidental()+self.octave()
        return note_all
    # 各音符的数值模式
    def note_num_mode(self):
        note_num=self.note_num
        note_base_num=(self.converter())[0]
        octave_num=(self.converter())[1] # 仅表示第几组
        accidental_num=self.accidental_num
        return note_num,note_base_num,accidental_num,octave_num
    # 音符名称本地化
    def note_name(self):
        # 对升降记号进行一定的处理
        zh=["","升","重升","重降","降"]
        en=["","sharp","double sharp","double flat","flat"]
        sign=["","#","x","bb","b"]
        accidental_name=[zh[self.accidental_num],en[self.accidental_num],sign[self.accidental_num]]
        # 对组别的名称进行一定的处理
        octave_name_list=['小字组',"小字一组","小字二组","小字三组","小字四组","小字五组","大字四组","大字三组","大字二组","大字一组","大字组"]
        octave_name=octave_name_list[self.converter()[1]]
        return accidental_name,octave_name
    # 把音转换成音数
    def count_num(self):
        note_base_num=self.note_num_mode()[1]
        base_l=['',1,3,5,6,8,10,12]
        # 基本音级转换
        note_num=base_l[note_base_num] if note_base_num>0 else base_l[note_base_num]*-1
        # 加上升降记号的变化
        note_num+=self.note_num_mode()[2]
        # 加上音组的变化
        note_num+=self.note_num_mode()[3]*12
        return note_num

# 音程的类
class module_interval:
    def __init__(self,note_t1,note_t2):
        self.note_t1=note_t1
        self.note_t2=note_t2
        self.minor=[['e','f'],['b','c'],['d','f'],['e','g'],['a','c'],['b','d'],['e','c'],['a','f'],['b','g'],['d','c'],['e','d'],['g','f'],['a','g'],['b','a']]
        self.aug=[['f','b'],[]]
        self.dim=[['b','f'],[]]
        self.property_1=['d_d','d','m','M','A','d_A']
        self.property_2=['d_d','d','p','A','d_A']
    def step1(self):
        interval_step1_num=self.note_t2.note_num_mode()[0]-self.note_t1.note_num_mode()[0]
        interval_step1_num+=1 # 调整成正确的度数
        return interval_step1_num
    def step2(self):
        # 排除复音程的影响
        interval_step2_num=self.step1()
        while interval_step2_num>8:
            interval_step2_num-=7
        # 计算音程的性质
        inter_list=[self.note_t1.note(),self.note_t2.note()]
            # 一四五八叫做纯
        if interval_step2_num in [1,8]:
            property_num=2
        if interval_step2_num==4 and inter_list not in self.aug:
            property_num=2
        if interval_step2_num==5 and inter_list not in self.dim:
            property_num=2
            # 二三六七有大小
        if interval_step2_num in [2,3,6,7] and inter_list in self.minor:
            property_num=2
        if interval_step2_num in [2,3,6,7] and inter_list not in self.minor:
            property_num=3
            # 增四减五也叫三全音
        if interval_step2_num==4 and inter_list in self.aug:
            property_num=3
        if interval_step2_num==5 and inter_list in self.dim:
            property_num=1
        return interval_step2_num,property_num
    def step3(self): # 标记错误的音程性质
        interval_step3_num,property_step3_num=self.step2()
        property_step3_num+=self.note_t2.note_num_mode()[2]-self.note_t1.note_num_mode()[2]
        if interval_step3_num in [3,6,7]:
            errors='fail' if property_step3_num<0 or property_step3_num>5 else ''
        elif interval_step3_num in [4,5,8]:
            errors='fail' if property_step3_num<0 or property_step3_num>4 else ''
        elif interval_step3_num==2:
            errors='fail' if property_step3_num<1 or property_step3_num>4 else ''
        elif interval_step3_num==1:
            errors='fail' if property_step3_num<2 or property_step3_num>4 else ''
        else:
            errors=''
        return property_step3_num,errors
    # 得出音程的度数
    def interval_num(self):
        interval_num1=self.step1()
        interval_num2=self.step2()[0]
        return interval_num1,interval_num2
    # 得出音程的名称|M,A的格式
    def property_name(self):
        # 确定性质列表
        interval_step_2_num=self.step2()[0]
        property_l=self.property_1 if interval_step_2_num in [2,3,6,7] else self.property_2
        # 得出性质的名字
        property_step3_num,errors=self.step3()
        property_name='fail' if errors=='fail' else property_l[property_step3_num]
        return property_name
    # 音程名称本地化
    def interval_name(self):
        # 性质名称本地化
        l_1=['d_d','d','m','M','A','d_A','p','fail']
        l_2=['倍减','减','小','大','增','倍增','纯','fail']
        property_name=l_2[l_1.index(self.property_name())]
        # 得出音程的名称
        interval_num_name=num_to_zh(self.step2()[0])
        if self.step1()>8:
            interval_name="复"+property_name+interval_num_name+'度'
            interval_name_co=property_name+num_to_zh(self.step1())+'度'
        else:
            interval_name=property_name+interval_num_name+'度'
            interval_name_co=interval_name
        return interval_name,interval_name_co
    # 以后再写吧
    def interval_name_en(self):
        l_1=['d_d','d','m','M','A','d_A','p','fail']
        l_2=['double_diminished','diminished','minor','major','augmented','double_augmented','perfect','fail']
        property_name=l_2[l_1.index(self.property_name())]
        return 

# 和弦的类
class module_chord:
    def __init__(self,root_note_t,chord_name,inversion_num):
        self.root_note=root_note_t
        self.chord_name=chord_name
        self.inversion_num=inversion_num
        self.triad_chord=['major','minor','aug','dim']
        self.seventh_chord=['MM7','Mm7','mm7','dm7','dd7']
    # 根据根音以及和弦结构生成其他的和弦音
    def create_chord_note(self):
        # 各种和弦的结构，以后可以扩展
        # 三和弦
        if self.chord_name=='major':
            interval_3,interval_5=[3,'M'],[3,'m']
        if self.chord_name=='minor':
            interval_3,interval_5=[3,'m'],[3,'M']
        if self.chord_name=='aug':
            interval_3,interval_5=[3,'M'],[3,'M']
        if self.chord_name=='dim':
            interval_3,interval_5=[3,'m'],[3,'m']
        # 七和弦
        if self.chord_name=='MM7':
            interval_3,interval_5,interval_7=[3,'M'],[3,'m'],[3,'M']
        if self.chord_name=='Mm7':
            interval_3,interval_5,interval_7=[3,'M'],[3,'m'],[3,'m']
        if self.chord_name=='mm7':
            interval_3,interval_5,interval_7=[3,'m'],[3,'M'],[3,'m']
        if self.chord_name=='dm7':
            interval_3,interval_5,interval_7=[3,'m'],[3,'m'],[3,'M']
        if self.chord_name=='dd7':
            interval_3,interval_5,interval_7=[3,'m'],[3,'m'],[3,'m']

        note_3,errors_3=interval_to_note(self.root_note,interval_3)
        note_5,errors_5=interval_to_note(note_3,interval_5)
        if self.chord_name in self.triad_chord:
            note_7=''
            errors_7=''
        else:
            note_7,errors_7=interval_to_note(note_5,interval_7)
        errors=[errors_3,errors_5,errors_7]
        return self.root_note,note_3,note_5,note_7,errors
    # 生成包含和弦音的列表
    def chord(self):
        invert=lambda x:module_note(x.note_num_mode()[0]+7,x.note_num_mode()[2])
        root_note,note_3,note_5,note_7,errors=self.create_chord_note()
        # 考虑转位音程
        if self.inversion_num==1:
            chord_normal_l=[invert(root_note),note_3,note_5,note_7]
            chord_inversion_l=[note_3,note_5,note_7,invert(root_note)]
        if self.inversion_num==2:
            chord_normal_l=[invert(root_note),invert(note_3),note_5,note_7]
            chord_inversion_l=[note_5,note_7,invert(root_note),invert(note_3)]
        if self.inversion_num==3:
            chord_normal_l=[invert(root_note),invert(note_3),invert(note_5),note_7]
            chord_inversion_l=[note_7,invert(root_note),invert(note_3),invert(note_5)]
        if self.inversion_num==0:
            chord_normal_l=[root_note,note_3,note_5,note_7]
            chord_inversion_l=[root_note,note_3,note_5,note_7]
        # 移除空集
        remove=lambda x:x.remove('') if '' in x else x
        remove(chord_normal_l)
        remove(chord_inversion_l)
        return chord_normal_l,chord_inversion_l,errors
    # 和弦名称本地化
    def chord_name_zh(self):
        # 和弦种类本地化
        triad_chord_name=['大','小','增','减']
        seventh_chord_name=['大大','大小','小小','减小','减减']
        if self.chord_name in self.triad_chord:
            chord_name=triad_chord_name[self.triad_chord.index(self.chord_name)]
        else:
            chord_name=seventh_chord_name[self.seventh_chord.index(self.chord_name)]
        # 和弦转位本地化
        triad_invert_l=['三和弦','六和弦','四六和弦','']
        seven_invert_l=['七和弦','五六和弦','三四和弦','二和弦']
        if self.chord_name in self.triad_chord:
            inversion_name=triad_invert_l[self.inversion_num]
        else:
            inversion_name=seven_invert_l[self.inversion_num]
        return chord_name,inversion_name

# 调式的类
class module_key:
    def __init__(self,key_num,sharp_flat):
        self.key_num=key_num
        self.sharp_flat=sharp_flat
        # 调式主音列表
        self.sharp_tonic_l=['c','g','d','a','e','b','f','c']
        self.flat_tonic_l=['c','f','b','e','a','d','g','c']
        # 调号列表
        self.key_sharp_l=['','f','c','g','d','a','e','b','']
        self.key_flat_l=['','b','e','a','d','g','c','f','']
        # 基本音级列表
        self.scale_base=['']+['c','d','e','f','g','a','b']*10
    # 计算出调式主音
    def tonic(self):
        tonic=self.sharp_tonic_l[self.key_num] if self.sharp_flat=='sharp' else self.flat_tonic_l[self.key_num]
        tonic_num=self.scale_base.index(tonic)
        return tonic,tonic_num
    # 获取调号的信息
    def key_list(self):
        # 调号列表
        key_list=self.key_sharp_l[:self.key_num+1] if self.sharp_flat=='sharp' else self.key_flat_l[:self.key_num+1]
        # 升降记号的建议
        add_dim=1 if self.sharp_flat=='sharp' else -1
        return key_list,add_dim
    # 调号的ly格式
    def key_sign_ly(self):
        sharp_list = ['\key c \major','\key g \major','\key d \major','\key a \major','\key e \major','\key b \major','\key fis \major','\key cis \major',]
        flat_list = ['\key c \major','\key f \major','\key bes \major','\key ees \major','\key aes \major','\key des \major','\key ges \major','\key ces \major']
        key_sign_ly=sharp_list[self.key_num] if self.sharp_flat=='sharp' else flat_list[self.key_num]
        return key_sign_ly

# 节奏的类
class module_rythem:
    def __init__(self,time_sign):
        self.time_sign=time_sign
        # 单拍子与复拍子
        if self.time_sign[0] in [2,3,4] and self.time_sign[1]==4:
            self.time_class='24_34_44'
        if self.time_sign[0] in [3,6,9,12] and self.time_sign[1]==8:
            self.time_class='38_68_98_128'
        if self.time_sign[0] in [2,3,4] and self.time_sign[1]==2:
            self.time_class='22_32_42'
        if self.time_sign[0] in [6,9,12] and self.time_sign[1]==4:
            self.time_class='64_94_124'
        if self.time_sign[0] in [3,6,9,12] and self.time_sign[1]==16:
            self.time_class='316_616_916_1216'
        # 不规则拍
        if self.time_sign[0] in [5,7] and self.time_sign[1]==16:
            self.time_class='5_7_16'
        if self.time_sign[0] in [5,7] and self.time_sign[1]==8:
            self.time_class='5_7_8'
        if self.time_sign[0] in [5,7] and self.time_sign[1]==4:
            self.time_class='5_7_4'
        if self.time_sign[0] in [5,7] and self.time_sign[1]==2:
            self.time_class='5_7_2'
        # 两个通常情况下不会使用到的拍号
        if self.time_sign[0]==2 and self.time_sign[1] in [8,16]:
            self.time_class='28_216'
        # 计算每个小节的容量，32分音符令为数字1
        type_time_converter=[2,4,8,16]
        type_time=[16,8,4,2]
        self.bar_volume=type_time_converter[type_time.index(self.time_sign[1])]*self.time_sign[0]
    
    # 计算使用什么节奏型，使用多少次的所有可能
    def select_rythem_list(self):
        def irregular():
            if self.time_sign[1]==16:
                rythem_t2=module_rythem([2,16])
                rythem_t3=module_rythem([3,16])
            if self.time_sign[1]==8:
                rythem_t2=module_rythem([2,8])
                rythem_t3=module_rythem([3,8])
            if self.time_sign[1]==4:
                rythem_t2=module_rythem([2,4])
                rythem_t3=module_rythem([3,4])
            if self.time_sign[1]==2:
                rythem_t2=module_rythem([2,2])
                rythem_t3=module_rythem([3,2])
            select_all_l2=rythem_t2.select_rythem_list()
            select_all_l3=rythem_t3.select_rythem_list()
            return select_all_l2,select_all_l3
        def main():
            # 不规则拍
            if self.time_class in ['5_7_16','5_7_8','5_7_4','5_7_2']:
                select_all_l2,select_all_l3=irregular()
                return select_all_l2,select_all_l3
            # 28_216
            if self.time_class=='28_216':
                select_all_list=[[x1] for x1 in range(10) if x1*4==self.bar_volume]
            # 24_34_44
            if self.time_class=='24_34_44':
                select_all_list=[[x1,x2,x3,x4,x5] for x1 in range(10) for x2 in range(10)for x3 in range(10)for x4 in range(10)for x5 in range(10) if x1*8+x2*8+x3*16+x4*24+x5*32==self.bar_volume]
            # 38_68_98_128
            if self.time_class=='38_68_98_128':
                select_all_list=[[x1,x2,x3,x4,x5] for x1 in range(10) for x2 in range(10)for x3 in range(10)for x4 in range(10)for x5 in range(10) if x1*12+x2*12+x3*12+x4*12+x5*24==self.bar_volume]
            # 22_32_42
            if self.time_class=='22_32_42':
                select_all_list=[[x1,x2,x3,x4] for x1 in range(10) for x2 in range(10)for x3 in range(10)for x4 in range(10) if x1*8+x2*16+x3*24+x4*32==self.bar_volume]
            # 64_94_124
            if self.time_class=='64_94_124':
                select_all_list=[[x1,x2,x3,x4,x5] for x1 in range(10) for x2 in range(10)for x3 in range(10)for x4 in range(10)for x5 in range(10) if x1*24+x2*24+x3*24+x4*24+x5*48==self.bar_volume]
            # 316_616_916_1216
            if self.time_class=='316_616_916_1216':
                select_all_list=[[x1,x2,x3,x4,x5] for x1 in range(10) for x2 in range(10)for x3 in range(10)for x4 in range(10)for x5 in range(10) if x1*6+x2*6+x3*6+x4*6+x5*12==self.bar_volume]
            return select_all_list
        return main()

    # 一个工具函数，移除掉不需要出现的节奏型类
    def remove_select_rythem_list(self,select_all_list,remove_rythem_l):
        def bool_check(remove_num,select_all_list):
            bool=0
            for v1 in select_all_list:
                bool+=1 if v1[remove_num]!=0 else 0
            return bool
        def remove():
            # 把remove_rythem_l转成remove_num_l
            if self.time_class=='24_34_44':
                remove_num_l=[['8','4','2','2.','1'].index(v1) for v1 in remove_rythem_l]
            elif self.time_class=='38_68_98_128':
                remove_num_l=[['4.1','4.2','4.3','4.4','2.'].index(v1) for v1 in remove_rythem_l]
            elif self.time_class=='22_32_42':
                remove_num_l=[['4','2','2.','1'].index(v1) for v1 in remove_rythem_l]
            elif self.time_class=='64_94_124':
                remove_num_l=[['2.1','2.2','2.3','2.4','1.'].index(v1) for v1 in remove_rythem_l]
            elif self.time_class=='316_616_916_1216':
                remove_num_l=[['8.1','8.2','8.3','8.4','4.'].index(v1) for v1 in remove_rythem_l]
            else:
                remove_num_l=[] # 28_216的时候不需要移除列表
            # 移除不能出现的列表
            for remove_num in remove_num_l:
                while bool(bool_check(remove_num,select_all_list)):
                    for v3 in select_all_list:
                        if v3[remove_num]!=0:
                            select_all_list.remove(v3)
            return select_all_list
        select_all_list=remove()
        return select_all_list

    # 根据拍号选择使用哪些节奏型
    def rythem_list(self):
        # 总时值为八分音符
        self.quaver_list=['8','16 16','16 32 32','32 32 16','32 32 32 32','16. 32','32 16 32',"\\tuplet 3/2 {a' 16 16 16 }",'32 16.']
        # 总时值为附点八分音符
        self.dotted_quaver_1_list=['8.','8 16','16 8','8 32 32','32 32 8']
        self.dotted_quaver_2_list=['8.','16 16 16','32 32 16 16','16 32 32 16','16 16 32 32','32 32 32 32 16','32 32 16 32 32','16 32 32 32 32','32 32 32 32 32 32']
        self.dotted_quaver_3_list=['8.','16. 32 16','16 16. 32','16. 32 32 32','32 32 16. 32','32 16. 16','16 32 16.','32 16. 32 32','32 32 32 16.']
        self.dotted_quaver_4_list=['8.','32 16 32 16','16 32 16 32','16 32 16 32 32','32 32 32 16 32','32 16 16 32']
        # 总时值为四分音符
        self.crotchet_list=['4','8 8','8 16 16','16 16 8','16 16 16 16','8. 16','16 8 16',"\\tuplet 3/2 {a' 8 8 8 }",'16 8.']
        # 总时值为附点四分音符
        self.dotted_crotchet_1_list=['4.','4 8','8 4','4 16 16','16 16 4']
        self.dotted_crotchet_2_list=['4.','8 8 8','16 16 8 8','8 16 16 8','8 8 16 16','16 16 16 16 8','16 16 8 16 16','8 16 16 16 16','16 16 16 16 16 16']
        self.dotted_crotchet_3_list=['4.','8. 16 8','8 8. 16','8. 16 16 16','16 16 8. 16','16 8. 8','8 16 8.','16 8. 16 16','16 16 16 8.']
        self.dotted_crotchet_4_list=['4.','16 8 16 8','8 16 8 16','8 16 8 16 16','16 16 16 8 16','16 8 8 16']
        # 总时值为二分音符
        self.minim_list=['2','4. 8','4. 16 16','8 4 8','16 16 4 8','8 4 16 16','16 16 4 16 16','8 4.','16 16 4.']
        # 总时值为附点二分音符
        self.dotted_minim_list=['2.','8 4 4 8','16 16 4 4 8','16 16 4 4 16 16']
        self.dotted_minim_1_list=['2.','2 4','4 2','2 8 8','8 8 2']
        self.dotted_minim_2_list=['2.','4 4 4','8 8 4 4','4 8 8 4','4 4 8 8 ','8 8 8 8 4','8 8 4 8 8','4 8 8 8 8','8 8 8 8 8 8']
        self.dotted_minim_3_list=['2.','4. 8 4','4 4. 8','4. 8 8 8','8 8 4. 8','8 4. 4','4 8 4.','8 4. 8 8','8 8 8 4.']
        self.dotted_minim_4_list=['2.','8 4 8 4','4 8 4 8','4 8 4 8 8','8 8 8 4 8','8 4 4 8']
        # 总时值为全音符
        self.semibreve_list=['1','8 4 4 4 8','16 16 4 4 4 8','16 16 4 4 4 16 16']
        # 总时值为倍全音符
        self.breve_list=["\override Staff.NoteHead.style = #'altdefault a'\\breve "]

        # 28_216列表
        time_28_216_list_1=[self.quaver_list,[0,1,2,3,4,5,6,7]] # 0-7
        # 24_34_44列表1——总时值为八分音符
            # 本列表做了一些特别的处理，为了4分音符为单位拍的节奏型看起来友善一点
        time_24_34_44_list_1=[]
        time_24_34_44_list_1+=[v1+' '+v2 for v1 in self.quaver_list for v2 in self.quaver_list]
        time_24_34_44_list_1+=[v1+' '+v2 for v1 in ['8'] for v2 in self.quaver_list]
        time_24_34_44_list_1+=[v1+' '+v2 for v1 in self.quaver_list for v2 in ['8']]
        time_24_34_44_list_1=[time_24_34_44_list_1,[v1 for v1 in range(len(time_24_34_44_list_1))]]
        # 24_34_44列表2——总时值为四分音符|0-8
        time_24_34_44_list_2=[self.crotchet_list,[0,1,2,3,4]]
        # 24_34_44列表3——总时值为二分音符|0-8
        time_24_34_44_list_3=[self.minim_list,[0,1,2,3,4,5,6,7,8]]
        # 24_34_44列表4——总时值为附点二分音符|0-3
        time_24_34_44_list_4=[self.dotted_minim_list,[0,1,2,3]]
        # 24_34_44列表5——总时值为全音符|0-3
        time_24_34_44_list_5=[self.semibreve_list,[0,1,2,3]]
        # ————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
        # 38_68_98_128列表——总时值为附点四分音符
        time_38_68_98_128_list_1=[self.dotted_crotchet_1_list,[0,1,2,3,4]] # 0-4
        time_38_68_98_128_list_2=[self.dotted_crotchet_2_list,[0,1,2,3,4,5,6,7,8]] # 0-8
        time_38_68_98_128_list_3=[self.dotted_crotchet_3_list,[0,1,2,3,4,5,6,7,8]] # 0-8
        time_38_68_98_128_list_4=[self.dotted_crotchet_4_list,[0,1,2,3,4,5]] # 0-5
        # 38_68_98_128列表——总时值为附点二分音符
        time_38_68_98_128_list_5=[['2.'],[0]]
        # ————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
        # 22_32_42列表1——总时值为四分音符|0-8
        time_22_32_42_list_1=[self.crotchet_list,[0,1,2,3,4,5,6,7,8]]
        # 22_32_42列表2——总时值为二分音符|0-8
        time_22_32_42_list_2=[self.minim_list,[0,1,2,3,4,5,6,7,8]]
        # 22_32_42列表4——总时值为附点二分音符|0-3
        time_22_32_42_list_3=[self.dotted_minim_list,[0,1,2,3]]
        # 22_32_42列表5——总时值为全音符|0-3
        time_22_32_42_list_4=[self.semibreve_list,[0,1,2,3]]
        # ————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
        # 64_94_124列表——总时值为附点二分音符
        time_64_94_124_list_1=[self.dotted_minim_1_list,[0,1,2,3,4]] # 0-4
        time_64_94_124_list_2=[self.dotted_minim_2_list,[0,1,2,3,4,5,6,7,8]] # 0-8
        time_64_94_124_list_3=[self.dotted_minim_3_list,[0,1,2,3,4,5,6,7,8]] # 0-8
        time_64_94_124_list_4=[self.dotted_minim_4_list,[0,1,2,3,4,5]] # 0-5
        # 64_94_124列表——总时值为附点全音符
        time_64_94_124_list_5=[['1.'],[0]]
        # ————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
        # 316_616_916_1216——总时值为附点八分音符
        time_316_616_916_1216_list_1=[self.dotted_quaver_1_list,[0,1,2,3,4]] # 0-4
        time_316_616_916_1216_list_2=[self.dotted_quaver_2_list,[0,1,2,3,4,5,6,7,8]] # 0-8
        time_316_616_916_1216_list_3=[self.dotted_quaver_3_list,[0,1,2,3,4,5,6,7,8]] # 0-8
        time_316_616_916_1216_list_4=[self.dotted_quaver_4_list,[0,1,2,3,4,5]] # 0-5
        # 316_616_916_1216——总时值为附点四分音符
        time_316_616_916_1216_list_5=[['4.'],[0]] 
        # 整合列表
        time_82_216_list=[time_28_216_list_1]
        time_24_34_44_list=[time_24_34_44_list_1,time_24_34_44_list_2,time_24_34_44_list_3,time_24_34_44_list_4,time_24_34_44_list_5]
        time_38_68_98_128_list=[time_38_68_98_128_list_1,time_38_68_98_128_list_2,time_38_68_98_128_list_3,time_38_68_98_128_list_4,time_38_68_98_128_list_5]
        time_22_32_42_list=[time_22_32_42_list_1,time_22_32_42_list_2,time_22_32_42_list_3,time_22_32_42_list_4]
        time_64_94_124_list=[time_64_94_124_list_1,time_64_94_124_list_2,time_64_94_124_list_3,time_64_94_124_list_4,time_64_94_124_list_5]
        time_316_616_916_1216_list=[time_316_616_916_1216_list_1,time_316_616_916_1216_list_2,time_316_616_916_1216_list_3,time_316_616_916_1216_list_4,time_316_616_916_1216_list_5]
        # 进行判断
        if self.time_class=='28_216':
            rythem_list=time_82_216_list
        if self.time_class=='24_34_44':
            rythem_list=time_24_34_44_list
        if self.time_class=='38_68_98_128':
            rythem_list=time_38_68_98_128_list
        if self.time_class=='22_32_42':
            rythem_list=time_22_32_42_list
        if self.time_class=='64_94_124':
            rythem_list=time_64_94_124_list
        if self.time_class=='316_616_916_1216':
            rythem_list=time_316_616_916_1216_list
        # 不规则拍
        if self.time_class in ['5_7_16','5_7_8','5_7_4','5_7_2']:
            rythem_list=self.irregular_rythem_list()
        return rythem_list

    # 不规则拍生成
    def irregular_rythem_list(self):
        if self.time_sign[1]==16: 
            rythem_t2=module_rythem([2,16])
            rythem_t3=module_rythem([3,16])  
            rythem_list=[rythem_t2.rythem_list(),rythem_t3.rythem_list()]
        if self.time_sign[1]==8:
            rythem_t2=module_rythem([2,8])
            rythem_t3=module_rythem([3,8])  
            rythem_list=[rythem_t2.rythem_list(),rythem_t3.rythem_list()]
        if self.time_sign[1]==4: # 生成一个实例即可，比如5/4拍都是由24_34_44这一类构成的
            rythem_t=module_rythem([2,4]) 
            rythem_list=[rythem_t.rythem_list(),rythem_t.rythem_list()]
        if self.time_sign[1]==2: # 生成一个实例即可，比如5/2拍也是由22_32_42这一类构成的
            rythem_t=module_rythem([2,2]) 
            rythem_list=[rythem_t.rythem_list(),rythem_t.rythem_list()]
        return rythem_list
    
    # lilypond的连杆规则
    def beam(self,irregular_mode):
        # 确定type_time
        type_time=self.time_sign[1]
        # 确定beatStructure
        if self.time_class in ['5_7_16','5_7_8','5_7_4','5_7_2']:
            beatStructure=irregular_mode
        else:
            beatStructure='1,1,1,1,1,1,1,1'
        # 组合beam表示
        beam1=" \set Timing.beamExceptions = #'()  "
        beam2=" \set Timing.baseMoment = #(ly:make-moment 1/%d) "%type_time
        beam3=" \set Timing.beatStructure = %s "%beatStructure
        beam=beam1+beam2+beam3
        return beam
    # lilypond的拍号格式
    def time_ly(self):
        time_ly="\\time %d/%d "%(self.time_sign[0],self.time_sign[1])
        return time_ly
        
# 大小调的类
class scale_Mm:
    def __init__(self,key_num,sharp_flat,Mm_mode_c):
        self.scale_base=['']+['c','d','e','f','g','a','b']*10
        self.key_t=module_key(key_num,sharp_flat)
        self.key_num=key_num
        self.sharp_flat=sharp_flat
        self.Mm_mode_c=Mm_mode_c
    # 得出主音|顺便转换小调主音
    def tonic(self):
        if self.Mm_mode_c[0]=='minor':
            tonic_num=self.key_t.tonic()[1]+5
            tonic=self.scale_base[tonic_num]
        else:
            tonic,tonic_num=self.key_t.tonic()
        return tonic,tonic_num
    # 找到6、7级是哪几个音，升还是降
    def scale_67th(self):
        tonic_num=self.tonic()[1]
        # 找到6、7级音
        scale_6th=self.scale_base[tonic_num+5]
        scale_7th=self.scale_base[tonic_num+6]
        # 6、7级音的升降建议
        scale_67th=[]
        if self.Mm_mode_c[1]=='harmony':
            scale_67th.append(scale_6th if self.Mm_mode_c[0]=='major' else scale_7th)
        if self.Mm_mode_c[1]=='melody':
            scale_67th=[scale_6th,scale_7th]
        # 根据升降给出add_dim的建议
        add_dim=-1 if self.Mm_mode_c[0]=='major' else 1
        return scale_67th,add_dim
    # 调式音阶的名称
    def scale_name_zh(self):
        Mm_mode_l1_zh=['大调','小调']
        Mm_mode_l1=['major','minor']
        Mm_mode_l2_zh=['自然','和声','旋律']
        Mm_mode_l2=['nature','harmony','melody']
        # modal拼接
        modal1=Mm_mode_l1_zh[Mm_mode_l1.index(self.Mm_mode_c[0])]
        modal2=Mm_mode_l2_zh[Mm_mode_l2.index(self.Mm_mode_c[1])]
        # 关于主音
        sharp_flat=['','升','降']
        tonic0=sharp_flat[self.key_t.key_list()[1]] if self.tonic()[0] in self.key_t.key_list()[0] else ''
        tonic1=self.tonic()[0] if self.Mm_mode_c[0]=='minor' else self.tonic()[0].upper()
        tonic=tonic0+tonic1
        return tonic,modal2,modal1


# 中国民族性调式的类
class scale_chinese:
    def __init__(self,key_num,sharp_flat,chinese_scale_tonic_num):
        self.scale_base=['']+['c','d','e','f','g','a','b']*10
        self.chinese_scale_tonic_num=chinese_scale_tonic_num-1
        self.key_t=module_key(key_num,sharp_flat)
        self.key_tonic=self.key_t.tonic()[1] # 代表宫音的数字
    # 主音的音级
    def tonic(self):
        add_num=self.chinese_scale_tonic_num if self.chinese_scale_tonic_num not in [3,4] else self.chinese_scale_tonic_num+1 
        tonic_num=self.key_tonic+add_num
        tonic=self.scale_base[tonic_num]
        return tonic,tonic_num
    # 调式的名字，只是函数内部进行调用
    def scale_name_zh(self):
        # 关于调式
        tonic_num_l=['宫','商','角','徵','羽']
        tonic2=tonic_num_l[self.chinese_scale_tonic_num]
        # 关于主音
        sharp_flat=['','升','降']
        tonic0=sharp_flat[self.key_t.key_list()[1]] if self.tonic()[0] in self.key_t.key_list()[0] else ''
        tonic1=self.tonic()[0] if self.chinese_scale_tonic_num+1 in [2,3,5] else self.tonic()[0].upper()
        return tonic0+tonic1+tonic2
    # 五声调式
    def pentatonic(self):
        # 得出偏音的列表
        note_4th=self.scale_base[self.key_tonic+3]
        note_7th=self.scale_base[self.key_tonic+6]
        remove_list=[note_4th,note_7th]
        # 合成名字
        scale_name=self.scale_name_zh()+'五声调式'
        return remove_list,scale_name
    # 六声调式
    def hexatonic(self,chinese_hexa_num):
        # 得出特别的列表
        remove_list=self.pentatonic()[0]
        add_note=remove_list[0] if chinese_hexa_num==0 else remove_list[1]
        remove_note=remove_list[1] if chinese_hexa_num==0 else remove_list[0]
        # 合成名字
        modal_name='加清角' if chinese_hexa_num==0 else '加变宫'
        scale_name=self.scale_name_zh()+'六声调式'+'('+modal_name+')'
        return add_note,remove_note,scale_name
    # 七声调式
    def heptatonic(self,chinese_hepta_num):
        # 得出偏音的列表
        remove_list=self.pentatonic()[0]
        if chinese_hepta_num==0: # 清乐
            note_47th=[[remove_list[0],0],[remove_list[1],0]]
        if chinese_hepta_num==1: # 雅乐
            note_47th=[[remove_list[0],1],[remove_list[1],0]]
        if chinese_hepta_num==2: # 燕乐
            note_47th=[[remove_list[0],0],[remove_list[1],-1]]
        # 合成名字
        modal_name='清乐' if chinese_hepta_num==0 else '雅乐' if chinese_hepta_num==1 else '燕乐'
        scale_name=self.scale_name_zh()+'七声'+modal_name+'调式'
        return note_47th,scale_name

# 中古调式的类
class scale_church:
    def __init__(self,key_num,sharp_flat,chinese_scale_tonic_num):
        self.chinese_scale_tonic_num=chinese_scale_tonic_num-1
        self.scale_base=['']+['c','d','e','f','g','a','b']*10
        self.key_t=module_key(key_num,sharp_flat)
        self.key_tonic=self.key_t.tonic()[1] # 代表伊奥尼亚的数字
    # 主音
    def tonic(self):
        tonic_num=self.key_tonic+self.chinese_scale_tonic_num
        tonic=self.scale_base[tonic_num]
        return tonic,tonic_num
    # 调式音阶的名称
    def scale_name_zh(self):
        scale_name_l=['伊奥尼亚','多利亚','弗利几亚','利底亚','混合利底亚','爱奥里亚','洛克利亚']
        scale_name=scale_name_l[self.chinese_scale_tonic_num]
        # 关于主音
        sharp_flat=['','升','降']
        tonic0=sharp_flat[self.key_t.key_list()[1]] if self.tonic()[0] in self.key_t.key_list()[0] else ''
        tonic1=self.tonic()[0] if self.chinese_scale_tonic_num+1 in [2,3,6,7] else self.tonic()[0].upper()
        return tonic0+tonic1+scale_name+'调式'

# 半音阶的类
class scale_chromatic:
    def __init__(self,key_num,sharp_flat):
        self.key_num=key_num
        self.sharp_flat=sharp_flat
        self.scale_base=['']+['c','d','e','f','g','a','b']*10
    def major_chromatic(self):
        Mm_t=scale_Mm(self.key_num,self.sharp_flat,['major','nature'])
        tonic_num=Mm_t.tonic()[1]
        # 上行应该改变的音与升降建议
        chromatic_asc=[self.scale_base[tonic_num+v1] for v1 in [0,1,3,4,6]]
        asc_l=[[v1,v2] for v1,v2 in zip (chromatic_asc,[1,1,1,1,-1])]
        # 下行应该改变的音与升降建议
        chromatic_des=[self.scale_base[tonic_num+v1] for v1 in [1,2,3,5,6]]
        des_l=[[v1,v2] for v1,v2 in zip (chromatic_des,[-1,-1,1,-1,-1])]
        # 音阶的名字
        tonic,modal2,modal1=Mm_t.scale_name_zh()
        scale_name=tonic+modal1+'半音阶'
        return Mm_t,asc_l,des_l,scale_name
    def minor_chromatic(self):
        Mm_t=scale_Mm(self.key_num,self.sharp_flat,['minor','nature'])
        tonic_num=Mm_t.tonic()[1]
        # 应该改变的音与升降建议
        l1=[self.scale_base[tonic_num+v1] for v1 in [1,2,3,5,6]]
        chromatic_l=[[v1,v2] for v1,v2 in zip (l1,[-1,1,1,1,1])]
        # 音阶的名字
        tonic,modal2,modal1=Mm_t.scale_name_zh()
        scale_name=tonic+modal1+'半音阶'
        return Mm_t,chromatic_l,scale_name

# 音程、和弦解决的类
class module_resolution:
    def __init__(self,Mm_t):
        self.Mm_t=Mm_t
    # 音程解决
    def interval_resolution(self,note_t1,note_t2):
        # 根据传入的音找到需要解决的音级
        add_dim_1=-1 if scale_step(self.Mm_t.tonic()[0],note_t1.note()) in [2,4,6] else 1 if scale_step(self.Mm_t.tonic()[0],note_t1.note())==7 else 0
        add_dim_2=-1 if scale_step(self.Mm_t.tonic()[0],note_t2.note()) in [2,4,6] else 1 if scale_step(self.Mm_t.tonic()[0],note_t2.note())==7 else 0
        # 生成两个新的，被解决的音，并添加好调内的升降记号
        change_l=self.Mm_t.key_t.key_list()
        interval_resolution_l=add_accidental_to_note([module_note(note_t1.note_num+add_dim_1,0),module_note(note_t2.note_num+add_dim_2,0)],change_l)
        return [note_t1,note_t2],interval_resolution_l
    # 和弦解决|这怎么这么多缩进？
    def chord_resolution(self,chord_t):
        # 属七和弦与导七和弦的解决
        def Mm7_dd7_resolution():
            if chord_t.chord_name=='Mm7':
                chord_resolution=[]
                for v1 in chord_t.chord()[1]:
                    tonic=self.Mm_t.tonic()[0]
                    if chord_t.inversion_num==0:
                        add_dim=-1 if scale_step(tonic,v1.note()) in [2,4,6] else 1 if scale_step(tonic,v1.note())==7 else 3 if scale_step(tonic,v1.note())==5 else 0
                    else:
                        add_dim=-1 if scale_step(tonic,v1.note()) in [2,4,6] else 1 if scale_step(tonic,v1.note())==7 else 0
                    change_l=self.Mm_t.key_t.key_list()
                    note_resolution=add_accidental_to_note([module_note(v1.note_num+add_dim,0)],change_l)
                    chord_resolution+=note_resolution
            if chord_t.chord_name=='dd7':
                chord_resolution=[]
                for v1 in chord_t.chord()[1]:
                    tonic=self.Mm_t.tonic()[0]
                    add_dim=-1 if scale_step(tonic,v1.note()) in [4,6] else 1 if scale_step(tonic,v1.note()) in [2,7] else 0
                    change_l=self.Mm_t.key_t.key_list()
                    note_resolution=add_accidental_to_note([module_note(v1.note_num+add_dim,0)],change_l)
                    chord_resolution+=note_resolution
            chord_l=chord_t.chord()[1]
            return chord_l,chord_resolution
        def main():
            # 先判断是不是大小七和弦或者导七和弦
            if chord_t.chord_name in ['Mm7','dd7']:
                chord_l,chord_resolution=Mm7_dd7_resolution()
                return chord_l,chord_resolution
            # 找出和弦应该解决到哪个音
            chord_resolution_l=[]
            for v1 in chord_t.chord()[1]:
                add_dim=-1 if scale_step(self.Mm_t.tonic()[0],v1.note()) in [2,4,6] else 1 if scale_step(self.Mm_t.tonic()[0],v1.note())==7 else 0
                change_l=self.Mm_t.key_t.key_list()
                note_resolution=add_accidental_to_note([module_note(v1.note_num+add_dim,0)],change_l)
                chord_resolution_l+=note_resolution
            chord_l=chord_t.chord()[1]
            return chord_l,chord_resolution_l
        chord_l,chord_resolution_l=main()
        return chord_l,chord_resolution_l

# 全音半音的类
class tone_semitone:
    def __init__(self,note_t1,note_t2):
        # 保证t2的音数会大一点
        if note_t1.count_num()>note_t2.count_num():
            note_t1,note_t2=note_t2,note_t1
        self.note_t1,self.note_t2=note_t1,note_t2
    def simple(self):
        count_num=self.note_t2.count_num()-self.note_t1.count_num()
        # 查看全音半音的情况
        if count_num==0:
            tone_semitone=''
            errors='fail'
        elif count_num==1:
            tone_semitone='semitone'
            errors=''
        elif count_num==2:
            tone_semitone='tone'
            errors=''
        else:
            tone_semitone=''
            errors='fail'
        # 转成中文名称
        tone_semitone_zh='全音' if tone_semitone=='tone' else '半音'
        tone_semitone_en=tone_semitone
        return tone_semitone_zh,tone_semitone_en,errors
    def hard(self):
        tone_semitone_zh,tone_semitone_en,errors=self.simple()
        # 生成一个音程实例判断一下度数
        interval=abs(self.note_t1.note_num-self.note_t2.note_num)+1
        # 根据度数与音数判断自然全音等
        kind_en='nature' if interval==2 else 'chromatic'
        kind_zh='自然' if kind_en=='nature' else '变化'
        return kind_zh+tone_semitone_zh,kind_en+' '+tone_semitone_en,errors






# 数字转中文     
def num_to_zh(num):
    _MAPPING = ('零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二', '十三', '十四', '十五', '十六', '十七','十八', '十九')
    _P0 = ('', '十', '百', '千',)
    _S4 = 10 ** 4
    assert (0 <= num and num < _S4)
    if num < 20:
        return _MAPPING[num]
    else:
        lst = []
        while num >= 10:
            lst.append(num % 10)
            num = num / 10
        lst.append(num)
        c = len(lst)  # 位数
        result = ''

        for idx, val in enumerate(lst):
            val = int(val)
            if val != 0:
                result += _P0[idx] + _MAPPING[val]
                if idx < c - 1 and lst[idx + 1] == 0:
                    result += '零'
        return result[::-1]

# 根据音域转换成数字
def range_to_num(range_low_c,range_high_c):
    # 主要元素
    note_list=['']+['c','d','e','f','g','a','b']*10
    # 音域转换 转成数字形式
    range_high_num=note_list.index(range_high_c[0])+range_high_c[1]*7
    range_low_num=note_list.index(range_low_c[0])+range_low_c[1]*7
    return range_low_num,range_high_num

# 导出音域中所有的音的实例
def range_all_note(range_low_c,range_high_c):
    # 限制一个音域
    low,high=range_to_num(range_low_c,range_high_c)
    # 音域里所有的音
    note_num_l=[i for i in range(low,high+1)]
    # 生成一个对应的升降记号表
    accidental_l=[0]*len(note_num_l)
    # 生成音符实例
    note_list=[module_note(v1,v2) for v1,v2 in zip(note_num_l,accidental_l)]
    return note_list

# 生成等音列表
def enharmonica(note_t):
    count_num=note_t.count_num()
    # 找出上下的音
    add_dim=[1,2,-1,-2]
    accidental=[0,1,2,-1,-2]
    note_t2_l=[module_note(note_t.note_num_mode()[0]+v2,v1) for v1 in accidental for v2 in add_dim]
    # 筛选出需要的音
    result_l=[v3 for v3 in note_t2_l if v3.count_num()==count_num]
    return result_l

# 给列表上的音加上调号
def add_accidental_to_note(note_list,change_l): # note_list|list 这个列表里面都是音符的实例 change_l|list嵌套列表，前面是需要改变的音，后面是升高或降低的建议 
    i=-1
    for v1 in note_list:
        i+=1
        if v1.note() in change_l[0]:
            v1=module_note(v1.note_num,v1.accidental_num+change_l[1])
        note_list[i]=v1
    return note_list

# 音符在调内的级数
def scale_step(tonic,note): # tonic|str主音 note|str将要比较的那个音
    scale_base=['']+['c','d','e','f','g','a','b']*10
    tonic_num=scale_base.index(tonic)
    note_num=scale_base.index(note)
    if tonic_num==note_num:
        scale_step=1
    if tonic_num<note_num:
        scale_step=note_num-tonic_num+1
    if tonic_num>note_num:
        scale_step=note_num+7-tonic_num+1
    return scale_step

# 根据音程的根音与音程的名称，生成音程的冠音
def interval_to_note(note_t,interval_c): # interval_l包含了音程的名称以及音程的数字
    interval_num,interval_name=interval_c
    interval_num-=1
    note_num=note_t.note_num_mode()[0]
    note_num+=interval_num
    # 循环生成
    for v1 in [0,1,2,-1,-2]:
        note_t2=module_note(note_num,v1)
        interval_t=module_interval(note_t,note_t2)
        if interval_t.property_name()==interval_name:
            errors=''
            break
        else:
            errors='fail'
    return note_t2,errors

# 在一个调内，根据给出的根音，判断生成的和弦应该是什么性质
def judge_Mm_chord(Mm_t,root_note): # root_note|str这里传入根音的基本音级，晚点会把整个和弦加上升降记号
    def step1():
        # 得出三和弦与七和弦的基本音级列表|都是音符的实例
        scale_base=['']+['c','d','e','f','g','a','b']*10
        note_num=scale_base.index(root_note)
        convert=lambda x:module_note(note_num+x,0)
        triad_chord=[convert(0),convert(2),convert(4)]
        seventh_chord=[convert(0),convert(2),convert(4),convert(6)]
        # 加上调号
        triad_chord_l=add_accidental_to_note(triad_chord,Mm_t.key_t.key_list())
        seventh_chord_l=add_accidental_to_note(seventh_chord,Mm_t.key_t.key_list())
        # 加上67级的变化
        triad_chord_l=add_accidental_to_note(triad_chord_l,Mm_t.scale_67th())
        seventh_chord_l=add_accidental_to_note(seventh_chord_l,Mm_t.scale_67th())
        # 根据三和弦列表与七和弦列表得出升降记号列表，为了跟下一步对比
        triad_accidental_l=[v1.accidental_num for v1 in triad_chord_l]
        seventh_accidental_l=[v2.accidental_num for v2 in seventh_chord_l]
        return triad_chord_l,seventh_chord_l,triad_accidental_l,seventh_accidental_l
    def step2():
        triad_chord_l,seventh_chord_l,triad_accidental_l,seventh_accidental_l=step1()
        # 把根音传入和弦实例中并与现在的列表进行对比
        for v1 in ['major','minor','aug','dim']:
            triad_chord_t=module_chord(triad_chord_l[0],v1,0)
            # 得出和弦音的升降记号列表并进行比较
            triad_chord_acc_l=[x.accidental_num for x in triad_chord_t.chord()[0]]
            if triad_chord_acc_l==triad_accidental_l:
                triad_chord_name=v1
        for v2 in ['MM7','Mm7','mm7','dm7','dd7']:
            seventh_chord_t=module_chord(seventh_chord_l[0],v2,0)
            # 得出和弦音的升降记号列表并进行比较
            seventh_chord_acc_l=[x.accidental_num for x in seventh_chord_t.chord()[0]]
            if seventh_chord_acc_l==seventh_accidental_l:
                seventh_chord_name=v2
                break
            else:
                seventh_chord_name=''
        return triad_chord_name,seventh_chord_name
    triad_chord_name,seventh_chord_name=step2()
    return triad_chord_name,seventh_chord_name

# 根据传入的音组找到所有能用的八度
def cut_octave(note_list,tonic): # tonic|实例 主音的实例
    # 抽取这个列表里面的所有主音
    tonic_list=[v1 for v1 in note_list if v1.note()+v1.accidental()==tonic.note()+tonic.accidental()]
    # 导出八度列表
    octave_all_l=[]
    for i in range(len(tonic_list)-1):
        # 查看在音组中的位置
        tonic1_num=note_list.index(tonic_list[i])
        tonic2_num=note_list.index(tonic_list[i+1])
        # 导出这个八度
        octave_l=[note_list[v1] for v1 in range(tonic1_num,tonic2_num+1)]
        # 添加到列表存储
        octave_all_l.append(octave_l)
    return octave_all_l

# 把一个列表的音插入到另一个列表|主要被半音阶所调用
def list_insert_list(note_list,insert_list):
    note_list_copy=note_list.copy()
    for v1 in insert_list:
        for v2 in note_list_copy:
            if v2.count_num()-v1.count_num()==1:
                note_list.insert(note_list.index(v2),v1)
    return note_list

# 音程转音数
def interval_to_num(interval_c): 
    note_t1=module_note(1,0)
    note_t2=interval_to_note(note_t1,interval_c)[0]
    count_num=abs(note_t2.count_num()-note_t1.count_num())
    return count_num


# 随机生成一个音符实例
def random_create_note(range_low_c,range_high_c,accidental_l):
    low,high=range_to_num(range_low_c,range_high_c)
    # 从音域范围内直接抽取一个数字
    note_num_all=random.randint(low,high)
    # 随机选择一个升降记号
    accidental_num=random.choice(accidental_l)
    # 传入class进行处理
    note_t=module_note(note_num_all,accidental_num)
    return note_t

# 随机一个全音半音实例
def random_create_semi_tone(range_low_c,range_high_c,accidental_l,semi_tone_interval_l):
    def step1():
        note_t1=random_create_note(range_low_c,range_high_c,accidental_l)
        note_t2_add=random.choice(semi_tone_interval_l)-1 # 第二个音与第一个音间隔的度数
        note_t2=module_note(note_t1.note_num+note_t2_add,random.choice(accidental_l))
        semi_tone_t=tone_semitone(note_t1,note_t2)
        return semi_tone_t
    # 剔除报错的实例
    def step2():
        semi_tone_t=step1()
        errors=semi_tone_t.simple()[2]
        while errors=='fail':
            semi_tone_t=step1()
            errors=semi_tone_t.simple()[2]
        return semi_tone_t
    semi_tone_t=step2()
    return semi_tone_t

# 随机生成一个音程的实例
def random_interval_t(range_low_c,range_high_c,accidental_l,interval_num_l,property_l):
    def step1():
        note_t1=random_create_note(range_low_c,range_high_c,accidental_l)
        # 生成一个上方的音
        note_t2_add=random.choice(interval_num_l)-1
        note_t2=module_note(note_t1.note_num_mode()[0]+note_t2_add,random.choice(accidental_l))
        interval_t=module_interval(note_t1,note_t2)
        return interval_t
    def step2():# 控制不要生成禁止的音程
        interval_t=step1()
        while interval_t.property_name()=='fail':
            interval_t=step1()
        return interval_t
    def step3(): # 控制性质
        interval_t=step2()
        while interval_t.property_name() not in property_l:
            interval_t=step2()
        return interval_t
    def step4(): # 控制音域
        high=range_to_num(range_low_c,range_high_c)[1]
        interval_t=step3()
        while interval_t.note_t2.note_num_mode()[0] >high:
            interval_t=step3()
        return interval_t
    interval_t=step4()
    return interval_t

# 生成一组自然音程|可以控制间隔
def random_nature_interval_list(range_low_c,range_high_c,space_c,interval_num_l,property_l,list_num):
    # 默认参数
    key_num_l=[0,1,2,3,4,5,6,7]
    sharp_flat_l=['sharp','flat']
    Mm_mode_c=[['major'],['nature']],[['minor'],['nature']]
    # 算出间隔的音数
    space_min,space_max=interval_to_num(space_c[0]),interval_to_num(space_c[1])
    # 生成一个音程实例
    def step1():
        # 生成一串大小调音组
        note_list,Mm_t=random_Mm_note_list(range_low_c,range_high_c,key_num_l,sharp_flat_l,Mm_mode_c)
        # 随机选择两个音，并排列高低顺序
        note_t1,note_t2=random.choice(note_list),random.choice(note_list)
        if note_t1.note_num>note_t2.note_num:
            note_t1,note_t2=note_t2,note_t1
        # 生成一个音程实例
        interval_t=module_interval(note_t1,note_t2)
        return interval_t
    # 保证音程在我们所需的范围内
    def step2():
        interval_t=step1()
        # 在生成的时候不需要考虑音程实例中报错的情况，因为自然音程一定可以生成。
        while interval_t.interval_num[0] not in interval_num_l or interval_t.property_name()[0] not in property_l:
            interval_t=step1()
        return interval_t
    # 生成音程的列表
    def step3():
        interval_seed=step2()
        interval_l=[interval_seed]
        while len(interval_l)!=list_num:
            interval_t=step2()
            count_num1,count_num2=interval_t.note_t1.count_num(),interval_l[-1].note_t1.count_num()
            while abs(count_num1-count_num2)>space_max or abs(count_num1-count_num2)<space_min:
                interval_t=step2()
                count_num1,count_num2=interval_t.note_t1.count_num(),interval_l[-1].note_t1.count_num()
            interval_l.append(interval_t)
        return interval_l
    interval_l=step3()
    return interval_l

# 随机生成一组音程的解决
def random_interval_resolution(range_low_c,range_high_c,key_num_l,sharp_flat_l,Mm_mode_l):
    # 生成带调号的一串音
    note_l,Mm_t=random_Mm_note_list(range_low_c,range_high_c,key_num_l,sharp_flat_l,Mm_mode_l)
    # 抽取任意的两个音
    note_t1,note_t2=random.choice(note_l),random.choice(note_l)
    interval_resolution=module_resolution(Mm_t)
    [note_t1,note_t2],interval_resolution_l=interval_resolution.interval_resolution(note_t1,note_t2)
    return [note_t1,note_t2],interval_resolution_l,interval_resolution.Mm_t

# 随机生成一个和弦实例
def random_chord_t(range_low_c,range_high_c,accidental_l,chord_name_l,inversion_l): 
    def create_chord_t():
        # 更新最低音
        inversion_num=random.choice(inversion_l)
        low_add=-2 if inversion_num==1 else -4 if inversion_num==2 else -6 if inversion_num==3 else 0
        low=range_to_num(range_low_c,range_high_c)[0]
        low_t=module_note(low+low_add,0)
        low_c_new=[low_t.note(),low_t.note_num_mode()[3]]
        # 生成和弦实例
        note_t=random_create_note(low_c_new,range_high_c,accidental_l)
        chord_name=random.choice(chord_name_l)
        chord_t=module_chord(note_t,chord_name,inversion_num)
        return chord_t
    def step_1(): # 控制不要生成报错的和弦
        chord_t=create_chord_t()
        while chord_t.chord()[2]=='fail':
            chord_t=create_chord_t()
        return chord_t
    def step_2(): # 控制不要生成超过音域的和弦
        high=range_to_num(range_low_c,range_high_c)[1]
        chord_t=step_1()
        chord_l=chord_t.chord()[1]
        while chord_l[-1].note_num_mode()[0]>high:
            chord_t=step_1()
            chord_l=chord_t.chord()[1]
        return chord_t
    chord_t=step_2()
    return chord_t



# 随机生成一组和弦的解决
def random_chord_resolution(range_low_c,range_high_c,key_num_l,sharp_flat_l,Mm_mode_l,chord_name_l,inversion_l):
    # 更新最低音
    inversion_num=random.choice(inversion_l)
    low_add=-2 if inversion_num==1 else -4 if inversion_num==2 else -6 if inversion_num==3 else 0
    low=range_to_num(range_low_c,range_high_c)[0]
    low_t=module_note(low+low_add,0)
    low_c_new=[low_t.note(),low_t.note_num_mode()[3]]
    def step1():
        # 随机一个大小调
        Mm_t=random_Mm_t(key_num_l,sharp_flat_l,Mm_mode_l)
        # 随机一个根音，并求出在这个调里应该是什么和弦
        root_note_t=random_create_note(low_c_new,range_high_c,[0])
        triad_chord_name,seventh_chord_name=judge_Mm_chord(Mm_t,root_note_t.note())
        return Mm_t,[triad_chord_name,seventh_chord_name],root_note_t
    def step2(): # 筛选出我们需要的和弦性质、调
        Mm_t,chord_list,root_note_t=step1()
        chord_name=random.choice(chord_name_l)
        while chord_name not in chord_list:
            Mm_t,chord_list,root_note_t=step1()
        return Mm_t,chord_name,root_note_t
    def step3():
        Mm_t,chord_name,root_note_t=step2()
        # 把根音转化成调内的根音
        root_note_t=add_accidental_to_note([root_note_t],Mm_t.key_t.key_list())[0]
        root_note_t=add_accidental_to_note([root_note_t],Mm_t.scale_67th())[0]
        chord_t=module_chord(root_note_t,chord_name,inversion_num)
        return Mm_t,chord_t
    def step4(): # 控制不要生成超过音域的和弦
        Mm_t,chord_t=step3()
        high=range_to_num(range_low_c,range_high_c)[1]
        # 循环控制
        chord_l=chord_t.chord()[1]
        while chord_l[-1].note_num_mode()[0]>high:
            Mm_t,chord_t=step3()
            chord_l=chord_t.chord()[1]
        return Mm_t,chord_t
    def step5(): # 大小七和弦不要出现在自然小调中
        Mm_t,chord_t=step4()
        while chord_t.chord_name=='Mm7' and Mm_t.Mm_mode_c==['minor','nature']:
            Mm_t,chord_t=step4()
        return Mm_t,chord_t
    def step6():
        Mm_t,chord_t=step5()
        resolution_t=module_resolution(Mm_t)
        chord_l,chord_resolution_l=resolution_t.chord_resolution(chord_t)
        return Mm_t,chord_t,chord_l,chord_resolution_l
    Mm_t,chord_t,chord_l,chord_resolution_l=step6()
    return Mm_t,chord_t,chord_l,chord_resolution_l

# 随机生成一个大小调的实例
def random_Mm_t(key_num_l,sharp_flat_l,Mm_mode_l): 
    key_num=random.choice(key_num_l)
    sharp_flat=random.choice(sharp_flat_l)
    modal=random.choice(Mm_mode_l)
    Mm_mode_list=[random.choice(modal[0]),random.choice(modal[1])]
    Mm_t=scale_Mm(key_num,sharp_flat,Mm_mode_list)
    return Mm_t

# 随机生成一个中古调式的实例
def random_church_t(key_num_l,sharp_flat_l,church_scale_tonic_l):
    key_num=random.choice(key_num_l)
    sharp_flat=random.choice(sharp_flat_l)
    chinese_scale_tonic_num=random.choice(church_scale_tonic_l)
    church_t=scale_church(key_num,sharp_flat,chinese_scale_tonic_num)
    return church_t

# 随机生成一个五声调式的实例
def random_chinese_t(key_num_l,sharp_flat_l,chinese_scale_tonic_l):
    key_num=random.choice(key_num_l)
    sharp_flat=random.choice(sharp_flat_l)
    chinese_scale_tonic_num=random.choice(chinese_scale_tonic_l)
    chinese_t=scale_chinese(key_num,sharp_flat,chinese_scale_tonic_num)
    return chinese_t

# 随机生成一个半音阶的实例
def random_chromatic_t(key_num_l,sharp_flat_l):
    key_num=random.choice(key_num_l)
    sharp_flat=random.choice(sharp_flat_l)
    chromatic_t=scale_chromatic(key_num,sharp_flat)
    return chromatic_t

# 随机生成一串大小调的音组
def random_Mm_note_list(range_low_c,range_high_c,key_num_l,sharp_flat_l,Mm_mode_l):
    note_list=range_all_note(range_low_c,range_high_c)
    Mm_t=random_Mm_t(key_num_l,sharp_flat_l,Mm_mode_l)
    # 给音加上调号
    key_list=Mm_t.key_t.key_list()
    note_list=add_accidental_to_note(note_list,key_list)
    # 对音调整6、7级
    scale_67th=Mm_t.scale_67th()
    note_list=add_accidental_to_note(note_list,scale_67th)
    return note_list,Mm_t

# 随机生成一串中古调式的音组
def random_church_note_list(range_low_c,range_high_c,key_num_l,sharp_flat_l,church_scale_tonic_l):
    note_list=range_all_note(range_low_c,range_high_c)
    church_t=random_church_t(key_num_l,sharp_flat_l,church_scale_tonic_l)
    # 给音加上调号
    key_list=church_t.key_t.key_list()
    note_list=add_accidental_to_note(note_list,key_list)
    return note_list,church_t

# 随机生成一串中国民族性调式的音组|包含五声、六声、七声
class random_chinese_note_list:
    def __init__(self,range_low_c,range_high_c,key_num_l,sharp_flat_l,chinese_scale_tonic_l,chinese_hexa_l,chinese_hepta_l):
        self.note_list=range_all_note(range_low_c,range_high_c)
        self.chinese_t=random_chinese_t(key_num_l,sharp_flat_l,chinese_scale_tonic_l)
        self.chinese_hexa_num=random.choice(chinese_hexa_l)
        self.chinese_hepta_num=random.choice(chinese_hepta_l)
    def penta(self):
        remove_list,scale_name=self.chinese_t.pentatonic()
        # 移除不需要的音
        penta_list=[v1 for v1 in self.note_list if v1.note() not in remove_list]
        # 加上调号
        penta_list=add_accidental_to_note(penta_list,self.chinese_t.key_t.key_list())
        return penta_list,scale_name
    def hexa(self):
        add_note,remove_note,scale_name=self.chinese_t.hexatonic(self.chinese_hexa_num)
        # 移除不需要的音
        hexa_list=[v1 for v1 in self.note_list if v1.note()!=remove_note]
        # 加上调号
        hexa_list=add_accidental_to_note(hexa_list,self.chinese_t.key_t.key_list())
        return hexa_list,add_note,scale_name
    def hepta(self):
        note_47th,scale_name=self.chinese_t.heptatonic(self.chinese_hepta_num)
        # 加上调号
        hepta_list=add_accidental_to_note(self.note_list,self.chinese_t.key_t.key_list())
        # 对两个偏音进行调整
        hepta_list=add_accidental_to_note(hepta_list,note_47th[0])
        hepta_list=add_accidental_to_note(hepta_list,note_47th[1])
        # 导出两个偏音的基本音级
        note_47th=[note_47th[0][0],note_47th[1][0]]
        return hepta_list,note_47th,scale_name

# 随机生成一组半音阶的音组
class random_chromatic_note_list:
    def __init__(self,range_low_c,range_high_c,key_num_l,sharp_flat_l):
        self.note_list=range_all_note(range_low_c,range_high_c)
        self.chromatic_t=random_chromatic_t(key_num_l,sharp_flat_l)
    def create_insert_note(self,note_list,chromatic_l):
        # 生成要插入的音的实例
        insert_list=[module_note(v1.note_num,v1.accidental_num) for v1 in note_list if v1.note() in [v2[0] for v2 in chromatic_l]] 
        # 加上应有的变音记号
        for i in range(len(chromatic_l)):
            insert_list=add_accidental_to_note(insert_list,[[chromatic_l[i][0]],chromatic_l[i][1]])
        # 把列表进行插入
        result_list=note_list.copy()
        result_list=list_insert_list(result_list,insert_list)
        return result_list
    def major(self):
        Mm_t,asc_l,des_l,scale_name=self.chromatic_t.major_chromatic()
        # 给音加上调号
        note_list=add_accidental_to_note(self.note_list.copy(),Mm_t.key_t.key_list())
        # 插入半音
        asc_note_list=self.create_insert_note(note_list,asc_l)
        des_note_list=self.create_insert_note(note_list,des_l)
        return Mm_t,asc_note_list,des_note_list,scale_name
    def minor(self):
        Mm_t,chromatic_l,scale_name=self.chromatic_t.minor_chromatic()
        # 给音加上调号
        note_list=add_accidental_to_note(self.note_list.copy(),Mm_t.key_t.key_list())
        # 插入半音
        note_list=self.create_insert_note(note_list,chromatic_l)
        return Mm_t,note_list,scale_name

# 随机生成一组大小调的音阶
def random_Mm_scale(range_low_c,range_high_c,key_num_l,sharp_flat_l,Mm_mode_l):
    def step1(): # 生成一个八度音的列表
        note_list,Mm_t=random_Mm_note_list(range_low_c,range_high_c,key_num_l,sharp_flat_l,Mm_mode_l)
        # 生成一个主音的实例
        tonic=add_accidental_to_note([module_note(Mm_t.tonic()[1],0)],Mm_t.key_t.key_list())[0]
        octave_l=random.choice(cut_octave(note_list,tonic))
        return Mm_t,octave_l
    def step2(): # 随机上行或下行
        Mm_t,octave_l=step1()
        asc_des='asc' if Mm_t.Mm_mode_c==['minor','melody'] else 'des' if Mm_t.Mm_mode_c==['major','melody'] else random.choice(['asc','des'])
        if asc_des=='des':
            octave_l.reverse()
        return Mm_t,octave_l,asc_des
    Mm_t,octave_l,asc_des=step2()
    return Mm_t,octave_l,asc_des

# 随机生成一组中古调式的音阶
def random_church_scale(range_low_c,range_high_c,key_num_l,sharp_flat_l,church_scale_tonic_l):
    note_list,church_t=random_church_note_list(range_low_c,range_high_c,key_num_l,sharp_flat_l,church_scale_tonic_l)
    # 生成一个主音的实例
    tonic=add_accidental_to_note([module_note(church_t.tonic()[1],0)],church_t.key_t.key_list())[0]
    octave_l=random.choice(cut_octave(note_list,tonic))
    # 随机上下行
    asc_des=random.choice(['asc','des'])
    if asc_des=='des':
        octave_l.reverse()
    return church_t,octave_l,asc_des

# 随机生成一组中国民族调式音阶
class random_chinese_scale():
    def __init__(self,range_low_c,range_high_c,key_num_l,sharp_flat_l,chinese_scale_tonic_l,chinese_hexa_l,chinese_hepta_l):
        self.random_chinese_t=random_chinese_note_list(range_low_c,range_high_c,key_num_l,sharp_flat_l,chinese_scale_tonic_l,chinese_hexa_l,chinese_hepta_l)
        # 生成一个主音的实例
        self.tonic=add_accidental_to_note([module_note(self.random_chinese_t.chinese_t.tonic()[1],0)],self.random_chinese_t.chinese_t.key_t.key_list())[0]
    def penta(self):
        note_list,scale_name=self.random_chinese_t.penta()
        penta_octave_l=random.choice(cut_octave(note_list,self.tonic))
        return penta_octave_l,scale_name
    def hexa(self):
        note_list,add_note,scale_name=self.random_chinese_t.hexa()
        hexa_octave_l=random.choice(cut_octave(note_list,self.tonic))
        return hexa_octave_l,add_note,scale_name
    def hepta(self):
        note_list,note_47th,scale_name=self.random_chinese_t.hepta()
        hepta_octave_l=random.choice(cut_octave(note_list,self.tonic))
        return hepta_octave_l,note_47th,scale_name

# 随机生成一组半音阶
class random_chromatic_scale:
    def __init__(self,range_low_c,range_high_c,key_num_l,sharp_flat_l):
        self.random_chromatic_t=random_chromatic_note_list(range_low_c,range_high_c,key_num_l,sharp_flat_l)
    def major(self):
        Mm_t,asc_note_list,des_note_list,scale_name=self.random_chromatic_t.major()
        # 生成一个主音的实例
        tonic=add_accidental_to_note([module_note(Mm_t.tonic()[1],0)],Mm_t.key_t.key_list())[0]
        # 挑选一个组别 
        asc_octave_l=random.choice(cut_octave(asc_note_list,tonic))
        des_octave_l=random.choice(cut_octave(des_note_list,tonic))
        return Mm_t,asc_octave_l,des_octave_l,scale_name
    def minor(self):
        Mm_t,note_list,scale_name=self.random_chromatic_t.minor()
        # 生成一个主音的实例
        tonic=add_accidental_to_note([module_note(Mm_t.tonic()[1],0)],Mm_t.key_t.key_list())[0]
        octave_l=random.choice(cut_octave(note_list,tonic))
        return Mm_t,octave_l,scale_name

# 根据传入的音组，随机选出几个|每两个音之间需要在一定的间隔之内
def random_select_note(note_list,space_c,list_num,important_list):
    def step1():
        # 算出间隔的音数
        space_min,space_max=interval_to_num(space_c[0]),interval_to_num(space_c[1])
        # 选出一个种子音
        max_num=len(note_list)-1
        note_seed=note_list[random.randint(0,max_num)]
        # 挑出音的列表
        result_list=[note_seed]
        while len(result_list)!=list_num:
            note_new=note_list[random.randint(0,max_num-1)]
            count_num1,count_num2=note_new.count_num(),result_list[-1].count_num()
            while abs(count_num1-count_num2)>space_max or abs(count_num1-count_num2)<space_min:
                note_new=note_list[random.randint(0,max_num-1)]
                count_num1,count_num2=note_new.count_num(),result_list[-1].count_num()
            result_list.append(note_new)
        return result_list
    def step2(): # 控制最少出现两个调号音
        result_list=step1()
        key_note=[v1 for v1 in result_list if v1.note() in important_list]
        if len(key_note)==0:
            return result_list
        while len(key_note)<2:
            result_list=step1()
            key_note=[v1 for v1 in result_list if v1.note() in important_list]
        return result_list
    result_list=step2()
    return result_list


# 随机生成一组节奏型
def random_group_rythem(rythem_c):
    rythem_t=module_rythem()
    def simple_time():
        # 选择从哪几个列表里面抽节奏型
        rythem_list=[v2 for v1,v2 in zip(rythem_c[1],rythem_t.simple_time_list) if v1!=0]
        # 随机抽取规定的节奏型
        start=-1
        rythem=[]
        for v1,v2 in zip(rythem_c[1],rythem_list):
            start+=1
            for i in range(v1):
                rythem.append(v2[random.choice(rythem_c[2][start])])
        # 打乱节奏型
        random.shuffle(rythem)
        # 计算应该生成什么拍号
        time_num=0
        for v1,v2 in zip(rythem_c[1],[1,2,3,4]):
            time_num+=v1*v2
        time_sign=' \\time %d/4 '%time_num
        return rythem,time_num,time_sign
    def compund_time():
        # 选择从哪几个列表里面抽节奏型
        rythem_list=[v2 for v1,v2 in zip(rythem_c[1],rythem_t.compund_time_list) if v1!=0]
        # 随机抽取规定的节奏型
        start=-1
        rythem=[]
        for v1,v2 in zip(rythem_c[1],rythem_list):
            start+=1
            for i in range(v1):
                rythem.append(v2[random.choice(rythem_c[2][start])])
        # 打乱节奏型
        random.shuffle(rythem)
        # 计算应该生成什么拍号
        time_num=0
        for v1,v2 in zip(rythem_c[1],[3,3,3,3,6]):
            time_num+=v1*v2
        time_sign=' \\time %d/8 '%time_num
        return rythem,time_num,time_sign
    def main():
        rythem,time_num,time_sign=simple_time() if rythem_c[0]=='simple_time' else compund_time()
        return rythem,time_num,time_sign
    rythem,time_num,time_sign=main()
    return rythem,time_num,time_sign

# 随机生成一小节的节奏型
def random_rythem_bar_list(time_sign,remove_rythem_l,irregular_mode): # remove_rythem_l在不规则拍的时候依旧只要填一个列表
    # 生成一个节奏实例
    rythem_t=module_rythem(time_sign)
    def normal():
        # 得到节奏型的select列表
        select_all_list=rythem_t.select_rythem_list()
        # 移除不需要的节奏型种类
        select_all_list=rythem_t.remove_select_rythem_list(select_all_list,remove_rythem_l)
        # 得到节奏型列表
        rythem_list=rythem_t.rythem_list()
        # 生成1小节的节奏型
        select_list=random.choice(select_all_list) # 抽取其中select列表
        rythem_l=[]
        for v1,v2 in zip(rythem_list,select_list):
            for i in range(v2):
                rythem_l.append(v1[0][random.choice(v1[1])])
        # 删除空集
        while [] in rythem_l:
            rythem_l.remove([])
        random.shuffle(rythem_l) # 打乱节奏型
        return rythem_l
    # 不规则拍的节奏型
    def irregular_rythem(select_all_l,rythem_list):
        select_list=random.choice(select_all_l) # 抽取其中select列表
        rythem_l=[]
        for v1,v2 in zip(rythem_list,select_list):
            for i in range(v2):
                rythem_l.append(v1[0][random.choice(v1[1])])
        # 删除空集
        while [] in rythem_l:
            rythem_l.remove([])
        # 打乱节奏型
        random.shuffle(rythem_l) 
        return rythem_l
    def irregular():
        # 得到节奏型的select列表
        select_all_l2,select_all_l3=rythem_t.select_rythem_list()
        # 移除不需要的节奏型种类
        select_all_l2=rythem_t.remove_select_rythem_list(select_all_l2,remove_rythem_l)
        select_all_l3=rythem_t.remove_select_rythem_list(select_all_l3,remove_rythem_l)
        # 得到节奏型列表
        rythem_time2,rythem_time3=rythem_t.rythem_list()
        # 确定好不规则拍的节奏模式
        if time_sign[0]==5:
            rythem_l2=irregular_rythem(select_all_l2,rythem_time2)
            rythem_l3=irregular_rythem(select_all_l3,rythem_time3)
            rythem_l=[rythem_l2,rythem_l3] if irregular_mode=='2,3' else [rythem_l3,rythem_l2]
        if time_sign[0]==7:
            rythem_l21=irregular_rythem(select_all_l2,rythem_time2)
            rythem_l22=irregular_rythem(select_all_l2,rythem_time2)
            rythem_l3=irregular_rythem(select_all_l3,rythem_time3)
            if irregular_mode=='2,2,3':
                rythem_l=[rythem_l21,rythem_l22,rythem_l3]
            if irregular_mode=='2,3,2':
                rythem_l=[rythem_l21,rythem_l3,rythem_l22]
            if irregular_mode=='3,2,2':
                rythem_l=[rythem_l3,rythem_l21,rythem_l22]
        return rythem_l
    def main():
        if rythem_t.time_class in ['5_7_16','5_7_8','5_7_4','5_7_2']:
            rythem_l=irregular()
        else:
            rythem_l=normal()
        return rythem_l,rythem_t
    return main()

# 生成一条节奏型|固定的拍号
def random_rythem_list(time_sign,remove_rythem_l,irregular_mode,bar_num):
    # 生成节奏型
    def step1():
        # 判断是不是不规则拍子
        if module_rythem(time_sign).time_class not in ['5_7_16','5_7_8','5_7_4','5_7_2']:
            # 生成一小节的节奏型
            rythem_list=[]
            for i in range(bar_num):
                rythem_bar,rythem_t=random_rythem_bar_list(time_sign,remove_rythem_l,irregular_mode)
                rythem_list+=rythem_bar
        else:
            # 生成一小节的节奏型
            rythem_list=[]
            for i in range(bar_num):
                rythem_bar,rythem_t=random_rythem_bar_list(time_sign,remove_rythem_l,irregular_mode)
                # 解开嵌套列表
                v2=[]
                for v1 in rythem_bar:
                    v2+=v1
                # 节奏型合到一起
                rythem_list+=v2
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

# 判断整条节奏型中的节奏型是否满足要求
def judge_rythem_list(rythem_l,time_class):
    # 默认规则
    def default_rule():
        #得到32分音符列表
        rythem_t=module_rythem([2,4])
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
            list_32=[v1 for v1 in rythem_l if v1 in rythem_32]
            if len(list_32)>2:
                errors_list.append('error')
        return errors_list
    # 控制某个节奏型出现多少次
    def rythem_control_num():
        return ['']
    # 报错信息集中
    def main():
        errors_list=default_rule()+rythem_control_num()
        errors='error' if 'error' in errors_list else ''
        return errors
    errors=main()
    return errors

# 调式中的音级
def random_scale_Mm_step(range_low_c,range_high_c,key_num_l,sharp_flat_l,Mm_mode_l):
    # 随机生成一条大小调的音组
    note_list,Mm_t=random_Mm_note_list(range_low_c,range_high_c,key_num_l,sharp_flat_l,Mm_mode_l)
    # 从中随机选择一个音
    note=random.choice(note_list)
    # 传入函数中的得到音级的数字
    tonic=Mm_t.tonic()[0]
    step_num=scale_step(tonic,note.note())
    # 根据音级的数字得到音级的名称
    step_name_l1=['','主音','上主音','中音','下属音','属音','下中音','导音']
    step_name_l2=['','I','II','III','IV','V','VI','VII']
    step_name_mode1=step_name_l1[step_num]
    step_name_mode2=step_name_l2[step_num]
    return Mm_t,note,[step_name_mode1,step_name_mode2]
