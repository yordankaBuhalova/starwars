import requests as req
import petl as etl
import uuid
from multiprocessing import Process, Manager
from datetime import date
from StarWarsApp.models import DatasetCSV
from starwars.settings import MEDIA_ROOT, SWAPI_URL
import os
import logging

logger = logging.getLogger(__name__)


def collect():
    people = collect_data('people')
    planets = collect_data('planets')

    transform_data(people, planets)
    # queryset of files
    files = DatasetCSV.objects.all()

    return files


def collect_data(dataset):
    '''
        Collect data
        Args: "people" or "planets"
    '''
    manager = Manager()
    # elements count
    el_count = manager.Value(int,0)
    data = manager.list()
    # set data url
    data_url = "{}/{}/".format(SWAPI_URL, dataset)
    # fetch data
    fetch(data_url, el_count, data)
    # page counter
    total_pages = count_total_pages(el_count, len(data))
    # set url for one page
    data_url = data_url + '?page='

    for page_num in range(2, total_pages + 1):
        # fetch the data from all pages
        r = Process(target=fetch, args=(data_url + str(page_num), el_count, data))
        r.start()
        r.join()

    return data


def fetch(url, el_count, data_result):
    '''
    Fetch the Information from SWAPI
    Args:
        url, el_count, data_result
    '''
    r = req.get(url, verify=False)
    logger.info(url)

    if r.status_code == 200:
        res = r.json()
        if '?page=' not in url:
            el_count.value= res["count"]

        data = res["results"]
        for i in data:
            data_result.append(i)
    else:
        logger.error(r)


def count_total_pages(element_count, count_per_page):
    '''
    Page total counter
    Args:
        element_count, count_per_page
    '''
    total_pages = int(element_count/10)
    if element_count % 10 != 0:
        total_pages = total_pages + 1

    return total_pages


def transform_data(people, planets):
    '''
        Transporm data and save it in csv, crate db obj
        Args:
            people, planets
    '''

    people_table = build_people_table(people)
    planet_table = build_planets_table(planets)

    # resolve homeword url field into names
    data_tb = etl.join(people_table, planet_table, lkey='world', rkey='url')
    # remove column
    data_tb = etl.cutout(data_tb, 'world')
    # add date column
    data_tb = add_date(data_tb)
    # crate csv and save the path to a db obj
    create_dataset(data_tb)

    return data_tb


def build_people_table(people):

    people_table = etl.fromdicts(people)
    remove_headers = [
        'films',
        'vehicles',
        'starships',
        'created',
        'edited',
        'url',
        'species'
    ]
    # remove unwanted columns
    people_table = etl.cutout(people_table, *remove_headers)
    # rename column
    people_table = etl.rename(people_table, {'homeworld': 'world'})

    return people_table


def build_planets_table(planets):
    # add only selected columns to table
    planet_table = etl.fromdicts(planets, header={'name', 'url'})
    # rename column
    planet_table = etl.rename(planet_table, {'name': 'homeworld'})

    return planet_table


def add_date(data_tb):
    '''
        Add date field to table
    '''
    today = date.today()
    data_tb = etl.addfield(data_tb, 'date', today)

    return data_tb


def create_dataset(data_tb):
    '''
    Save to csv, create new db obj

    '''
    # if dir not exist - create one
    os.makedirs(os.path.dirname(MEDIA_ROOT), exist_ok=True)
    filename = 'dataset_' + str(uuid.uuid4()) + '.csv'
    name = MEDIA_ROOT + '/csv/' + filename
    # create csv
    etl.tocsv(data_tb, name)
    # create obj
    dataset = DatasetCSV(path=name, filename=filename)

    dataset.save()
