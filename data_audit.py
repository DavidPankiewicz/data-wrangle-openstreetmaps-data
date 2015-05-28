import xml.etree.ElementTree as ET
import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", 
            "Square", "Lane", "Road", "Trail", "Parkway", "Commons"]
                
def audit_street_type(street_types, street_name):
    """ Returns a set of street types that are abbrevaited or unexpected"""
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            if street_type not in street_types.keys():
                street_types[street_type] = set()
            street_types[street_type].add(street_name)
    return    
    
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def split_colon(element_list):
    """ 
    Splits keys with colons into "{main key A: set(subkeys A), main key B:...}"
    Currently, key = "mainkey:subkey". 
    """
    colon_dictionary = {}
    for element in element_list:
        colon_index = element.find(":")
        
        # Split the element by colon into its category and sub category
        
        main_cat, sub_cat = element[:colon_index], element[colon_index+1:]
        if main_cat not in colon_dictionary:
            colon_dictionary[main_cat] = []
        else:
            colon_dictionary[main_cat].append(sub_cat)
    return colon_dictionary

def create_text_file(dictionary, filename):
    """Creates a text file of all keys and a set of their distinct values"""
    key_list = dictionary.keys()
    with open("{0}.txt".format(filename), "w") as f:
        for key in sorted(key_list):
            value = str(list(dictionary[key]))
            f.write("KEY: {0}\tVALUES: {1}\n".format(key, value))
    return

def build_dictionary(element, dictionary, entry_counts, street_types):
    """Updates values of dictionary, counts, and street_types"""
    if element.tag == "tag":
        item_key, item_value =  element.attrib['k'], element.attrib['v']
        
        if is_street_name(element):
            audit_street_type(street_types, element.attrib['v'])

        # Add category to dictionary if doesn't exist
        if item_key not in dictionary:
            dictionary[item_key] = set()
            entry_counts[item_key] = 0
        
        # Add data to set, increase count    
        dictionary[item_key].add(item_value)
        entry_counts[item_key] +=1
    
    return dictionary, entry_counts, street_types            
        
def key_type(element, key_counts, keys_to_inspect):
    """
    For each key, the function adds 1 to the appropriate category
    For non all lowercase keys, it adds their value to the category set
    """
    if element.tag == "tag":
        item =  element.attrib['k']
        
        if lower.search(item) is not None:
            key_counts['lower'] +=1
            
        elif lower_colon.search(item) is not None:
            keys_to_inspect['lower_colon'].add(item)
            key_counts['lower_colon'] += 1
            
        elif problemchars.search(item) is not None:
            keys_to_inspect['problemchars'].add(item)
            key_counts['problemchars'] +=1
             
        else:
            keys_to_inspect['other'].add(item)
            key_counts['other'] +=1
                        
    return key_counts, keys_to_inspect

def print_report(key_counts, keys_to_inspect, entry_counts, street_types):   
    
    print "\n ***** Counts of keys by occurences *****\n"
    print key_counts
    
    print "\n***** Keys to inspect***** \n"
    keys_to_inspect_list = keys_to_inspect.keys()
    for key in keys_to_inspect_list:
        value = str(list(keys_to_inspect[key]))
        print ("TYPE: {0}\tKEY NAMES: {1}".format(key, value))
    
    
    print "\n***** Potential Key Reshapings (from \'lower_colon\')*****"
    print "\n***** current format is \"mainkey:subkey\" as entire key ***** \n"
    # Prints keys comprised of a mainkey and subkey
    # See docstring for split_colon()
    colon_values = split_colon(keys_to_inspect['lower_colon'])         
    colon_keys = colon_values.keys()
    for key in sorted(colon_keys):
        print ("TYPE: {0}\tKEY NAMES: {1}".format(key, colon_values[key]))

    
    entry_keys = entry_counts.keys()    
    num_keys = len(entry_keys)
    num = 0
    print "\n******** {0} Total Keys *******\n".format(num_keys)
    print "***** Count of Appearances for each key *****"
    print "Key #"
    for key in sorted(entry_keys):
        num += 1
        print ("{0}\tCount: {1}\tTag: {2}".format(num, entry_counts[key], key))

        
    print "\n ***** Street Name Audit Results ***** \n"
    street_keys = street_types.keys()
    for key in sorted(street_keys):
        print ("Abbreviation: {0}\t Base Names: {1}".format(key, 
                                                    list(street_types[key])))    
    return


def process_map(filename):
    """
    Takes in an OSM file, and print information that is useful for auditing
    Calls a function that outputs a text file with all keys and a set of 
    their distinct values
    """
    tag_dictionary = {}
    entry_counts= {}
    street_types = {}
    
    keys_to_inspect = {"lower_colon": set(), "problemchars": set(), 
                                                                "other": set()}
    key_counts = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}

    for event, element in ET.iterparse(filename, events=("start",)):
        
        # Update key_counts, keys_to_inspect
        key_counts, keys_to_inspect= key_type(element, key_counts, 
                                                                keys_to_inspect)
        
        #Update tag_dcitionary, entry_counts, street_types
        tag_dictionary, entry_counts, street_types = build_dictionary(element, 
                                    tag_dictionary, entry_counts, street_types)

    # Create text file and print report
    create_text_file(tag_dictionary, "tag_key_values")    
    print_report(key_counts, keys_to_inspect, entry_counts, street_types)    
    return     




file_in = "polk_sf_square.osm"
#file_in = "large-sf-square.osm"

process_map(file_in)

