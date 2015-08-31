# Data Wrangling and Cleaning

Note: This project was completed for a Udacity course. The writeup for Udacity is contained in the PDF above. The information contained in this README is a complete writeup of the project assuming zero familiarity with the supporting Udacity course.

##Introduction and Background:
The objective of this project was to go “end to end” in performing an an analysis.

Specifically:
*	**Sourcing**: pulling raw data from an API
*	**Auditing**: assessing the quality of the data for validity, accuracy, completeness, consistency, and uniformity
*	**Cleaning**: programmatically correcting human errors, unifying formats, etc.
*	**Conversion**: from OSM XML to JSON format
*	**Storage**: inserting the data into MongoDB
*	**Analysis**: aggregating and querying data in MongoDB for insights

## The Dataset and Sourcing
This dataset comes from the OpenStreetMap Foundation (OSM). 

(For more information on OSM, see [Wikipedia](https://en.wikipedia.org/wiki/OpenStreetMap) and the [OSM Wiki](http://wiki.openstreetmap.org/wiki/Main_Page)).

My dataset contains location data on the northeast section of San Francisco (the portion of SF that I and many people are most familiar with). Roughly, the southern boundary is Cesar Chazvez St (the southern edge of the Mission) and the western boundary is the Presidio. Note the area inside the black rectangle on the map below:
![SFmap](http://i.imgur.com/weR1Hi9.png)

To pull the data, I used the [Overpass API Query Form](http://overpass-api.de/query_form.html). The exact query is as follows:  
`(node(37.746299, -122.457169, 37.814679,-122.378548);<;);out meta;`

Note that I originally downloaded this data on May 24th, 2015. With the passage of time the data is subject to change.

The format of the data is in OSM XML. The full dataset is ~ 130 MB, but a 10 MB sample of the data is available as `polk_sf_square.osm`.

## Auditing and Cleaning
To understand the data and have a sense of how I may need to clean it, I wrote functions to generate a text file with a summary of the dataset (see `data_audit.py`). After reviewing the text file, I decided where and how the data should be cleaned. My programmatic cleaning solutions are contained in `clean.py`.

For more information on the specifics of auditing and cleaning, see pages 2 and 3 of the PDF of my writeup.

## Conversion and Storage
For ease of insertion into MongoDB, I converted the format of the data from OSM XML to JSON. See `create_json`.py


## Analysis
Analysis of the data was performed using MongoDb's query aggregation framework. 

Examples of Queries:

How many businesses in SF accept bitcoin?

    {"$match": {"payment": {"$exists":1}}},
    {"$group": {"_id": "$payment.bitcoin", "count": {"$sum":1}}}
yes: 77, no:4


## Limitations and Future Work

