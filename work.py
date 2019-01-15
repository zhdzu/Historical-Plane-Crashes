# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 17:02:53 2018

@author: Administrator
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

path = r'C:\Users\Administrator\Desktop\大数据学院\统计软件\期末资料\空难数据\Airplane_Crashes_and_Fatalities_Since_1908.csv'
f = open(path,encoding='utf-8')
df = pd.read_csv(f)

df.info()
# 只有Date没有缺失值，Time、Flight # 、Route 、cn/In缺失值很多

print("dimennsion of airplane crashes data:{}".format(df.shape)) #(5268, 13)


# get year,month from Date
def getdate(df):
    date = []
    year = []
    month = []
    for i in range(len(df)):
        list = re.split('/',df.Date[i])
        date.append(list)
        year.append(int(list[2]))
        month.append(int(list[0]))
    return date, year, month
date, year, month = getdate(df)
# year[::]show all elements in list
set(year[::])  # 1908-2009
set(month[::]) # 01-12

# get number of different years
yearlist = [item for item in set(year[::])]
yearnum = [year.count(i) for i in yearlist]

from pyecharts import Bar
bar = Bar("Airplane crashes", "year")
bar.add("空难", yearlist, yearnum)
# bar.print_echarts_options() # 该行只为了打印配置项，方便调试时使用
bar.render()    # 生成本地 HTML 文件

# get number of different months
monthlist = [item for item in set(month[::])]
monthnum = [month.count(i) for i in monthlist]

from pyecharts import Bar
bar1 = Bar("Airplane crashes", "month")
bar1.add("空难", monthlist, monthnum)
# bar.print_echarts_options() # 该行只为了打印配置项，方便调试时使用
bar1.render("空难分布月份.html")    # 生成本地 HTML 文件
bar1


# get 3-D picture
# 获得年份和月份分布的频数
data = np.zeros((102,12))
for i in range(5268):
    data[year[i]-1908,month[i]-1] = data[year[i]-1908,month[i]-1]+1

# 发生空难次数最多的月份
data.max()  # 17

# 构建三维数据集
# (y,x,z)格式
data1 = []
for i in range(102):
    for j in range(12):
        data1.append([j,i,data[i,j]])

# get 3-D picture
from pyecharts import Bar3D

bar3d = Bar3D("空难分布 3D 柱状图","year-month", width=1200, height=600)
x_axis = yearlist
y_aixs = monthlist

range_color = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
               '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
bar3d.add("", x_axis, y_aixs, [[d[1], d[0], d[2]] for d in data1], is_visualmap=True,
          visual_range=[0, 20], visual_range_color=range_color, grid3d_width=200, grid3d_depth=80)
bar3d.render("空难分布年月3D.html")    # 生成本地 HTML 文件
bar3d


# 画空难次数随小时变化的情况
import matplotlib.pyplot as plt
import seaborn as sns

def get_hour(x):
    hour = x.split(":")[0]
    try:
        hour = float(hour)
        if int(hour) == hour and hour < 24:
            return hour
        else:
            return np.nan
    except:
        return np.nan
    
time_df = df[df["Time"].isnull() == False]
time_df["hour"] = time_df["Time"].map(get_hour)
time_df.info()

# get number of different hours
'''对np.series按index进行排序'''
hourlist = time_df.hour.value_counts().sort_index()
hourlist = [item for item in set(time_df.hour[::])]
hournum = [hour.count(i) for i in hourlist]



# 处理df中的location，画词云图，并在世界地图上可视化
import re
location_df = df[df["Location"].isnull() == False].reset_index()

def getwords(location_df):
    words = []
    for i in range(len(location_df)):
        word = re.sub(" ","",location_df["Location"][i]).split(',')
        words.extend(word) 
    return words

words = getwords(location_df)

