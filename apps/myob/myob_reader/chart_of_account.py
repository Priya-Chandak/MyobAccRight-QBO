import traceback
from ast import Break

import requests

from apps.home.data_util import add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database
from apps.home.data_util import  write_task_execution_step,update_task_execution_status
import sys



def get_chart_of_account(job_id,task_id):
    try:
        dbname = get_mongodb_database()
        Collection = dbname["chart_of_account"]
        no_of_records = dbname["chart_of_account"].count_documents({'job_id':job_id})
        payload, base_url, headers = get_settings_myob(job_id)

        url = f"{base_url}/GeneralLedger/Account?$top=1000&$skip={no_of_records}"
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            JsonResponse = response.json()
            JsonResponse1 = JsonResponse["Items"]
            if len(JsonResponse["Items"])>0:

                arr = []
                for i in range(0, len(JsonResponse1)):
                    QuerySet = {"job_id": job_id,"task_id": task_id,"is_pushed":0,"table_name":"chart_of_account", "Account_Type": JsonResponse1[i]["Type"], "UID": JsonResponse1[i]["UID"],
                                "payload":None,"Name": JsonResponse1[i]["Name"],"error":None, "Detail_Type": JsonResponse1[i]["Type"],
                                "Description": JsonResponse1[i]["Description"], "DisplayId": JsonResponse1[i]["DisplayID"],"Number": JsonResponse1[i]["Number"],
                                "IsActive": JsonResponse1[i]["IsActive"], "IsHeader": JsonResponse1[i]["IsHeader"],
                                "RowVersion": JsonResponse1[i]["RowVersion"]}
                        
                    if JsonResponse1[i]["ParentAccount"] is not None:
                        QuerySet["ParentAccount"] = JsonResponse1[i]["ParentAccount"]
                    else:
                        QuerySet["ParentAccount"] = None

                    # if JsonResponse1[i]['TaxCode'] is not None:
                    #     QuerySet['Tax_Code'] = JsonResponse1[i]['TaxCode']['Code']
                    # else:
                    #     QuerySet['Tax_Code'] = None

                    if JsonResponse1[i]["TaxCode"] is not None:
                        QuerySet["TaxCode"] = JsonResponse1[i]["TaxCode"]
                    else:
                        QuerySet["TaxCode"] = None

                    if JsonResponse1[i]["IsActive"] == True:
                        arr.append(QuerySet)

                Collection.insert_many(arr)

                if JsonResponse["NextPageLink"] is not None:
                    url = JsonResponse["NextPageLink"]
                    get_chart_of_account(job_id, task_id)
                else:
                    Break

                step_name = "Reading data from myob chart of account"
                write_task_execution_step(task_id, status=1, step=step_name)
            
    except Exception as ex:
        print("------------------------------")
        step_name = "Access token not valid"
        write_task_execution_step(task_id, status=0, step=step_name)
        update_task_execution_status( task_id, status=0, task_type="write")
        import traceback
        traceback.print_exc()
        print(ex)
        sys.exit(0)
        