
# coding: utf-8

# 実施予定日： 2018/05/28
# 
# - 記入者: y-ito, s-kanai
# 
# ## このノートの目的
# 
# - イベント: https://serakumedia.connpass.com/event/88165/
# - 元のkernelを読み解き、データ解析（可視化、表現するに有効な特徴量選択）についての理解を深める
#     - 元のkernel: https://www.kaggle.com/uciml/breast-cancer-wisconsin-data
#         - 取り扱うデータセット： 乳がん検査のデジタル画像を元に細胞の特徴を列挙したもの。

# ![](https://preview.ibb.co/bKsv9k/k.jpg)
# # INTRODUCTION
# In this data analysis report, I usually focus on feature visualization and selection as a different from other kernels. Feature selection with correlation, univariate feature selection, recursive feature elimination, recursive feature elimination with cross validation and tree based feature selection methods are used with random forest classification. Apart from these, principle component analysis are used to observe number of components.
# 
# **Enjoy your data analysis!!!**
# 
# 

# 【訳】 序論
# 
# このデータ分析レポートでは、通常、私は他のカーネルとは違うものとして、特徴量の視覚化と選択に焦点を当てています。
# 
# - 相関による特徴量選択
# - 単変量特徴量選択
# - 再帰的な特徴量の除去
# - クロスバリデーションによる再帰的な特徴量の削除
# - 木構造を用いた特徴選択方法
# 
# これらは、ランダムなフォレストによる分類処理で良く使用されます。
# 
# それとは別に
# 
# - Principle Component Analysis (PCA、主成分分析) 
# 
# を扱うことで特徴量の個数を検討することができます。
# 
# **それではデータの分析をお楽しみください！！！**
# 
# 【メモ】 
# 
# > このデータ分析レポートでは、通常、私は他のカーネルとは違うものとして、
# 
# 一般的なKernelはコンペのスコアを上げるためのTIPS、モデルの検証などがほとんどのため、
# 今回のコンペのないデータセットと区別していると思います。
# 

# # Data Analysis

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

# 【訳】 このPython3の環境（kaggle kernelのnote）便利なライブラリがインストールされています。
# 内容はこちらで定義されています。: https://github.com/kaggle/docker-python
# 例えば以下の便利なパッケージがロードできます。

import numpy as np # linear algebra 数値計算を効率的に行うための拡張モジュール
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv) データセットを操作するためのデータ構造と演算をサポートするモジュール
import seaborn as sns # data visualization library  可視化モジュール
import matplotlib.pyplot as plt # 可視化用関数
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
import time
from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


data = pd.read_csv('../input/data.csv')


# Before making anything like feature selection,feature extraction and classification, firstly we start with basic data analysis. 
# Lets look at features of data.

# 【訳】 特徴量選択、抽出、そして分類などを行う前にまず基本的なデータ分析から始めます。
# データの特徴量を見てみましょう。

# In[ ]:


data.head()  # head method show only first 5 rows


# **There are 4 things that take my attention**
# 
# 1) There is an **id** that cannot be used for classificaiton 
# 
# 2) **Diagnosis** is our class label
# 
# 3) **Unnamed: 32** feature includes NaN so we do not need it.
# 
# 4) I do not have any idea about other feature names actually I do not need because machine learning is awesome **:)**
# 
# Therefore, drop these unnecessary features. However do not forget this is not a feature selection. This is like a browse a pub, we do not choose our drink yet !!!

# 【訳】 **私の注意を引く点が4つある**
# 
# 1）分類には使用できない ** id ** があります
# 
# 2） **Diagnosis(診断結果)** はクラスラベルです
# 
# 3） **Unnamed: 32** 列にはNaNが含まれているので、必要ありません。
# 
# 4） その他の特徴量の名称についてはわかりません。 実際には機械学習がすばらしいので、理解する必要はありません。 **:)** 
# 
# したがって、これらの不要な特徴量を削除してください。 しかし、これは特徴量選択の作業ではないことを忘れないでください。 これはパブを眺めるようなものですが、まだドリンクを選んいるわけではないですよ!!!

