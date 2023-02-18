#***********************************************************
#*******《多元统计分析》(何晓群)（第5版）R代码 ***********
#************************ 朱春华 ***************************
###因子分析------------------------------------------------------
###教材例6-1
#R包stats的函数factanal可以实现极大似然方法因子载荷求解，psych包的principal函数使用主成分方法计算因子载荷。
library(foreign)
rm(list=ls())
eg6.1 <- read.spss("data/例5-3.sav", head=TRUE, fileEncoding="utf-8")  ###读取文本格式数据文件
eg6.1<-data.frame(eg6.1)
dat61 <-eg6.1[,-1]
rownames(dat61) <- eg6.1[,1] 
dat61<-scale(dat61,center=TRUE,scale=TRUE)###数据标准化
p<-dim(dat61)###数据维数
p
library(psych)
###主成分法因子分析，从协方差矩阵出发（即covar=TRUE，这里数据已标准化，其实就是相关矩阵）
###选取2个因子，残差矩阵，未旋转
fit61<-principal(dat61,nfactors=2,rotate="none",covar=TRUE)
summary(fit61)
#特征值
lam<-fit61$values
lam
cumlam<-cumsum(lam)/sum(lam)
cumlam
VE<-data.frame(lam,lam/sum(lam),cumlam)
colnames(VE)<-c("特征值","比例","累计比例")
round(VE,3)

#因子载荷
#load是因子载荷矩阵
load<-as.matrix.data.frame(fit61$loadings)
rownames(load)<-colnames(dat61)
round(load,3)

#因子得分
#因子得分矩阵就是提取的因子被原始变量表示的系数矩阵
#score=(a_ij)n*p
#n是观测变量的个数n,p为提取因子的个数
#用这个系数矩阵乘原始数据就得到了各个因子的实际得分（降维后的数据）
#varci是特征值向量
varci<-fit61$Vaccounted[1,]
varci
varci_mat<-matrix(varci,p[2],2,byrow=TRUE)
varci_mat
score_mat<-load/varci_mat
score_mat
rownames(score_mat)<-colnames(dat61)
round(score_mat,3)

#进行因子分析前,我们往往先要了解变量之间的相关性,以判断是否适合对数据做因子分析
sigm<-cov(dat61)
round(sigm,3)
#检验
KMO(dat61)
#Bartlett检验
r<-cor(dat61)
cortest.bartlett(r,n=31)


#另外,得到初始载荷矩阵与公共因子后,为了解释方便,往往需要对因子进行旋转。我们首先进行方差最大正交旋转。
fit61_var<-principal(dat61,nfactors=2,rotate="varimax",covar=TRUE)###主成分法因子分析，从协方差矩阵出发（即covar=TRUE，这里数据已标准化，其实就是相关矩阵），选取2个因子，残差矩阵，未旋转
#因子载荷
load_var<-as.matrix.data.frame(fit61_var$loadings)
rownames(load_var)<-colnames(dat61)
round(load_var,3)
#旋转矩阵
fit61_var$rot.mat
#因子得分
xx<-t(dat61)%*%dat61
xy_var<-t(dat61)%*%fit61_var$scores
score_mat_var<-solve(xx)%*%xy_var

rownames(score_mat_var)<-colnames(dat61)
round(score_mat_var,digits=3)

#有时为了使公共因子的实际意义更容易解释,往往需要放弃公共因子之间互不相关的约束而进行斜交旋转,最常用的斜交旋转方法为Promax方法。
fit61_pro<-principal(dat61,nfactors=2,rotate='promax',covar=TRUE)
#Pattern Matrix
load_pro<-as.matrix.data.frame(fit61_pro$loadings)
round(load_pro,3)
#Structure Matrix
fit61_pro$Structure
#因子得分
score_mat_pro<-fit61_pro$scores
load_pro%*%cor(score_mat_pro)

summary(score_mat_pro)
apply(score_mat_pro,2,std)
plot(fit61_pro$score,pch="+",xlab="第一因子",ylab="第二因子")
abline(h=0,lty=2)
abline(v=0,lty=2)
text(fit61_pro$scores,eg6.1[,1],adj=-0.05)


###----------------------------------------------------------------------
#例6-2
library(foreign)
eg62<-read.spss("data/例6-2.sav")
eg62<-data.frame(eg62)
eg62<-eg62[1:30,]#直接读取，数据中出现无效行
dat62<-eg62[1:30,-1]
rownames(dat62)<-eg62[,1]
dat62<-scale(dat62,center=TRUE,scale=TRUE)

library(psych)
#KMO检验
KMO(dat62)
#Bartlett检验
r<-cor(dat62)
cortest.bartlett(r,n=30)


#(一)主成分法#
fit62=principal(dat62, nfactors=3, residuals=TRUE, rotate="none", covar=FALSE)  #主成分法因子分析，从相关矩阵出发（即covar=FALSE，为缺省选项），选取2个因子，残差矩阵，未旋转
lam62<-fit62$values#特征值
#方差解释
cumlam62<-cumsum(lam62)/sum(lam62)
VE62<-data.frame(lam62,lam62/sum(lam62),cumlam62)
colnames(VE62)<-c("特征值","比例","累计比例")
round(VE62,3)
#碎石图
plot(lam62,type="o",xlab="因子序号",ylab="特征值")

