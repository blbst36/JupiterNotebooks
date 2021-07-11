
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Float

# Store filepath in a variable
goodreads_csv = 'Input/goodreads.csv'
amazon_csv = 'Input/amazon.csv'
nyt_csv = 'Input/nyt.csv'

# Read Data file with the pandas library
goodreads_orig = pd.read_csv(goodreads_csv, encoding='ISO-8859-1')
amazon_orig = pd.read_csv(amazon_csv, encoding='ISO-8859-1')
nyt_orig = pd.read_csv(nyt_csv, encoding='ISO-8859-1')

# get only relevant columns from nyt and rename columns
nyt = nyt_orig[['Title', 'First', 'Last', 'Rank']]
nyt['source'] = 'New York Times'
nyt = nyt.rename(columns={'Rank': 'Rating'})

# get only relevant columns from amazon and rename columns
amazon = amazon_orig[['Book_Title', 'First', 'Last', 'UserRating']]
amazon['source'] = 'Amazon'
amazon = amazon.rename(columns={'Book_Title': 'Title', 'UserRating': 'Rating'})

# preserve original dataframe, then split the author name.  Grab only relevant columns
goodreads = goodreads_orig.copy()

# Added dash to name to assist with splitting first and last
goodreads.at[3, 'Author'] = 'Mary-Beth Keane'
goodreads[['First', 'Last']] = goodreads.Author.str.split(expand=True)
goodreads_drop = goodreads[['Title', 'First', 'Last', 'Rating']]
goodreads_drop['source'] = 'Goodreads'

# Add two dataframes together
total = goodreads_drop.copy()
total = total.append(amazon)
total = total.append(nyt)

# create author table/dataframe using the index as a PK
author = pd.DataFrame(total.groupby(['Last', 'First']).count())
author = author.reset_index()
author_final = author[['First', 'Last']]
author_final = author_final.drop_duplicates()
author_final = author_final.reset_index()
author_final = author_final.rename(columns={'index': 'author_id', 'First': 'first_name', 'Last': 'last_name'})

# find the author's last name and replace with the author PK number
books = total.copy()
for name in author_final.index:
    books = books.replace(to_replace=author_final.iloc[name]['last_name'],
                          value=author_final.loc[name]['author_id'])

# Finish finageling the books table/dataframe using the index as a PK
books_final = books[['Title', 'Last']]
books_final = books_final.reset_index(drop=True)
books_final = books_final.drop_duplicates()
books_final = books_final.reset_index()
books_final = books_final.rename(columns={'index': 'book_id', 'Title': 'title', 'Last': 'author_fk'})

# Create source table/dataframe
source = pd.DataFrame()
source['source_name'] = ['Goodreads', 'Amazon', 'New York Times']
source['type'] = ['User Rating', 'User Rating', 'Bestseller']
source_final = source.reset_index()
source_final = source_final.rename(columns={'index': 'source_id'})

# Create review table/dataframe.  Replace source and title with ids
review = total.copy()
for name in source_final.index:
    review = review.replace(to_replace=source_final.iloc[name]['source_name'],
                            value=source_final.loc[name]['source_id'])

for name in books_final.index:
    review = review.replace(to_replace=books_final.iloc[name]['title'], value=books_final.loc[name]['book_id'])
review_final = review[['Title', 'Rating', 'source']]
review_final = review_final.reset_index(drop=True)
review_final = review_final.reset_index()
review_final = review_final.rename(
    columns={'index': 'review_id', 'Title': 'book_fk', 'source': 'source_fk', 'Rating': 'rating'})

# enter password for postgres
rds_connection_string = "postgres:postgres@localhost:5432/ETL_Project"
engine = create_engine(f'postgresql://{rds_connection_string}')

meta = MetaData()

author_table = Table(
    'author', meta,
    Column('author_id', Integer, primary_key=True),
    Column('first_name', String),
    Column('last_name', String)
)

book_table = Table(
    'book', meta,
    Column('book_id', Integer, primary_key=True),
    Column('title', String),
    Column('author_fk', Integer)
)

source_table = Table(
    'source', meta,
    Column('source_id', Integer, primary_key=True),
    Column('source_name', String),
    Column('type', String)
)

review_table = Table(
    'review', meta,
    Column('review_id', Integer, primary_key=True),
    Column('book_fk', Integer),
    Column('source_fk', Integer),
    Column('rating', Float)
)

meta.create_all(engine)

# Add data to empty tables.
author_final.to_sql(name='author', con=engine, if_exists='append', index=False)
books_final.to_sql(name='book', con=engine, if_exists='append', index=False)
source_final.to_sql(name='source', con=engine, if_exists='append', index=False)
review_final.to_sql(name='review', con=engine, if_exists='append', index=False)