cities = ['Afghanistan','Albania','Algeria','Andorra','Angola',
          'Antigua and Barb.','Argentina','Armenia','Australia',
          'Austria','Azerbaijan','Bahrain','Bangladesh','Barbados',
          'Belarus','Belgium','Belize','Benin','Bermuda',
          'Bhutan','Bolivia','Bosnia and Herz.','Botswana','Brazil',
          'Br. Indian Ocean Ter.','Brunei','Bulgaria','Burkina Faso',
          'Burundi','Cambodia','Cameroon','Canada','Cape Verde',
          'Cayman Is.','Central African Rep.','Chad','Chile','Colombia','China',
          'Comoros','Dem. Rep. Congo','Cook Islands','Coral Sea Islands Territory',
          'Costa Rica','Croatia','Cuba','Cyprus','Czechia',
          'Denmark','Djibouti','Dominica','Dominican Republic','East Timor',
          'Ecuador','Egypt','El Salvador','Equatorial Guinea','Eritrea',
          'Estonia','Ethiopia','Falkland Islands','Faroe Islands','Federated States of Micronesia',
          'Fiji','Finland','France','Gabon','Georgia',
          'Germany','Ghana','Gibraltar','Greece','Greenland',
          'Guatemala','Guernsey','Guinea-Bissau','Guinea','Guyana',
          'Haiti','Honduras','Hungary','Iceland','India',
          'Indonesia','Iraq','Ireland','Iran','Isle of Man',
          'Israel','Italy','Jamaica','Japan','Jersey',
          'Jordan','Kazakhstan','Kenya','Kiribati','Kuwait',
          'Kyrgyzstan','Laos','Latvia','Lebanon','Lesotho',
          'Liberia','Libya','Liechtenstein','Lithuania','Luxemburg',
          'Macedonia','Madagascar','Malawi','Malaysia','Maldives',
          'Mali','Malta','Marshall Islands','Mauritania','Mauritius',
          'Mexico','Moldova','Monaco','Mongolia','Montenegro',
          'Montserrat','Morocco','Mozambique','Myanmar','Namibia',
          'Nepal','New Zealand','Nicaragua','Niger','Nigeria',
          'Niue','North Korea','Norway','Oman','Pakistan',
          'Palau','Palestine','Panama','Papua New Guinea','Paraguay','Puerto Rico',
          'Peru','Philippines','Pitcairn Islands','Poland','Portugal',
          'Qatar','Republic of Kosovo','Romania','Russia','Rwanda',
          'Sahrawi Arab Democratic Republic','Saint Helena Ascension and Tristan da Cunha','Saint Kitts and Nevis','Saint Lucia','Saint Vincent and the Grenadines',
          'Samoa','San Marino','Saudi Arabia','Senegal','Serbia',
          'Seychelles','Sierra Leone','Singapore','Slovakia','Slovenia',
          'Solomon Islands','Somalia','South Africa','South Georgia and the South Sandwich Islands','South Korea',
          'S. Sudan','Spain','Sri Lanka','Sudan','Suriname',
          'Switzerland','Sweden','Syria','Tajikistan','Tanzania',
          'Thailand','Bahamas','Gambia','Netherlands','Togo',
          'Tokelau','Tonga','Trinidad and Tobago','Tunisia','Turkey',
          'Turkmenistan','Turks and Caicos Islands','Tuvalu','Uganda','Ukraine',
          'United Arab Emirates','United Kingdom','Uruguay','United States','Uzbekistan',
          'Vanuatu','Vatican City','Venezuela','Vietnam','Yemen',
          'Zambia','Zimbabwe']

states_usa_pyecharts = [
        'Alabama','Alaska','Arizona','Arkansas','California',
        'Colorado','Columbia','Connecticut','Delaware','Florida',
        'Georgia','Hawaii','Idaho','Illinois','Indiana',
        'Iowa','Kansas','Kentucky','Louisiana','Maine',
        'Maryland','Massachusetts','Michigan','Minnesota','Mississippi',
        'Missouri','Montana','Nebraska','Nevada','New Hampshire',
        'New Jersey','New Mexico','New York','North Carolina','North Dakota',
        'Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island',
        'South Carolina','South Dakota','Tennessee','Texas','Utah',
        'Vermont','Virginia','Washington','West Virginia','Wisconsin',
        'Wyoming','Puerto Rico']

# 需要将pyecharts和words中的洲名一一对应
# New Hampshire -- NewHampshire    # New Jersey -- NewJersey   # New Mexico -- NewMexico
# North Carolina -- NorthCarolina  # New York -- NewYork       # North Dakota -- NorthDakota
# Rhode Island -- RhodeIsland      # South Carolina -- SouthCarolina
# South Dakota -- SouthDakota      # West Virginia -- WestVirginia
# Puerto Rico -- PuertoRico

states_usa_words = [
        'Alabama','Alaska','Arizona','Arkansas','California',
        'Colorado','Columbia','Connecticut','Delaware','Florida',
        'Georgia','Hawaii','Idaho','Illinois','Indiana',
        'Iowa','Kansas','Kentucky','Louisiana','Maine',
        'Maryland','Massachusetts','Michigan','Minnesota','Mississippi',
        'Missouri','Montana','Nebraska','Nevada','NewHampshire',
        'NewJersey','NewMexico','NewYork','NorthCarolina','NorthDakota',
        'Ohio','Oklahoma','Oregon','Pennsylvania','RhodeIsland',
        'SouthCarolina','SouthDakota','Tennessee','Texas','Utah',
        'Vermont','Virginia','Washington','WestVirginia','Wisconsin',
        'Wyoming','PuertoRico']

states_usa_num = [words.count(state) for state in states_usa_words]


# 统计各个国家发生空难的次数
# 由于历史原因或其他原因导致words中国家名需要修改，左边是words中数据，右边是pyecharts中的数据
# England -- United Kingdom
# USSR -- 苏联61次 -- Russia
# SouthVietnam -- 二战38次 -- Vietnam
# NewGuinea -- 巴布亚新几内亚独立国 -- Papua New Guinea
# PuertoRico -- Puerto Rico
# SouthAfrica -- South Africa
# PapuaNewGuinea -- Papua New Guinea
# Congo -- 刚果 -- Dem. Rep. Congo
# DemocratiRepubliCongo -- 刚果 -- Dem. Rep. Congo
# SouthKorea -- 朝鲜 -- South Korea
# SaudiArabia -- 沙特 -- Saudi Arabia
# Czechoslovakia -- 捷克 -- Slovakia
# Taiwan 36 -- China
# Scotland 17 -- United Kingdom
# Ireland -- United Kingdom

