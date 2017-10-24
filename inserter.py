
from config import config
import hashlib
from random import *
import random
from datetime import datetime
import os
from uuid import uuid4
import psycopg2.extras
import json
import numpy as np
psycopg2.extras.register_uuid()
# 10 datasets
# 100 files for each datasets
# 3 annotations for each file
# 1 single source fine
#
#
# dataset really doesnt depend on anything
# file doesnt depend on anything
# source_type - doesnt depend on anything.
#
# dataset_assingment - FK file, dataset
# annotation - FK file, annotation_source
# annoation source - FK source_type
#SELECT * FROM dataman.annotation WHERE data ? 'face';

#different datasets to have different annotations one dataset(cars,ppl,nuke) diff(ppl, animal, stopsigns)
#fix click on dataset websitething
#


## some random words to use and todays date
wordbank = ["test", "foo", "face", "stuff", "things", "lots", "o", "image"]
today = str(datetime.now())
annot_catagory_words = ['face', 'automobile', 'building']
annot_face_subcat_1 = ['male', 'female', 'attack_helicopter']
annot_face_subcat_2 = ['None', 'Sunglasses','yes']
annot_face_subcat_3 = [[40, 60, 100, 120], [20, 40, 60, 100], [60, 80, 120, 200]]
annot_auto_subcat_1 = ['subaru', 'toyota', 'ford', 'honda']
annot_auto_subcat_2 = ['red', 'white', 'blue', 'tan', 'teal', 'pink']
annot_auto_subcat_3 = [2, 4, 6, 18, 1]
annot_bld_subcat_1 = ['store', 'house', 'restaurant', 'warehouse', 'none']
annot_bld_subcat_2 = ['glass', 'brick', 'steel', 'sign', 'wood', 'damage', 'pillar']
annot_bld_subcat_3 = [0, 2, 4, 3, 5, 100]
annot_shp_subcat_1 = ['cruise', 'fishing', 'dinghy', 'battleship', 'carrier', 'barge']
annot_shp_subcat_2 = ['white', 'red', 'grey', 'rust', 'yellow']
annot_shp_subcat_3 = ['USA', 'GERMANY', 'FRANCE', 'RUSSIA', 'LEBANON', 'INDIA']
annot_pln_subcat_1 = ['JET', 'AIRLINE', 'TWO-SEAT', 'BOMBER', 'DRONE']
annot_pln_subcat_2 = ['GROUNDED', 1000, 7000, 13500, 25000, 39000]
annot_pln_subcat_3 = ['STORM', 'CLOUDY', 'CLEAR', 'HANGAR', 'SNOW']
annot_person_subcat_1 = ['male', 'female']
annot_person_subcat_2 = ['5"5', '5"6', '5"7', '5"8', '5"9', '5"10', '5"11', '6', '6"1', '6"2', '6"3', '6"4', '6"5']
annot_person_subcat_3 = ['fat', 'tall', 'short', 'sitting', 'standing', 'walking', 'running', 'crouching']
conn = psycopg2.connect(**config)
if conn is not None:
    print('connected')
cur = conn.cursor()
src_type_id= 1
d_src_type = (src_type_id, 'test)')
insert_src_type = """
    INSERT INTO dataman.source_type(source_type_id, source_type_desc)
    VALUES (%s, %s);
    """
# cur.execute(insert_src_type, d_src_type)
src_id = uuid4()
source_name = 'test'
d_src = (src_id, source_name, src_type_id)
insert_annot_source = """
    INSERT INTO dataman.source(source_id, name, source_type_fk)
    VALUES (%s, %s, %s)
    """
cur.execute(insert_annot_source, d_src)


dataset_ids = []
for idx in range(10):
    d_descrip = random.choice(wordbank) + random.choice(wordbank) + random.choice(wordbank)
    name = "test%d" % (randint(1, 1000))
    owner = "redge"
    created = today
    ds_id = uuid4()
    dataset_data = (ds_id, name, d_descrip, owner, today)
    SQL_INSERT_DATASET = """
          INSERT INTO dataman.dataset(dataset_id, name, description, owner, created) 
          VALUES (%s, %s, %s, %s, %s);
        """
    cur.execute(SQL_INSERT_DATASET, dataset_data)
    dataset_ids.append(ds_id)


f_ids = []
# dataset_ids is a list of all the valid datasets
for ds_id in dataset_ids:
    for y in range(100):
        f_id = uuid4()

        # insert the row into the file table
        data_f_insert = (f_id, '/', '/')
        f_insert = """
        INSERT INTO dataman.file(file_id, last_path, hash)
        VALUES( %s, %s, %s)
        """
        cur.execute(f_insert, data_f_insert)
        data_ds_assignment = (ds_id, f_id)
        # associate file with a dataset by inserting into dataset_assignment
        insert_ds_assignment = """
        INSERT INTO dataman.dataset_assignment(dataset_fk, file_fk)
        VALUES (%s, %s)
        """
        cur.execute(insert_ds_assignment, data_ds_assignment)
        f_ids.append(f_id)
for f_id in f_ids:
    y = random.choice([0, 1, 2])
    for x in range(3):
        j = y
        # insert an annotation
        a_id = uuid4()
        annot_1 = {'face': {'gender': random.choice(annot_face_subcat_1), 'glasses': random.choice(annot_face_subcat_2),
                            'boundingbox': random.choice(annot_face_subcat_3)}}

        annot_2 = {
            'automobile': {'make': random.choice(annot_auto_subcat_1), 'color': random.choice(annot_auto_subcat_2),
                           'wheels': random.choice(annot_auto_subcat_3)}}

        annot_3 = {'building': {'type': random.choice(annot_bld_subcat_1), 'feature': random.choice(annot_bld_subcat_2),
                                'windows': random.choice(annot_bld_subcat_3)}}
        annot_4 = {'ship': {'type': random.choice(annot_shp_subcat_1), 'color': random.choice(annot_shp_subcat_2),
                           'flag': random.choice(annot_shp_subcat_3)}}
        annot_5 = {'plane': {'type': random.choice(annot_pln_subcat_1), 'altitude': random.choice(annot_pln_subcat_2),
                            'conditions': random.choice(annot_pln_subcat_3)}}
        annot_6 = {'person': {'gender': random.choice(annot_person_subcat_1), 'height': random.choice(annot_person_subcat_2),
                             'defining_feature': random.choice(annot_person_subcat_3)}}
        src_name = 'test'
        annot_lst = [annot_1, annot_2, annot_3]
        annot_lst_2 = [annot_6, annot_4, annot_1]
        annot_lst_3 = [annot_5, annot_1, annot_4]
        if j == 0:
            data_a_assignment = (a_id, src_id, f_id, today, '/', json.dumps(annot_lst_2[x]))
        if j % 2 == 0:
            data_a_assignment = (a_id, src_id, f_id, today, '/', json.dumps(annot_lst_3[x]))
        else:
            data_a_assignment = (a_id, src_id, f_id, today, '/', json.dumps(annot_lst[x]))
        insert_a_assignment = """
                INSERT INTO dataman.annotation(annotation_id, source_fk, file_fk, last_date, last_user, data)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
        cur.execute(insert_a_assignment, data_a_assignment)


conn.commit()
cur.close()
conn.close()

