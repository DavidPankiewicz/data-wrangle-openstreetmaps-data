# Data Wrangling and Cleaning

Note: This project was completed for a Udacity course. The writeup for Udacity is contained in the PDF in the folder above. The information contained in this README is a complete writeup of the project and its objectives requiring zero k

##Introduction and Background:
The objective of this project was to go “end to end” in performing an analysis with a dataset. 

Specifically:
*	**Sourcing**: pulling raw data from an API
*	**Auditing**: assessing the quality of the data for validity, accuracy, completeness, consistency, and uniformity
*	**Cleaning**: programmatically correcting human errors, unifying formats, etc.
*	**Conversion**: from OSM XML to JSON format
*	**Storage**: inserting the data into MongoDB
*	**Analysis**: aggregating and querying data in MongoDB for insights

## 1. The Dataset and Sourcing
This dataset comes from the OpenStreetMap Foundation (OSM). 

(For more information on OSM, see [Wikipedia](https://en.wikipedia.org/wiki/OpenStreetMap) and the [OSM Wiki](http://wiki.openstreetmap.org/wiki/Main_Page)).

My dataset contains location data on the northeast section of San Francisco (the portion of SF that I and many people are most familiar with). Note the area inside the black rectangle on the map below:

![SFmap](http://i.imgur.com/weR1Hi9.png)

Roughly, the southern boundary is Cesar Chazvez St (the southern edge of the Mission) and the western boundary is the Presidio. 

To pull the data, I used the Overpass API. 

Note that I originally downloaded this data on May 24th, 2015. Given the open source nature of the data, current data will almost surely not be perfectly identical. 

