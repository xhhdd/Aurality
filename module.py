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
                tone_semitone='fail'
            elif abs(self.sharpe_flat_Dvalue)==1:
                tone_semitone='semitone'
            elif abs(self.sharpe_flat_Dvalue)==2:
                tone_semitone='tone'
            else:
                tone_semitone='fail'
        # 当两音为二度时
        if self.scale_degree==1:
            if self.t1.note() in ['e','b']:
                if self.sharpe_flat_Dvalue==0:
                    tone_semitone='semitone'
                elif self.sharpe_flat_Dvalue==1:
                    tone_semitone='tone'
                else:
                    tone_semitone='fail'
            else:
                if self.sharpe_flat_Dvalue==0:
                    tone_semitone='tone'
                elif self.sharpe_flat_Dvalue==-1:
                    tone_semitone='semitone'
                else:
                    tone_semitone='fail'
        # 当两音为三度时
        if self.scale_degree==2:
            if self.t1.note() in ['c','f','g']:
                if self.sharpe_flat_Dvalue==-3:
                    tone_semitone='semitone'
                elif self.sharpe_flat_Dvalue==-2:
                    tone_semitone='tone'
                else:
                    tone_semitone='fail'
            else:
                if self.sharpe_flat_Dvalue==-2:
                    tone_semitone='semitone'
                elif self.sharpe_flat_Dvalue==-1:
                    tone_semitone='tone'
                else:
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
        self.property_1=['d_d','d','m','M','A','d_A']
        self.property_2=['d_d','d','p','A','d_A']
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
        # 性质名称本地化
        l_1=['d_d','d','m','M','A','d_A','p','fail']
        l_2=['倍减','减','小','大','增','倍增','纯','fail']
        property_name=l_2[l_1.index(self.property_name())]

        # 得出音程的名称
        interval_num_name=num_to_str(self.step_2()[0])
        if self.step_1()>8:
            interval_name="复"+property_name+interval_num_name+'度'
            interval_name_co=property_name+num_to_str(self.step_1())+'度'
        else:
            interval_name=property_name+interval_num_name+'度'
            interval_name_co=interval_name
        return interval_name,interval_name_co
    def interval_name_en(self):
        l_1=['d_d','d','m','M','A','d_A','p','fail']
        l_2=['double_diminished','diminished','minor','major','augmented','double_augmented','perfect','fail']
        property_name=l_2[l_1.index(self.property_name())]
        return # 还没写好

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

# 根据音程的根音与音程的名称，生成音程的冠音
def interval_to_note(t1,interval_c):
    interval_num,interval_name=interval_c
    interval_num-=1
    note_num=t1.note_num_mode()[0]
    t2_note_num=note_num+interval_num
    # 循环生成一个t2的音符实例
    for v1 in [0,1,2,-1,-2]:
        t2=module_note(t2_note_num,v1)
        t3=module_interval(t1,t2)
        if t3.property_name()==interval_name:
            break
    errors=t3.step_3()[1]
    return t2,errors

