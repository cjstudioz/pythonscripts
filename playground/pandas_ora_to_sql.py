'''
-- on oracle db
create table testtable(
    idx number,
    val varchar2(1024)
)
'''

import pandas as pd    
import sqlalchemy as sa
engine = sa.create_engine('oracle+cx_oracle://user:pw@host:port/sid') 
    
df = pd.DataFrame({
     'idx': range(10000),          
     'val': [str(x) for x in range(10000)],
})                 
    
#this is fast
sql = "insert into testtable (idx, val) values (:idx, :val)"
engine.execute(sql, df.to_dict('record'))

#this is really slow
df.to_sql('testtable', engine, 
  if_exists='append',
  index=False,  
)
