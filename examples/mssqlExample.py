import sqlalchemy

def connectcb():
    import pyodbc
    conn_str='DSN=mssql;Server=dfsdf,15001;database=dsfsdf;UID=sdfsdf;PWD=fsdf;'
    return pyodbc.connect(conn_str, autocommit=True, timeout=120)
        
engine = sqlalchemy.create_engine('mssql://', creator=connectcb)