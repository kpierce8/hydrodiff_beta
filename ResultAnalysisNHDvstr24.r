#NHDvsStr24

dbflist1 <- dir("c:/data/hydrodiff/results/NHDvsStr24/")
dbfnum  <- grep(dbflist1,pat="dbf")
dbflist <- dbflist1[dbfnum]

FDlist  <- dbflist[grep(dbflist,pat="FD")]
NHDlist  <- dbflist[grep(dbflist,pat="NHD")]
NWlist  <- dbflist[grep(dbflist,pat="NWIFC")]



datalist<-NHDlist
hdiff_report <- data.frame(matrix(0,length(datalist),7))
names(hdiff_report) <- c("Target", 1,10,40,1080,1095,9999)
for(i in 1:length(datalist)){
print(i)

dbf1 <- read.dbf(paste("c:/data/hydrodiff/results/NHDvsStr24/",datalist[i],sep=""))
props<-tapply(dbf1$Shape_Leng,dbf1$COWBUF,sum)/sum(dbf1$Shape_Leng)


catid <- match(c(1,10,40,1080,1095,9999),names(props))
catid <- catid[!is.na(catid)]
propid <- match(names(props),names(hdiff_report))
propid <- propid[!is.na(propid)]
hdiff_report[i,1]<- datalist[i]
hdiff_report[i,propid] <- props[catid]/sum(props[catid]) 

}
hdiff_report[,-1]<-sig3(hdiff_report[,-1])
FD_report<- hdiff_report
write.csv(FD_report,"c:/data/hydrodiff/results/NHDvsStr24/NHDvsStr24report.csv")