class module_chord:
    def __init__(self,note_t1,chord_name,invert_class):
        self.root_note=note_t1
        self.chord_name=chord_name
        self.invert_class=invert_class
        self.triad_chord=['major','minor','aug','dim']
        self.seventh_chord=['MM7','Mm7','mm7','dm7','dd7']
    def create_chord_note(self):
        # 各种和弦的结构，以后可以扩展
        if self.chord_name=='major':
            interval_c_3=[3,'M']
            interval_c_5=[3,'m']
        if self.chord_name=='minor':
            interval_c_3=[3,'m']
            interval_c_5=[3,'M']
        if self.chord_name=='aug':
            interval_c_3=[3,'M']
            interval_c_5=[3,'M']
        if self.chord_name=='dim':
            interval_c_3=[3,'m']
            interval_c_5=[3,'m']
        # 七和弦
        if self.chord_name=='MM7':
            interval_c_3=[3,'M']
            interval_c_5=[3,'m']
            interval_c_7=[3,'M']
        if self.chord_name=='Mm7':
            interval_c_3=[3,'M']
            interval_c_5=[3,'m']
            interval_c_7=[3,'m']
        if self.chord_name=='mm7':
            interval_c_3=[3,'m']
            interval_c_5=[3,'M']
            interval_c_7=[3,'m']
        if self.chord_name=='dm7':
            interval_c_3=[3,'m']
            interval_c_5=[3,'m']
            interval_c_7=[3,'M']
        if self.chord_name=='dd7':
            interval_c_3=[3,'m']
            interval_c_5=[3,'m']
            interval_c_7=[3,'m']
        note_3,errors_3=interval_to_note(self.root_note,interval_c_3)
        note_5,errors_5=interval_to_note(note_3,interval_c_5)
        if self.chord_name in self.triad_chord:
            note_7=''
            errors_7=''
        else:
            note_7,errors_7=interval_to_note(note_5,interval_c_7)
        errors=[errors_3,errors_5,errors_7]

        return self.root_note,note_3,note_5,note_7,errors
    def chord(self):
        invert=lambda x:module_note(x.note_num_mode()[0]+7,x.note_num_mode()[2])
        # 考虑转位音程
        root_note,note_3,note_5,note_7,errors=self.create_chord_note()
        if self.invert_class==1:
            chord_l=[note_3,note_5,note_7,invert(root_note)]
        if self.invert_class==2:
            chord_l=[note_5,note_7,invert(root_note),invert(note_3)]
        if self.invert_class==3:
            chord_l=[note_7,invert(root_note),invert(note_3),invert(note_5)]
        if self.invert_class==0:
            chord_l=[root_note,note_3,note_5,note_7]
        
        if '' in chord_l:
            chord_l.remove('')
        return chord_l
    def chord_name_zh(self):
        # 和弦种类本地化
        triad_chord_name=['大','小','减','增']
        seventh_chord_name=['大大','大小','小小','减小','减减']
        if self.chord_name in self.triad_chord:
            chord_name=triad_chord_name[self.triad_chord.index(self.chord_name)]
        else:
            chord_name=seventh_chord_name[self.seventh_chord.index(self.chord_name)]
        # 和弦转位本地化
        triad_invert_l=['三和弦','六和弦','四六和弦','']
        seven_invert_l=['七和弦','五六和弦','三四和弦','二和弦']

        if self.chord_name in self.triad_chord:
            invert_name=triad_invert_l[self.invert_class]
        else:
            invert_name=seven_invert_l[self.invert_class]

        return chord_name+invert_name

def random_create_chord(low_c,high_c,sharpe_flat_l,chord_name_c,invert_class_c):
    def create_chord_t():
        # 生成根音
        note_t=random_create_note(low_c,high_c,sharpe_flat_l)
        chord_name=random.choice(chord_name_c)
        invert_class=random.choice(invert_class_c)
        chord_t=module_chord(note_t,chord_name,invert_class)
        return chord_t
    def step_1(): # 控制不要生成报错的和弦
        chord_t=create_chord_t()
        while chord_t.create_chord_note()=='fail':
            chord_t=create_chord_t()
        return chord_t
    def step_2(): # 控制不要生成超过音域的和弦
        high=range_to_num(low_c,high_c)[1]

        chord_t=step_1()
        chord_l=chord_t.chord()
        while chord_l[-1].note_num_mode()[0]>high:
            chord_t=step_1()
            chord_l=chord_t.chord()
        return chord_t
    chord_t=step_2()
    return chord_t

