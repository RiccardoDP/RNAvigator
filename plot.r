## GPLv3 Delli Ponti 2022

args <- commandArgs()
file<-as.character(args[5])
length<-as.integer(args[6])

png("output/plot.png",width = 12, height = 5, units = 'in',res=300)
data<-read.table(file)
library(ggplot2)
ggplot(data,aes(as.numeric(data$V2),1))+geom_col(aes(fill=data$V1 ))+theme_classic()+theme(axis.text.x=element_text(size=12),axis.title.x=element_blank(),axis.title.y=element_blank(),axis.ticks.y=element_blank(),axis.text.y=element_blank(),legend.position = "none")+scale_fill_manual(values=c("red", "blue","green"))+facet_wrap(~data$V1, scales="free",ncol=1)+coord_cartesian(xlim=c(0,length))
dev.off()
