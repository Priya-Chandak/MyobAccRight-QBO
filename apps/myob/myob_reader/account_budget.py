import traceback
from ast import Break

import requests

from apps.home.data_util import add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_account_budget(job_id):
    try:
        dbname = get_mongodb_database()
        Collection = dbname["account_budget"]

        payload, base_url, headers = get_settings_myob(job_id)
        no_of_records = dbname["account_budget"].count_documents({})
        url = f"{base_url}/GeneralLedger/AccountBudget?$top=100&$skip={no_of_records}"
        add_job_status(job_id, "account_budget")
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]
        arr = []

        for i in range(0, len(JsonResponse1)):
            QuerySet = {}
            QuerySet["Job_ID"] = job_id
            QuerySet["UID"] = JsonResponse1[i]["UID"]
            QuerySet["Description"] = JsonResponse1[i]["Description"]
            QuerySet["Number"] = JsonResponse1[i]["Number"]
            QuerySet["Name"] = JsonResponse1[i]["Name"]
            QuerySet["AssetAccount"] = JsonResponse1[i]["AssetAccount"]
            QuerySet["ExpenseAccount"] = JsonResponse1[i]["ExpenseAccount"]
            QuerySet["IncomeAccount"] = JsonResponse1[i]["IncomeAccount"]
            QuerySet["Is_Tax_Inclusive"] = JsonResponse1[i]["SellingDetails"][
                "IsTaxInclusive"
            ]
            QuerySet["Quantity_On_Hand"] = JsonResponse1[i]["QuantityOnHand"]
            QuerySet["LastModified"] = JsonResponse1[i]["LastModified"]
            QuerySet["AverageCost"] = JsonResponse1[i]["AverageCost"]
            QuerySet["BaseSellingPrice"] = JsonResponse1[i]["BaseSellingPrice"]

            if JsonResponse1[i]["QuantityOnHand"] > 0:
                QuerySet["TrackQtyOnHand"] = True
            else:
                QuerySet["TrackQtyOnHand"] = False

            if JsonResponse1[i]["AssetAccount"] is not None:
                QuerySet["Asset_Account_ID"] = JsonResponse1[i]["AssetAccount"]["UID"]
                QuerySet["Asset_Account_Name"] = JsonResponse1[i]["AssetAccount"][
                    "Name"
                ]
            else:
                pass

            if JsonResponse1[i]["IncomeAccount"] is not None:
                QuerySet["Income_Account_ID"] = JsonResponse1[i]["IncomeAccount"]["UID"]
                QuerySet["Income_Account_Name"] = JsonResponse1[i]["IncomeAccount"][
                    "Name"
                ]
            else:
                pass

            if JsonResponse1[i]["CostOfSalesAccount"] is not None:
                QuerySet["Expense_Account_ID"] = JsonResponse1[i]["CostOfSalesAccount"][
                    "UID"
                ]
                QuerySet["Expense_Account_Name"] = JsonResponse1[i][
                    "CostOfSalesAccount"
                ]["Name"]

            arr.append(QuerySet)
        Collection.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            get_account_budget(job_id)

        else:
            Break

        add_job_status(job_id, "account_budget", started_or_complete="complete")

    except Exception as ex:
        traceback.print_exc()
        