class module_key:
    def __init__(self,key_num,sharpe_flat,key_class,key_kind):
        # 基本元素
        self.key_num=key_num
        self.sharpe_flat=sharpe_flat
        self.key_class=key_class
        self.key_kind=key_kind
        # 基本音级
        self.scale_base=['c','d','e','f','g','a','b']
        # 大小调的调名
        self.major_sharpe=['c','g','d','a','e','b','fis','cis']
        self.major_flat=['c','f','bes','ees','aes','des','ges','ces']
        self.minor_sharpe=['a','e','b','fis','cis','gis','dis','ais']
        self.minor_flat=['a','d','g','c','f','bes','ees','aes']
        # 调号列表
        self.key_sign_sharpe_l=['','f','c','g','d','a','e','b','']
        self.key_sign_flat_l=['','b','e','a','d','g','c','f','']
    # 本函数计算出主音，返回两个结果。
    def key_tonic(self):
        # 计算出主音
        if self.key_class=='major':
            if self.sharpe_flat=='sharpe':
                key_tonic=self.major_sharpe[self.key_num]
            else:
                key_tonic=self.major_flat[self.key_num]
        if self.key_class=='minor':
            if self.sharpe_flat=='sharpe':
                key_tonic=self.minor_sharpe[self.key_num]
            else:
                key_tonic=self.minor_flat[self.key_num]
        # 计算出不带es、is的主音
        key_tonic_base=key_tonic
        if 'is' in key_tonic:
            key_tonic_base=key_tonic.replace('is','')
        if 'es' in key_tonic:
            key_tonic_base=key_tonic.replace('es','')

        return key_tonic,key_tonic_base
    # 本函数计算出主音的6级音与7级音，并带上升或降的建议
    def scale_67th(self):
        key_tonic,key_tonic_base=self.key_tonic()
        # 找到6、7级
        scale_base=self.scale_base*2
        scale_6th=scale_base[scale_base.index(key_tonic_base)+5]
        scale_7th=scale_base[scale_base.index(key_tonic_base)+6]
        # 根据调式种类输出6、7级
        if self.key_kind=='nature':
            scale_67th=[]
        if self.key_kind=='harmony':
            if self.key_class=='major':
                scale_67th=[scale_6th]
            else:
                scale_67th=[scale_7th]
        if self.key_kind=='melody':
            scale_67th=[scale_6th,scale_7th]
        # 根据升降给出add_dim的建议
        if self.key_class=='major':
            add_dim=-1
        else:
            add_dim=1
        return scale_67th,add_dim
    # 本函数输出调号列表
    def key_sign_list(self):
        # 调号列表
        if self.sharpe_flat=='sharpe':
            key_sign_list=self.key_sign_sharpe_l[:self.key_num+1]
        else:
            key_sign_list=self.key_sign_flat_l[:self.key_num+1]
        # 升降记号的建议
        if self.sharpe_flat=='sharpe':
            add_dim=1
        else:
            add_dim=-1
        return key_sign_list,add_dim
    # 本函数输出ly格式的调号标记
    def key_sign_ly(self):
        sharpe_list = ['\key c \major','\key g \major','\key d \major','\key a \major','\key e \major','\key b \major','\key fis \major','\key cis \major',]
        flat_list = ['\key c \major','\key f \major','\key bes \major','\key ees \major','\key aes \major','\key des \major','\key ges \major','\key ces \major']
        if self.sharpe_flat=='sharpe':
            key_sign_ly=sharpe_list[self.key_num]
        else:
            key_sign_ly=flat_list[self.key_num]
        return key_sign_ly
    # 调名字符化
    def key_name_Mm_zh(self):
        # 大调或小调
        if self.key_class=='major':
            key_class_str='大调'
        else:
            key_class_str='小调'
        # 得出主音与升降
        key_tonic=self.key_tonic()[0]
        if 'is' not in key_tonic and 'es' not in key_tonic:
            key_sharpeflat_str=''
        if 'is' in key_tonic:
            key_sharpeflat_str='升'
            key_tonic=key_tonic.replace('is','')
        if 'es' in key_tonic:
            key_sharpeflat_str='降'
            key_tonic=key_tonic.replace('es','')
        # 得出调式种类
        key_kind_str_l=('自然','和声','旋律')
        key_kind_l=('nature','harmony','melody')
        key_kind_str=key_kind_str_l[key_kind_l.index(self.key_kind)]
        # 主音进行大小写的转换
        if self.key_class=='major':
            key_tonic=key_tonic.upper()
        # 合成最后的两个名字
        key_sign_str=key_sharpeflat_str+key_tonic+key_kind_str+key_class_str
        key_sign_str_base=key_sharpeflat_str+key_tonic+key_class_str
        return key_sign_str,key_sign_str_base

def random_create_key(key_num_c,sharpe_flat_c,key_class_c,key_kind_c):
    key_num=random.choice(key_num_c)
    sharpe_flat=random.choice(sharpe_flat_c)
    key_class=random.choice(key_class_c)
    key_kind=random.choice(key_kind_c)
    key_t=module_key(key_num,sharpe_flat,key_class,key_kind)
    return key_t

def range_to_notelist_addkey(low_c,high_c,key_num_c,sharpe_flat_c,key_class_c,key_kind_c):
    # 本函数求出一个音域里面的所有音，并且附加了升降记号为0的列表
    def range_all_note():
        # 限制一个音域
        low,high=range_to_num(low_c,high_c)
        note_num_l=[]
        sharp_flat_l=[]
        # 取得这个音域里面的所有音
        for i in range(high-low+1):
            note_num_l.append(low)
            low+=1
        # 根据上面这个列表生成升降记号，为生成note实例做准备
        sharp_flat_l=[0]*len(note_num_l)
        return note_num_l,sharp_flat_l

    # 本函数根据列表生成音的同时，改变其中的升降记号
    def note_add_key():
        note_num_l,sharp_flat_l=range_all_note()
        # 生成一个跟调号有关的实例
        key_t=random_create_key(key_num_c,sharpe_flat_c,key_class_c,key_kind_c)
        key_sign_list,add_dim=key_t.key_sign_list()
        scale_67th,add_dim_67th=key_t.scale_67th()
        # 先给音加上调号，形成一条新的升降记号列表
        sharp_flat_l_update=[]
        for v1,v2 in zip(note_num_l,sharp_flat_l):
            t2=module_note(v1,v2)
            if t2.note() in key_sign_list:
                sharp_flat=0+add_dim
            if t2.note() not in key_sign_list:
                sharp_flat=0
            # 接着再考虑调内6、7级的情况
            if t2.note() in scale_67th:
                sharp_flat+=add_dim_67th
            sharp_flat_l_update.append(sharp_flat)
        return note_num_l,sharp_flat_l_update,key_t
        
    # 本函数把音进行转换，并得到其他的相关信息
    def note_to_scale():
        note_num_l,sharp_flat_l_update,key_t=note_add_key()
        # 得到一条所有音的列表
        note_t_l=[]
        for v1,v2 in zip(note_num_l,sharp_flat_l_update):
            t2=module_note(v1,v2)
            note_t_l.append(t2)
        return key_t,note_t_l
    key_t,note_t_l=note_to_scale()
    return key_t,note_t_l

