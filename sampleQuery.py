import _mysql
import IPython

from MySQLdb.constants import FIELD_TYPE
my_conf = { FIELD_TYPE.BIGINT: int}


db = _mysql.connect(user="testMetaRO", host="localhost", db="nov_meta", passwd="test")
db.query("""
         SELECT * FROM charge LIMIT 20;
         """)

result=db.store_result()
row = result.fetch_row(how=1)[0]
IPython.embed()
