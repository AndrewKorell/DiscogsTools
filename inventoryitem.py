import collections
from pprint import pprint



def get_artist_names(item) :
    artist_names = ""
    for y in range(len(item.release.artists)) :
        if y + 1 >= len(item.release.artists) :
            artist_names += item.release.artists[y].name
        else :
            artist_names += item.release.artists[y].name + ', '

    return artist_names 

def clean_format(format_set) :
    '''
        takes the format set and cleans up general redundancies for human display 

        redundancies: 
            LP + Album
            Limited Edition + Deluxe Edition
    '''
    #TODO: requirements and implementation required 

    return format_set

def get_label(release_labels) :
    '''
        labels is a list of objects

        In this case human readable is label_name

        release_formats = inventory_listening.release.labels
    '''
    label_set = set()

    for label in release_labels :
        label_set.add(label.name)

    return label_set

def get_format(release_formats):
    '''
        takes the formats object from an inventory listening and
        creates a set

        format is a list of dictionaries containing various chunks of infomration
        including LP, Album, Deluxe Edition, Gatefold, vinyl colour
        Not going to try to pick an ultimate value so I will make it one of each

        release_formats = inventory_listing.release.formats
    '''
    format_set = set()
    for format in release_formats :
        format_set.add(format['name'])
        for description in format['descriptions'] :
            format_set.add(description)
    return format_set

def get_record(item):
    record = collections.namedtuple('record',
    [
        "id",
        "release_id",
        "release_url",
        "artist", 
        "title", 
        "label",
        "year", 
        "price",
        "format",
        "country", 
        "disc_cond", 
        "cover_cond", 
        "comment",  
        "price_suggestions",
        "catalog_number",
        "description"
    ])

    return record(
                    id=item.id, 
                    release_id=item.release.id, 
                    release_url=item.release.url,
                    artist=get_artist_names(item),
                    title=item.release.title,
                    format=get_format(item.release.formats),
                    label = get_label(item.release.labels),
                    catalog_number= item.release.catalog_number,
                    description=item.release.description,
                    year=item.release.year,
                    price=item.price,
                    country=item.release.country,
                    disc_cond=item.condition,
                    cover_cond=item.sleeve_condition,
                    comment=item.comments,
                    price_suggestions="",      
                )
