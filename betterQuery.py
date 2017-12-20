
db_host="localhost"
db_name="nov_meta"
merchant=194013
month=12
year=2017

import IPython

import MySQLdb
import calendar

class Context:
    def __init__(self, db_user, db_host, db_name, merchant_id, month, year):
        self.merchant=merchant_id
        self.month=month
        self.year=year
        self.db = MySQLdb.connect(user=db_user, host=db_host, db=db_name, passwd="test")


def net_montly_plan_charge_per_day(target):

    days_in_month = calendar.monthrange(target.year, target.month)[1]

    cursor = target.db.cursor()
    cursor.execute(
        """
        SELECT amount, plan_charge_type                
            FROM charge                                                                 
            INNER JOIN merchant_plan_charge                                             
                ON merchant_plan_charge.charge_id = charge.id                           
        WHERE merchant_id = {}                                                      
        AND MONTH(merchant_plan_charge.created_time) = {}
        ORDER BY merchant_plan_charge.created_time DESC                                 
        ;             
         """.format(target.merchant, target.month))

    owes=0
    is_owed=0
    for amount, charge_type in cursor.fetchall():
        print(amount, charge_type)
        if charge_type == 'ADJUSTMENT':
            is_owed += amount;
        elif charge_type == 'ADVANCE':
            owes += amount;
        else:
            raise ValueError("Unexpected charge type: {}".format(charge_type))

    m = owes/days_in_month;
    b = -is_owed

    # at 0 this gives the total adjustment amount
    # at <last day in month> it gives the total billed amount
    # it is linear in between
    def f(x):
        return m * x + b

    return [f(x) for x in range(days_in_month)]

context = Context('testMetaRO', db_host, db_name, merchant, month, year)
plan_days = net_montly_plan_charge_per_day(context)

IPython.embed()
