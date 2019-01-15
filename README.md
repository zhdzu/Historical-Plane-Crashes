# Historical-Plane-Crashes

Kaggle 数据集网址：https://www.kaggle.com/nguyenhoc/plane-crash/home
记录了 1908 年- 2009 年发生空难的主要信息。

## 主要工具
matplotlib\seaborn\pyecharts\nltk 以pyecharts\nltk为主

## 主要工作
1.空难次数随年份、月份和小时变换情况；  
2.空难次数随年份和月份交替的 3D 图；  
3.地图可视化  
3.1 pyecharts编辑美国各州信息，全球地区信息  
3.2 数据中地理信息和pyecharts中地区一一对应  
3.3 地区词云图  
3.4 美国各州发生空难可视化  
3.5 全球各地区发生空难可视化  
3.6 排名靠前的城市可视化  
4.伤亡分析  
4.1 地面伤亡人数分析  
4.2 每年登机和遇难人数分析  
5.机型分析  
6.遇难原因分析  
分词处理-小写处理-除标点符号和停用词-词干化处理-简单的统计汇总-上下文相关内容-画词云图  
7.词性标注

## 代码说明
Airplane Crashes.ipynb 是当时运行的代码，部分生成的地图可视化和词云图见文件 Pictures。  
work.py 关于空难数据集和pyecharts画图的部分代码，大约有1000多行代码。用Spyder分模块跑的，有些可能没法运行。是空难数据集的代码汇总。

## pyecharts 文件夹
由于 pyecharts 官网没有给出各个国家和地区的名称，或给出的名称和实际使用的名称不一致，本文对 pyecharts 用到的地理名称进行了梳理。  
主要存储了 pyecharts 中美国52个地区的地区名，和全球218个国家和地区的 pyechats 名称。  
除了两个地区 pyecharts 在地图上无法标注外，其余国家和地区均在这个文件中存在。  

## UCL 二分类数据集
ucl_credit6000.ipynb 储存了 LR、KNN、DecisionTree、RF、GBDT 和 Neural Networks 在二分类数据集上的代码。部分利用 GridSearchCV 进行了调参。
