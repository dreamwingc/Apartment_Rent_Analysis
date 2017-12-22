## Capstone Project for Web Crawler and Machine Learning
Chen, 12/04/2017

### Overview

In this project, a web crawler based on Python and Scrapy is implemented to crawl apartment rental information from craigslist website. Useful information, such as rental price, floor plan, locations, etc., would be crawled from the webpages. The crawled data are saved in MySQL, and the inverted index are built in Memcached for later process. Also, a simple webpage is created to visualize the crawled data and return valuable information to be analyzed. Finally, a discussion is performed by visualization, as well as the predictions obtained from machine learning models.

### Main Use Case

In the modern society, apartment rental is a general requirement for people, especially in cities with large population. However, the cost to rent apartment in this kind of area might be much higher than other places. In order to find a best fit apartment, many conditions need to be considered. For instance, the security of one area is extremely important for most people. In other hand, the price and traffic information would be main factors whether to choose the apartment or not. Therefore, people spend much time to search the desired place to live in. Comparing with the manually search, the ongoing project could provide a much easier way to analyze the apartment rental in the entire area. This project evaluates the situations include all the factors which might be considered for apartment rental and returns a final result/curve to assist people to make decisions.

### High Level Design Diagram
As mentioned in the Overview section, the capstone project is constructed by a web crawler and machine learning models. Figure 1 illustrates the workflow of this capstone project.

<center>![alt text](Apartment_Rent_Analysis/image/Webcrawler.png)</center>
<center>Figure 1 Workflow of the capstone project for web crawler and machine learning</center>

<br>
Firstly, the right page of apartment rental from craigslist need to be selected. The search area, such as San Francisco Bay Area which applied in this project, is set to the right place. The url of the proper webpage is copied for later use. Information which need to be crawled could be find via the frontend webpage by inspection. Secondly, the web crawler could crawl the required information from the saved url, then, the crawled data would be sent to MySQL to build forward index. Memcached accesses the data in MySQL to build the inverted index for searching demand. Furthermore, the machine learning models would work with the crawled data obtained from MySQL to analyze and return a learning curve. Finally, users could make the final decision based on the results calculated by the machine learning models.

### Detailed Design
In this section, the detailed design is explained based on the workflow in Figure 1. Useful information which crawled from craigslist is discussed here. For web crawler, the crawled data storage is introduced. Moreover, the structure of the table in MySQL is illustrate. Last but not least, the applied machine learning model is analyzed as well.

#### Useful Information
Before starting the crawl task, some useful information needs to be recorded and applied to the web crawler, such as the url of target webpage, the prefix/category of the crawled data, other urls which might help the data collection. In this project, the url of apartment rental of craigslist is used to be the target page. From the target page, there are different links to the detailed apartment information. The monthly rent, floor plan and location details are in each apartment webpage, and these details could be crawled based on the prefix of the frontend inspections. After all the useful information being located, the web crawler would crawl data based on the provided information. Figure 2 and Figure 3 show examples of useful information obtained from craigslist.

<center>![alt text](image\craigslistURL.png)</center>
<center>Figure 2 Main webpage for data crawling</center>

<br>

<center>![alt text](image\usefulInfo.png)</center>
<center>Figure 3 Examples of useful information obtained from frontend web details</center>

#### Web Crawler
Scrapy which is a powerful framework for web crawling performs the crawl task of this project. It helps build an impactful web crawler with less code and simpler structure. Figure 4 illustrates an example structure of a simple crawler created by Scrapy.

<center>![alt text](image\scrapy.png)</center>
<center>Figure 4 An example structure of a simple crawler created by Scrapy obtained from scrapy.org</center>

<br>

 Web crawler would be defined under the spiders folder, and the pipelines.py would include the settings to save the crawled data, so that the connections with MySQL could be set up here. With the useful information discussed above, the price, the floor plan and the location details could be crawled, then, the crawled details would be sent to MySQL. In other words, a forward indexer cooperates with MySQL to save the crawled information in the relational database. Then, a inverted indexer is built via Memcached to fulfill the searching requests based on the price ranges, locations and floor plans. Also, a visualization webpage would be returned after the searching requests.

#### Database Information
To store data to MySQL, a schema with related tables is required to be created. In this project, a schema called "web_crawler" is created, as well as the related table named as "web_crawler". In table "web_crawler", several columns are created to store the crawled data, such as the column "price", "floor_plan", "location", etc. These columns could be extracted by the inverted indexer and the machine learning model. Figure 5 exhibits a screen shot from MySQL workbench.

<center>![alt text](image\MySQL.png)</center>
<center>Figure 5 A screen shot from MySQL workbench</center>

#### Machine Learning Model
Machine learning is widely used for prediction in recent years. It is applied to this project to analyze and predict apartment rental price in a given area, so that a regression model, such as linear regression, would achieve the goal. Figure 6 represents a trained model mapping for linear regression. For training part, the rental price is the training label. The location, floor plan and other useful information are the features of each observation. The optimized model would be tested, evaluated and obtained by the crawled data.

<center>![alt text](image\linearRegression.png)</center>
<center>Figure 5 A trained model mapping for linear regression obtained from https://commons.wikimedia.org/wiki/File:Linear_regression.svg</center>

<br>

If all the sub-designs work correctly, the capstone system should return a webpage with the suggested rental price and apartment details obtained from the machine learning model and the data saved in Memcached when user asks requests with the desired location, floor plan and other useful information.

### Future Work
In the future work, this capstone project could be applied to analyze the house for sale, used car market, stock exchange, etc. The required information in this project need to be modified to satisfy distinct situations. Some fine-tuning strategies should be assigned to the trained machine learning model to fit the new crawled data.
