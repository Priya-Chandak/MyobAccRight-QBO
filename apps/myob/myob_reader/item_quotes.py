import traceback
from ast import Break

import requests
from sqlalchemy.orm import aliased

from apps.home.data_util import add_job_status
from apps.home.models import Jobs, Tool
from apps.mmc_settings.post_myob import post_myob_settings
from apps.myconstant import *
from apps.util.db_mongo import get_mongodb_database


def get_item_quote(job_id):
    try:
        db = get_mongodb_database()
        Collection = db["item_quote"]
        no_of_records = db["item_quote"].count_documents({})
        tool1 = aliased(Tool)
        tool2 = aliased(Tool)

        jobs, input_tool, output_tool = (
            db.session.query(
                Jobs,
                tool1.account_type.label("input_tool"),
                tool2.account_type.label("output_tool"),
            )
            .join(tool1, Jobs.input_account_id == tool1.id)
            .join(tool2, Jobs.output_account_id == tool2.id)
            .filter(Jobs.id == job_id)
            .first()
        )
        if input_tool == MYOB:
            payload, base_url, headers = get_settings_myob(job_id)

        elif output_tool == MYOB:
            payload, base_url, headers = post_myob_settings(job_id)

        url = f"{base_url}/Sale/Quote/Item?$top=1000&$skip={no_of_records}"
        response = requests.request("GET", url, headers=headers, data=payload)
        JsonResponse = response.json()
        JsonResponse1 = JsonResponse["Items"]

        arr = []
        for i in range(0, len(JsonResponse1)):
            QuerySet = {"Line": []}
            QuerySet["job_id"] = job_id
            QuerySet["Number"] = JsonResponse1[i]["Number"]
            QuerySet["Date"] = JsonResponse1[i]["Date"]
            QuerySet["Customer"] = JsonResponse1[i]["Customer"]["Name"]
            QuerySet["IsTaxInclusive"] = JsonResponse1[i]["IsTaxInclusive"]
            QuerySet["Subtotal"] = JsonResponse1[i]["Subtotal"]
            QuerySet["TotalTax"] = JsonResponse1[i]["TotalTax"]
            QuerySet["TotalAmount"] = JsonResponse1[i]["TotalAmount"]
            QuerySet["TotalAmount"] = JsonResponse1[i]["TotalAmount"]
            QuerySet["Comment"] = JsonResponse1[i]["Comment"]
            QuerySet["JournalMemo"] = JsonResponse1[i]["JournalMemo"]
            QuerySet["JournalMemo"] = JsonResponse1[i]["JournalMemo"]
            QuerySet["BalanceDueAmount"] = JsonResponse1[i]["BalanceDueAmount"]

            for j in range(0, len(JsonResponse1[i]["Lines"])):
                QuerySet1 = {}
                QuerySet1["ShipQuantity"] = JsonResponse1[i]["Lines"][j]["ShipQuantity"]
                QuerySet1["UnitPrice"] = JsonResponse1[i]["Lines"][j]["UnitPrice"]
                QuerySet1["UnitCount"] = JsonResponse1[i]["Lines"][j]["UnitCount"]
                QuerySet1["DiscountPercent"] = JsonResponse1[i]["Lines"][j][
                    "DiscountPercent"
                ]
                QuerySet1["Total"] = JsonResponse1[i]["Lines"][j]["Total"]
                QuerySet1["Item_Name"] = JsonResponse1[i]["Lines"][j]["Item"]["Name"]
                QuerySet1["Acc_Name"] = JsonResponse1[i]["Lines"][j]["account"]["Name"]

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
            get_item_quote(job_id)

        else:
            Break

    except Exception as ex:
        traceback.print_exc()
        
