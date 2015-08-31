# Data Wrangling and Cleaning

Note: This project was completed for a Udacity course. The writeup for Udacity is contained in the PDF in the folder above. The information contained in this README is a complete writeup of the project and its objectives requiring zero k

##Introduction and Background:
The objective of this project was to go “end to end” in performing an analysis with a dataset. 

Specifically:
*	**Sourcing**: pulling raw data from an API
*	**Auditing**: assessing the quality of the data for validity, accuracy, completeness, consistency, and uniformity
*	**Cleaning**: programmatically correcting human errors, unifying formats, etc.
*	**Conversion**: converting from OSM XML to JSON format
*	**Storage**: inserting the data into MongoDB
*	**Analysis**: querying and aggregating data in MongoDB for numerical insights

## 1. The Dataset and Sourcing
This dataset comes from the OpenStreetMap Foundation (OSM). (For more information on OSM, see [Wikipedia](https://en.wikipedia.org/wiki/OpenStreetMap) and the [OSM Wiki](http://wiki.openstreetmap.org/wiki/Main_Page)).

My dataset contains information on the northeast portion of San Francisco that I and many people are most familiar with. To see the area on a map, note the black rectangle in [this image](http://imgur.com/weR1Hi9). Neighborhoods included are North of Cesar Chazvez St (the southern edge of the Mission) and east of the Presidio. 

