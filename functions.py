import csv
import datetime
from datetime import date, timedelta
   
def read_csv(path):
    record = {}
    table = []
    with open(path,'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        header = next(reader)
        for row in reader:
            iterable = zip(header,row)
            record = {key: value for key, value in iterable}
            table.append(record)
    return table

def date_txt_to_ISOex(ISOex_date): 
    formated_date = date(int(ISOex_date[0:4]),int(ISOex_date[5:7]),int(ISOex_date[8:10]))
    return formated_date

def date_diff(end_date,start_date):
    diff = end_date - start_date
    return diff.days

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4) 
    last_day = next_month - datetime.timedelta(days=next_month.day) 
    return last_day

def distributor(dict):
    if dict['stage'] == 'Deal lost':
        return     
    close_date = date_txt_to_ISOex(dict['close_date'])  
    start_date = date_txt_to_ISOex(dict['start_date'])  
    end_date = date_txt_to_ISOex(dict['end_date'])      
    duration = date_diff(end_date,start_date)           
    value_per_day = float(dict['value'])/duration              
    contract_value = float(dict['value'])                      
    product = dict['product']                           
    cod = dict['id']                                   
    contract_distribution=[]                            
    counter = 0                                         
    month = [start_date]                                
    while contract_value > 0:
        row = {}                                                                                      
        row['month'] = last_day_of_month(start_date).isoformat()                                                  
        if contract_value > date_diff(last_day_of_month(start_date),month[counter]) * value_per_day:    
            row['value'] = date_diff(last_day_of_month(start_date),month[counter]) * value_per_day  
        else:
            row['value'] = contract_value    
        row['id'] = cod
        row['product'] = product
        contract_distribution.append(row)
        month.append(last_day_of_month(start_date))
        start_date = last_day_of_month(start_date) + timedelta(days=1)
        contract_value = contract_value - row['value']
        counter += 1
    return contract_distribution   