def create_scale_8th(low_c,high_c,key_num_c,sharpe_flat_c,key_class_c,key_kind_c):
    key_t,t2_l=range_to_notelist_addkey(low_c,high_c,key_num_c,sharpe_flat_c,key_class_c,key_kind_c)
    # 首先抽出所有的调式主音
    tonic_base=key_t.key_tonic()[1]
    scale_tonic_l=[]
    for v1 in t2_l:
        if tonic_base==v1.note():
            scale_tonic_l.append(v1)
    # 随机抽取一个范围内的主音
    scale_tonic=random.choice(scale_tonic_l[:len(scale_tonic_l)-1])
    # 截取8个实例
    if t2_l.index(scale_tonic)+8 >= len(t2_l):
        scale_l=t2_l[int(t2_l.index(scale_tonic)):]
    else:
        scale_l=t2_l[int(t2_l.index(scale_tonic)):int(t2_l.index(scale_tonic)+8)]
    return key_t,scale_l

# 生成大小调音阶的准备
def random_create_Mm_scale(low_c,high_c,key_num_c,sharpe_flat_c,key_class_c,key_kind_c,asc_dsc_c):
    key_t,scale_l=create_scale_8th(low_c,high_c,key_num_c,sharpe_flat_c,key_class_c,key_kind_c)
    # 确定上行或下行
    asc_des=random.choice(asc_dsc_c)
    # 如果是旋律调式的话则更新列表
    if key_t.key_kind=='melody':
        add_dim=0
        if key_t.key_class=='major' and asc_des=='上行':
            add_dim=1
        if key_t.key_class=='minor' and asc_des=='下行':
            add_dim=-1
        sharpeflate_uppdate_6th=(scale_l[5].note_num_mode())[2]+add_dim
        sharpeflate_uppdate_7th=(scale_l[6].note_num_mode())[2]+add_dim
        # 根据新的升降记号数字替换之前的实例
        scale_l[5]=module_note(scale_l[5].note_num_mode()[0],sharpeflate_uppdate_6th)
        scale_l[6]=module_note(scale_l[6].note_num_mode()[0],sharpeflate_uppdate_7th)
    # 根据上行或下行调整列表顺序
    if asc_des=='下行':
        scale_l.reverse()
    return key_t,scale_l,asc_des

# 生成一条半音阶
def random_create_chromatic_scale(low_c,high_c,key_num_c,sharpe_flat_c,key_class_c,asc_dsc_c):
    key_t,scale_l=create_scale_8th(low_c,high_c,key_num_c,sharpe_flat_c,key_class_c,['nature'])
    # 确定上行或下行
    asc_des=random.choice(asc_dsc_c)
    add=lambda x:module_note(x.note_num_mode()[0],x.note_num_mode()[2]+1)
    dim=lambda x:module_note(x.note_num_mode()[0],x.note_num_mode()[2]-1)
    # 生成5个半音
    chromatic_l=[]
    if key_t.key_class=='major':
        if asc_des=='上行':
            for v1 in [0,1,3,4]:
                chromatic_l.append(add(scale_l[v1]))
            chromatic_l.append(dim(scale_l[6]))
        else:
            chromatic_l.append(dim(scale_l[1]))
            chromatic_l.append(dim(scale_l[2]))
            chromatic_l.append(add(scale_l[3]))
            chromatic_l.append(dim(scale_l[5]))
            chromatic_l.append(dim(scale_l[6]))
    else:
        chromatic_l.append(dim(scale_l[1]))
        for v1 in [2,3,5,6]:
            chromatic_l.append(add(scale_l[v1]))
        
    # 放到音阶里面去
    if key_t.key_class=='major':
        for v1,v2 in zip([1,3,6,8,10],chromatic_l):
            scale_l.insert(v1,v2)
    else:
        for v1,v2 in zip([0,3,5,8,10],chromatic_l):
            scale_l.insert(v1,v2) 

    # 根据上行或下行调整列表顺序
    if asc_des=='下行':
        scale_l.reverse()
    return key_t,scale_l,asc_des