# 【メモ】
# 
# 4) について、実務においてはこのスタンスはちょっと悩ましいと思いました。
# 
# この後データの分布や変数間の相関を見て分析するフェーズにはいるはずで、
# データの傾向を見つけたときに **そのデータの意味を知っているとその傾向について確信がもてるかもしれない** ので意味について知っておくのは大事と考えます。
# また、データの意味と傾向に違和感などに気づくこともできます。
# （データの意味が間違っていたり、整形段階で誤った処理を行っているなど）
# 
# ただし、意味に捕らわれて時間がかかってしまったり、
# 本来の目的を忘れて別の調査をしてしまうなどもやりがちなので、
# ほどほどにして進めるのが良さそうです。
# 
# 

# In[ ]:


# feature names as a list
col = data.columns       # .columns gives columns names in data 
print(col)


# In[ ]:


# y includes our labels and x includes our features
y = data.diagnosis   # M or B 
list = ['Unnamed: 32','id','diagnosis']   # 除外したい対象の列名
x = data.drop(list,axis = 1 )   # listという配列をもとに除外
x.head()


# In[ ]:


# 個人的には .T関数で転置すると表示が縦になるので見やすい場合もあります。
# x.head().T


# In[ ]:


ax = sns.countplot(y,label="Count")       # M = 212, B = 357
B, M = y.value_counts()
print('Number of Benign: ',B)
print('Number of Malignant : ',M)


# Okey, now we have features but **what does they mean** or actually **how much do we need to know about these features**
# The answer is that we do not need to know meaning of these features however in order to imagine in our mind we should know something like variance, standart deviation, number of sample (count) or max min values.
# These type of information helps to understand about what is going on data. For example , the question is appeared in my mind the **area_mean** feature's max value is 2500 and **smoothness_mean** features' max 0.16340. Therefore **do we need standirdization or normalization before visualization, feature selection, feature extraction or classificaiton?** The answer is yes and no not surprising ha :) Anyway lets go step by step and start with visualization.  

# 【訳】　オッケー、この特徴量ですが、**それらの意味について** や **これらの特徴量についてどれだけ知る必要があるのでしょうか？**
# 答えは、これらの意味を知る必要はありません。 
# しかし、データのイメージを掴むため分散、標準偏差、サンプル数（カウント）、または最大最小値については知っておいたほうが良いでしょう。 
# これら代表値の情報は、データの状況を理解するのに役立ちます。 
# たとえば、**area_mean** の最大値は2500、**smoothness_mean**機能の最大値は0.16340です。 
# その場合、**可視化、特徴量選択、特徴量抽出または分類の前に、標準化または正規化が必要でしょうか？** 
# 答えは「イエス」であり、驚くべきことではありません。 :）
# とにかく一歩ずつ進めて、次に可視化の作業を始めましょう。

# 【メモ】
# ここでもここの特徴量について知る必要は無いという意見でしたが、特徴量を選ぶタイミングでは意味を知っておいたほうが良いと思っています。
# もしかしたら、今回のノートでは手法の紹介と割り切っているためかもしれません。参加者のみなさんと議論したいところ。

# In[ ]:


x.describe()


# In[ ]:


# これも転置させると全部見れる。
# x.describe().T


# # Visualization
# In order to visualizate data we are going to use seaborn plots that is not used in other kernels to inform you and for diversity of plots. What I use in real life is mostly violin plot and swarm plot. Do not forget we are not selecting feature, we are trying to know data like looking at the drink list at the pub door.

# 【訳】 可視化
# 
# データを視覚化するために、他のカーネルでは使用されていないseabornプロットを使用して、多数の描画方法について紹介します。 私がよく使っているのは、主にバイオリン図とスワームプロット（蜂群図）です。 我々は特徴量選択をしているわけでないことに注意してください、我々はパブのドアで飲み物のリストを眺めているように、データを知ろうとしているところです。

