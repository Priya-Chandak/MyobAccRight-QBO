import traceback
from ast import Break

import requests

from apps.home.data_util import add_job_status
from apps.mmc_settings.all_settings import *
from apps.util.db_mongo import get_mongodb_database


def get_item_purchase_order(job_id):
    try:
        db = get_mongodb_database()
        Collection = db["item_purchase_order"]
        no_of_records = db["item_purchase_order"].count_documents({})
        payload, base_url, headers = get_settings_myob(job_id)

        url = f"{base_url}/Purchase/Order/Item?$top=1000&$skip={no_of_records}"
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        arr = []
        for i in range(0, len(JsonResponse1)):
            QuerySet = {
                "Line": [],
                "job_id": job_id,
                "Number": JsonResponse1[i]["Number"],
                "Date": JsonResponse1[i]["Date"],
                "Supplier": JsonResponse1[i]["Supplier"]["Name"],
                "IsTaxInclusive": JsonResponse1[i]["IsTaxInclusive"],
                "Subtotal": JsonResponse1[i]["Subtotal"],
                "TotalTax": JsonResponse1[i]["TotalTax"],
                "TotalAmount": JsonResponse1[i]["TotalAmount"],
                "Comment": JsonResponse1[i]["Comment"],
                "JournalMemo": JsonResponse1[i]["JournalMemo"],
                "BalanceDueAmount": JsonResponse1[i]["BalanceDueAmount"],
            }

            for j in range(0, len(JsonResponse1[i]["Lines"])):
                QuerySet1 = {
                    "BillQuantity": JsonResponse1[i]["Lines"][j]["BillQuantity"],
                    "UnitPrice": JsonResponse1[i]["Lines"][j]["UnitPrice"],
                    "ReceivedQuantity": JsonResponse1[i]["Lines"][j][
                        "ReceivedQuantity"
                    ],
                    "DiscountPercent": JsonResponse1[i]["Lines"][j]["DiscountPercent"],
                    "Total": JsonResponse1[i]["Lines"][j]["Total"],
                }

                if JsonResponse1[i]["Lines"][j]["Item"] is not None:
                    QuerySet1["Item_Name"] = JsonResponse1[i]["Lines"][j]["Item"][
                        "Name"
                    ]

                if "account" in JsonResponse1[i]["Lines"][j]:
                    QuerySet1["Acc_Name"] = JsonResponse1[i]["Lines"][j]["account"][
                        "Name"
                    ]

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
            get_item_purchase_order(job_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
