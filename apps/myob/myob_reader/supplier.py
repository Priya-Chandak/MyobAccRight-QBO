import traceback
from ast import Break

import requests

from apps.home.data_util import add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database
from apps.home.data_util import  write_task_execution_step,update_task_execution_status
import sys



def get_supplier(job_id,task_id):
    try:
        dbname = get_mongodb_database()
        Collection = dbname["supplier"]
        payload, base_url, headers = get_settings_myob(job_id)
        no_of_records = dbname["supplier"].count_documents({'job_id':job_id})
        url = f"{base_url}/Contact/Supplier?$top=1000&$skip={no_of_records}"
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        if response.status_code == 200 or response.status_code == 201:
            arr = []
            for i in range(0, len(JsonResponse1)):
                
                QuerySet = {}
                QuerySet["job_id"] = job_id
                QuerySet["task_id"] = task_id
                QuerySet['table_name'] = "supplier"
                QuerySet['error'] = None
                QuerySet["is_pushed"] = 0
                QuerySet["UID"] = JsonResponse1[i]["UID"]
                QuerySet["DisplayID"] = JsonResponse1[i]["DisplayID"]

                if JsonResponse1[i]["IsIndividual"] == True:
                    QuerySet["FirstName"] = JsonResponse1[i]["FirstName"]
                    QuerySet["LastName"] = JsonResponse1[i]["LastName"]
                    if JsonResponse1[i]["FirstName"].endswith(" - S"):
                        QuerySet["DisplayName"] = (
                            QuerySet["FirstName"][:-4] + " " + QuerySet["LastName"][:-4]
                        )
                    else:
                        QuerySet["DisplayName"] = (
                            QuerySet["FirstName"] + " " + QuerySet["LastName"]
                        )

                    QuerySet["CompanyName"] = None
                else:
                    QuerySet["FirstName"] = None
                    QuerySet["LastName"] = None
                    QuerySet["CompanyName"] = JsonResponse1[i]["CompanyName"]

                QuerySet["ABN"] = JsonResponse1[i]["BuyingDetails"]["ABN"]
                QuerySet["BSB"] = JsonResponse1[i]["PaymentDetails"]["BSBNumber"]
                QuerySet["Bank_Acc_no"] = JsonResponse1[i]["PaymentDetails"][
                    "BankAccountNumber"
                ]
                QuerySet["Bank_Acc_Name"] = JsonResponse1[i]["PaymentDetails"][
                    "BankAccountName"
                ]
                QuerySet["Statement_Text"] = JsonResponse1[i]["PaymentDetails"][
                    "StatementText"
                ]

                if JsonResponse1[i]["BuyingDetails"]["ExpenseAccount"] is not None:
                    QuerySet["Expense_Account"] = JsonResponse1[i]["BuyingDetails"][
                        "ExpenseAccount"
                    ]["Name"]
                else:
                    QuerySet["Expense_Account"] = None

                if JsonResponse1[i]["Addresses"] is not None:
                    for j in range(0, len(JsonResponse1[i]["Addresses"])):
                        QuerySet["city"] = JsonResponse1[i]["Addresses"][0]["City"]
                        QuerySet["Country"] = JsonResponse1[i]["Addresses"][0]["Country"]
                        QuerySet["State"] = JsonResponse1[i]["Addresses"][0]["State"]
                        QuerySet["PostCode"] = JsonResponse1[i]["Addresses"][0]["PostCode"]
                        QuerySet["Email"] = JsonResponse1[i]["Addresses"][0]["Email"]
                        QuerySet["Fax"] = JsonResponse1[i]["Addresses"][0]["Fax"]
                        QuerySet["Website"] = JsonResponse1[i]["Addresses"][0]["Website"]
                        QuerySet["Contact_Person"] = JsonResponse1[i]["Addresses"][0][
                            "ContactName"
                        ]
                        QuerySet["Phone"] = JsonResponse1[i]["Addresses"][0]["Phone1"]

                else:
                    QuerySet["city"] = None
                    QuerySet["Country"] = None
                    QuerySet["State"] = None
                    QuerySet["PostCode"] = None
                    QuerySet["Email"] = None
                    QuerySet["Website"] = None
                    QuerySet["Contact_Person"] = None
                    QuerySet["Phone"] = None
                    QuerySet["Fax"] = None

                arr.append(QuerySet)

            Collection.insert_many(arr)

            if JsonResponse["NextPageLink"] is not None:
                get_supplier(job_id, task_id)

            else:
                Break

            step_name = "Reading data from myob supplier"
            write_task_execution_step(task_id, status=1, step=step_name)
        
        else:
            step_name = f"No Data Fetched due to response error code - {response.status_code}"
            write_task_execution_step(task_id, status=0, step=step_name)
        
    except Exception as ex:
        import traceback
        traceback.print_exc()
        