#或者调用名命令确定因子个数
fit62$loadings 

fit62_var=principal(dat62, nfactors=3, rotate="varimax", scores=TRUE)  #使用最大方差旋转法，计算因子得分（缺省时为回归法）
fit62_var$loadings  #旋转后的因子载荷矩阵等
#因子载荷
load62<-as.matrix.data.frame(fit62_var$loadings)
rownames(load62)<-colnames(dat62)
round(load62, 3)  #旋转矩阵

factor.plot(fit62_var, xlim=c(0, 1.0), ylim=c(0, 1.0))  #因子载荷图
round(fit62_var$weights, 3)  #标准化得分系数
scores=round(fit62_var$scores, 3)  #因子得分
scores[order(scores[, 1]), ]  #按因子1得分排序
scores[order(scores[, 2]), ]  #按因子2得分排序
scores[order(scores[, 3]), ]  #按因子3得分排序
#对前两个因子得分作图
#plot(scores[,1], scores[,2], xlab=colnames(scores)[1], ylab=colnames(scores)[2], xlim=c(-1.3, 3.9), ylim=c(-1.8, 3.8))
#text(scores[,1], scores[,2], row.names(dat62), pos=4, cex=0.7)
#abline(v=0, h=0, lty=3)


#拓展~~~
#psych::fa():使用MinRes(最小残差)和Exploratory Factor analysis（主因子、加权最小二乘或最大似然）进行探索性因子分析

#(2)主因子法#
#未旋转
fapa=fa(dat62, nfactors=3, residuals=TRUE, rotate="none", fm="pa", covar=FALSE, SMC=TRUE)  #主因子法因子分析（fm="pa"），从相关矩阵出发（covar=FALSE，为缺省选项），对每个原始变量取初始共性方差为该变量与其余所有变量的样本复相关系数的平方（SMC=TRUE，为缺省选项）
fapa$loadings  #因子载荷矩阵，列元素的平方和、因子所解释的总方差的比例及累计比例
round(fapa$communality, 3)  #共性方差
residual=fapa$residual-diag(diag(fapa$residual))  #残差矩阵
round(residual, 3)

fapa.varimax=fa(dat62, nfactors=2, rotate="varimax", fm="pa", scores="regression")  #"regression"是scores的缺省选项，即按回归法计算因子得分
round(fapa.varimax$rot.mat, 3)  #旋转矩阵
fapa.varimax$loadings  #旋转后的因子载荷矩阵，列元素的平方和、因子所解释的总方差的比例及累计比例
factor.plot(fapa.varimax, xlim=c(0, 1.0), ylim=c(0, 1.0))  #因子载荷图
round(fapa.varimax$weights, 3)  #标准化得分系数
scores=round(fapa.varimax$scores, 3)  #因子得分
scores[order(scores[, 1]), ]  #按因子1得分排序
scores[order(scores[, 2]), ]  #按因子2得分排序
scores[order(scores[, 3]), ]  #按因子3得分排序
#对前两个因子得分作图
#plot(scores[,1], scores[,2], xlab=colnames(scores)[1], ylab=colnames(scores)[2], xlim=c(-1.3, 3.9), ylim=c(-1.8, 3.8))
#text(scores[,1], scores[,2], row.names(dat62), pos=4, cex=0.7)
#abline(v=0, h=0, lty=3)

#(3)极大似然法#
faml=fa(dat62, nfactors=3, residuals=TRUE, rotate="none", fm="ml")  #极大似然法因子分析（fm="ml"），选取2个因子，残差矩阵，未旋转
faml$loadings  #因子载荷矩阵，列元素的平方和、因子所解释的总方差的比例及累计比例
round(faml$communality, 3)  #共性方差
residual=faml$residual-diag(diag(faml$residual))  #残差矩阵
round(residual, 3)
faml.varimax=fa(dat62, nfactors=3, rotate="varimax", fm="ml", scores="regression")  #极大似然法因子分析，选取2个因子，使用最大方差旋转法，计算因子得分（缺省时为回归法）
round(faml.varimax$rot.mat, 3)
faml.varimax$loadings  #旋转后的因子载荷矩阵，列元素的平方和、因子所解释的总方差的比例及累计比例
factor.plot(faml.varimax, xlim=c(0, 1.0), ylim=c(0, 1.0))  #因子载荷图
round(faml.varimax$weights, 3)  #标准化得分系数
scores=round(faml.varimax$scores, 3)  #因子得分
scores[order(scores[, 1]), ]  #按因子1得分排序
scores[order(scores[, 2]), ]  #按因子2得分排序
scores[order(scores[, 3]), ]  #按因子2得分排序
plot(scores[,1], scores[,2], xlab=colnames(scores)[1], ylab=colnames(scores)[2], xlim=c(-1.3, 3.9), ylim=c(-1.8, 3.8))
text(scores[,1], scores[,2], row.names(dat62), pos=4, cex=0.7)
abline(v=0, h=0, lty=3)