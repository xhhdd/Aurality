# -*- coding: utf-8 -*-
import random


def num_to_str(num):
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
        result = u''

        for idx, val in enumerate(lst):
            val = int(val)
            if val != 0:
                result += _P0[idx] + _MAPPING[val]
                if idx < c - 1 and lst[idx + 1] == 0:
                    result += u'零'
        return result[::-1]
class module_note:
    def __init__(self,note_num_all,sharpe_flat_num):
        self.note_num_all=note_num_all
        self.sharpe_flat_num=sharpe_flat_num
    # 根据数字分离出音与vavb
    def converter(self): #此函数作为工具，生成实例后不调用
        # 计算出vavb的数值
        if self.note_num_all<=7 or self.note_num_all>=1:
            vavb_num=0
        if self.note_num_all > 7:
            if self.note_num_all%7==0:
                vavb_num=(self.note_num_all-7)//7
            else:
                vavb_num=self.note_num_all//7
        if self.note_num_all<=0:
            v2=self.note_num_all-1
            vavb_num=v2//7
        # 计算出音符的数值
        note_num=self.note_num_all-vavb_num*7
        return note_num,vavb_num
    # 音的三个基本性质
    def note(self):
        note_list=('r','c','d','e','f','g','a','b')
        note_num=(self.converter())[0]
        note=note_list[note_num]
        return note
    def vavb(self):
        vavb_list=('',"'","''","'''","''''","'''''",",,,,,",",,,,",",,,",",,",",")
        vavb_num=(self.converter())[1]
        vavb=vavb_list[vavb_num]
        return vavb
    def sharpe_flat(self):
        sharpe_flat_list=["","is","isis","eses","es"]
        sharpe_flat=sharpe_flat_list[self.sharpe_flat_num]
        return sharpe_flat
    # 音符的完整形式
    def note_all(self):
        note_all=self.note()+self.sharpe_flat()+self.vavb()
        return note_all
    # 各种音符的数值
    def note_num_mode(self):
        note_num_all=self.note_num_all
        note_num=(self.converter())[0]
        vavb_num=(self.converter())[1]# 仅表示第几组
        sharpe_flat_num=self.sharpe_flat_num
        return note_num_all,note_num,sharpe_flat_num,vavb_num
    # 音符名称本地化
    def note_name(self):
        # 对升降记号进行一定的处理
        sharpe_flat_name_list_zh=["","升","重升","重降","降"]
        sharpe_flat_name_list_en=["","sharpe","double sharpe","double flat","flat"]
        sharpe_flat_name_list_sign=["","#","x","bb","b"]
        sharpe_flat_name_zh=sharpe_flat_name_list_zh[self.sharpe_flat_num]
        sharpe_flat_name_en=sharpe_flat_name_list_en[self.sharpe_flat_num]
        sharpe_flat_name_sign=sharpe_flat_name_list_sign[self.sharpe_flat_num]
        sharpe_name=[sharpe_flat_name_zh,sharpe_flat_name_en,sharpe_flat_name_sign]
        # 对组别的名称进行一定的处理
        vavb_name_list=('小字组',"小字一组","小字二组","小字三组","小字四组","小字五组","大字四组","大字三组","大字二组","大字一组","大字组")
        vavb_num=(self.converter())[1]
        vavb_name=vavb_name_list[vavb_num]
        return sharpe_name,vavb_name
    # 加上升降记号计算音数
    def count_num(self):
        if self.note() in ['d','g','a']:
            sharpe_flat_num=self.note_num_mode()[2]*0.5
        if self.note() in ['c','f']:
            if self.note_num_mode()[2] in [1,2]:
                sharpe_flat_num=self.note_num_mode()[2]*0.5
            elif self.note_num_mode()[2] ==-1:
                sharpe_flat_num=-1
            elif self.note_num_mode()[2]==-2:
                sharpe_flat_num=-1.5
            else:
                sharpe_flat_num=0
        if self.note() in ['e','b']:
            if self.note_num_mode()[2] in [-1,-2]:
                sharpe_flat_num=self.note_num_mode()[2]*0.5
            elif self.note_num_mode()[2]==1:
                sharpe_flat_num=1
            elif self.note_num_mode()[2]==2:
                sharpe_flat_num=1.5
            else:
                sharpe_flat_num=0
        count_num=self.note_num_mode()[0]+sharpe_flat_num
        return count_num
