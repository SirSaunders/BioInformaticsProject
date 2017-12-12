##Johnathan Saunders 
## 4/15/2017

## --First Function call starts at the bottom of the page--

# train to find classification from trianing data and testing data
library(plyr)
library(rpart)
library(caret)
library(rpart.plot)
formula = V75~V1+V2+V3+V4+V5+V6+V7+V8+V9+V10+V11+V12+V13+V14+V15+V16+V17+V18+V19+V20+V21+V22+V23+V24+V25+V26+V27+V28+V29+V30+V31+V32+V33+V34+V35+V36+V37+V38+V39+V40+V41+V42+V43+V44+V45+V46+V47+V48+V49+V50+V51+V52+V53+V54+V55+V56+V57+V58+V59+V60+V61+V62+V63+V64+V65+V66+V67+V68+V69+V70+V71+V72+V73+V74
forestTrain<-function(testingData, trainingData){
  print("Taining Random Forest")
  #library(randomForest)
  formula = as.factor(V75)~V1+V2+V3+V4+V5+V6+V7+V8+V9+V10+V11+V12+V13+V14+V15+V16+V17+V18+V19+V20+V21+V22+V23+V24+V25+V26+V27+V28+V29+V30+V31+V32+V33+V34+V35+V36+V37+V38+V39+V40+V41+V42+V43+V44+V45+V46+V47+V48+V49+V50+V51+V52+V53+V54+V55+V56+V57+V58+V59+V60+V61+V62+V63+V64+V65+V66+V67+V68+V69+V70+V71+V72+V73+V74  
  fit <- rpart(formula,
               method="class",
                      data=trainingData,
               control=rpart.control(minsplit=1, minbucket=1, cp=0.001))
  printcp(fit) # display the results 
  plotcp(fit) # visualize cross-validation results 
  summary(fit) # detailed summary of splits
  
  # plot tree 
  plot(fit, uniform=TRUE, 
       main="Classification Tree for Kyphosis")
  text(fit, use.n=TRUE, all=TRUE, cex=.8)
  
  rpart.plot(fit,
             main="titanic survived\n(binary response)")
  
  rpart.plot(fit,
             box.palette="Grays",         # override default GnBu palette
             main="titanic survived\nbox.palette = \"Grays\"")
  
  
 
  library(caret)
  print(varImp(fit))

  
  printcp(fit)
  testingData$result <- predict(fit, testingData)
  print(testingData$results)
  results = count(testingData,c("V75","result"))
  findPercentError(results)
  return(results)
}
nnetTrain <- function(testingData, trainingData){
  print("Training NNET")
  
  dim(trainingData)
  dim(testingData)
  library("neuralnet")
  
  names(trainingData)
  
  nnet<-neuralnet(formula,trainingData, hidden=64, threshold=0.1)
  results<-compute(nnet,testingData[,1:514])
  testingData$result<- sapply(results$net.result, function(b) {
    if (b<=.5){
      return(0)
    }else{
      return(1)
    }})
  results = count(testingData,c("V515","result"))
  findPercentError(results)
  return (results)
}

# finds the percent error given the input is the result matrix from 
findPercentError <- function(results){
  # calculate error
  totalErrors = 0
  totalCorrect = 0
  for(i in 1:nrow(results)){
    if(results[i,1] != results[i,2]){
      totalErrors = totalErrors + results[i,3]
    }
    totalCorrect = totalCorrect + results[i,3]
  }
  
  
  err = totalErrors/totalCorrect
  print(results)
  cat("Percent Error:" , err*100,"\n")
  
  return(err)
}


# train dection  given the directory and filename of the data
trainClassifiers <- function(directory,fileName,testfile,isKFold){
  ##get csv file
  setwd(directory)
  file=read.csv(file=fileName,header=F,stringsAsFactors = TRUE)
  testFile=read.csv(file=testfile,header=F,stringsAsFactors = TRUE)
  
  
  ## Randomize rows of file data
  r1<-file[sample(nrow(file)),1]
  
  folds <- cut(seq(1,nrow(file)),breaks=5,labels=FALSE)
  
  df <- data.frame(folds,r1)
  
  
  if(isKFold){
    for(i in 1:5){
      
      testIndexes <- which(folds==i,arr.ind=TRUE)
      testData <- file[testIndexes, ]
      trainData <- file[-testIndexes, ]
      
     #teachingResult = nnetTrain(testData,trainData)
      teachingResult = forestTrain(testData,trainData)
      cat("\n")
    }
  }else{
    f<-file
    train=sample(1:nrow(f),nrow(f)*(8/10))
    test=-train
    trainData=f
    testData=testFile
    
    #teachingResult = nnetTrain(testData,trainData)
    teachingResult = forestTrain(testData,trainData)
  }
}

### Change Directory name and file name to match file you want
trainClassifiers("~/Desktop/Bioinfo/BioInformaticsProject/Project/","cleaned_without_weird.csv","cleaned.csv",FALSE)