# Before violin and swarm plot we need to normalization or standirdization. Because differences between values of features are very high to observe on plot. I plot features in 3 group and each group includes 10 features to observe better.

# 【訳】バイオリン、スワームプロットを作成する前に、正規化(normalization)や標準化(standardization)が必要です。 特徴量の値の間の差はグラフで観察するのが非常に大きすぎるためです。
# 私は3つのグループに特徴量をプロットし、各グループには10つの特徴量が含まれています。

# 【メモ】 正規化、標準化について
# 
# 単位や次元が違うことで、数量をそのまま比較することができないものを代表値などで割るなどして比較できるようにすること。
# 
# 以下では
# 
# $$
# z = \frac{X - \mu}{\sigma}
# $$
# 
# という式で平均0標準偏差1の分布に変換しています。

# In[ ]:


# first ten features
data_dia = y
data = x
data_n_2 = (data - data.mean()) / (data.std())              # standardization
data = pd.concat([y,data_n_2.iloc[:,0:10]],axis=1)
data = pd.melt(data,id_vars="diagnosis",
                    var_name="features",
                    value_name='value')
plt.figure(figsize=(10,10))
sns.violinplot(x="features", y="value", hue="diagnosis", data=data,split=True, inner="quart")
plt.xticks(rotation=90);


# Lets interpret the plot above together. For example, in **texture_mean** feature, median of the *Malignant* and *Benign* looks like separated so it can be good for classification. However, in **fractal_dimension_mean** feature,  median of the *Malignant* and *Benign* does not looks like separated so it does not gives good information for classification.

# 【訳】　上記のプロットを一緒に解釈しましょう。 たとえば、**texture_mean** では、 *悪性腫瘍(Malignant)* 　と　*良性腫瘍(Benign)*　の中央値が分離しているように見えるため、分類に適していると言えそうです。 しかし、 *fractal_dimension_mean* は、悪性および良性の中央値は分離されていないように見えるので、分類のための良い情報は得られていません。

# 【メモ】 上のコードは今までの中では長めのコードになるので、順を追って見てみます。

# In[ ]:


data_dia = y  #  y = data.diagnosis
data = x
data_n_2 = (data - data.mean()) / (data.std())              # standardization
data = pd.concat([y,data_n_2.iloc[:,0:10]],axis=1)


# 列が横長になっているものを列名を持つ列を追加した上で縦長に整形(ここでは前半3行のデータのみ使って整形しています)
data = pd.melt(data.head(3),id_vars="diagnosis",
                    var_name="features",
                    value_name='value')

# データを縦長にもたせseabornのプロットに適した形に整形している。
data


# In[ ]:


# Second ten features
data = pd.concat([y,data_n_2.iloc[:,10:20]],axis=1)
data = pd.melt(data,id_vars="diagnosis",
                    var_name="features",
                    value_name='value')
plt.figure(figsize=(10,10))
sns.violinplot(x="features", y="value", hue="diagnosis", data=data,split=True, inner="quart")
plt.xticks(rotation=90)


# In[ ]:


# Second ten features
data = pd.concat([y,data_n_2.iloc[:,20:31]],axis=1)
data = pd.melt(data,id_vars="diagnosis",
                    var_name="features",
                    value_name='value')
plt.figure(figsize=(10,10))
sns.violinplot(x="features", y="value", hue="diagnosis", data=data,split=True, inner="quart")
plt.xticks(rotation=90)


# Lets interpret one more thing about plot above, variable of **concavity_worst** and **concave point_worst** looks like similar but how can we decide whether they are correlated with each other or not.
# (Not always true but, basically if the features are correlated with each other we can drop one of them)

