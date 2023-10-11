# import traceback

# from apps import db
# from apps.home.data_util import add_job_status
# from apps.home.models import Jobs
# from apps.home.models import Tool, ToolSettings


# def get_qbo_settings(job_id):
#     try:
#         keys = (
#             db.session.query(Jobs, ToolSettings.keys, ToolSettings.values)
#                 .join(Tool, Jobs.input_account_id == Tool.id)
#                 .join(ToolSettings, ToolSettings.tool_id == Tool.id)
#                 .filter(Jobs.id == job_id)
#                 .all()
#         )
#         for row in keys:
#             if row[1] == "client_id":
#                 client_id = row[2]
#             if row[1] == "client_secret":
#                 client_secret = row[2]
#             if row[1] == "base_url":
#                 base_url1 = row[2]
#             if row[1] == "company_id":
#                 company_id = row[2]
#             if row[1] == "minor_version":
#                 minorversion = row[2]
#             if row[1] == "user_agent":
#                 UserAgent = row[2]
#             if row[1] == "access_token":
#                 access_token = row[2]
#             if row[1] == "refresh_token":
#                 refresh_token = row[2]

#         base_url = f"{base_url1}/v3/company/{company_id}"
#         headers = {
#             "User-Agent": "QBOV3-OAuth2-Postman-Collection",
#             "Accept": "application/json",
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer {access_token}",
#         }

#         get_data_header = {
#             "User-Agent": "QBOV3-OAuth2-Postman-Collection",
#             "Accept": "application/json",
#             "Content-Type": "application/text",
#             "Authorization": f"Bearer {access_token}",
#         }

#         report_headers = {
#             "User-Agent": "QBOV3-OAuth2-Postman-Collection",
#             "Accept": "application/json",
#             "Authorization": f"Bearer {access_token}",
#         }

#         return (
#             base_url,
#             headers,
#             company_id,
#             minorversion,
#             get_data_header,
#             report_headers,
#         )

#     except Exception as ex:
#         traceback.print_exc()
#         


import traceback
import requests

from apps import db
from apps.home.data_util import add_job_status
from apps.home.models import Jobs
from apps.home.models import Tool, ToolSettings
import base64



def get_qbo_settings(job_id):
    try:
        url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
       
        if "refresh_token" in session:
            refresh_token1=session["refresh_token"]
            company_id=session["company_id"]
            minorversion=14
            base_url1="https://sandbox-quickbooks.api.intuit.com"
            redirect_uri="https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl"

            payload=f'grant_type=refresh_token&refresh_token={refresh_token1}&redirect_uri={redirect_uri}'

            CLIENT_ID = "ABpWOUWtcEG1gCun5dQbQNfc7dvyalw5qVF97AkJQcn5Lh09o6"
            CLIENT_SECRET="LepyjXTADW592Dq5RYUP8UbGLcH5xtqDQhrf2xJN"
            clientIdSecret = CLIENT_ID + ':' + CLIENT_SECRET
            encoded_u = base64.b64encode(clientIdSecret.encode()).decode()
            auth_code = "%s" % encoded_u
            # print(auth_code)

            headers = {
                'Authorization': "Basic" "  "+  f'{auth_code}',
                'Content-Type': 'application/x-www-form-urlencoded'
                }

            response = requests.request("POST", url, headers=headers, data=payload)
            re = response.json()
            access_token1 = re["access_token"]
            
            base_url = f"{base_url1}/v3/company/{company_id}"
            headers = {
                "User-Agent": "QBOV3-OAuth2-Postman-Collection",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token1}",
            }

            get_data_header = {
                "User-Agent": "QBOV3-OAuth2-Postman-Collection",
                "Accept": "application/json",
                "Content-Type": "application/text",
                "Authorization": f"Bearer {access_token1}",
            }

            report_headers = {
                "User-Agent": "QBOV3-OAuth2-Postman-Collection",
                "Accept": "application/json",
                "Authorization": f"Bearer {access_token1}",
            }

            return (
                base_url,
                headers,
                company_id,
                minorversion,
                get_data_header,
                report_headers,
            )

    except Exception as ex:
        traceback.print_exc()
        