cities_pyecharts = ['Afghanistan','Albania','Algeria','Andorra','Angola',
          'Antigua and Barb.','Argentina','Armenia','Australia',
          'Austria','Azerbaijan','Bahrain','Bangladesh','Barbados',
          'Belarus','Belgium','Belize','Benin','Bermuda',
          'Bhutan','Bolivia','Bosnia and Herz.','Botswana','Brazil',
          'Br. Indian Ocean Ter.','Brunei','Bulgaria','Burkina Faso',
          'Burundi','Cambodia','Cameroon','Canada','Cape Verde',
          'Cayman Is.','Central African Rep.','Chad','Chile','Colombia','China',
          'Comoros','Congo','Dem. Rep. Congo','Cook Islands','Coral Sea Islands Territory',
          'Costa Rica','Croatia','Cuba','Cyprus','N. Cyprus','Czech Rep.',
          'Denmark','Djibouti','Dominica','Dominican Rep.','Timor-Leste',
          'Ecuador','Egypt','El Salvador','Eq. Guinea','Eritrea',
          'Estonia','Ethiopia','Falkland Is.','Faroe Islands','Federated States of Micronesia',
          'Fiji','Finland','France','Gabon','Georgia',
          'Germany','Ghana','Gibraltar','Greece','Greenland',
          'Guatemala','Guernsey','Guinea-Bissau','Guinea','Guyana',
          'Haiti','Honduras','Hungary','Iceland','India',
          'Indonesia','Iraq','Ireland','Iran','Isle of Man',
          'Israel','Italy','Jamaica','Japan','Jersey',
          'Jordan','Kazakhstan','Kenya','Kiribati','Kuwait',
          'Kyrgyzstan','Lao PDR','Latvia','Lebanon','Lesotho',
          'Liberia','Libya','Liechtenstein','Lithuania','Luxemburg',
          'Macedonia','Madagascar','Malawi','Malaysia','Maldives',
          'Mali','Malta','Marshall Islands','Mauritania','Mauritius',
          'Mexico','Moldova','Monaco','Mongolia','Montenegro',
          'Montserrat','Morocco','Mozambique','Myanmar','Namibia',
          'Nepal','New Zealand','Nicaragua','Niger','Nigeria',
          'Niue','Dem. Rep. Korea','Norway','Oman','Pakistan',
          'Palau','Palestine','Panama','Papua New Guinea','Paraguay','Puerto Rico',
          'Peru','Philippines','Pitcairn Islands','Poland','Portugal',
          'Qatar','Republic of Kosovo','Romania','Russia','Rwanda',
          'Sahrawi Arab Democratic Republic','Saint Helena Ascension and Tristan da Cunha','Saint Kitts and Nevis','Saint Lucia','Saint Vincent and the Grenadines',
          'Samoa','San Marino','Saudi Arabia','Senegal','Serbia',
          'Seychelles','Sierra Leone','Singapore','Slovakia','Slovenia',
          'Solomon Is.','Somalia','South Africa','S. Geo. and S. Sandw. Is.','Korea',
          'S. Sudan','Spain','Sri Lanka','Sudan','Suriname',
          'Switzerland','Sweden','Swaziland','Syria','Tajikistan','Tanzania',
          'Thailand','Bahamas','Gambia','Netherlands','Togo',
          'Tokelau','Tonga','Trinidad and Tobago','Tunisia','Turkey',
          'Turkmenistan','Turks and Caicos Islands','Tuvalu','Uganda','Ukraine',
          'United Arab Emirates','United Kingdom','Uruguay','United States','Uzbekistan',
          'Vanuatu','Vatican City','Venezuela','Vietnam','Yemen',
          'Zambia','Zimbabwe','W. Sahara','Siaoher Glacier','New Caledonia','Fr.S. Antarctic Lands']

