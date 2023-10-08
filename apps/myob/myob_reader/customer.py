import traceback
from ast import Break

import requests
from apps.home.data_util import update_task_execution_status, write_task_execution_step


from apps.home.data_util import add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database



def get_customer(job_id,task_id):
    try:
        dbname = get_mongodb_database()
        Collection = dbname["customer"]
        payload, base_url, headers = get_settings_myob(job_id)

        no_of_records = dbname["customer"].count_documents({'job_id':job_id})
        url = f"{base_url}/Contact/Customer?$top=1000&$skip={no_of_records}"
        print(url)
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]
        print(len(JsonResponse1))

        if response.status_code == 200 or response.status_code == 201:
        
            arr = []
            for i in range(0, len(JsonResponse1)):
                QuerySet = {}
                QuerySet["job_id"] = job_id
                QuerySet["task_id"] = task_id
                QuerySet['table_name'] = "customer"
                QuerySet['error'] = None
                QuerySet["is_pushed"] = 0
                            
                QuerySet["UID"] = JsonResponse1[i]["UID"]
                QuerySet["Display_ID"] = JsonResponse1[i]["DisplayID"]

                if JsonResponse1[i]["IsIndividual"] == True:
                    QuerySet["FirstName"] = JsonResponse1[i]["FirstName"]
                    QuerySet["LastName"] = JsonResponse1[i]["LastName"]

                    if JsonResponse1[i]["FirstName"].endswith(" - C"):
                        QuerySet["DisplayName"] = (
                            QuerySet["FirstName"][:-4] + " " + QuerySet["LastName"][:-4]
                        )
                    else:
                        QuerySet["DisplayName"] = (
                            QuerySet["FirstName"] + " " + QuerySet["LastName"]
                        )

                    QuerySet.update({"Company_Name": None})
                else:
                    QuerySet.update({"Company_Name": JsonResponse1[i]["CompanyName"]})
                    QuerySet.update({"First_Name": None})
                    QuerySet.update({"Last_Name": None})

                QuerySet["Notes"] = JsonResponse1[i]["Notes"]

                if "Addresses" in JsonResponse["Items"][i]:
                    if not JsonResponse1[i]["Addresses"]:
                        QuerySet["Addresses"] = None
                    else:
                        QuerySet["Addresses"] = JsonResponse1[i]["Addresses"]

                arr.append(QuerySet)

            Collection.insert_many(arr)

            if JsonResponse["NextPageLink"] is not None:
                get_customer(job_id, task_id)

            else:
                Break

            step_name = "Reading data from myob customer"
            write_task_execution_step(task_id, status=1, step=step_name)
        
        else:
            step_name = f"No Data Fetched due to response error code - {response.status_code}"
            write_task_execution_step(task_id, status=0, step=step_name)
            

    except Exception as ex:
        import traceback
        traceback.print_exc()
        