# 根据音域转换成数字
def range_to_num(low_c,high_c):
    # 主要元素
    note_list=('r','c','d','e','f','g','a','b')
    # 音域转换 转成数字形式
    high=note_list.index(high_c[0])+high_c[1]*7
    low=note_list.index(low_c[0])+low_c[1]*7
    return low,high

# 生成音符的函数
def random_create_note(low_c,high_c,sharpe_flat_l):
    low,high=range_to_num(low_c,high_c)
    # 从音域范围内直接抽取一个数字
    note_num_all=random.randint(low,high)
    # 随机选择一个升降记号
    sharpe_flat_num=random.choice(sharpe_flat_l)
    # 传入class进行处理
    note=module_note(note_num_all,sharpe_flat_num)
    return note

class module_tone_semitone:
    # 这里传入的两个参数t2的数值要大于或等于t1
    def __init__(self,t1,t2):
        self.t1,self.t2=t1,t2
        self.scale_degree=t2.note_num_mode()[0]-t1.note_num_mode()[0]
        self.sharpe_flat_Dvalue=t2.note_num_mode()[2]-t1.note_num_mode()[2]
    def simpel(self):
        # 当两音音级相同时
        if self.scale_degree==0:
            if self.sharpe_flat_Dvalue==0:
                print('两音为等音')
                tone_semitone='fail'
            elif abs(self.sharpe_flat_Dvalue)==1:
                tone_semitone='semitone'
            elif abs(self.sharpe_flat_Dvalue)==2:
                tone_semitone='tone'
            else:
                print('超过全音半音的范围')
                tone_semitone='fail'
        # 当两音为二度时
        if self.scale_degree==1:
            if self.t1.note() in ['e','b']:
                if self.sharpe_flat_Dvalue==0:
                    tone_semitone='semitone'
                elif self.sharpe_flat_Dvalue==1:
                    tone_semitone='tone'
                else:
                    print('超过全音半音的范围')
                    tone_semitone='fail'
            else:
                if self.sharpe_flat_Dvalue==0:
                    tone_semitone='tone'
                elif self.sharpe_flat_Dvalue==-1:
                    tone_semitone='semitone'
                else:
                    print('超过全音半音的范围')
                    tone_semitone='fail'
        # 当两音为三度时
        if self.scale_degree==2:
            if self.t1.note() in ['c','f','g']:
                if self.sharpe_flat_Dvalue==-3:
                    tone_semitone='semitone'
                elif self.sharpe_flat_Dvalue==-2:
                    tone_semitone='tone'
                else:
                    print('超过全音半音的范围')
                    tone_semitone='fail'
            else:
                if self.sharpe_flat_Dvalue==-2:
                    tone_semitone='semitone'
                elif self.sharpe_flat_Dvalue==-1:
                    tone_semitone='tone'
                else:
                    print('超过全音半音的范围')
                    tone_semitone='fail'
        tone_semitone_zh='全音' if tone_semitone=='tone' else '半音'
        tone_semitone_en=tone_semitone
        return tone_semitone_zh,tone_semitone_en
    
    def hard(self):
        zh,en=self.simpel()
        if self.scale_degree==1:
            kind_en='nature'
            kind_zh='自然'
        else:
            kind_en='chromatic'
            kind_zh='变化'
        tone_semitone_zh=kind_zh+zh
        tone_semitone_en=kind_en+' '+en
        return tone_semitone_zh,tone_semitone_en