cities_pyecharts = [
        'Afghanistan','Albania','Algeria','Andorra','Angola',
        'Antigua and Barb.','Argentina','Armenia','Australia','Austria',
        'Azerbaijan','Bahamas','Bahrain','Bangladesh','Barbados',
        'Belarus','Belgium','Belize','Benin','Bermuda',
        'Bhutan','Bolivia','Bosnia and Herz.','Botswana','Br. Indian Ocean Ter.',
        'Brazil','Brunei','Bulgaria','Burkina Faso','Burundi',
        'Cambodia','Cameroon','Canada','Cape Verde','Cayman Is.',
        'Central African Rep.','Chad','Chile','China','Colombia',
        'Comoros','Congo','Cook Islands','Coral Sea Islands Territory','Costa Rica','Croatia',
        'Cuba','Cyprus','Czech Rep.','Dem. Rep. Congo','Dem. Rep. Korea',
        'Denmark','Djibouti','Dominica','Dominican Rep.','Ecuador',
        'Egypt','El Salvador','Eq. Guinea','Eritrea','Estonia',
        'Ethiopia','Falkland Is.','Faroe Islands','Federated States of Micronesia','Fiji',
        'Finland','Fr.S. Antarctic Lands','France','Gabon','Gambia',
        'Georgia','Germany','Ghana','Gibraltar','Greece',
        'Greenland','Guatemala','Guernsey','Guinea','Guinea-Bissau',
        'Guyana','Haiti','Honduras','Hungary','Iceland',
        'India','Indonesia','Iran','Iraq','Ireland',
        'Isle of Man','Israel','Italy','Jamaica','Japan',
        'Jersey','Jordan','Kazakhstan','Kenya','Kiribati',
        'Korea','Kuwait','Kyrgyzstan','Lao PDR','Latvia',
        'Lebanon','Lesotho','Liberia','Libya','Liechtenstein',
        'Lithuania','Luxemburg','Macedonia','Madagascar','Malawi',
        'Malaysia','Maldives','Mali','Malta','Marshall Islands',
        'Mauritania','Mauritius','Mexico','Moldova','Monaco',
        'Mongolia','Montenegro','Montserrat','Morocco','Mozambique',
        'Myanmar','N. Cyprus','Namibia','Nepal','Netherlands',
        'New Caledonia','New Zealand','Nicaragua','Niger','Nigeria',
        'Niue','Norway','Oman','Pakistan','Palau',
        'Palestine','Panama','Papua New Guinea','Paraguay','Peru',
        'Philippines','Pitcairn Islands','Poland','Portugal','Puerto Rico',
        'Qatar','Republic of Kosovo','Romania','Russia','Rwanda',
        'S. Geo. and S. Sandw. Is.','S. Sudan','Sahrawi Arab Democratic Republic',
        'Saint Helena Ascension and Tristan da Cunha','Saint Kitts and Nevis',
        'Saint Lucia','Saint Vincent and the Grenadines','Samoa','San Marino','Saudi Arabia',
        'Senegal','Serbia','Seychelles','Siaoher Glacier','Sierra Leone',
        'Singapore','Slovakia','Slovenia','Solomon Is.','Somalia',
        'South Africa','Spain','Sri Lanka','Sudan','Suriname',
        'Swaziland','Sweden','Switzerland','Syria','Tajikistan',
        'Tanzania','Thailand','Timor-Leste','Togo','Tokelau',
        'Tonga','Trinidad and Tobago','Tunisia','Turkey','Turkmenistan',
        'Turks and Caicos Islands','Tuvalu','Uganda','Ukraine','United Arab Emirates',
        'United Kingdom','United States','Uruguay','Uzbekistan','Vanuatu',
        'Vatican City','Venezuela','Vietnam','W. Sahara','Yemen',
        'Zambia','Zimbabwe']

import nltk

# 出现最频繁的地点
fd =nltk.FreqDist(words).most_common()

cites_words = [fd[i][0] for i in range(len(fd))]
def getfreq(cites_words, cities_pyecharts, words, states_usa_words):
    same = []
    none = []
    k = 0
    for i in range(len(cites_words)):
        if cites_words[i] in cities_pyecharts:
            same.append([cites_words[i],words.count(cites_words[i])])
        elif cites_words[i] in states_usa_words:
            k = k+1
        else:
            none.append([cites_words[i],words.count(cites_words[i])])
    return same, none

same, none = getfreq(cites_words, cities_pyecharts, words, states_usa_words)

print('数据集和pyecharts有多少个地名相同'+' '+str(len(same)))
print('数据集和pyecharts有多少个地名不同（去除美国51个洲）'+' '+str(len(none)))


'''地点出现次数大于10的均转化成pyecharts中的地名'''
# England -- 105 -- United Kingdom
# USSR -- 苏联61 -- Russia
# SouthVietnam -- 二战时的越南38 -- Vietnam
# Taiwan -- 台湾 -- China
# Laos -- 老挝26 -- Lao PDR
# NewZealand -- 纽西兰 -- New Zealand
# NewGuinea -- 巴布亚新几内亚独立国 -- Papua New Guinea
# PuertoRico -- Puerto Rico
# SouthAfrica -- South Africa
# PapuaNewGuinea -- Papua New Guinea
# Scotland -- United Kingdom
# Congo -- 刚果 -- Congo
# SouthKorea -- 朝鲜 -- Korea
# DemocratiRepubliCongo -- 刚果民主共和国 -- Dem. Rep. Congo
# SaudiArabia -- 沙特 -- Saudi Arabia
# Czechoslovakia -- 捷克斯洛伐克二战  -- Slovakia
# Czechoslovakia -- 捷克斯洛伐克二战  -- Czech Rep.
# Yugoslavia -- 二战南斯拉夫
# SriLanka -- 斯里兰卡 -- Sri Lanka
# CostaRica -- 哥斯达黎加 -- Costa Rica
# Burma -- 二战缅甸 -- Myanmar
# HongKong -- 香港 -- China

country_transform_dic = {'England':'United Kingdom','USSR':'Russia','SouthVietnam':'Vietnam',
                     'Taiwan':'China','Laos':'Lao PDR','NewZealand':'New Zealand',
                     'NewGuinea':'Papua New Guinea','PuertoRico':'Puerto Rico','SouthAfrica':'South Africa',
                     'PapuaNewGuinea':'Papua New Guinea','Scotland':'United Kingdom','SouthKorea':'Korea',
                     'DemocratiRepubliCongo':'Dem. Rep. Congo','SaudiArabia':'Saudi Arabia',
                     'Czechoslovakia':'Slovakia','SriLanka':'Sri Lanka','CostaRica':'Costa Rica',
                     'Burma':'Myanmar','HongKong':'China',
                     'DominicanRepublic':'Dominican','ElSalvador':'El Salvador','CentralAfricanRepublic':'Central African Rep.',
                     '':'','':'','':'','':''}
