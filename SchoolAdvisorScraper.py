import requests
from bs4 import BeautifulSoup
from WebsitesLink import urls
import csv
import numpy as np
import pandas as pd
from pandas import DataFrame
from MapsReviews import main

headers ={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136'
}


Links_Page = requests.get('https://www.ischooladvisor.com/city/Cairo?page=1#results',headers=headers)
Page_src = Links_Page.content
soap = BeautifulSoup(Page_src, "lxml")


Links = []
SchoolNames = []
CommentsDIV =  soap.find("section", {'class': 'mainContentSection packagesSection'})
Schools = CommentsDIV.find_all("div", {'class': 'row school-container'})


for school in Schools:
    SchoolName = school.find("h3").find("a").attrs['title']
    SchoolLink = school.find("h3").find("a").attrs['href']
    CommentsCountDiv = school.find("div", {'class': 'rating-container'})
    CommentsBeforeSplit = CommentsCountDiv.find("b").text
    CommentsArr = CommentsBeforeSplit.split(' ')
    CommentsCount = int(CommentsArr[0])

    if(CommentsCount > 4):

        Links.append(SchoolLink)
        SchoolNames.append(SchoolName)

    MapsComments,MapsAuthors = main(SchoolName)




CommentsStrArr = []
AuthorsStrArr = []

i = 0
for link in Links:

    CommentsStr = ""
    AuthorsStr = ""
    page = requests.get('https://www.ischooladvisor.com'+link, headers=headers)
    src = page.content
    soap2 = BeautifulSoup(src, "lxml")
    CommentsDIV2 = soap2.find("div", {'class': 'row margin-bottom-20'})
    Comments = soap2.find_all("div", {'class': 'review-panel white-info-box'})
    School_Name = SchoolNames[i]
    i+=1

    for com in Comments:
        CommentAuthor = com.find("a").text
        Ps = com.find_all("p")
        Comment = Ps[1].text

        CommentsStr = CommentsStr+Comment+"#"
        AuthorsStr = AuthorsStr+CommentAuthor+"#"


    for com in MapsComments:
        CommentsStr = CommentsStr+com+"#"
    for auth in MapsAuthors:
        AuthorsStr = AuthorsStr+auth+"#"
        


    CommentsStrArr.append(CommentsStr)
    AuthorsStrArr.append(AuthorsStr)




df2 = DataFrame({'School_Name':SchoolNames, 'Comments': CommentsStrArr, 'Authors':AuthorsStrArr})

df2.to_excel('GoogleMaps_SchoolAdvisor_Reviews.xlsx', sheet_name='sheet1', index=False)









