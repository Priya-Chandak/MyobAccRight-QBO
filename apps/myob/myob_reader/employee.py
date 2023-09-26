import traceback
from ast import Break

import requests

from apps.home.data_util import add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_employee(job_id,task_id):
    try:
        db = get_mongodb_database()
        no_of_records = db["employee"].count_documents({})
        payload, base_url, headers = get_settings_myob(job_id)

        url1 = f"{base_url}/Contact/Employee/?$top=100&$skip={no_of_records}"
        url2 = f"{base_url}/Payroll/Timesheet/?$top=100&$skip={no_of_records}"
        url3 = (
            f"{base_url}/Contact/EmployeePayrollDetails/?$top=100&$skip={no_of_records}"
        )
        Collection = db["employee"]
        response1 = requests.request("GET", url1, headers=headers, data=payload)
        response2 = requests.request("GET", url2, headers=headers, data=payload)
        response3 = requests.request("GET", url3, headers=headers, data=payload)

        JsonResponse1 = response1.json()
        JsonResponse2 = response2.json()
        JsonResponse3 = response3.json()

        arr = []
        for i in range(0, len(JsonResponse1["Items"])):
            if JsonResponse1["Items"][i]['IsActive'] == True:
                QuerySet = {}
                QuerySet["job_id"] = job_id
                QuerySet["task_id"] = task_id
                QuerySet['table_name'] = "employee"
                QuerySet['error'] = None
                QuerySet["is_pushed"] = 0
                QuerySet["is_active"] = JsonResponse1["Items"][i]['IsActive']
                QuerySet["Employee_ID"] = JsonResponse1["Items"][i]["DisplayID"]
                QuerySet["Employee_ID_Number"] = JsonResponse1["Items"][i]["UID"]

                for i3 in range(0, len(JsonResponse2["Items"])):
                    if (
                        JsonResponse1["Items"][i]["DisplayID"]
                        == JsonResponse2["Items"][i3]["Employee"]["DisplayID"]
                    ):
                        QuerySet["Start_Date"] = JsonResponse2["Items"][i3]["StartDate"]
                        QuerySet["End_Date"] = JsonResponse2["Items"][i3]["EndDate"]

                for i1 in range(0, len(JsonResponse3["Items"])):
                    if (
                        JsonResponse1["Items"][i]["DisplayID"]
                        == JsonResponse3["Items"][i1]["Employee"]["DisplayID"]
                    ):
                        if JsonResponse3["Items"][i1]["DateOfBirth"] is not None:
                            QuerySet["Birth_Date"] = JsonResponse3["Items"][i1][
                                "DateOfBirth"
                            ]
                        else:
                            QuerySet["Birth_Date"] = None

                if JsonResponse3["Items"][i]["Gender"] is not None:
                    QuerySet["Gender"] = JsonResponse3["Items"][i]["Gender"]
                else:
                    QuerySet["Gender"] = None

                QuerySet["Notes"] = JsonResponse1["Items"][i]["Notes"]

                if JsonResponse1["Items"][i]["IsIndividual"] == True:
                    QuerySet["FirstName"] = JsonResponse1["Items"][i]["FirstName"]
                    QuerySet["LastName"] = JsonResponse1["Items"][i]["LastName"]
                    QuerySet["Company_Name"] = None
                else:
                    QuerySet["Company_Name"] = JsonResponse1["Items"][i]["CompanyName"]
                    QuerySet["FirstName"] = None
                    QuerySet["LastName"] = None

                if JsonResponse1["Items"][i]["TimeBillingDetails"] is not None:
                    QuerySet["Cost_Per_Hour"] = JsonResponse1["Items"][i][
                        "TimeBillingDetails"
                    ]["CostPerHour"]
                    QuerySet["EmployeeBillingRateExcludingTax"] = JsonResponse1["Items"][i][
                        "TimeBillingDetails"
                    ]["EmployeeBillingRateExcludingTax"]
                else:
                    QuerySet["Cost_Per_Hour"] = None
                    QuerySet["EmployeeBillingRateExcludingTax"] = None

                if "Addresses" in JsonResponse1["Items"][i]:
                    if not JsonResponse1["Items"][i]["Addresses"]:
                        QuerySet["Addresses"] = None
                    else:
                        QuerySet["Addresses"] = JsonResponse1["Items"][i]["Addresses"]
                
                arr.append(QuerySet)

            Collection.insert_many(arr)

        if JsonResponse1["NextPageLink"] is not None:
            get_employee(job_id, task_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