country_transform = ['England','USSR','SouthVietnam',
                     'Taiwan','Laos','NewZealand',
                     'NewGuinea','PuertoRico','SouthAfrica',
                     'PapuaNewGuinea','Scotland','SouthKorea',
                     'DemocratiRepubliCongo','SaudiArabia',
                     'Czechoslovakia','SriLanka','CostaRica',
                     'Burma','HongKong']

# words中地名替换成pyecharts中地名
same_country = [same[i][0] for i in range(len(same))]
same_num = [same[i][1] for i in range(len(same))]

none_country = [none[i][0] for i in range(len(none))]
none_num = [none[i][1] for i in range(len(none))]

# 进行替换
def transform(none_country, country_transform, country_transform_dic):
    for i in range(len(none_country)):
        if none_country[i] in set(country_transform):
            for key,value in country_transform_dic.items():
                none_country[i] = none_country[i].replace(key,value)
        else:
            none_country[i] = none_country[i]
    return none_country

none_country = transform(none_country, country_transform, country_transform_dic)
none_country[0:20]
            

country = same_country+(none_country)
num = same_num+none_num
print('各地区空难数最大值'+' '+str(max(num)))
print('各地区空难数最小值'+' '+str(min(num)))
print('美国各州加和'+' '+str(sum(states_usa_num)))

# 加入美国和斯洛伐克，显示方便，美国空难数记作200
country = country+['Czech Rep.','United States']
num = num+[15,200]

# 全球一共218个地区在pyecharts地图上有所显示+2个地区无法显示
from pyecharts import Map
map1 = Map("全球发生空难次数","1908-2009", width=1200, height=600)
map1.add("全球发生空难次数", country, num, maptype="world", visual_range=[0, 200],
         is_visualmap=True, visual_text_color='#000', is_map_symbol_show=False)
map1.render('全球发生空难次数.html')
map1

fw = open("country.txt", 'w', encoding='utf-8') 
for i in range(len(country)):
        fw.write(country[i])
        fw.write('\n')
fw.close()



# 伤亡分析
# 去掉文本信息
df1 = df.drop(["Summary","cn/In","Flight #","Route","Location","Type"],axis=1)

# 显示伤亡人数最多的事故
print('1908-2009年空难伤亡总人数'+' '+str(df1["Fatalities"].sum()))

fatal = df1[df1["Fatalities"].notnull()]
fatal = fatal.sort_values(by="Fatalities")
print(fatal[-5:])

print("伤亡概率: {:.3f}".format(fatal[fatal["Fatalities"] != 0]["Fatalities"].sum() / fatal[fatal["Fatalities"] != 0]["Aboard"].sum()))

print('内特里费空难：两架波音-747相撞，死亡583人，又称世纪大空难')
print('日航123空难：波音747撞富士山，单架飞机失事最高死亡记录')
print('恰尔基达德里撞机事件，最严重的的空中撞机事件')
print('土耳其航空981号班机空难：货舱门未锁定导致爆炸性施压')
print('印度航空182号班机：恐怖袭击')


# Ground
# Kaggle上查阅资料，发现这三个数字字段有以下含义
# Aboard: Total aboard (passengers / crew)
# Fatalities: Total fatalities aboard (passengers / crew)
# Ground:  Total killed on the ground

fata2 = df1[df1["Ground"].notnull()]
fata2 = fata2.sort_values(by="Ground")
print(fata2[-6:]) # 前6个死亡人数大于100的

# 提取年份信息，对Ground变量进行处理
def get_year(x):
    return x.split("/")[-1]
fata2['year'] = fata2["Date"].map(get_year)
year_ground_fata2 = fata2[fata2["year"] != np.NaN][["year","Ground"]]
year_ground_fata2.info()

def year_analysis(x):
    return pd.Series({"year_ground_num":x["Ground"].sum(),"year_ground_max":x["Ground"].max(),
                      "year_ground_average":x["Ground"].sum() / len(x["Ground"])})
year_ground = year_ground_fata2.groupby(["year"]).apply(year_analysis)
year_ground = year_ground.sort_index()


from pyecharts import Bar

bar3 = Bar("空难地面死亡人数")
bar3.add("sum", yearlist, year_ground["year_ground_num"], mark_point=["min","max"])
bar3.add("max", yearlist, year_ground["year_ground_max"], mark_line=["min", "max"])
bar3.add("average", yearlist, year_ground["year_ground_average"], mark_line=["average"])
bar3.render('空难地面死亡人数.html')
bar3

# 去掉911事件
year_ground_fata2_new = year_ground_fata2[year_ground_fata2['Ground'] != 2750.0]
len(year_ground_fata2_new)

year_ground_new = year_ground_fata2_new.groupby(["year"]).apply(year_analysis)
year_ground_new = year_ground_new.sort_index()

from pyecharts import Bar

bar4 = Bar("空难地面死亡人数")
bar4.add("sum", yearlist, year_ground_new["year_ground_num"], mark_point=["min","max"])
bar4.add("max", yearlist, year_ground_new["year_ground_max"], mark_line=["min", "max"])
bar4.add("average", yearlist, year_ground_new["year_ground_average"], mark_line=["average"])
bar4.render('空难地面死亡人数1.html')
bar4


# Abiard Fatalities
# 提取年份信息
#def get_year(x):
    #return x.split("/")[-1]
