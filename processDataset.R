# load("D:/Proyectos/lak-challenge/data/LAK-Dataset.RData")
# 
# fileConn<-file("D:\\Proyectos\\lak-challenge\\data\\people.csv")
# for (p in people){
#   writeLines(paste(paste(p['name'], p['location'], sep=","), p['affiliation'], sep=",ad"), fileConn)
#   show(p)  
# }
# close(fileConn)

# 
# out_file <- file("D:\\Proyectos\\lak-challenge\\data\\people.csv", open="a")  #creates a file in append mode
# l<- people
# for (i in seq_along(l)){
#   write.table(l[[i]], file=out_file, sep=",", dec=".", quote=FALSE)  #writes the data.frames
# }
# close(out_file)  #close connection to file.csv

peopleFrame <- as.data.frame(people)
write.csv(peopleFrame, "D:\\Proyectos\\lak-challenge\\data\\people.csv")

authorFrame <- as.data.frame(authorship)
write.csv(authorFrame, "D:\\Proyectos\\lak-challenge\\data\\authorship.csv")

papersFrame <- as.data.frame(papers)
write.csv(papersFrame, "D:\\Proyectos\\lak-challenge\\data\\papers.csv")