class random_create_tone_semitone:
    def __init__(self,low_c,high_c,sharpe_flat_l,t2_c):
        self.t2_c=t2_c
        self.low_c=low_c
        self.high_c=high_c
        self.sharpe_flat_l=sharpe_flat_l
    # 生成全音与半音
    def simpel(self,tone_semitone_c):
        def step_1():
            # 生成一个实例
            t1=random_create_note(self.low_c,self.high_c,self.sharpe_flat_l)
            # 生成一个上方的音
            t2_add=random.choice(self.t2_c)
            t2_sharpe_flat=random.choice(self.sharpe_flat_l)
            t2=module_note(t1.note_num_mode()[0]+t2_add,t2_sharpe_flat)
            # 生成一个全音半音实例
            t3=module_tone_semitone(t1,t2)
            tone_semitone=t3.simpel()
            return tone_semitone,t1,t2
        def step_2():
            tone_semitone,t1,t2=step_1()
            while 'fail' in tone_semitone[1] or tone_semitone[1] not in tone_semitone_c:
                tone_semitone,t1,t2=step_1()
            return tone_semitone,t1,t2
        tone_semitone,t1,t2=step_2()
        return tone_semitone,t1,t2
    def hard(self,tone_semitone_c):
        def step_1():
            # 生成一个实例
            t1=random_create_note(self.low_c,self.high_c,self.sharpe_flat_l)
            # 生成一个上方的音
            t2_add=random.choice(self.t2_c)
            t2_sharpe_flat=random.choice(self.sharpe_flat_l)
            t2=module_note(t1.note_num_mode()[0]+t2_add,t2_sharpe_flat)
            # 生成一个全音半音实例
            t3=module_tone_semitone(t1,t2)
            tone_semitone=t3.hard()
            return tone_semitone,t1,t2
        def step_2():
            tone_semitone,t1,t2=step_1()
            while 'fail' in tone_semitone[1] or tone_semitone[1] not in tone_semitone_c:
                tone_semitone,t1,t2=step_1()
            return tone_semitone,t1,t2
        tone_semitone,t1,t2=step_2()
        return tone_semitone,t1,t2

def enharmonica(t1):
    count_num=t1.count_num()
    
    # 找出上下的音
    add_dim=[1,2,-1,-2]
    sharpe_flat=[0,1,2,-1,-2]
    t2_l=[]
    for v1 in sharpe_flat:
        for v2 in add_dim:
            t2=module_note(t1.note_num_mode()[0]+v2,v1)
            t2_l.append(t2)
    # 筛选出需要的音
    t3_l=[]
    for v3 in  t2_l:
        if v3.count_num()==count_num:
            t3_l.append(v3)
    return t3_l

def note_list_space_c(low_c,high_c,sharpe_flat_l,space,list_num):
    # 对传入参数进行处理
    space_low,space_high=space[0],space[1]
    space_low,space_high=space_low-1,space_high-1
    # 根据音域生成出第一个音
    low,high=range_to_num(low_c,high_c)
    note_seed=random_create_note(low_c,high_c,sharpe_flat_l)
    # 随机生成列表中剩下的音，并且在一个范围内进行控制
    note_seed_num=note_seed.note_num_mode()[0]
    note_num_all=note_seed_num # 防止循环中改变上一个音
    note_list_num=[note_seed_num]
    for i in range(list_num-1):
        start=0
        while note_num_all>high or note_num_all<low or start==0:
            note_num_all=note_seed_num # 防止循环中改变上一个音
            start=1
                # 控制相邻两个音之间是升高还是降低|范围控制
            add=random.randint(space_low,space_high)
            dim=random.randint(space_high*(-1),space_low*(-1))
                # 随机选择+or-
            note_num_all+=random.choice([add,dim])
        note_seed_num=note_num_all # 防止循环中改变上一个音
        note_list_num.append(note_num_all)
    # 根据上面的列表生成一个升降记号列表
    note_list_sharpeflat=[note_seed.note_num_mode()[2]]
    for i in range(len(note_list_num)-1):
        note_list_sharpeflat.append(random.choice(sharpe_flat_l))
    # 把两个列表配对合成一个大列表，准备传入class
    note_list=[]
    for v1,v2 in zip(note_list_num,note_list_sharpeflat):
        note_list.append([v1,v2])
        
    return note_list

