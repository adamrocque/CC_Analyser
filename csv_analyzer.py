import sys
import glob
import os
import subprocess
import json
import string
import sys
import os
import datetime

#from evertz.mediator.ws import MediatorHttpClientV1

import csv
import shutil
import datetime
from tempfile import NamedTemporaryFile

##Lists of Categories

#Alc
alc = {
    "total": 0,
    "list":["THE BEER STORE", "LCBO"],
}

#Amazon
amazon = {
    "total": 0,
    "list":['AMZN','AMAZON'],
}
amzn_list = ['AMZN','AMAZON']

#Bar
bar_list = ['BLACK DOG']

#CarPayment
car_pay_list = ['HONDA']

##CC_Payment
#cc_payment_list = ['PAYMENT']

#Food
food = {
    "total": 0,
    "list":["OSMOW'S","MCDONALD'S","WENDY'S","TIM HORTONS","SPRING GRILL HOUSE KOREAN","SUNRISE CARIBBEAN","CHUCK'S ROADHOUSE BAR"],
}

#food_list = ['OSMOWS',"MCDONALD'S","WENDY'S","TIM HORTONS"]

#Fun
fun_list = ['CONFUNDRUM','BEST BUY','BARANGA']

#Gas
gas_list = ['PETROCAN']

#Groc
groc_list = ['SOBEYS','FORTINOS','LOBLAWS','FARM BOY','FRESHCO']

#Gym
gym_list = ['GOODLIFE']

#House
house_list = ['HOME DEPOT','EQUIFAX','WAL-MART','ZEHRS']

#Insurance
insur_list = ['INSURANCE']

#Paypal
paypal_list = ['PAYPAL']

#Travel

def get_length(file_path):
    with open("data.csv") as csvfile:
        reader = csv.reader(csvfile)
        reader_list = list(reader)
        print(reader_list)
        return len(reader_list)

def append_data(file_path, name, email, amount):
    fieldnames = ['id', 'name', 'email', 'amount', 'sent','date']
    #the number of rows
    next_id = get_length(file_path)
    with open("data.csv", "a") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerow({
            "id": next_id,
            "name": name,
            "email":email,
            "amount": "1293.23",
            "sent":"",
            "date": datetime.datetime.now(),            
            })

def enter_catergory(row,count):
    print(row['Transaction'])
    transaction = row['Transaction']

    # Find Store numbers and remove them
    try:
        if transaction.index("#") >= 0:
            transaction = transaction[0:transaction.index("#") -1]
    except ValueError:
        print("This transaction has no # signs in it")

    print("Checking if {0} is in the food list".format(transaction))
    #if any(transaction in s for s in food_list):
    if any(transaction[0:10] in s for s in food["list"]):
        print("\nWe found a transaction [{0}] that should be catergorized as an Food purchase".format(transaction))
        print("Adding [{0}] to the food total\n".format(float(row["Debit"])))
        food["total"] += float(row["Debit"])
        #print(row['Transaction'])

    else:
        print("Nope, not in the food list")
#append_data("data.csv", "Adam", "adam@evertz.com",123.22)


file_path = '/srv/storage/medias/store/'
#file_path = "/srv/tx_upload/internal/medias/tx_upload_store/"
#default_search_path = "/srv/tx_upload/internal/medias/tx_upload_store/"
#default_search_path = "/home/evertz/"

filename = "test_cc.csv"
temp_file = NamedTemporaryFile(delete=False)
#temp_file = "data2.csv"
food_dict = {}

with open(filename, "rb") as csvfile, temp_file:
    reader = csv.DictReader(csvfile)
    fieldnames = ['Date','Transaction','Debit','Credit','Total','Category']
    writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
    writer.writeheader()
    count = 0
    for row in reader:
        enter_catergory(row,count)

print("We found this total spent in food: {0}".format(food_dict))

#         ##if row['Transaction']

#         mediainfo_path = file_path + row['MatID'] +".dir/" + row['MatID'] +".mxf"
#         print(mediainfo_path)
#         try:
#             writ_app = subprocess.check_output(['mediainfo', '--Inform=General;%Encoded_Application_CompanyName%', mediainfo_path ])
#             row['Writing Application'] = str(writ_app)
#         except:
#             print("Failed to get mediainfo of {}".format(str(row['MatID'])))
#         writer.writerow(row)
#         print(row)
#     #print(writer)
# shutil.move(temp_file.name, filename)