#fatal = df1[df1["Fatalities"].notnull()]
#fatal['year'] = fatal["Date"].map(get_year)
#year_fatalities_fata1 = fata1[fata1["year"] != np.NaN][["year","Aboard","Fatalities"]]
# year_ground_fata1.info()

year_fatalities_fata1 = fata2[['year', 'Aboard', 'Fatalities']]

# 提取每年空难死亡人数和发生空难次数和死亡率
def year_analysis_fatalities(x):
    return pd.Series({"year_fatalities_num":x["Fatalities"].sum(),"year_fatalities_time":x.shape[0],
                      "year_fatalities_ratio":x["Fatalities"].sum() / x["Aboard"].sum()})
year_fatalities = year_fatalities_fata1.groupby(["year"]).apply(year_analysis_fatalities)
year_fatalities = year_fatalities.sort_index()
year_fatalities.info()

plt.close()
plt.figure(figsize=(16,4))
plt.subplot(1,3,1)
year_fatalities["year_fatalities_num"].plot(title="fata_num")
plt.subplot(1,3,2)
year_fatalities["year_fatalities_time"].plot(title="crash_time")
plt.subplot(1,3,3)
year_fatalities["year_fatalities_ratio"].plot(title="fata_ratio")
plt.show()

# 提取小时信息
def get_hour(x):
    hour = x.split(":")[0]
    try:
        hour = float(hour)
        if int(hour) == hour and hour < 24:
            return hour
        else:
            return np.nan
    except:
        return np.nan

fata3 = df[df["Time"].isnull() == False]
fata3["hour"] = fata3["Time"].map(get_hour)
year_fatalities_fata3 = fata3[['hour', 'Aboard', 'Fatalities']]

# 提取每年空难死亡人数和发生空难次数和死亡率
def hour_analysis_fatalities(x):
    return pd.Series({"hour_fatalities_num":x["Fatalities"].sum(),"hour_fatalities_time":x.shape[0],
                      "hour_fatalities_ratio":x["Fatalities"].sum() / x["Aboard"].sum()})
hour_fatalities = year_fatalities_fata3.groupby(["hour"]).apply(hour_analysis_fatalities)
hour_fatalities.info()

plt.close()
plt.figure(figsize=(16,4))
plt.subplot(1,3,1)
hour_fatalities["hour_fatalities_num"].plot(title="fata_num")
plt.subplot(1,3,2)
hour_fatalities["hour_fatalities_time"].plot(title="crash_time")
plt.subplot(1,3,3)
hour_fatalities["hour_fatalities_ratio"].plot(title="fata_ratio")
plt.show()

# 提取 Aboard 的信息
def year_analysis_aboard(x):
    return pd.Series({"year_aboard_num":x["Aboard"].sum(),"year_aboard_time":x.shape[0]})
year_aboard = year_fatalities_fata1.groupby(["year"]).apply(year_analysis_aboard)
year_aboard = year_aboard.sort_index()

# 画 Aboard 和 Fatalities 对比图
from pyecharts import Bar

bar5 = Bar("每年登机和遇难人数")
bar5.add("Aboard", yearlist, year_aboard["year_aboard_num"], mark_line=["average"], mark_point=["max", "min"])
bar5.add("Fatalities", yearlist, year_fatalities["year_fatalities_num"], mark_line=["average"], mark_point=["max", "min"])
bar5.render('每年登机和遇难人数.html')
bar5

print(sum(year_fatalities["year_fatalities_num"]))
print(sum(year_aboard["year_aboard_num"]))
print(sum(year_fatalities["year_fatalities_num"]) / sum(year_aboard["year_aboard_num"]))



# 机型
type_df = df["Type"]
def type_handle(x):
    x = str(x)
    if "McDonnell Douglas" in x:
        return "McDonnell Douglas"
    elif ("Douglas" in x) & ("McDonnell Douglas" not in x):
        return "Douglas"
    elif ("McDonnell" in x) & ("McDonnell Douglas" not in x):
        return "McDonnell"
    elif "Antonov" in x:
        return "Antonov"
    elif "Boeing" in x:
        return "Boeing"
    elif "Cessna" in x:
        return "Cessna"
    elif "de Havilland" in x:
        return "de Havilland"
    elif "Airbus" in x:
        return "Airbus"
    elif "Embraer" in x:
        return "Embraer"
    elif "Fokker" in x:
        return "Fokker"
    elif "Ilyushin" in x:
        return "Ilyushin"
    elif "Lockheed" in x:
        return "Lockheed"
    else:
        return "other"
company_df = type_df.map(type_handle)
print(pd.value_counts(company_df))

company_describe = ['其他','道格拉斯-美国','波音-美国','洛克希德-美国','塞斯纳-苏联','德.哈维尔-英国','安东诺夫-法国',
                   '福克-荷兰','麦克唐纳.道格拉斯-美国','伊尔-苏联','巴西航空工业公司-巴西','空客-法国','麦克唐纳-美国']
company_sol = pd.value_counts(company_df)
company = ['Other','Douglas','Boeing','Lockheed','Cessna','de Havilland','Antonov',
           'Fokker','McDonnell Douglas','Ilyushin','Embraer','Airbbus','McDonnell']
company_num = company_sol.values.tolist()

