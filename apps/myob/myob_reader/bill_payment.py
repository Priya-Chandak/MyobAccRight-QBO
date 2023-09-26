import traceback
from ast import Break

import requests

from apps.home.data_util import get_job_details, add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


# myclient = MongoClient("mongodb://localhost:27017/")
# db = myclient["MMC"]
# bill_payment = db['bill_payment']

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
#             if JsonResponse1[i]['Items'] != []:
#                 QuerySet={}
#                 QuerySet['Invoice']=JsonResponse1[i]['Items'][0]['Sale']['Number']
#                 QuerySet['CreditMemo']=JsonResponse1[i]['CreditFromInvoice']['Number']
#                 QuerySet['paid_amount'] = JsonResponse1[i]['Items'][0]['AmountApplied']
#                 QuerySet['customer']=JsonResponse1[i]['Customer']['Name']

#                 arr.append(QuerySet)

#         print(arr)

#         bill_payment.insert_many(arr)

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


def get_bill_payment(job_id,task_id):
    try:
        start_date, end_date = get_job_details(job_id)
        payload, base_url, headers = get_settings_myob(job_id)
        dbname = get_mongodb_database()

        bill_payment = dbname["bill_payment"]
        no_of_records = dbname["bill_payment"].count_documents({'job_id':job_id})

        if start_date == "" and end_date == "":
            url = f"{base_url}/Purchase/SupplierPayment?$top=1000&$skip={no_of_records}"

        else:
            url = f"{base_url}/Purchase/SupplierPayment?$top=1000&$skip={no_of_records}&$filter=Date ge datetime'{start_date[0:10]}' and Date le datetime'{end_date[0:10]}'"
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]
        arr = []
        for i in range(0, len(JsonResponse1)):
            if JsonResponse1[i]["Lines"] != []:
                for i1 in range(0, len(JsonResponse1[i]["Lines"])):
                    QuerySet = {"Line": []}
                    QuerySet["job_id"] = job_id
                    QuerySet["task_id"] = task_id
                    QuerySet['table_name'] = "bill_payment"
                    QuerySet['error'] = None
                    QuerySet['UID'] =JsonResponse1[i]["UID"]
                    QuerySet["is_pushed"] = 0
                    QuerySet["AccName"] = JsonResponse1[i]["Account"]["Name"]
                    QuerySet["AccId"] = JsonResponse1[i]["Account"]["DisplayID"]
                    QuerySet["CreditMemo"] = JsonResponse1[i]["PaymentNumber"]
                    QuerySet["Date"] = JsonResponse1[i]["Date"]
                    QuerySet["Memo"] = JsonResponse1[i]["Memo"]
                    QuerySet["supplier"] = JsonResponse1[i]["Supplier"]["Name"]
                    QuerySet1 = {}
                    QuerySet1["Type"] = JsonResponse1[i]["Lines"][i1]["Type"]
                    QuerySet1["UID"] = JsonResponse1[i]["Lines"][i1]["Purchase"]["UID"]
                    QuerySet1["Invoice"] = JsonResponse1[i]["Lines"][i1]["Purchase"][
                        "Number"
                    ]
                    QuerySet1["paid_amount"] = JsonResponse1[i]["Lines"][i1][
                        "AmountApplied"
                    ]
                    QuerySet["Line"].append(QuerySet1)

                    arr.append(QuerySet)

        bill_payment.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            get_bill_payment(job_id, task_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
