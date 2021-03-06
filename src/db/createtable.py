from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import pyodbc
from sqlalchemy import create_engine
import urllib

params = urllib.parse.quote_plus \
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine_azure = create_engine(conn_str,echo=True)

meta = MetaData()

students = Table(
   'students', meta, 
   Column('id', Integer, primary_key = True), 
   Column('name', String), 
   Column('lastname', String),
)
meta.create_all(engine_azure)