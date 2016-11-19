import sphere_coord_scraper
import pprint
from pymongo import MongoClient

client = MongoClient('mongodb://backend:password@ds155727.mlab.com:55727/campus-360')
db = client['campus-360']
schools_coll = db['schools']
spheres_coll = db['spheres']

pp = pprint.PrettyPrinter(indent=4)


def go():
    schools = ["el camino college", "cal poly pomona"]

    for school_name in schools:
        store_in_mongo(school_name)


def store_in_mongo(school_name):
    school_id = store_school_in_mongo(school_name)
    schools_photo_spheres = sphere_coord_scraper.scrape(school_name)
    store_spheres_in_mongo(school_name, school_id, schools_photo_spheres)


def store_spheres_in_mongo(school_name, school_id, schools_photo_spheres):
    for sphere in schools_photo_spheres:
        sphere['school_id'] = school_id
        sphere['school_name'] = school_name
        sphere['views'] = 0

    pp.pprint(schools_photo_spheres)

    spheres_coll.insert_many(schools_photo_spheres)


def store_school_in_mongo(school_name):
    school_doc = dict()
    school_doc['name'] = school_name

    _id = schools_coll.insert(school_doc)

    return _id


go()
