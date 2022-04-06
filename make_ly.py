# -*- coding: utf-8 -*-

# 生成ly文件
def make_ly(ly_layout_c,chord,clef,note,lyric,file_name):
    # 解包控制元件
    bar_num_c,time_sign_c,midi_c,tempo_c,tempo,time,key_sign_c,clef_sign_c,note_before=ly_layout_c

    # 这一项参数不需要进行变化
    header = '\
    \\version "2.22.1" \n\
    \paper {  \n\
        #(set-paper-size "a4") %设定页面大小 \n\
        indent = 0 %首行无缩进 \n\
        system-system-spacing = #\'((padding . 8)) %谱子之间的距离 \n\
        top-margin = 20 %页面上边距\n\
        print-page-number = ##f %去掉页码 \n\
    }\n\
    \header { \n\
    tagline = ##f %去掉默认的页脚 \n\
    } \n\
    colorNote =#(define-music-function (my-color my-music) (color? ly:music?) #{	\override NoteHead.color = #my-color $my-music #}) \n\
    colorStem =#(define-music-function (my-color my-music) (color? ly:music?) #{	\override Stem.color = #my-color $my-music #}) \n\
    colorBeam =#(define-music-function (my-color my-music) (color? ly:music?) #{	\override Beam.color = #my-color $my-music #}) \n\
    colorAccidental =#(define-music-function (my-color my-music) (color? ly:music?) #{	\override Accidental.color = #my-color $my-music #})' 
    
    # 这个变量负责音符下面的文字
    lyric='\n\
    lyric = \lyricmode{ %s }' %lyric
    # 这个变量负责谱面上的音符，同时会有谱号、和弦模式两个控制
    main='\n\
    main=%s{ %s  %s }'%(chord,clef,note)

    # 下面的变量都是对于谱子上其他内容的控制，通常来说，1就是显示，0就是不显示
    score_1=' \n\
    \score{ \n\
        \layout{ \n\
        '
    # 0表示不显示小节号，1表示显示小节号
    if bar_num_c==0:
        bar_num='\context { \Score  \omit BarNumber }'
    else:
        bar_num=''
    # 0表示去掉拍号，1表示显示拍号
    if time_sign_c==0:
        time_sign='\n\
        \context { \Staff \\remove "Time_signature_engraver"} \n\
        '
    else:
        time_sign=''
    # 0表示不要生成音频，1表示生成音频
    if midi_c==0:
        midi=''
    else:
        midi='\midi{ } '

    score_2='\n\
    <<  \n\
    { \n\
        \set Staff.printKeyCancellation = ##f \set Staff.explicitKeySignatureVisibility = #end-of-line-invisible '

    # 0表示不要加上速度，1则是要加上
    if tempo_c==0:
        tempo=''

    score_3='\main \n\
    } \n\
    \\new Lyrics \lyricmode {\lyric} \n\
    >> \n\
    } \n\
    ' 
    
    # 把谱面信息汇总
    score=score_1+bar_num+time_sign+'}'+midi+score_2+tempo+"\n "+time+"\n "+key_sign_c+"\n "+clef_sign_c+"\n "+note_before+"\n "+score_3
    # 拉起ly文件
    with open(file_name+'.ly', 'w') as projectFile : 
        projectFile.write(header)
        projectFile.write(lyric)
        projectFile.write(main)
        projectFile.write(score)



