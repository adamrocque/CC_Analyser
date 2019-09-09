import sys
import glob
import os
import subprocess
import json
import string
import sys
import os
import datetime
import csv
import shutil
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
#amzn_list = ['AMZN','AMAZON']

#Bar
bar = {
    "total": 0,
    "list":['BLACK DOG',"LOOKOUT SPORTS LOUNGE"],
}
#bar_list = ['BLACK DOG']

#CarPayment
car_pay = {
    "total": 0,
    "list":['HONDA'],
}
#car_pay_list = ['HONDA']

##CC_Payment
#cc_payment_list = ['PAYMENT']

#Food
food = {
    "total": 0,
    "list":["OSMOW'S","MCDONALD'S","WENDY'S","TIM HORTONS","SPRING GRILL HOUSE KOREAN","SUNRISE CARIBBEAN","CHUCK'S ROADHOUSE BAR"],
}

#food_list = ['OSMOWS',"MCDONALD'S","WENDY'S","TIM HORTONS"]

#Fun
fun = {
    "total": 0,
    "list":['CONFUNDRUM','BEST BUY','BARANGA', "THE MULE INC"],
}

#fun_list= ['CONFUNDRUM','BEST BUY','BARANGA']

#Gas
gas = {
    "total": 0,
    "list":['PETROCAN'],
}

#gas_list = ['PETROCAN']

#Groc
groc = {
    "total": 0,
    "list":['SOBEYS','FORTINOS','LOBLAWS','FARM BOY','FRESHCO', "ASLAN"],
}

#groc_list = ['SOBEYS','FORTINOS','LOBLAWS','FARM BOY','FRESHCO']

#Gym
gym = {
    "total": 0,
    "list":['GOODLIFE'],
}

#gym_list = ['GOODLIFE']

#House
house  = {
    "total": 0,
    "list":['HOME DEPOT','EQUIFAX','WAL-MART','ZEHRS',"BELL CANADA", "CDN TIRE"],
}
#house_list = ['HOME DEPOT','EQUIFAX','WAL-MART','ZEHRS']

#Insurance
insur  = {
    "total": 0,
    "list":['INSURANCE'],
}

#insur_list = ['INSURANCE']

#Paypal
paypal  = {
    "total": 0,
    "list":['PAYPAL'],
}

#paypal_list = ['PAYPAL']

