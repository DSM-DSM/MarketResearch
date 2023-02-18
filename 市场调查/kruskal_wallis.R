library(stringr)
str = 'Q28'
data <- read.table(paste('data/', str, ' K-Wtest.csv', sep = ''))
data = as.data.frame(data)
r = lengths(data)[1]
lst = list()
i = 1
alpha = 0.05
while (i<=r) {
  x = str_split(data[i,],',')
  x = as.array.default(lapply(x[1],as.numeric)) 
  lst[[i]] = x[[1]]
  i = i+1
}
kruskal.test(lst)
test = kruskal.test(lst)
if (test$p.value < alpha){
  print(paste(str,'显著！',sep=''))
  # 画箱线图
  library(readxl)
  data_box = read_excel('data/data.xlsx')
}



