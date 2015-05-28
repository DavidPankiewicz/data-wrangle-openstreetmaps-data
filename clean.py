""" 
Imported and called by create_json.py
Cleans predefined categories of data
"""

import re

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_mapping= { 
            "St": "Street",
            "St.": "Street",
            "Rd.": "Road",
            "Ave": "Avenue",
            "Rd" : "Road",
            "Ave.": "Avenue",
            "Abenue": "Avenue",
            "Blvd": "Boulevard",
            "Pl": "Place"
            }

base_name_mapping = {
            "California": "California Street",
            "Columbus": "Columbus Avenue",
            "Van Ness": "Van Ness Avenue",
            "Pine": "Pine Street",
            "Polk": "Polk Street",
            "Post": "Post Street",
            "Powell":"Powell Street",
}

street_abbreviations = street_mapping.keys()
base_streetnames = base_name_mapping.keys()

def clean_amenity(amenity):
    # replace underscores with spaces
    if "_" in amenity:
        amenity = amenity.replace("_", " ")
    return amenity

def clean_routes(routes):
    # Split data on semicolons and return as list
    if ";" in routes:
        routes = routes.split(";")
        return routes
    return [routes]

def clean_streetname(street):  
    # Check if street is a major street name 
    # without any street type
    if street in base_streetnames:
        return base_name_mapping[street]
    
    # Scrape the street type with a regex
    street_type_scraped = street_type_re.search(street)
    if street_type_scraped:
        street_type = street_type_scraped.group()
        
        # Check if scraped type matches a common abbreviation
        # if so, expand to full name
        if street_type in street_abbreviations:
            index = street.find(street_type)
            base_name = street[:index]
            return base_name + street_mapping[street_type]      
    return street

def clean_cuisine(cuisine):
    # replace underscores with spaces
    if "_" in cuisine:
        cuisine = cuisine.replace("_", " ")
    return cuisine


def clean_data(category, data):    
    if category == "amenity":
        cleaned_amenity = clean_amenity(data)
        return cleaned_amenity
    
    if category == "city":
        return "San Francisco"
    
    if category == "route_ref":
        cleaned_routes = clean_routes(data)
        return cleaned_routes
        
    if category == "street":
        cleaned_street = clean_streetname(data)
        return cleaned_street
     
    if category == "cuisine":
        cleaned_cuisine = clean_cuisine(data)
        return cleaned_cuisine 
    
    # If inputs do not match a predefined category                         
    print "Data was not cleaned:\t{0}:{1}".format(category, data)
    return data


