# -*- coding: utf-8 -*-

# 与音相关
#----------------------------------------------
# 列表前一个是音名，后一个是组别
range_low_c=['g',0]
range_high_c=['d',2] 
# -2重降，-1降，0无，1升，2重升
accidental_l=[0]

# 与音程相关
#----------------------------------------------
interval_num_l=[4]
property_l=['M','m']
# 与调号相关
#----------------------------------------------
key_num_l=[0] # 调号数量
sharp_flat_l=['sharp'] # 升号调填sharp,降号调填flat
modal_l=[[['major'],['nature']],[['major'],['nature']]] # 前面填大调或小调，后面填写调式种类


# 与版面相关
#----------------------------------------------
# 选择谱号
clef='S' 

# 表示两音之间的跨度
space_l=[[2,'m'],[8,'p']]

# 表示对某一个元素重复的次数，如节奏型里的小节数，单音的个数等。
list_num=10

midi_repeat=1

# 与节奏相关
#----------------------------------------------
# 需要移除哪一类节奏型。每种拍号里含有的节奏型种类都不太一样。
# 28_216 []
# 24_34_44 ['8','4','2','2.','1']
# 38_68_98_128['4.1','4.2','4.3','4.4','2.']
# 22_32_42['4','2','2.','1']
# 64_94_124 ['2.1','2.2','2.3','2.4','1.']
# 316_616_916_1216 ['8.1','8.2','8.3','8.4','4.']
remove_rythem_l=['8','2.','1']
# 不规则拍的节奏模式
# '2,3','3,2','2,2,3','2,3,2','3,2,2'
irregular_mode=['2,3']
# 在一类节奏型中选择哪几个节奏型。
# 28_216 7
# 24_34_44 99,8,8,3,3
# 38_68_98_128 4,8,8,5,0
# 22_32_42 8,8,3,3
# 64_94_124 4,8,8,5
# 316_616_916_1216 4,6,6,5,0
rythem_range_list=[[0],[0,1,2,3,4,5,6,7,8],[0,1,2,3,4,5,6,7,8],[0],[0]]
# 控制某一些节奏型最少出现多少次
important_rythem_list=[['2','4. 8','4. 16 16','8 4 8','16 16 4 8','8 4 16 16','16 16 4 16 16','8 4.','16 16 4.'],2]