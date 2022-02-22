

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

note_t=module.module_note(1,0)

chord_t=module.module_chord(note_t,'major',0)

new_root_note=module.enharmonic_chord(chord_t)
for v1 in new_root_note:
    print(v1.note_all())






