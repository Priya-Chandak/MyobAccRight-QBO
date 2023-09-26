import traceback
from ast import Break

import requests

from apps.home.data_util import get_job_details, add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_professional_bill(job_id,task_id):
    try:
        start_date, end_date = get_job_details(job_id)
        db = get_mongodb_database()
        payload, base_url, headers = get_settings_myob(job_id)
        no_of_records = db["professional_bill"].count_documents({})
        Collection = db["professional_bill"]

        if start_date == "" and end_date == "":
            url = (
                f"{base_url}/Purchase/Bill/Professional?$top=1000&$skip={no_of_records}"
            )
        else:
            url = f"{base_url}/Purchase/Bill/Professional?$top=1000&$skip={no_of_records}&$filter=Date ge datetime'{start_date[0:10]}' and Date le datetime'{end_date[0:10]}'"

        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        arr = []
        for i in range(0, len(JsonResponse1)):
            QuerySet = {}
            QuerySet["job_id"] = job_id
            QuerySet["task_id"] = task_id
            QuerySet['table_name'] = "professional_bill"
            QuerySet['error'] = None
            QuerySet["is_pushed"] = 0
            QuerySet["UID"] = JsonResponse1[i]["UID"]

            for j in range(0, len(JsonResponse1[i]["Lines"])):
                QuerySet["Account_Name"] = JsonResponse1[i]["Lines"][j]["account"][
                    "Name"
                ]
                QuerySet["DisplayID"] = JsonResponse1[i]["Lines"][j]["account"][
                    "DisplayID"
                ]

                QuerySet["Job"] = JsonResponse1[i]["Lines"][j]["Job"]

                if JsonResponse1[i]["Lines"][j]["TaxCode"] is not None:
                    QuerySet["Tax_Code"] = JsonResponse1[i]["Lines"][j]["TaxCode"][
                        "Code"
                    ]
                else:
                    QuerySet["Tax_Code"] = None

            # QuerySet['Total_Amount'] = JsonResponse1[i]['Subtotal']

            arr.append(QuerySet)

        Collection.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            get_professional_bill(job_id, task_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
