- 👋 Hi, I’m @yoosj1212
- 👀 I’m interested in ...
- 🌱 I’m currently learning ...
- 💞️ I’m looking to collaborate on ...
- 📫 How to reach me ...

<!---
yoosj1212/yoosj1212 is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->
from turtle import color
from matplotlib import colors
import numpy as np
import pandas as pd
from matplotlib import cm
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap
from matplotlib.patches import Arc
import matplotlib.image as mpimg
from mplsoccer import VerticalPitch, Pitch
from mplsoccer.cm import create_transparent_cmap
from mplsoccer.scatterutils import arrowhead_marker
from mplsoccer.statsbomb import read_event, EVENT_SLUG
from mplsoccer.utils import FontManager


def viz(percentage, x1, x2, y1, y2):
    text_kwargs = dict(ha='center', va='center', fontsize=20, color='navy')
    test_msg = '%.f%%' % (percentage)
    #sns.kdeplot(x,y, shade="True", shade_lowest=False,alpha=.2, n_levels=50, cmap='magma')
    plt.text((y1+y2)/2, (x1+x2)/2, test_msg, **text_kwargs)

csv_file_list = ['PA1.csv', 'PA2.csv', 'PA3.csv', 'PA4.csv','PA5.csv','PA6.csv']

list_of_dataframes = []
for filename in csv_file_list:
    list_of_dataframes.append(pd.read_csv(filename))

df = pd.concat(list_of_dataframes)
df = df.reset_index(drop=True)
df = pd.DataFrame(df, columns=['id','timestamp','team_name','type_name', 'technique_name', 'location_y'
                ,'pass_height_name','outcome_name','end_location_x', 'end_location_y','player_name','pass_recipient_name'], index= None)
df= df.drop_duplicates(subset=['id','team_name','type_name', 'technique_name'
                ,'pass_height_name','outcome_name','end_location_x', 'location_y','end_location_y','player_name','pass_recipient_name'], keep='first')
df = df.loc[((df['type_name']=='Corner') & (df['team_name'] =='Plymouth Argyle'))]

num = len (df['end_location_x'])
Right_Left = []  
for i in range (num):
    y = df['location_y'].values 
    if y[i] == 0.1:
    # if (abs(x[i] - 100) < 0.1) and (y[i] >= 25 and y[i] < 31):
        Right_Left.append('Left')
    elif y[i] == 80:
        Right_Left.append('Right')
df['Right_Left'] = Right_Left
df = df.loc[((df['Right_Left']=='Left') & (df['type_name'] =='Corner'))]

num = len (df['end_location_x'])
end_location = []

for i in range (num):
    x = df['end_location_x'].values
    y = df['end_location_y'].values
    if (x[i] >= 100 and x[i] < 120) and (y[i] >= 18 and y[i] < 30): 
    # if (abs(x[i] - 100) < 0.1) and (y[i] >= 25 and y[i] < 31):
        end_location.append('LW Shot')
    elif(x[i] >= 100 and x[i] < 120) and (y[i] >= 50 and y[i] < 62): 
        end_location.append('RW Shot')
    elif(x[i] >= 100 and x[i] < 120) and (y[i] >= 30 and y[i] < 37): 
        end_location.append('Near post')
    elif(x[i] >= 100 and x[i] < 120) and (y[i] >= 37 and y[i] < 43): 
        end_location.append('Middle')
    elif(x[i] >= 100 and x[i] < 120) and (y[i] >= 43 and y[i] < 50): 
        end_location.append('Far post')
    else:
        end_location.append('Short')
df['end_location'] = end_location
x1 = [105, 105, 105, 105, 105, 105]
x2=[120,120,120,120,120, 120]
y1=[18, 50, 30, 37, 43, 62]
y2=[30, 62, 37, 43, 50, 79.5]
num =len(df['Right_Left'])
for i in range (num):
    z=df['Right_Left'].values
    if z[i] == 'Left': 
        x1[5]=105
        x2[5]=120
        y1[5]=18
        y2[5]=0.2

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.axis('equal')
langs = df['technique_name'].value_counts(normalize=True).keys()
students = df['technique_name'].value_counts(normalize=True).values
ax.pie(students, labels = langs,autopct='%1.2f%%', colors=['green', 'yellow', 'blue'], textprops={'fontsize': 14})
plt.show()

player = df['player_name'].value_counts(normalize=True).keys()
energy = df['player_name'].value_counts(normalize=True).values

x_pos = [i for i, name in enumerate(player)]

plt.bar(x_pos, energy, color='green',width = 0.3)
plt.xlabel("Player name")
plt.ylabel("Percentage")
plt.xticks(x_pos, fontsize=15)
plt.title("Corner kick Takers")
plt.xticks(x_pos, player)
plt.show()

print(df['pass_recipient_name'].value_counts(normalize=True).sort_index(ascending=True)*100)
print(df['player_name'].value_counts(normalize=True).sort_index(ascending=True)*100)
print(df['technique_name'].value_counts(normalize=True).sort_index(ascending=True)*100)
Shot_location = df['end_location'].value_counts(normalize=True).sort_index(ascending=True)*100
print(Shot_location)
percentage =[0, 33, 22, 33, 11,0]
shot = Shot_location.keys()
shot_val = Shot_location.values

fig, ax = plt.subplots(figsize=(10,10))
fig.set_facecolor('#38383b')
ax.patch.set_facecolor('#38383b')
pitch = VerticalPitch(half=True,pitch_type='statsbomb',orientation='horizontal',
             pitch_color='#aabb97',line_color='white',figsize=(50,50),
             constrained_layout=False,tight_layout=True,view='full')
pitch.draw(ax=ax)
for i in range (len(x1)):
    viz(percentage[i], x1[i], x2[i], y1[i], y2[i])
plt.plot ([30,30], [102,120], color='white')
plt.plot ([50,50],[102,120],  color='White')
plt.plot ([43,43],[102,120],  color='White')
plt.plot ([37,37],[102,120],  color='White')
plt.scatter(y, x, color= 'white',s=15) 
#sns.kdeplot(y,x, shade="True", shade_lowest=False,alpha=.2, n_levels=50, cmap='magma')
fig.suptitle('Plymouth Defending Corner Right', x=0.5, y=0.95, fontsize=30,fontname="Times New Roman",color= 'white')
plt.show()

from scipy.stats import chi2_contingency
df['outcome_name'] = df['outcome_name'].replace(np.nan, 'Complete')
df['outcome_name'] = df['outcome_name'].replace('Out', 'Incomplete')
df['outcome_name'] = df['outcome_name'].map({'Complete': 1, 'Incomplete': 0})
crosstab=pd.crosstab(df.outcome_name, df.player_name)
chiVal, pVal, df, exp = chi2_contingency(crosstab)
print(chiVal, pVal)
print(crosstab)
print(exp)
