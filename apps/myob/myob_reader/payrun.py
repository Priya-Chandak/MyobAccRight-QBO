import traceback
from ast import Break

import requests

from apps.home.data_util import get_job_details, add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_payrun(job_id):
    try:
        start_date, end_date = get_job_details(job_id)
        db = get_mongodb_database()
        journal_transaction = db["journal_transaction"]
        employee_payroll_advice = db["employee_payroll_advice"]

        payload, base_url, headers = get_settings_myob(job_id)
        no_of_records1 = db["journal_transaction"].count_documents({})
        no_of_records2 = db["employee_payroll_advice"].count_documents({})

        if start_date == "" and end_date == "":
            url1 = f"{base_url}/GeneralLedger/JournalTransaction"
        else:
            url1 = f"{base_url}/GeneralLedger/JournalTransaction?$filter=DateOccurred ge datetime'{start_date[0:10]}' and DateOccurred le datetime'{end_date[0:10]}'"

        url2 = f"{base_url}/Report/Payroll/EmployeePayrollAdvice"

        response1 = requests.request("GET", url1, headers=headers, data=payload)
        JsonResponse11 = response1.json()
        JsonResponse1 = JsonResponse11["Items"]

        response2 = requests.request("GET", url2, headers=headers, data=payload)
        JsonResponse22 = response2.json()
        JsonResponse2 = JsonResponse22["Items"]

        chart_of_account1 = db["chart_of_account"].find({"job_id": job_id})

        chart_of_account = []
        for p1 in chart_of_account1:
            chart_of_account.append(p1)

        arr1 = []
        arr2 = []

        for i in range(0, len(JsonResponse1)):
            arr1.append(JsonResponse1[i])
        journal_transaction.insert_many(arr1)

        for j in range(0, len(JsonResponse2)):
            arr2.append(JsonResponse2[j])
        employee_payroll_advice.insert_many(arr2)

        if JsonResponse11["NextPageLink"] is not None:
            get_payrun(job_id)
        else:
            Break

        if JsonResponse22["NextPageLink"] is not None:
            get_payrun(job_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
