library(readxl)
library(writexl)
str = 'Q25'
data = read_excel('data/factor_analysis.xlsx',sheet = str)
data = as.data.frame(data)
r = lengths(data)[1]
c = length(data)

library(psych)
#检验
KMO(data)
#Bartlett检验
cor<-cor(data)
cortest.bartlett(cor,n=r)

#使用最大方差旋转法,计算因子得分(缺省时为回归法)
fit_var=principal(data, nfactors=3, rotate="varimax", scores=TRUE)  
fit_var$loadings  #旋转后的因子载荷矩阵等

lam<-fit_var$values#特征值
#方差解释
cumlam<-cumsum(lam)/sum(lam)
VE<-data.frame(lam,lam/sum(lam),cumlam)
colnames(VE)<-c("特征值","比例","累计比例")
var_explain = round(VE,3)
#碎石图
plot(lam,type="o",xlab="因子序号",ylab="特征值")

#因子载荷
load<-as.matrix.data.frame(fit_var$loadings)
rownames(load)<-colnames(data)
factor = round(load, 3)  #旋转矩阵
factor = as.data.frame(factor)
scores=round(fit_var$scores, 3)  #因子得分

#保存数据
write_xlsx(var_explain,paste('data/',str,'方差解释(已旋转).xlsx',sep=''))
write_xlsx(factor,paste('data/',str,'旋转后的因子荷载矩阵.xlsx',sep=''))