company_describe_se = pd.Series(company_describe)
company_se = pd.Series(company)
company_num_se = pd.Series(company_num)
company_se = pd.concat([company_se, company_describe_se, company_num_se], axis=1)

company_se

company_sol = pd.value_counts(company_df)
company = ['Other','Douglas','Boeing','Lockheed','Cessna','de Havilland','Antonov',
           'Fokker','McDonnell Douglas','Ilyushin','Embraer','Airbbus','McDonnell']
company_num = company_sol.values.tolist()

# 画柱状图
from pyecharts import Bar
bar6 = Bar("出事飞行制造商")
bar6.add("company", company, company_num, is_datazoom_show=True, mark_point=["max", "min"], is_label_show=True)
bar6.render("出事飞行制造商.html")
bar6


def airplane_count(x):
    fatal_ratio = x["Fatalities"].sum() / x["Aboard"].sum()
    crash_time = x.shape[0]
    fatal_num = x["Fatalities"].sum()
    return pd.Series({"fatal_num":fatal_num,"crash_time":crash_time,"fatal_ratio":fatal_ratio})

company_fata4 = fata4.groupby(['Company']).apply(airplane_count)

plt.close()
plt.figure(figsize=(16,4))
plt.subplot(1,3,1)
company_fata4['crash_time'].drop("other").plot(kind='bar',title="time")
plt.subplot(1,3,2)
company_fata4['fatal_num'].drop("other").plot(kind='bar',title="fatal_num")
plt.subplot(1,3,3)
company_fata4['fatal_ratio'].plot(kind='bar',title="fatal_ratio")
plt.show()



# 评论
summary = df[df['Summary'].isnull() == False][['Summary']]
# 数据框转化为列表
summary = np.array(summary).tolist()

# 分句处理
import nltk

sent=[]
for i in range(len(summary)):
    sent.append(nltk.tokenize.sent_tokenize(summary[i][0]))
sent[0:3]

# 分词处理
word = []
for i in sent:
    for j in i:
        word.extend(nltk.tokenize.word_tokenize(j))  # 把各个句子中的词合成一块了
word[0:3]

# 小写处理
word_lower=[i.lower() for i in word]
word_lower[0:3]

# 去除标点符号和停用词
from nltk.corpus import stopwords
english_stopwords = stopwords.words("english")
english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '!', '@', '#', '%', '$', '*', '...'] # 自定义英文表单符号列表
word_clear=[]
for i in word_lower:
    if i not in english_stopwords: # 过滤停用词
        if i not in english_punctuations: # 过滤标点符号
            word_clear.append(i)

print ("/".join(word_clear[0:10]))

# 词干化处理
# 将动词去掉-ed, -ing等语态，名词去掉复数形式等
# nltk.stem.porter.PorterStemmer()、nltk.stem.lancaster.LancasterStemmer() 等
from nltk.stem.porter import PorterStemmer
pt = PorterStemmer()
word_stem=[pt.stem(word) for word in word_clear]
word_stem[0:5]

# 简单的统计汇总
# 利用函数 Text() 将分词结果转换为 Text 格式
from nltk.text import Text
word_text=Text(word_stem)

# 识别评论文本中常用固定词组搭配
word_text.collocations(num=20, window_size=2)

# 与不进行词干化处理进行比较
word_text_clear=Text(word_clear)
word_text_clear.collocations(num=20, window_size=2)

# 利用 Counter 计数器统计出现次数最多的前 20 个单词
from collections import Counter
word_counter=Counter(word_stem)
word_counter.most_common(20)

# 与不进行词干化处理进行比较
from collections import Counter
word_counter_clear=Counter(word_clear)
word_counter_clear.most_common(20)

# 上下文相关内容
word_text.concordance("weather",lines=10)

# 上下文相关内容
word_text_clear.concordance("weather",lines=10)

print(len(set(word_clear)))
print(len(set(word_stem)))

# 画词云图
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator

backgroud_Image = plt.imread('C:\\Users\\Administrator\\Desktop\\大数据学院\\统计软件\\期末资料\\空难数据\\plane.jpg')   # 自己可以换
wc1 = WordCloud(mask = backgroud_Image,
               max_words = 2000,
               max_font_size = 100,
              background_color='white') 
wc1.generate(' '.join(word_clear))
image_colors = ImageColorGenerator(backgroud_Image)
wc1.recolor(color_func = image_colors)
plt.imshow(wc1)
plt.axis('off')
plt.show()

# 储存图片
wc.to_file("summary.jpg")


# 天气
# icing, fog, turbulence, meteorological气象, thunderstorm, poor, whiteout
word_text_clear = Text(word_clear)
word_text_clear.similar('weather')


# 词性标注








