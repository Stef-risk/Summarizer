# Fríst摘要器



​	Fríst摘要器采用抽取式摘要的方法（Extractive Summarization）,选取整篇文章中保留了最重要的要
点的词语子集来对文章进行摘要。整体的实现思想即为对一个句子的重要部分进行加权，并使用生成的
权重来形成总结，即对词语加权后排序，最后选择排名最前的N个句子，作为整篇文章的摘要。

​	Fríst摘要器整体使用了无监督学习的方法，输入的数据没有标签，在使用时不需要提前建立并训练模
型。为了计算词语的权重，本摘要器中使用了余弦相似度来判断两个句子的相似度来构造一个相似度矩
阵，即将句子表示为向量束，并计算每两个向量夹角的余弦值。在构造完相似度矩阵之后，将相似度矩
阵作为邻接矩阵生成一个带权的图，之后使用pagerank算法，根据无向图中每个节点的入边的个数来计
算这个节点的权重，该算法最初被设计为对网页进行排序。之后依据pagerank的排序结果，对存储着文
本中每个句子的列表进行排序。最后只需要输出用户要求摘取的前n个权重最高的句子作为整篇文章的摘要即可。



## 使用说明书

为了制作适合普通用户使用的程序，在完成程序内核的编写工作之后，使用pySimpleGui软件包
为程序制作了图形用户界面。并对做好的程序使用pyinstaller进行打包。

要使用该摘要器，用户可将压缩包内的exe文件以及cn_stopwords.txt解压到同一个文件夹中，之后
可以直接点击exe文件进行使用。

用户打开该名为Frist的程序后，首先进入选择文件和指定摘要句子数量的界面：

选好后点击"submit"提交，之后程序会对用户选项进行确认：

确认后进入分析运行阶段：

摘要完成后弹出提示窗口，在此窗口下点击‘“查看”即可在新弹窗中查看摘要内容：

本程序一次打开可以对一个文本进行摘要，查看完摘要之后，将小弹窗关闭即可退出程序。