import traceback
from ast import Break

import requests

from apps.home.data_util import add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_service_purchase_order(job_id):
    try:
        db = get_mongodb_database()
        Collection = db["service_purchase_order"]
        no_of_records = db["service_purchase_order"].count_documents({})
        payload, base_url, headers = get_settings_myob(job_id)
        url = f"{base_url}/Purchase/Order/Service?$top=1000&$skip={no_of_records}"
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        arr = []
        for i in range(0, len(JsonResponse1)):
            if JsonResponse1[i]["Status"] == "Open":
                QuerySet = {"Line": []}
                QuerySet["job_id"] = job_id
                QuerySet["Number"] = JsonResponse1[i]["Number"]
                QuerySet["Date"] = JsonResponse1[i]["Date"]
                QuerySet["Supplier"] = JsonResponse1[i]["Supplier"]["Name"]
                QuerySet["IsTaxInclusive"] = JsonResponse1[i]["IsTaxInclusive"]
                QuerySet["Subtotal"] = JsonResponse1[i]["Subtotal"]
                QuerySet["TotalTax"] = JsonResponse1[i]["TotalTax"]
                QuerySet["TotalAmount"] = JsonResponse1[i]["TotalAmount"]
                QuerySet["TotalAmount"] = JsonResponse1[i]["TotalAmount"]
                QuerySet["Comment"] = JsonResponse1[i]["Comment"]
                QuerySet["JournalMemo"] = JsonResponse1[i]["JournalMemo"]
                QuerySet["BalanceDueAmount"] = JsonResponse1[i]["BalanceDueAmount"]

                for j in range(0, len(JsonResponse1[i]["Lines"])):
                    QuerySet1 = {}
                    QuerySet1["Total"] = JsonResponse1[i]["Lines"][j]["Total"]
                    QuerySet1["Description"] = JsonResponse1[i]["Lines"][j][
                        "Description"
                    ]

                    if "account" in JsonResponse1[i]["Lines"][j]:
                        QuerySet1["Acc_Name"] = JsonResponse1[i]["Lines"][j]["account"][
                            "Name"
                        ]
                        QuerySet1["Acc_Display_ID"] = JsonResponse1[i]["Lines"][j][
                            "account"
                        ]["DisplayID"]

                    if JsonResponse1[i]["Lines"][j]["TaxCode"] is not None:
                        QuerySet1["taxcode"] = JsonResponse1[i]["Lines"][j]["TaxCode"][
                            "Code"
                        ]
                    else:
                        QuerySet1["taxcode"] = None

                    if JsonResponse1[i]["Lines"][j]["Job"] is not None:
                        QuerySet1["Job"] = JsonResponse1[i]["Lines"][j]["Job"]["Name"]
                    else:
                        QuerySet1["Job"] = None

                    QuerySet["Line"].append(QuerySet1)

                arr.append(QuerySet)

        Collection.insert_many(arr)

        if JsonResponse["NextPageLink"] is not None:
            url = JsonResponse["NextPageLink"]
            get_service_purchase_order(job_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