# 【訳】 上のプロットについてもう一つ解釈すると、 **concavity_worst** と **convex_worst** は同様のように見えますが、どうやって相関しているかどうかを判断できえうしょうか。 （絶対ではないが、基本的に特徴量が相関が強い場合、その特徴量の1つを削除できます）
# 
# 【メモ】
# 
# 機械学習、統計モデルでは、各説明変数は独立変数であるという仮定を置くので、
# 説明変数間で強い相関がある＝独立ではない　となるとそもそもの仮定が間違ってしまいます。
# 強い相関のある特徴量を含んだままモデルの構築（パラメタ推定）を行うと、安定しなかったり、性能が悪くなってしまうので注意が必要です。
# 詳しくは　「マルチコ」、「多重共線性」というワードで調べてみてください。

# In order to compare two features deeper, lets use joint plot. Look at this in joint plot below, it is really correlated.
#  Pearsonr value is correlation value and 1 is the highest. Therefore, 0.86 is looks enough to say that they are correlated. Do not forget, we are not choosing features yet, we are just looking to have an idea about them.

# 【訳】 この2つの特徴量をより深く比較するために、ジョイントプロットを使用できます。 下のジョイントプロットを見てみるとやはり強い相関を示しています。 ピアソン相関係数は、1が最も高い。 したがって、0.86は十分相関があると言えます。 私たちはまだ特徴量選択をしていないことを忘れないでください。私たちは特徴量選択のためのアイデアを探している段階です。

# In[ ]:


import warnings
warnings.filterwarnings('ignore')  # 最新でパッチがあたるので今は無視 https://github.com/mwaskom/seaborn/issues/1392

sns.jointplot(x=x.loc[:,'concavity_worst'], y=x.loc[:,'concave points_worst'], kind="reg", color="#ce1414");


# What about three or more feauture comparision ? For this purpose we can use pair grid plot. Also it seems very cool :)
# And we discover one more thing **radius_worst**, **perimeter_worst** and **area_worst** are correlated as it can be seen pair grid plot. We definetely use these discoveries for feature selection.

# 【訳】 3つ以上の特徴量の比較はにはペアグリッドプロットを使用することができます。 それは非常にクールだ:)
# 
# 私たちは新たに **radius_worst**、 **perimeter_worst** と **area_worst** について相関があることを発見し、
# ペアグリッドプロットとでも確認できます。 
# 我々はこれらの発見を特徴選択のために使用します。

# In[ ]:


sns.set(style="white")
df = x.loc[:,['radius_worst','perimeter_worst','area_worst']]
g = sns.PairGrid(df, diag_sharey=False)
g.map_lower(sns.kdeplot, cmap="Blues_d")  # 下部を2変量のカーネル密度推定値の描画
g.map_upper(plt.scatter)  # 上部を散布図行列の描画
g.map_diag(sns.kdeplot, lw=3)  # 対角要素を　1変量のカーネル密度推定値の描画


# Up to this point, we make some comments and discoveries on data already. If you like what we did, I am sure swarm plot will open the pub's door :) 

# In swarm plot, I will do three part like violin plot not to make plot very complex appearance

# 【訳】　ここまで、データに関するコメントや発見を行ってきました。 私たちがしたことが好きなら、私はスウォームプロットがパブのドアを開けると確信しています:)
# 
# スウォームプロット（蜂群図）でも、繁雑な描画にならないように、バイオリンプロット同様に3つに分けて行います。

# In[ ]:


sns.set(style="whitegrid", palette="muted")
data_dia = y
data = x
data_n_2 = (data - data.mean()) / (data.std())              # standardization
data = pd.concat([y,data_n_2.iloc[:,0:10]],axis=1)
data = pd.melt(data,id_vars="diagnosis",
                    var_name="features",
                    value_name='value')
plt.figure(figsize=(10,10))
tic = time.time()
sns.swarmplot(x="features", y="value", hue="diagnosis", data=data)

plt.xticks(rotation=90)


# In[ ]:


data = pd.concat([y,data_n_2.iloc[:,10:20]],axis=1)
data = pd.melt(data,id_vars="diagnosis",
                    var_name="features",
                    value_name='value')
plt.figure(figsize=(10,10))
sns.swarmplot(x="features", y="value", hue="diagnosis", data=data)
plt.xticks(rotation=90)


