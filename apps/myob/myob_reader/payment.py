import traceback
from ast import Break

import requests

from apps.home.data_util import get_job_details, add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


# job_url = f"{base_url}/GeneralLedger/Job?$top=100&$skip=0"

# def get_payment(job_id):
#     try:
#         no_of_records = db['payment'].count_documents({})
#         payload, base_url, headers = get_settings_myob(job_id)
#         url = f"{base_url}/Sale/CreditSettlement?$top=100&$skip={no_of_records}"
#         print(url)
#         response = requests.request(
#             "GET", url, headers=headers, data=payload)
#         JsonResponse = response.json()
#         JsonResponse1 = JsonResponse['Items']

#         arr = []
#         for i in range(0,len(JsonResponse1)):
#             if JsonResponse1[i]['Invoices'] != []:
#                 QuerySet={}
#                 QuerySet['Invoice']=JsonResponse1[i]['Invoices'][0]['Sale']['Number']
#                 QuerySet['CreditMemo']=JsonResponse1[i]['CreditFromInvoice']['Number']
#                 QuerySet['paid_amount'] = JsonResponse1[i]['Invoices'][0]['AmountApplied']
#                 QuerySet['customer']=JsonResponse1[i]['Customer']['Name']

#                 arr.append(QuerySet)

#         print(arr)

#         Collection.insert_many(arr)

#         if JsonResponse['NextPageLink'] is not None:
#             print(JsonResponse['NextPageLink'])
#             get_payment(job_id)

#         else:
#             print("No more data to extract.")
#             Break


#     except Exception as ex:
#         print("------------------------------")
#         import traceback
#         traceback.print_exc()
#         print(ex)


# def get_invoice_payment(job_id):
#     try:
#         start_date, end_date = get_job_details(job_id)
#         payload, base_url, headers = get_settings_myob(job_id)

#         no_of_records = db['invoice_payment'].count_documents({})
#         payload, base_url, headers = get_settings_myob(job_id)

#         if (start_date == '' and end_date == ''):
#             url = f"{base_url}/Sale/CustomerPayment?$top=100&$skip={no_of_records}"
#         else:
#             url = f"{base_url}/Sale/CustomerPayment?$filter=Date ge datetime'{start_date[0:10]}' and Date le datetime'{end_date[0:10]}'"

#         print(url)

#         print(url)
#         response = requests.request(
#             "GET", url, headers=headers, data=payload)
#         JsonResponse = response.json()
#         JsonResponse1 = JsonResponse['Items']

#         arr = []
#         for i in range(0,len(JsonResponse1)):
#             if JsonResponse1[i]['Invoices'] != []:
#                 QuerySet={"Line":[]}

#                 for j in range(0,len(JsonResponse1[i]['Invoices'])):
#                     QuerySet1={}
#                     QuerySet1['Invoice']=JsonResponse1[i]['Invoices'][j]['Number']
#                     QuerySet1['paid_amount'] = JsonResponse1[i]['Invoices'][j]['AmountApplied']
#                     QuerySet['Line'].append(QuerySet1)

#                 QuerySet['AccName']=JsonResponse1[i]['account']['Name']
#                 QuerySet['AccId']=JsonResponse1[i]['account']['DisplayID']
#                 QuerySet['CreditMemo']=JsonResponse1[i]['ReceiptNumber']
#                 QuerySet['Date']=JsonResponse1[i]['Date']
#                 QuerySet['customer']=JsonResponse1[i]['Customer']['Name']

#                 arr.append(QuerySet)


#         Collection.insert_many(arr)

#         if JsonResponse['NextPageLink'] is not None:
#             print(JsonResponse['NextPageLink'])
#             get_invoice_payment(job_id)

#         else:
#             print("No more data to extract.")
#             Break


#     except Exception as ex:
#         print("------------------------------")
#         import traceback
#         traceback.print_exc()
#         print(ex)


def get_invoice_payment(job_id,task_id):
    try:
        db = get_mongodb_database()
        Collection = db["invoice_payment"]
        start_date, end_date = get_job_details(job_id)
        payload, base_url, headers = get_settings_myob(job_id)

        no_of_records = db["invoice_payment"].count_documents({'job_id':job_id})
        # url = f"{base_url}/Sale/CustomerPayment?$top=1000&$skip={no_of_records}"
        if start_date == "" and end_date == "":
            url = f"{base_url}/Sale/CustomerPayment?$top=1000&$skip={no_of_records}"
        else:
            url = f"{base_url}/Sale/CustomerPayment?$top=1000&$skip={no_of_records}&$filter=Date ge datetime'{start_date[0:10]}' and Date le datetime'{end_date[0:10]}'"
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
     
        JsonResponse1 = JsonResponse["Items"]

        cust = []
        arr = []
        for i in range(0, len(JsonResponse1)):
            if JsonResponse1[i]["Invoices"] != []:
                for j in range(0, len(JsonResponse1[i]["Invoices"])):
                    QuerySet = {}
                    QuerySet["job_id"] = job_id
                    QuerySet["task_id"] = task_id
                    QuerySet['table_name'] = "invoice_payment"
                    QuerySet['error'] = None
                    QuerySet["is_pushed"] = 0
                    QuerySet["Invoice"] = JsonResponse1[i]["Invoices"][j]["Number"]
                    QuerySet["UID"] = JsonResponse1[i]["Invoices"][j]["UID"]
                    QuerySet["paid_amount"] = JsonResponse1[i]["Invoices"][j][
                        "AmountApplied"
                    ]

                    QuerySet["AccName"] = JsonResponse1[i]["Account"]["Name"]
                    QuerySet["AccId"] = JsonResponse1[i]["Account"]["DisplayID"]
                    QuerySet["CreditMemo"] = JsonResponse1[i]["ReceiptNumber"]
                    QuerySet["Date"] = JsonResponse1[i]["Date"]
                    QuerySet["UID"] = JsonResponse1[i]["UID"]
                    QuerySet["customer"] = JsonResponse1[i]["Customer"]["Name"]
                    if QuerySet["customer"] not in cust:
                        cust.append(QuerySet["customer"])

                    arr.append(QuerySet)

        Collection.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            get_invoice_payment(job_id, task_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
