# import whatever we need
import pickle
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from getpass import getpass
import sys

# setup database engine
def setup_db(db_details):
    return create_engine(db_details)

db_details = f'postgresql://postgres:galvanize@3.128.75.60:5432/fraud_data'
# now we have a db connection setup
db_connection = setup_db(db_details)

# db table schema
'''
Schema |         Name         | Type  |  Owner   
--------+----------------------+-------+----------
 public | api_data             | table | postgres
 public | org_previous_payouts | table | postgres
 public | org_ticket_types     | table | postgres
 public | original_data        | table | postgres
 public | previous_payouts     | table | postgres
 public | ticket_types         | table | postgres

 fraud_data=# select * from previous_payouts limit 1;
 name |       created       | country | amount | state | address |   uid    |  event  | zip_code | object_id 
------+---------------------+---------+--------+-------+---------+----------+---------+----------+-----------
      | 2013-06-25 03:18:28 | US      |     45 |       |         | 64691249 | 7116643 |          |   7464371
(1 row)

fraud_data=# select * from ticket_types limit 1;
 event_id | cost | availability | quantity_total | object_id 
----------+------+--------------+----------------+-----------
  8122707 |  500 |            1 |              5 |   8122707
(1 row)
'''


# setup query to pull 100 records from db

# we will have a pandas df to play with..

# keep means from training data? 
# if statement for rows we can't predict on

# setup what we want to keep
cols = ['body_length',
 'channels',
 'delivery_method',
 'event_created',
 'event_end',
 'event_published',
 'event_start',
 'fb_published',
 'has_analytics',
 'has_header',
 'has_logo',
 'name_length',
 'object_id',
 'org_facebook',
 'org_twitter',
 'sale_duration',
 'show_map',
 'user_age',
 'user_created',
 'user_type',
 'venue_latitude',
 'venue_longitude']

# 3 parts:
# 1. from api_data

# example
# query = "SELECT body_length, channels, country, currency, delivery_method, description, email_domain, \
#             fb_published, has_analytics, name, org_name, \
#             sale_duration, user_age, venue_country, venue_name, created_at \
#             FROM api_data WHERE created_at IS NOT NULL ORDER BY created_at DESC LIMIT 100;"

query = f'SELECT {", ".join(x for x in cols)} FROM api_data;'
query
api_data_main = pd.read_sql(query, con=db_connection)
api_data_main.shape
api_data_main[api_data_main['object_id'] == 7116643] #event from prev
api_data_main[api_data_main['object_id'] == 7464371] #object from prev

object_ids = api_data_main['object_id'].unique()

# 2. from previous payouts

cols_prev_payouts = ['amount', 'object_id']
query = f'SELECT {", ".join(x for x in cols_prev_payouts)} FROM previous_payouts;'

prev_payouts = pd.read_sql(query, con=db_connection)
prev_payouts.shape

# get sum...

# 3. from ticket types table
cols_ticket_types = ['object_id', 'cost', 'quantity_total']
query = f'SELECT {", ".join(x for x in cols_ticket_types)} FROM ticket_types;'
ticket_types = pd.read_sql(query, con=db_connection)
ticket_types.shape
ticket_types.head()

#.... 

# output: 3 pandas dfs

# groupby and sum for prev payouts and tickets using object_id

# merge them together into one df (based on something.. object_id)

# clean whatever we need, maybe drop cols... (function)
# insert means for nans.. from training data

# --- get this from model.. does this give us a vector... 
# consider threshold and turn proba into fraud/not fraud

# update each row with a column called prediction

# final df with predictions


# to do list
# finish model prediction (this script)
# clean up read me
# use a simplier css layout for flask app
# we can talk about how we want it to look
# implement model prediction in app.py