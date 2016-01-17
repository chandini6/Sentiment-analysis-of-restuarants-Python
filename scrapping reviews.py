# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 18:22:05 2015


"""

import urllib2, re, time
browser = urllib2.build_opener()
browser.addheaders=[('User-agent', 'Mozilla/5.0')]

#User input for the city to scrape
city=raw_input("Please enter the city and state for example New York NY: ").split()

#Checking for sanity of the city and state name
if len(city)>2:
    City = city[0]+"+"+city[1]
    State= city[2]
else:
    City = city[0] 
    State= city[1]
##########find the number of restaurants and the number of pages to scrape
url = 'http://www.yelp.com/search?cflt=restaurants&find_loc='+City+'%2C+'+State+'%2C+USA#find_desc&start=0'
response = browser.open(url)
html = response.read()
restaurants = re.search('<span class="pagination-results-window">(.*?)</span>',html,re.S)
restMax = int(restaurants.group(1).strip()[16:])
restMaxPages = int(restaurants.group(1).strip()[16:])/10
if restMaxPages%10 > 0:
    restMaxPages = restMaxPages/10 + 1
#print "Total numer of pages: "+str(restMaxPages)
City_1=City.replace('+',' ')
print "Total number of restaurants in the city "+City_1+": "+str(restMax)
noOfRestaurants=int(raw_input("Please enter the number of restaurants that has to be scraped: "))
if noOfRestaurants%10 > 0:
    restPages=noOfRestaurants/10 + 1
else:
    restPages=noOfRestaurants/10
noOfReviews=int(raw_input("Please enter the number of reviews that has to be limited per restaurant: "))

print City_1+" "+State+" "+"Number of Restaurants: "+str(noOfRestaurants)+" "+"Number of Reviews: "+str(noOfReviews)
fileWriter=open('yelp_'+City_1+'_'+State+'.txt','w')
fileWriter.write(City_1+" "+State+" "+"Number of Restaurants: "+str(noOfRestaurants)+" "+"Number of Reviews: "+str(noOfReviews)+"\n")
fileWriter.write("################################################################################"+"\n\n\n\n")
#print restPages   
#########Iterate through each page of the restaurant list page until all the restaurant links are gathered.
restPage=0
restaurantCount=1 
while restPage<restPages:
    url = 'http://www.yelp.com/search?cflt=restaurants&find_loc='+City+'%2C+'+State+'%2C+USA&start='+str(restPage*10)
    #print url  
    response = browser.open(url)
    #time.sleep(10)
    html = response.read()
    #fileWriter.write(html)
    #time.sleep(10)
    #restNames = re.finditer('<a class="biz-name" href="(.*?)"',html)
    restNames = re.finditer('<a class="biz-name" href="(.*)" data-hovercard-id="(.*?)">(.*?)</a>',html)
    #advNames= re.search('Ad </span> <a class="biz-name" href="(.*)"',html,re.S)    
    #print advNames.group(1)  
    for name in restNames: 
        if len(name.group(1)) < 100:        
            if restaurantCount > noOfRestaurants:
                break
            else:
                restaurantName=name.group(1)
                restaurantId=name.group(2)
                restName=name.group(3)
                startTime=time.clock()
                print "Processing Restaurant: "+restName
                revUrl = 'http://www.yelp.com'+restaurantName #Get the number of review pages to scrape dynamically for each restaurant
                revResponse = browser.open(revUrl)
                revHtml = revResponse.read()
                reviews = re.search('<div class="page-of-pages">(.*?)</div>',revHtml,re.S)
                revMaxPages = int(reviews.group(1).strip()[10:])
                if restMaxPages%40 > 0:
                    restMaxPages = restMaxPages/40 + 1
                if noOfReviews%40 > 0:                
                    revPages=noOfReviews/40 + 1
                else:
                    revPages=noOfReviews/40
                #print str(revPages) + " revPages"
                #Get all the reviews for the current restaurant and then go to next restaurant
                #revPage=0            
                #print str(revPage) + " before while" 
                revPage=0 
                reviewCount=1
                while revPage < revPages:
                    #print str(revPage)+" inside while"
                    revUrl = 'http://www.yelp.com'+restaurantName+'?start='+str(revPage*40)+'&sort_by=rating_asc'
                    revResponse = browser.open(revUrl)
                    revHtml = revResponse.read()
                      
                    #reviews=re.finditer('<p itemprop="description" lang="en">(.*?)</p>',revHtml,re.S)
                    reviewData=re.finditer('<div class="review-wrapper">(.*?)<div class="review-footer clearfix">',revHtml,re.S)
                    """if len(reviewData) == 0:
                        print "No reviews for this restaurant"
                    else: """
                    for reviewInfo in reviewData:
                        if reviewCount > noOfReviews:
                            break
                        else:
                            date=re.search('<meta itemprop="datePublished" content="(.*?)"',reviewInfo.group(1),re.S)                        
                            rating=re.search('<meta itemprop="ratingValue" content="(.*?)"',reviewInfo.group(1),re.S)                        
                            review=re.search('<p itemprop="description" lang="en">(.*?)</p>',reviewInfo.group(1),re.S)
            
                            fileWriter.write("Restaurant Id: "+restaurantId+"\n"+"Restaurant Name: "+restName+"\n"+"Date: "+date.group(1)+"\n"+"Rating: "+rating.group(1)+"\n"+"Review: "+review.group(1)+"\n")
                            fileWriter.write("**********************************************************************************"+"\n\n")                      
                            reviewCount=reviewCount+1
                            #print "reviewCount " +str(reviewCount)
                    
                    revPage=revPage + 1
                #print str(revPage)+" increment"
                print " Time Taken: "+str(time.clock()-startTime)
                restaurantCount=restaurantCount+1
                #print "restaurantCount " + str(restaurantCount)
    restPage = restPage+1
fileWriter.close()