# In[ ]:


data = pd.concat([y,data_n_2.iloc[:,20:31]],axis=1)
data = pd.melt(data,id_vars="diagnosis",
                    var_name="features",
                    value_name='value')
plt.figure(figsize=(10,10))
sns.swarmplot(x="features", y="value", hue="diagnosis", data=data)
toc = time.time()
plt.xticks(rotation=90)
print("swarm plot time: ", toc-tic ," s")


# They looks cool right. And you can see variance more clear. Let me ask you a question, **in these three plots which feature looks like more clear in terms of classification.** In my opinion **area_worst** in last swarm plot looks like malignant and benign are seprated not totaly but mostly. Hovewer, **smoothness_se** in swarm plot 2 looks like malignant and benign are mixed so it is hard to classfy while using this feature.

# 【訳】 クールだね。 そして、あなたは分散をより明確に見えているでしょう。 質問をしてみましょう。 **これらの3つのプロットの中で、分類を行う上で有効な特徴量はどれでしょう?** 私の意見では最後の描画にある **area_worst** はほぼうまく分離しているように見えます。 一方二番目の描画に含まれている **smoothness_se**　については良性、悪性が混じっているため、この特徴量を利用してもクラス分けは難しいでしょう。

# **What if we want to observe all correlation between features?** Yes, you are right. The answer is heatmap that is old but powerful plot method.

# 【訳】　すべての特徴量について相関を見たい場合、どうすればよいでしょう？ はい、正解です。答えはヒートマップを使います。これは昔からある強力な描画方法です。

# In[ ]:


#correlation map
f,ax = plt.subplots(figsize=(18, 18))
sns.heatmap(x.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)


# Well, finaly we are in the pub and lets choose our drinks at feature selection part while using heatmap(correlation matrix).

# 【訳】 ここでやっと私たちはパブに入ったので、相関行列のヒートマップを使い、後半の特徴量選択パートで飲み物を選びましょう。

# # Feature Selection and Random Forest Classification
# Today our purpuse is to try new cocktails. For example, we are finaly in the pub and we want to drink different tastes. Therefore, we need to compare ingredients of drinks. If one of them includes lemon, after drinking it we need to eliminate other drinks which includes lemon so as to experience very different tastes.

# In this part we will select feature with different methods that are feature selection with correlation, univariate feature selection, recursive feature elimination (RFE), recursive feature elimination with cross validation (RFECV) and tree based feature selection. We will use random forest classification in order to train our model and predict. 

# ## 1) Feature selection with correlation and random forest classification

# As it can be seen in map heat figure **radius_mean, perimeter_mean and area_mean** are correlated with each other so we will use only **area_mean**. If you ask how i choose **area_mean** as a feature to use, well actually there is no correct answer, I just look at swarm plots and **area_mean** looks like clear for me but we cannot make exact separation among other correlated features without trying. So lets find other correlated features and look accuracy with random forest classifier. 

# **Compactness_mean, concavity_mean and concave points_mean** are correlated with each other.Therefore I only choose **concavity_mean**. Apart from these, **radius_se, perimeter_se and area_se** are correlated and I only use **area_se**.  **radius_worst, perimeter_worst and area_worst** are correlated so I use **area_worst**.  **Compactness_worst, concavity_worst and concave points_worst** so I use **concavity_worst**.  **Compactness_se, concavity_se and concave points_se** so I use **concavity_se**. **texture_mean and texture_worst are correlated** and I use **texture_mean**. **area_worst and area_mean** are correlated, I use **area_mean**.
# 
# 
# 

# In[ ]:


drop_list1 = ['perimeter_mean','radius_mean','compactness_mean','concave points_mean','radius_se','perimeter_se','radius_worst','perimeter_worst','compactness_worst','concave points_worst','compactness_se','concave points_se','texture_worst','area_worst']
x_1 = x.drop(drop_list1,axis = 1 )        # do not modify x, we will use it later 
x_1.head()


