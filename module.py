# -*- coding: utf-8 -*-
import random
class module_note:
    def __init__(self,note_num,accidental_num):
        self.note_num=note_num
        self.accidental_num=accidental_num
    # 根据数字分离出音与vavb
    def converter(self): #此函数作为工具，生成实例后不调用  
        # 计算出vavb的数值
        if self.note_num<=7 and self.note_num>=1:
            octave_num=0
        elif self.note_num > 7:
            if self.note_num%7==0:
                octave_num=(self.note_num-7)//7
            else:
                octave_num=self.note_num//7
        else: 
            v2=self.note_num-1
            octave_num=v2//7
        # 计算出不含高八度低八度的音符
        note_base_num=self.note_num-octave_num*7
        return note_base_num,octave_num
    # 音的三个基本性质
    def note(self):
        note_list=['r','c','d','e','f','g','a','b']
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
    # 各种音符的数值
    def note_num_mode(self):
        note_num=self.note_num
        note_base_num=(self.converter())[0]
        octave_num=(self.converter())[1] # 仅表示第几组
        accidental_num=self.accidental_num
        return note_num,note_base_num,accidental_num,octave_num
    # 音符名称本地化
    def note_name(self):
        # 对升降记号进行一定的处理
        accidental_name_list_zh=["","升","重升","重降","降"]
        accidental_name_list_en=["","sharpe","double sharpe","double flat","flat"]
        accidental_name_list_sign=["","#","x","bb","b"]
        accidental_name=[accidental_name_list_zh[self.accidental_num],accidental_name_list_en[self.accidental_num],accidental_name_list_sign[self.accidental_num]]
        # 对组别的名称进行一定的处理
        octave_name_list=['小字组',"小字一组","小字二组","小字三组","小字四组","小字五组","大字四组","大字三组","大字二组","大字一组","大字组"]
        octave_name=octave_name_list[self.converter()[1]]
        return accidental_name,octave_name
    # 加上升降记号计算音数
    def count_num(self):
        if self.note() in ['d','g','a']:
            accidental_num=self.note_num_mode()[2]*0.5
        if self.note() in ['c','f']:
            if self.note_num_mode()[2] in [1,2]:
                accidental_num=self.note_num_mode()[2]*0.5
            elif self.note_num_mode()[2] ==-1:
                accidental_num=-1
            elif self.note_num_mode()[2]==-2:
                accidental_num=-1.5
            else:
                accidental_num=0
        if self.note() in ['e','b']:
            if self.note_num_mode()[2] in [-1,-2]:
                accidental_num=self.note_num_mode()[2]*0.5
            elif self.note_num_mode()[2]==1:
                accidental_num=1
            elif self.note_num_mode()[2]==2:
                accidental_num=1.5
            else:
                accidental_num=0
        count_num=self.note_num_mode()[0]+accidental_num
        return count_num

class module_interval:
    def __init__(self,note_t1,note_t2):
        self.note_t1=note_t1
        self.note_t2=note_t2
        self.minor=[['e','f'],['b','c'],['d','f'],['e','g'],['a','c'],['b','d'],['e','c'],['a','f'],['b','g'],['d','c'],['e','d'],['g','f'],['a','g'],['b','a']]
        self.aug=(('f','b'),)
        self.dim=(('b','f'),)
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
        if interval_step2_num in [4] and inter_list not in self.aug:
            property_num=2
        if interval_step2_num in [5] and inter_list not in self.dim:
            property_num=2
            # 二三六七有大小
        if interval_step2_num in [2,3,6,7] and inter_list in self.minor:
            property_num=2
        if interval_step2_num in [2,3,6,7] and inter_list not in self.minor:
            property_num=3
            # 增四减五也叫三全音
        if interval_step2_num in [4] and inter_list in self.aug:
            property_num=3
        if interval_step2_num in [5] and inter_list in self.dim:
            property_num=1
        return interval_step2_num,property_num
    def step3(self):
        interval_step3_num,property_step3_num=self.step2()
        property_step3_num+=self.note_t2.note_num_mode()[2]-self.note_t1.note_num_mode()[2]
        # 防止错误的性质出现
        if interval_step3_num in [3,6,7]:
            errors='fail' if property_step3_num<0 or property_step3_num>5 else ''
        elif interval_step3_num in [4,5,8]:
            errors='fail' if property_step3_num<0 or property_step3_num>4 else ''
        elif interval_step3_num in [2]:
            errors='fail' if property_step3_num<1 or property_step3_num>4 else ''
        elif interval_step3_num in [1]:
            errors='fail' if property_step3_num<2 or property_step3_num>4 else ''
        else:
            errors=''
        return property_step3_num,errors
    def property_name(self):
        # 确定性质列表
        interval_step_2_num=self.step2()[0]
        property_l=self.property_1 if interval_step_2_num in [2,3,6,7] else self.property_2
        # 得出性质的名字
        property_step3_num,errors=self.step3()
        property_name='fail' if errors=='fail' else property_l[property_step3_num]
        return property_name
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
    def interval_name_en(self):
        l_1=['d_d','d','m','M','A','d_A','p','fail']
        l_2=['double_diminished','diminished','minor','major','augmented','double_augmented','perfect','fail']
        property_name=l_2[l_1.index(self.property_name())]
        return # 考虑以后写