# 生成Ly文件的准备
class ly_set:
    def __init__(self,note,lyric,note_back,lyric_back,clef):
        self.note=note
        self.lyric=lyric
        self.note_back=note_back
        self.lyric_back=lyric_back
        # 对谱号进行处理
        clef_l=['\clef treble','\clef alto','\clef tenor','\clef bass']
        clef_suoxie=['S','A','T','B']
        self.clef_file=clef
        self.clef=clef_l[clef_suoxie.index(clef)]
    def pitch_Mm(self,file_name):
        chord=''
        bar_num_c=1
        time_sign_c=0
        midi_c=0
        tempo_c=0
        tempo=''
        time='\\time 4/4'  
        key_sign_c='\override Staff.KeySignature.break-visibility = ##(#f #f #f)' #调号控制 
        clef_sign_c='\override Score.Clef.break-visibility = ##(#f #f #t)' #换行后谱号不再重写
        main_before='' #\skip
        ly_layout_1=[bar_num_c,time_sign_c,midi_c,tempo_c,tempo,time,key_sign_c,clef_sign_c,main_before]
        ly_layout_2=[bar_num_c,time_sign_c,1,tempo_c,tempo,time,key_sign_c,clef_sign_c,main_before]
        # 拉起ly文件
        make_ly(ly_layout_1,chord,self.clef,self.note,self.lyric,file_name)
        make_ly(ly_layout_2,chord,self.clef,self.note_back,self.lyric_back,file_name+'-midi')
        return 'ly文件生成完毕'
    def interval(self,file_name):
        chord=''
        bar_num_c=1
        time_sign_c=0
        midi_c=0
        tempo_c=0
        tempo=''
        time='\\time 4/4'  
        key_sign_c='\override Staff.KeySignature.break-visibility = ##(#f #f #f)' #调号控制 
        clef_sign_c='\override Score.Clef.break-visibility = ##(#f #f #t)' #换行后谱号不再重写
        main_before='' #\skip
        ly_layout_1=[bar_num_c,time_sign_c,midi_c,tempo_c,tempo,time,key_sign_c,clef_sign_c,main_before]
        ly_layout_2=[bar_num_c,time_sign_c,1,tempo_c,tempo,time,key_sign_c,clef_sign_c,main_before]
        # 拉起ly文件
        make_ly(ly_layout_1,chord,self.clef,self.note,self.lyric,file_name)
        make_ly(ly_layout_2,chord,self.clef,self.note_back,self.lyric_back,file_name+'-midi')
        return 'ly文件生成完毕'
    def rythem(self,file_name,time_ly,beam):
        chord=''
        bar_num_c=1
        time_sign_c=0
        midi_c=0
        tempo_c=0
        tempo=''
        time=time_ly 
        key_sign_c='\override Staff.KeySignature.break-visibility = ##(#f #f #f)' #调号控制 
        clef_sign_c='\override Score.Clef.break-visibility = ##(#f #f #t)' #换行后谱号不再重写
        main_before=beam #\skip
        ly_layout_1=[bar_num_c,time_sign_c,midi_c,tempo_c,tempo,time,key_sign_c,clef_sign_c,main_before]
        ly_layout_2=[bar_num_c,time_sign_c,1,tempo_c,tempo,time,key_sign_c,clef_sign_c,main_before]
        # 拉起ly文件
        make_ly(ly_layout_1,chord,self.clef,self.note,self.lyric,file_name)
        make_ly(ly_layout_2,chord,self.clef,self.note_back,self.lyric_back,file_name+'-midi')
        return 'ly文件生成完毕'
    def rythem_b(self,file_name,time_ly,beam):
        chord=''
        bar_num_c=1
        time_sign_c=0
        midi_c=0
        tempo_c=0
        tempo=''
        time=time_ly 
        key_sign_c='\override Staff.KeySignature.break-visibility = ##(#f #f #f)' #调号控制 
        clef_sign_c='\override Score.Clef.break-visibility = ##(#f #f #t)' #换行后谱号不再重写
        main_before=' \skip1*2 \\break \set Score.currentBarNumber = #1 \override Staff.BarLine.stencil = ##f \stopStaff '+beam #\skip
        ly_layout_1=[bar_num_c,time_sign_c,midi_c,tempo_c,tempo,time,key_sign_c,clef_sign_c,main_before]
        ly_layout_2=[bar_num_c,time_sign_c,1,tempo_c,tempo,time,key_sign_c,clef_sign_c,main_before]
        # 拉起ly文件
        make_ly(ly_layout_1,chord,self.clef,self.note,self.lyric,file_name)
        make_ly(ly_layout_2,chord,self.clef,self.note_back,self.lyric_back,file_name+'-midi')
        return 'ly文件生成完毕'