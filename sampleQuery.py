import _mysql
import calendar

import IPython

def net_montly_plan_charge_per_day(merchant_id, month, year):

    days_in_month = calendar.monthrange(year, month)[1]

    db = _mysql.connect(user="testMetaRO", host="localhost", db="nov_meta", passwd="test")
    db.query("""
            SELECT amount, plan_charge_type                
                FROM charge                                                                 
                INNER JOIN merchant_plan_charge                                             
                    ON merchant_plan_charge.charge_id = charge.id                           
            WHERE merchant_id = {}                                                      
            AND MONTH(merchant_plan_charge.created_time) = {}
            ORDER BY merchant_plan_charge.created_time DESC                                 
            ;             
             """.format(merchant_id, month))

    result=db.store_result()

    is_owed = 0
    owes = 0
    for row in result.fetch_row(how=1):
        charge_type = row['plan_charge_type'];
        print(charge_type)
        charge_amount = int(row['amount']);
        if charge_type == b'ADJUSTMENT':
            is_owed += charge_amount;
        elif charge_type == b'ADVANCE':
            owes += charge_amount;
        else:
            raise ValueError("Unexpected charge type: {}".format(charge_type))

    m = (owes - is_owed)/days_in_month;
    b = -is_owed

    # at 0 this gives the total adjustment amount
    # at <last day in month> it gives the total billed amount
    # it is linear in between
    def f(x):
        return m * x + b

    return [f(x) for x in range(days_in_month)]


plan_days = net_montly_plan_charge_per_day(194013, 12, 2017)
IPython.embed()