class module_interval:
    def __init__(self,t1,t2):
        self.t1=t1
        self.t2=t2
        self.minor=(
            ('e','f'),('b','c'),
            ('d','f'),('e','g'),('a','c'),('b','d'),
            ('e','c'),('a','f'),('b','g'),
            ('d','c'),('e','d'),('g','f'),('a','g'),('b','a'))
        self.aug=(('f','b'),)
        self.dim=(('b','f'),)
        self.property_1=('倍减','减','小','大','增','倍增')
        self.property_2=('倍减','减','纯','增','倍增')
    def step_1(self):
        interval_step_1_num=self.t2.note_num_mode()[0]-self.t1.note_num_mode()[0]
        interval_step_1_num+=1 # 调整成正确的度数
        return interval_step_1_num
    def step_2(self):
        interval_step_2_num=self.step_1()
        while interval_step_2_num > 8:
            interval_step_2_num-=7
        # 计算音程的性质
        inter_list=(self.t1.note(),self.t2.note())
        # 一四五八叫做纯
        if interval_step_2_num in [1,8]:
            property_num=2
        if interval_step_2_num in [4] and inter_list in self.aug:
            property_num=3

        if interval_step_2_num in [4] and inter_list not in self.aug:
            property_num=2

        if interval_step_2_num in [5] and inter_list in self.dim:
            property_num=1
        if interval_step_2_num in [5] and inter_list not in self.dim:
            property_num=2
        if interval_step_2_num in [2,3,6,7] and inter_list in self.minor:
            property_num=2
        if interval_step_2_num in [2,3,6,7] and inter_list not in self.minor:
            property_num=3
        return interval_step_2_num,property_num
    def step_3(self):
        interval_step_2_num,property_step_3_num=self.step_2()
        property_step_3_num=self.t2.note_num_mode()[2]-self.t1.note_num_mode()[2]+property_step_3_num
        # 防止错误的性质出现
        if interval_step_2_num in [3,6,7]:
            if property_step_3_num<0 or property_step_3_num>5:
                errors='fail'
            else:
                errors=''
        elif interval_step_2_num in [4,5,8]:
            if property_step_3_num<0 or property_step_3_num>4:
                errors='fail'
            else:
                errors=''
        elif interval_step_2_num in [2]:
            if property_step_3_num<1 or property_step_3_num>4:
                errors='fail'
            else:
                errors=''
        elif interval_step_2_num in [1]:
            if property_step_3_num<2 or property_step_3_num>4:
                errors='fail'
            else:
                errors=''
        else:
            errors=''
        return property_step_3_num,errors
    def property_name(self):
        # 确定性质列表
        interval_step_2_num=self.step_2()[0]
        if interval_step_2_num in [2,3,6,7]:
            property_l=self.property_1
        else:
            property_l=self.property_2
        # 得出性质的名字
        property_step_3_num,errors=self.step_3()
        if errors=='fail':
            property_name='fail'
        else:
            property_name=property_l[property_step_3_num]
        return property_name
    def interval_name(self):
        property_name=self.property_name()
        interval_num_name=num_to_str(self.step_2()[0])
        # 得出音程的名称
        if self.step_1()>8:
            interval_name="复"+property_name+interval_num_name+'度'
            interval_name_co=property_name+num_to_str(self.step_1())+'度'
        else:
            interval_name=property_name+interval_num_name+'度'
            interval_name_co=interval_name
        return interval_name,interval_name_co

def random_create_interval(low_c,high_c,sharpe_flat_l,interval_num_l,property_l):
    def step_1():
        t1=random_create_note(low_c,high_c,sharpe_flat_l)
        # 生成一个上方的音
        t2_add=random.choice(interval_num_l)-1
        t2_sharpe_flat=random.choice(sharpe_flat_l)
        t2=module_note(t1.note_num_mode()[0]+t2_add,t2_sharpe_flat)
        t3=module_interval(t1,t2)
        return t3
    def step_2():# 控制不要生成禁止的音程
        t1=step_1()
        while t1.property_name() in ['fail']:
            t1=step_1()
        return t1
    def step_3(): # 控制度数
        t1=step_2()
        while t1.step_2()[0] not in interval_num_l:
            t1=step_2()
        return t1
    def step_4(): # 控制性质
        t1=step_3()
        while t1.property_name() not in property_l:
            t1=step_3()
        return t1
    def step_5(): # 控制音域
        high=range_to_num(low_c,high_c)[1]
        t1=step_4()
        while t1.t2.note_num_mode()[0] >high:
            t1=step_4()
        return t1
    t1=step_5()
    return t1