class module_chord:
    def __init__(self,root_note_t,chord_name,invert_num):
        self.root_note=root_note_t
        self.chord_name=chord_name
        self.invert_num=invert_num
        self.triad_chord=['major','minor','aug','dim']
        self.seventh_chord=['MM7','Mm7','mm7','dm7','dd7']
    def create_chord_note(self):
        # 各种和弦的结构，以后可以扩展
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
    def chord(self):
        invert=lambda x:module_note(x.note_num_mode()[0]+7,x.note_num_mode()[2])
        root_note,note_3,note_5,note_7,errors=self.create_chord_note()
        # 考虑转位音程
        if self.invert_num==1:
            chord_normal_l=[invert(root_note),note_3,note_5,note_7]
            chord_invert_l=[note_3,note_5,note_7,invert(root_note)]
        if self.invert_num==2:
            chord_normal_l=[invert(root_note),invert(root_note),note_5,note_7]
            chord_invert_l=[note_5,note_7,invert(root_note),invert(note_3)]
        if self.invert_num==3:
            chord_normal_l=[invert(root_note),invert(root_note),invert(note_5),note_7]
            chord_invert_l=[note_7,invert(root_note),invert(note_3),invert(note_5)]
        if self.invert_num==0:
            chord_normal_l=[root_note,note_3,note_5,note_7]
            chord_invert_l=[root_note,note_3,note_5,note_7]
        # 移除空集
        remove=lambda x:x.remove('') if '' in x else x
        remove(chord_normal_l)
        remove(chord_invert_l)
        return chord_normal_l,chord_invert_l
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
            invert_name=triad_invert_l[self.invert_num]
        else:
            invert_name=seven_invert_l[self.invert_num]
        return chord_name,invert_name

class module_key:
    def __init__(self,key_num,sharpe_flat):
        self.key_num=key_num
        self.sharpe_flat=sharpe_flat
        # 调式主音列表
        self.sharpe_tonic_l=['c','g','d','a','e','b','f','c']
        self.flat_tonic_l=['c','f','b','e','a','d','g','c']
        # 调号列表
        self.key_sharpe_l=['','f','c','g','d','a','e','b','']
        self.key_flat_l=['','b','e','a','d','g','c','f','']
    # 计算出调式主音(仅得出音级)
    def tonic(self):
        tonic=self.sharpe_tonic_l[self.key_num] if self.sharpe_flat=='sharpe' else self.flat_tonic_l[self.key_num] 
        return tonic
    # 获取调号的信息
    def key_list(self):
        # 调号列表
        key_list=self.key_sharpe_l[:self.key_num+1] if self.sharpe_flat=='sharpe' else self.key_flat_l[:self.key_num+1]
        # 升降记号的建议
        add_dim=1 if self.sharpe_flat=='sharpe' else -1
        return key_list,add_dim
    def key_sign_ly(self):
        sharpe_list = ['\key c \major','\key g \major','\key d \major','\key a \major','\key e \major','\key b \major','\key fis \major','\key cis \major',]
        flat_list = ['\key c \major','\key f \major','\key bes \major','\key ees \major','\key aes \major','\key des \major','\key ges \major','\key ces \major']
        key_sign_ly=sharpe_list[self.key_num] if self.sharpe_flat=='sharpe' else flat_list[self.key_num]
        return key_sign_ly