# After drop correlated features, as it can be seen in below correlation matrix, there are no more correlated features. Actually, I know and you see there is correlation value 0.9 but lets see together what happen if we do not drop it.

# In[ ]:


#correlation map
f,ax = plt.subplots(figsize=(14, 14))
sns.heatmap(x_1.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)


# Well, we choose our features but **did we choose correctly ?** Lets use random forest and find accuracy according to chosen features.

# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score,confusion_matrix
from sklearn.metrics import accuracy_score

# split data train 70 % and test 30 %
x_train, x_test, y_train, y_test = train_test_split(x_1, y, test_size=0.3, random_state=42)

#random forest classifier with n_estimators=10 (default)
clf_rf = RandomForestClassifier(random_state=43)      
clr_rf = clf_rf.fit(x_train,y_train)

ac = accuracy_score(y_test,clf_rf.predict(x_test))
print('Accuracy is: ',ac)
cm = confusion_matrix(y_test,clf_rf.predict(x_test))
sns.heatmap(cm,annot=True,fmt="d")


# Accuracy is almost 95% and as it can be seen in confusion matrix, we make few wrong prediction. 
# Now lets see other feature selection methods to find better results.

# ## 2) Univariate feature selection and random forest classification
# In univariate feature selection, we will use SelectKBest that removes all but the k highest scoring features.
# <http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectKBest.html#sklearn.feature_selection.SelectKBest>

# In this method we need to choose how many features we will use. For example, will k (number of features) be 5 or 10 or 15? The answer is only trying or intuitively. I do not try all combinations but I only choose k = 5 and find best 5 features.

# In[ ]:


from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
# find best scored 5 features
select_feature = SelectKBest(chi2, k=5).fit(x_train, y_train)


# In[ ]:


print('Score list:', select_feature.scores_)
print('Feature list:', x_train.columns)


# Best 5 feature to classify is that **area_mean, area_se, texture_mean, concavity_worst and concavity_mean**. So lets se what happens if we use only these best scored 5 feature.

# In[ ]:


x_train_2 = select_feature.transform(x_train)
x_test_2 = select_feature.transform(x_test)
#random forest classifier with n_estimators=10 (default)
clf_rf_2 = RandomForestClassifier()      
clr_rf_2 = clf_rf_2.fit(x_train_2,y_train)
ac_2 = accuracy_score(y_test,clf_rf_2.predict(x_test_2))
print('Accuracy is: ',ac_2)
cm_2 = confusion_matrix(y_test,clf_rf_2.predict(x_test_2))
sns.heatmap(cm_2,annot=True,fmt="d")


# Accuracy is almost 96% and as it can be seen in confusion matrix, we make few wrong prediction. What we did up to now is that we choose features according to correlation matrix and according to selectkBest method. Although we use 5 features in selectkBest method accuracies look similar.
# Now lets see other feature selection methods to find better results.

# ## 3) Recursive feature elimination (RFE) with random forest
# <http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.RFE.html>
# Basically, it uses one of the classification methods (random forest in our example), assign weights to each of features. Whose absolute weights are the smallest are pruned from the current set features. That procedure is recursively repeated on the pruned set until the desired number of features

# Like previous method, we will use 5 features. However, which 5 features will we use ? We will choose them with RFE method.

# In[ ]:


from sklearn.feature_selection import RFE
# Create the RFE object and rank each pixel
clf_rf_3 = RandomForestClassifier()      
rfe = RFE(estimator=clf_rf_3, n_features_to_select=5, step=1)
rfe = rfe.fit(x_train, y_train)


# In[ ]:


print('Chosen best 5 feature by rfe:',x_train.columns[rfe.support_])


# Chosen 5 best features by rfe is **texture_mean, area_mean, concavity_mean, area_se, concavity_worst**. They are exactly similar with previous (selectkBest) method. Therefore we do not need to calculate accuracy again. Shortly, we can say that we make good feature selection with rfe and selectkBest methods. However as you can see there is a problem, okey I except we find best 5 feature with two different method and these features are same but why it is **5**. Maybe if we use best 2 or best 15 feature we will have better accuracy. Therefore lets see how many feature we need to use with rfecv method.

