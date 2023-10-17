import base64
import traceback

import requests

from apps import db
from apps.home.models import Jobs
from apps.home.models import Tool, ToolSettings,MYOBACCOUNTRIGHTQboTokens


def post_qbo_settings(job_id):
    try:
        url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
        data1 = db.session.query(MYOBACCOUNTRIGHTQboTokens).filter(MYOBACCOUNTRIGHTQboTokens.job_id == job_id).first()

        redirect_uri = 'http://localhost:5000/data_access'
        base_url1="https://sandbox-quickbooks.api.intuit.com"
        minorversion=14
        company_id=data1.qbo_company_id
        payload = f'grant_type=refresh_token&refresh_token={data1.qbo_refresh_token}&redirect_uri={redirect_uri}'
        CLIENT_ID = 'ABpWOUWtcEG1gCun5dQbQNfc7dvyalw5qVF97AkJQcn5Lh09o6'
        CLIENT_SECRET = 'LepyjXTADW592Dq5RYUP8UbGLcH5xtqDQhrf2xJN'
        clientIdSecret = CLIENT_ID + ':' + CLIENT_SECRET
        encoded_u = base64.b64encode(clientIdSecret.encode()).decode()
        auth_code = "%s" % encoded_u

        headers = {
            'Authorization': "Basic" "  " + f'{auth_code}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        re = response.json()
        access_token1 = re["access_token"]

        base_url = f"{base_url1}/v3/company/{data1.qbo_company_id}"
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