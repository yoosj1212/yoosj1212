import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch, Pitch
from mplsoccer.cm import create_transparent_cmap
from mplsoccer.scatterutils import arrowhead_marker
from mplsoccer.statsbomb import read_event, EVENT_SLUG
from mplsoccer.utils import FontManager
from scipy.spatial.distance import cdist
from scipy.stats import chi2_contingency
import matplotlib.image as mpimg
import seaborn as sns; sns.set_theme()
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox

def location(x,y,q,w,e,r,f):
    if (x[i] >= q and x [i]< w) and (y[i] >= e and y[i] < r): 
        Position.append(f)
    else:
        Position.append(np.nan)
csv_file_list =  [ 'R1.csv','R2.csv','R3.csv','R4.csv','R5.csv']
    
list_of_dataframes=[]
for filename in csv_file_list:
    list_of_dataframes.append(pd.read_csv(filename))

df = pd.concat(list_of_dataframes, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False,copy=True,)
df = df.reset_index(drop=True)
df = pd.DataFrame(df, columns= ['id','event_type_name','team_name'
                    ,'play_pattern_name','possession','location_x'
                    , 'location_y','timestamp','end_location_x', 'end_location_y'], index= None)
df = df.drop_duplicates(subset=['id','event_type_name','team_name'
                    ,'play_pattern_name','possession','location_x'
                    , 'location_y','timestamp','end_location_x', 'end_location_y'], keep='first')
df = df.loc[((df['play_pattern_name']=='From Counter') & (df['team_name'] =='Rotherham United'))]
df.drop(df[df['event_type_name'] == 'Ball Receipt*'].index, inplace = True)

num = len (df['location_x'])
Start_point =[]
for i in range (num):
    x = df['location_x'].values
    y = df['location_y'].values
    if (x[i] >= 0 and x[i] < 40) and (y[i] >= 0 and y[i] < 30): 
        Start_point.append('D1')
    elif (x[i] >= 0 and x[i] < 40) and (y[i] >= 30 and y[i] < 50): 
        Start_point.append('D2')
    elif (x[i] >= 0 and x[i] < 40) and (y[i] >= 50 and y[i] < 80): 
        Start_point.append('D3')
    elif (x[i] >= 40 and x[i] < 60) and (y[i] >= 0 and y[i] < 30): 
        Start_point.append('DM1')
    elif (x[i] >= 40 and x[i] < 60) and (y[i] >= 30 and y[i] < 50): 
        Start_point.append('DM2')
    elif (x[i] >= 40 and x[i] < 60) and (y[i] >= 50 and y[i] < 80): 
        Start_point.append('DM3')
    elif (x[i] >= 60 and x[i] < 80) and (y[i] >= 0 and y[i] < 30): 
        Start_point.append('AM1')
    elif (x[i] >= 60 and x[i] < 80) and (y[i] >= 30 and y[i] < 50): 
        Start_point.append('AM2')
    elif (x[i] >= 60 and x[i] < 80) and (y[i] >= 50 and y[i] < 80): 
        Start_point.append('AM3')
    elif (x[i] >= 80 and x[i] < 120) and (y[i] >= 0 and y[i] < 30): 
        Start_point.append('A1')
    elif (x[i] >= 80 and x[i] < 120) and (y[i] >= 30 and y[i] < 50): 
        Start_point.append('A2')
    elif (x[i] >= 80 and x[i] < 120) and (y[i] >= 50 and y[i] < 80): 
        Start_point.append('A3')
    else:
        Start_point.append(np.nan)

df['Start_point']= Start_point
a=df['possession'].values
b= df['event_type_name'].values
c=df['Start_point'].values
d=df['timestamp'].values
num = len(a)
R1_event=[]
R1_zone=[]
R1_time=[]
R2=[]
Re_event=[]
Re_zone=[]
Re_time=[]
for i in range(num-1):
    s_0= a[i-1]
    s_1= a[i]
    s_2=b[i]
    s_3= a[i+1]
    s_4=c[i]
    s_5=d[i]
    if s_0 != s_1:
        if s_2== 'Pressure'or'Duel'or 'Goal Keeper 'or 'Ball Recovery'or'Interception' or'pass':
            R1_event.append (s_2)
            R1_zone.append(s_4)
            R1_time.append(s_5)
    elif s_1 == s_3:
        if s_2== 'Foul Committed'or 'Pass'or 'Carries'or'Foul Committed':
            R2.append (s_2)
    elif s_1 != s_3:
        if s_2== 'Pressure'or 'Dispossessed'or 'Foul Won'or'Pass'or'Shot' or 'Carries':
            Re_event.append (s_2)
            Re_zone.append(s_4)
            Re_time.append(s_5)
Re_event.append (df["event_type_name"].iloc[-1])
Re_zone.append (df["Start_point"].iloc[-1])
Re_time.append (df["timestamp"].iloc[-1])
print (R1_zone)

label=[]
for i in range(num):
    a=df['possession'].values
    if a[i] == 174:
        label.append(0) 
    elif a[i] == 121:
        label.append(0)
    elif a[i] == 116:
        label.append(0)
    elif a[i] == 70:
        label.append(0)
    elif a[i] == 153:
        label.append(0)
    else:
        label.append(1)
df['label']=label
fig, ax = plt.subplots(figsize=(10,10))
fig.set_facecolor('#38383b')
ax.patch.set_facecolor('#38383b')

pitch = VerticalPitch(pitch_type='statsbomb',orientation='horizontal',
             pitch_color='#22312b',line_color='#efefef',figsize=(10,10),
             constrained_layout=False,tight_layout=True,view='full')

pitch.draw(ax=ax)
for i in range(num):
    x = df['location_x'].values
    y = df['location_y'].values
    o=df['end_location_x'].values
    p=df['end_location_y'].values
    k =df['label'].values
    if k[i]== 0:
        pitch.arrows(xstart=x[i],ystart=y[i],xend=o[i],yend=p[i],
                   color='red', ax=ax, width=2)
    else:
        pitch.arrows(xstart=x[i],ystart=y[i],xend=o[i],yend=p[i],
                   color='black', ax=ax, width=2)
fig.suptitle( 'RUFC CounterAttack', x=0.55, y=0.95, fontsize=30,fontname="Times New Roman", color='white')
legge = mpimg.imread('다운로드.PNG')
imagebox = OffsetImage(legge, zoom=0.3)
ab = AnnotationBbox(imagebox, (-1, 120))
ax.add_artist(ab)
plt.show()