#Travel
travel  = {
    "total": 0,
    "list":['PARKING',"PRESTO"],
}
#Unknown Entries
unknown = {}


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

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def enter_catergory(row,count):
    print(row['Transaction'])
    transaction = row['Transaction']

    # Find Store numbers and remove them
    try:
        if transaction.index("#") >= 0:
            transaction = transaction[0:transaction.index("#") -1]
    except ValueError:
        # print("This transaction has no # signs in it")
        transaction = transaction

    try:
        if transaction.upper().index("THE") == 0:
            # print("This transaction starts with a THE, omitting it")
            transaction = transaction[3:]
    except ValueError:
        transaction = transaction
        # print("This transaction does not start with a 'THE' ")

    try:
        if '/' in transaction:
            transaction = transaction[0:transaction.index("/") ]  
    except ValueError:
        transaction = transaction      
        # print("This transaction has no / signs in it")

    try:
        if '(' in transaction:
            transaction = transaction[0:transaction.index("(") -1]  
    except ValueError:
        transaction = transaction

    try:
        if '-' in transaction:
            try:
                if transaction.index("WAL-MART") > 0:
                    print("Found a dash, but its  WAL-MART, using WAL-MART")
                    transaction = transaction[0:transaction.index(" ")] 

            except:
                    print("Found a dash, but not WAL-MART, using transaction before -")
                    transaction = transaction[0:transaction.index("-")] 
    except ValueError:
        print("Defaulting here?")
        transaction = transaction


    try:
        spc_index = find_nth(transaction, " ", 1)
        if spc_index >= 0:
            transaction = transaction[0:spc_index]
        else:
            transaction = transaction[0:10]
    except ValueError:
        transaction = transaction
        # print("This transaction has fewer than 1 space in it, but it was also shorter than 10 chars")


    print("Checking if {0} is in any lists".format(transaction))
    #if any(transaction in s for s in food_list):
    if any(transaction in s for s in food["list"]):
        print("\nWe found a transaction [{0}] that should be catergorized as an FOOD purchase".format(transaction))
        print("Adding [{0}] to the food total\n".format(float(row["Debit"])))
        food["total"] += float(row["Debit"])
        #print(row['Transaction'])

    elif any(transaction in s for s in groc["list"]):
        print("\nWe found a transaction [{0}] that should be catergorized as an GROC purchase".format(transaction))
        print("Adding [{0}] to the food total\n".format(float(row["Debit"])))
        groc["total"] += float(row["Debit"])
        #print(row['Transaction'])


    elif any(transaction in s for s in alc["list"]):
        print("\nWe found a transaction [{0}] that should be catergorized as an ALC purchase".format(transaction))
        print("Adding [{0}] to the food total\n".format(float(row["Debit"])))
        alc["total"] += float(row["Debit"])
        #print(row['Transaction'])


    elif any(transaction in s for s in house["list"]):
        print("\nWe found a transaction [{0}] that should be catergorized as an HOUSE purchase".format(transaction))
        print("Adding [{0}] to the food total\n".format(float(row["Debit"])))
        house["total"] += float(row["Debit"])
        #print(row['Transaction'])

    elif any(transaction in s for s in travel["list"]):
        print("\nWe found a transaction [{0}] that should be catergorized as an HOUSE purchase".format(transaction))
        print("Adding [{0}] to the food total\n".format(float(row["Debit"])))
        travel["total"] += float(row["Debit"])
        #print(row['Transaction'])        

    elif any(transaction in s for s in gas["list"]):
        print("\nWe found a transaction [{0}] that should be catergorized as an GAS purchase".format(transaction))
        print("Adding [{0}] to the food total\n".format(float(row["Debit"])))
        gas["total"] += float(row["Debit"])
        #print(row['Transaction'])

    elif any(transaction in s for s in bar["list"]):
        print("\nWe found a transaction [{0}] that should be catergorized as an GAS purchase".format(transaction))
        print("Adding [{0}] to the food total\n".format(float(row["Debit"])))
        bar["total"] += float(row["Debit"])
        #print(row['Transaction'])  

    elif any(transaction in s for s in amazon["list"]):
        print("\nWe found a transaction [{0}] that should be catergorized as an GAS purchase".format(transaction))
        print("Adding [{0}] to the food total\n".format(float(row["Debit"])))
        amazon["total"] += float(row["Debit"])
        #print(row['Transaction'])                

    elif any(transaction in s for s in paypal["list"]):
        print("\nWe found a transaction [{0}] that should be catergorized as an GAS purchase".format(transaction))
        print("Adding [{0}] to the food total\n".format(float(row["Debit"])))
        paypal["total"] += float(row["Debit"])
        #print(row['Transaction'])        

    else:
        print("Nope, not in any of the lists, add to the unknown list")
        # unknown["total"] += float(row["Debit"])
        # unknown["list"].append(transaction)
        print("An Unknown Transaction: {0}, Its Value: {1} ".format(transaction,row["Debit"]))
        unknown[transaction] = row["Debit"]

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

#print("We found this total spent in food: {0}".format(food_dict))
print("We found this total spent in FOOD: {0}".format(food["total"]))
print("We found this total spent in ALC: {0}".format(alc["total"]))
print("We found this total spent in HOUSE: {0}".format(house["total"]))
print("We found this total spent in GAS: {0}".format(gas["total"]))
print("We found this total spent in GROC: {0}".format(groc["total"]))
print("We found this total spent in PAYPAL: {0}".format(paypal["total"]))

print("The transactions we couldn't understand: ")
for transac in unknown:
    print("Transaction: {0}  Value: {1}".format(transac, unknown[transac]))


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
