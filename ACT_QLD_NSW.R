rm(list=ls())
install.packages('tidyverse')
install.packages("dplyr")
library(tidyverse)
library(lubridate)
library(dplyr)
library(dbplyr)
library('plyr') 
library(readr)

GeneralData <- read_csv("C:/Users/User/Desktop/intern/GeneralData.csv")
GeneralData <- add_column(GeneralData, region=GeneralData[grep("(ACT|CBR|Australian Capital Territory)", GeneralData$`Pickup location`), ])




ACT<-GeneralData[grep("(ACT|CBR|Australian Capital Territory)", GeneralData$`Pickup location`), ]
ACT <- add_column(ACT, region='ACT')

NSW<-GeneralData[grep("NSW", GeneralData$`Pickup location`), ]
NSW <- add_column(NSW, region='NSW')

QLD<-GeneralData[grep("QLD", GeneralData$`Pickup location`), ]
QLD <- add_column(QLD, region='QLD')



GeneralData$week

write.csv(ACT, "C:/Users/User/Desktop/intern/ACT.csv", row.names = TRUE)
write.csv(NSW, "C:/Users/User/Desktop/intern/NSW.csv", row.names = TRUE)
write.csv(QLD, "C:/Users/User/Desktop/intern/QLD.csv", row.names = TRUE)

Location_table <- rbind.fill(ACT,NSW,QLD)
Location_table

write.csv(Location_table, "C:/Users/User/Desktop/intern/Location_table.csv", row.names = TRUE)

location_summarise<-Location_table %>% 
  group_by(week, month, region) %>% 
  dplyr::summarise(num_bookings=n(), total_revenue=sum(`Actual received($)`),
                   promoCosts=sum(`Promo amt($)`), num_customers=n())

location_summarise

