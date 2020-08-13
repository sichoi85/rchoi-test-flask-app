import pyodbc
from sqlalchemy import create_engine
import urllib

params = urllib.parse.quote_plus \
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine_azure = create_engine(conn_str,echo=True)

print('connection is ok')
print(engine_azure.table_names())