# ## 4) Recursive feature elimination with cross validation and random forest classification
# <http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.RFECV.html>
# Now we will not only **find best features** but we also find **how many features do we need** for best accuracy.

# In[ ]:


from sklearn.feature_selection import RFECV

# The "accuracy" scoring is proportional to the number of correct classifications
clf_rf_4 = RandomForestClassifier() 
rfecv = RFECV(estimator=clf_rf_4, step=1, cv=5,scoring='accuracy')   #5-fold cross-validation
rfecv = rfecv.fit(x_train, y_train)

print('Optimal number of features :', rfecv.n_features_)
print('Best features :', x_train.columns[rfecv.support_])


# Finally, we find best 11 features that are **texture_mean, area_mean, concavity_mean, texture_se, area_se, concavity_se, symmetry_se, smoothness_worst, concavity_worst, symmetry_worst and fractal_dimension_worst** for best classification. Lets look at best accuracy with plot.
# 

# In[ ]:


# Plot number of features VS. cross-validation scores
import matplotlib.pyplot as plt
plt.figure()
plt.xlabel("Number of features selected")
plt.ylabel("Cross validation score of number of selected features")
plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
plt.show()


# Lets look at what we did up to this point. Lets accept that guys this data is very easy to classification. However, our first purpose is actually not finding good accuracy. Our purpose is learning how to make **feature selection and understanding data.** Then last make our last feature selection method.

# ## 5) Tree based feature selection and random forest classification
# <http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html>
# In random forest classification method there is a **feature_importances_** attributes that is the feature importances (the higher, the more important the feature). **!!! To use feature_importance method, in training data there should not be correlated features. Random forest choose randomly at each iteration, therefore sequence of feature importance list can change.**
# 

# In[ ]:


clf_rf_5 = RandomForestClassifier()      
clr_rf_5 = clf_rf_5.fit(x_train,y_train)
importances = clr_rf_5.feature_importances_
std = np.std([tree.feature_importances_ for tree in clf_rf.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(x_train.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

# Plot the feature importances of the forest

plt.figure(1, figsize=(14, 13))
plt.title("Feature importances")
plt.bar(range(x_train.shape[1]), importances[indices],
       color="g", yerr=std[indices], align="center")
plt.xticks(range(x_train.shape[1]), x_train.columns[indices],rotation=90)
plt.xlim([-1, x_train.shape[1]])
plt.show()


# As you can seen in plot above, after 5 best features importance of features decrease. Therefore we can focus these 5 features. As I sad before, I give importance to understand features and find best of them. 

# # Feature Extraction
# <http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html>
# We will use principle component analysis (PCA) for feature extraction. Before PCA, we need to normalize data for better performance of PCA.
#  

# In[ ]:


# split data train 70 % and test 30 %
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
#normalization
x_train_N = (x_train-x_train.mean())/(x_train.max()-x_train.min())
x_test_N = (x_test-x_test.mean())/(x_test.max()-x_test.min())

from sklearn.decomposition import PCA
pca = PCA()
pca.fit(x_train_N)

plt.figure(1, figsize=(14, 13))
plt.clf()
plt.axes([.2, .2, .7, .7])
plt.plot(pca.explained_variance_ratio_, linewidth=2)
plt.axis('tight')
plt.xlabel('n_components')
plt.ylabel('explained_variance_ratio_')


# According to variance ration, 3 component can be chosen.

# # Conclusion
# Shortly, I tried to show importance of feature selection and data visualization. 
# Default data includes 33 feature but after feature selection we drop this number from 33 to 5 with accuracy 95%. In this kernel we just tried basic things, I am sure with these data visualization and feature selection methods, you can easily ecxeed the % 95 accuracy. Maybe you can use other classification methods.
# ### I hope you enjoy in this kernel
# ## If you have any question or advise, I will be apreciate to listen them ...