countries = ['Afghanistan',
'Albania',
'Algeria',
'Andorra',
'Angola',
'Anguilla',
'AntiguaandBarbuda',
'Argentina',
'Armenia',
'Australia',
'Austria',
'Azerbaijan',
'Bahrain',
'Bangladesh',
'Barbados',
'Belarus',
'Belgium',
'Belize',
'Benin',
'Bermuda',
'Bhutan',
'Bolivia',
'BosniaandHerzegovina',
'Botswana',
'Brazil',
'BritishIndianOceanTerritory',
'BritishVirginIslands',
'Brunei',
'Bulgaria',
'BurkinaFaso',
'Burundi',
'Cambodia',
'Cameroon',
'Canada',
'CapeVerde',
'CaymanIslands',
'CentralAfricanRepublic',
'Chad',
'Chile',
'Colombia',
'Comoros',
'Congo-Brazzaville',
'Congo-Kinshasa',
'CookIslands',
'CoralSeaIslandsTerritory',
'CostaRica',
'Croatia',
'Cuba',
'Cyprus',
'Czechia',
'Denmark',
'Djibouti',
'Dominica',
'DominicanRepublic',
'EastTimor',
'Ecuador',
'Egypt',
'ElSalvador',
'EquatorialGuinea',
'Eritrea',
'Estonia',
'Ethiopia',
'FalklandIslands',
'FaroeIslands',
'FederatedStatesofMicronesia',
'Fiji',
'Finland',
'France',
'Gabon',
'Georgia',
'Germany',
'Ghana',
'Gibraltar',
'Greece',
'Greenland',
'Guatemala',
'Guernsey',
'Guinea-Bissau',
'Guinea',
'Guyana',
'Haiti',
'Honduras',
'Hungary',
'Iceland',
'India',
'Indonesia',
'Iraq',
'Ireland',
'IslamicRepublicofIran',
'IsleofMan',
'Israel',
'Italy',
'Jamaica',
'Japan',
'Jersey',
'Jordan',
'Kazakhstan',
'Kenya',
'Kiribati',
'Kuwait',
'Kyrgyzstan',
'Laos',
'Latvia',
'Lebanon',
'Lesotho',
'Liberia',
'Libya',
'Liechtenstein',
'Lithuania',
'Luxemburg',
'Macedonia',
'Madagascar',
'Malawi',
'Malaysia',
'Maldives',
'Mali',
'Malta',
'MarshallIslands',
'Mauritania',
'Mauritius',
'Mexico',
'Moldova',
'Monaco',
'Mongolia',
'Montenegro',
'Montserrat',
'Morocco',
'Mozambique',
'Myanmar',
'Namibia',
'Nepal',
'NewZealand',
'Nicaragua',
'Niger',
'Nigeria',
'Niue',
'NorthKorea',
'Norway',
'Oman',
'Pakistan',
'Palau',
'Palestine',
'Panama',
'PapuaNewGuinea',
'Paraguay',
'Peru',
'Philippines',
'PitcairnIslands',
'Poland',
'Portugal',
'Qatar',
'RepublicofKosovo',
'Romania',
'Russia',
'Rwanda',
'SahrawiArabDemocraticRepublic',
'SaintHelenaAscensionandTristandaCunha',
'SaintKittsandNevis',
'SaintLucia',
'SaintVincentandtheGrenadines',
'Samoa',
'SanMarino',
'SaudiArabia',
'Senegal',
'Serbia',
'Seychelles',
'SierraLeone',
'Singapore',
'Slovakia',
'Slovenia',
'SolomonIslands',
'Somalia',
'SouthAfrica',
'SouthGeorgiaandtheSouthSandwichIslands',
'SouthKorea',
'SouthSudan',
'Spain',
'SriLanka',
'Sudan',
'Suriname',
'Swaziland',
'Sweden',
'Syria',
'Tajikistan',
'Tanzania',
'Thailand',
'TheBahamas',
'TheGambia',
'TheNetherlands',
'Togo',
'Tokelau',
'Tonga',
'TrinidadandTobago',
'Tunisia',
'Turkey',
'Turkmenistan',
'TurksandCaicosIslands',
'Tuvalu',
'Uganda',
'Ukraine',
'UnitedArabEmirates',
'UnitedKingdom',
'Uruguay',
'USA',
'Uzbekistan',
'Vanuatu',
'VaticanCity',
'Venezuela',
'Vietnam',
'Yemen',
'Zambia',
'Zimbabwe']


# get number of different years
Algorithms = ['LR','KNN','D.T.','RF','GBDT','SVM','BP-N.']
test = [0.857,0.83,0.791,0.847,0.832,0.84,0.851]
train = [0.859,0.86,1.000,0.874,0.919,0.99,0.888]

from pyecharts import Bar
bar = Bar("All Algorithms")
bar.add("Test Accuracy", Algorithms, test, mark_point=['max','min'], legend_text_color='red', is_label_show=True)
bar.add("Train Accuracy", Algorithms, train, mark_point=['max','min'], legend_text_color='red', is_label_show=True)
# bar.print_echarts_options() # 该行只为了打印配置项，方便调试时使用
bar.render("All Algorithms.html")    # 生成本地 HTML 文件
bar


Algorithms = ['RF','RF1','GBDT.','GBDT1','BP-N.','BP-N.1']
test = [0.838,0.847,0.832,0.832,0.83,0.851]
train = [1.000,0.874,0.902,0.919,0.89,0.888]

from pyecharts import Bar
bar = Bar("调参对比")
bar.add("Test Accuracy", Algorithms, test, legend_text_color='red', is_label_show=True)
bar.add("Train Accuracy", Algorithms, train, legend_text_color='red', is_label_show=True)
# bar.print_echarts_options() # 该行只为了打印配置项，方便调试时使用
bar.render("调参对比.html")    # 生成本地 HTML 文件
bar