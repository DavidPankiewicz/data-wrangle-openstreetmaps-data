import xml.etree.ElementTree as ET
import re
import codecs
import json
import clean

# Regular expressions 
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

created = [ "version", "changeset", "timestamp", "user", "uid"]
needs_cleaning = ["city", "route_ref", "street", "amenity"]
        
def shape_element(element):
    if element.tag != "node" and element.tag != "way":
        return None             
    
    # Create an empty JSON object
    # Note: node is used as a generic name
    # here for "nodes" and "ways"
    node = {}
    node['created'] = {}
    node['type'] = element.tag
    
    # Create an empty list for GPS position
    if node['type'] == "node":
        node['pos'] = []
    
    # Insert all attributes of the element
    key_list = element.keys()    
    for key in key_list:
        
        # Inserted "created" values into a nested dictionary
        if key in created:
            node['created'][key] = element.attrib[key]
       
        # Insert "pos" coordinates ordered into a list     
        elif key == 'lat' or key == 'lon':
            node['pos'] = [float(element.attrib['lat']), 
                            float(element.attrib['lon'])]
                            
        # Create a key, value entry for all other attributes
        else:
            node[key] = element.attrib[key]
    
    # Loop through all children of the element and include their attributes
    for child in element:
        if child.tag == 'tag':
            
            tag_key, tag_value = child.attrib['k'], child.attrib['v']

            # If the tag is all lowercase, clean the data if needed,
            # then insert it                                                            
            if lower.search(tag_key) is not None:
                if tag_key in needs_cleaning:
                    tag_value = clean.clean_data(tag_key, tag_value)
                node[tag_key] = tag_value

            # If there is a colon in the key, split it and created
            # a nested dictionary as the entry
            elif lower_colon.search(tag_key) is not None:
                colon_location = tag_key.find(":")
                main_key, nested_key = tag_key[:colon_location], tag_key[colon_location+1:]
                
                # name:(language) contains foreign characters
                # and is only present on a few entries. These are skipped.
                if main_key == "name":
                    # Continue to next child in element
                    continue
                    
                # Categories like building vs. building:levels conflict
                # because "building" contains a string and 
                #"building" with a colon wants to contains a dictionary.         
                # To preserve all data, "building" is converted to a 
                # nested dictioinary and the old data is stored under
                # ['building']['type']
                if main_key in node.keys() and type(node[main_key])==type("string"):
                    temp = node[main_key]
                    node[main_key]= {}
                    node[main_key]["type"] = temp
                
                
                if main_key not in node.keys():
                    node[main_key] = {}
                
                if nested_key in needs_cleaning:
                    tag_value = clean.clean_data(nested_key, tag_value)
                
                node[main_key][nested_key] = tag_value                                        
                
        # Add node references in list format
        if child.tag == 'nd':
            if "node_refs" not in node:
                node["node_refs"] = []
            node["node_refs"].append(child.attrib['ref'])

    return node


def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for event, element in ET.iterparse(file_in, events=("start",)):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

#file_in = "large-sf-square.osm"
file_in = "polk_sf_square.osm"    

process_map(file_in)