class scale_Mm:
    def __init__(self,key_num,sharpe_flat,modal_l):
        self.scale_base=['c','d','e','f','g','a','b']
        self.key_t=module_key(key_num,sharpe_flat)
        self.key_num=key_num
        self.sharpe_flat=sharpe_flat
        self.modal_l=modal_l
    # 小调主音的转换(仅得出音级)
    def tonic(self):
        sharpe_tonic_l=['a','e','b','f','c','g','d','a']
        flat_tonic_l=['a','d','g','c','f','b','e','a']
        if self.modal_l[0]=='minor':
            tonic=sharpe_tonic_l[self.key_num] if self.sharpe_flat=='sharpe' else flat_tonic_l[self.key_num]
        else:
            tonic=self.key_t.tonic()
        return tonic
    def scale_67th(self):
        tonic=self.tonic()
        # 找到6、7级音
        scale_base=self.scale_base*2
        scale_6th=scale_base[scale_base.index(tonic)+5]
        scale_7th=scale_base[scale_base.index(tonic)+6]
        # 6、7级音的升降建议
        scale_67th=[]
        if self.modal_l[1]=='harmony':
            scale_67th.append(scale_6th if self.modal_l[0]=='major' else scale_7th)
        if self.modal_l[1]=='melody':
            scale_67th=[scale_6th,scale_7th]
        # 根据升降给出add_dim的建议
        add_dim=-1 if self.modal_l[0]=='major' else 1
        return scale_67th,add_dim
    def sacle_name_zh(self):
        modal_l1_zh=['大调','小调']
        modal_l1=['major','minor']
        modal_l2_zh=['自然','和声','旋律']
        modal_l2=['nature','harmony','melody']
        # modal拼接
        modal1=modal_l1_zh[modal_l1.index(self.modal_l[0])]
        modal2=modal_l2_zh[modal_l2.index(self.modal_l[1])]
        # 关于主音
        sharpe_flat=['','升','降']
        tonic_0=sharpe_flat[self.key_t.key_list()[1]] if self.tonic() in self.key_t.key_list()[0] else ''
        tonic=self.tonic() if self.modal_l[0]=='minor' else self.tonic().upper()
        return tonic_0+tonic+modal2+modal1

class scale_chinese:
    def __init__(self,key_num,sharpe_flat,tonic_num):
        self.scale_base=['c','d','e','f','g','a','b']*2
        self.tonic_num=tonic_num-1
        self.key_t=module_key(key_num,sharpe_flat)
        self.tonic_1st_num=self.scale_base.index(self.key_t.tonic()) # 代表宫音的数字
    def tonic(self):
        tonic=self.scale_base[self.tonic_1st_num+self.tonic_num]
        return tonic
    def scale_name_zh(self):
        # 关于调式
        tonic_num_l=['宫','商','角','徵','羽']
        tonic2=tonic_num_l[self.tonic_num]
        # 关于主音
        sharpe_flat=['','升','降']
        tonic0=sharpe_flat[self.key_t.key_list()[1]] if self.tonic() in self.key_t.key_list()[0] else ''
        tonic1=self.tonic() if self.tonic_num in [1,2,4] else self.tonic().upper()
        return tonic0+tonic1+tonic2
    def pentatonic(self):
        # 得出特别的列表
        note_4th=self.scale_base[self.tonic_1st_num+3]
        note_7th=self.scale_base[self.tonic_1st_num+6]
        remove_list=[note_4th,note_7th]
        # 合成名字
        scale_name=self.scale_name_zh()+'五声调式'
        return remove_list,scale_name
    def hexatonic(self,modal_hexa):
        # 得出特别的列表
        remove_list=self.pentatonic()[0]
        remove_list.pop(1) if modal_hexa==0 else remove_list.pop(0) 
        # 合成名字
        modal_name='加清角' if modal_hexa==0 else '加变宫'
        scale_name=self.scale_name_zh()+'六声调式'+'('+modal_name+')'
        return remove_list,scale_name
    def heptatonic(self,modal_hepta):
        # 得出特别的列表
        remove_list=self.pentatonic()[0]
        if modal_hepta==0:
            note_47th=[[remove_list[0],0],[remove_list[1],0]]
        if modal_hepta==1:
            note_47th=[[remove_list[0],1],[remove_list[1],0]]
        if modal_hepta==2:
            note_47th=[[remove_list[0],0],[remove_list[1],-1]]
        # 合成名字
        modal_name='清乐' if modal_hepta==0 else '雅乐' if modal_hepta==0 else '燕乐'
        scale_name=self.scale_name_zh()+'七声'+modal_name+'调式'
        return note_47th,scale_name

class scale_church:
    def __init__(self):
        self.scale_t=scale_Mm(key_num,sharpe_flat,modal_l)
    def ionian(self):
        

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
    errors=t3.step3()[1]
    return t2,errors



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
        for v1,v2 in zip([1,4,6,9,11],chromatic_l):
            scale_l.insert(v1,v2) 

    # 根据上行或下行调整列表顺序
    if asc_des=='下行':
        scale_l.reverse()
    return key_t,scale_l,asc_des



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


key_num=6
sharpe_flat='sharpe'
tonic_num=5
scale_chinese_t=scale_chinese(key_num,sharpe_flat,tonic_num)

print('scale_chinese.pentatonic():',scale_chinese_t.pentatonic())
print('scale_chinese.hexatonic(0):',scale_chinese_t.hexatonic(1))
print('scale_chinese.heptatonic(2):',scale_chinese_t.heptatonic(0))