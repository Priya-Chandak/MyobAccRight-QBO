import traceback
from datetime import datetime

import requests
from flask import session

from apps import db
from apps.home.models import Jobs
from apps.home.models import Tool, ToolSettings,MYOBACCOUNTRIGHTQboTokens


def get_myob_settings(job_id):
    try:
        
        payload={}
        headers = {
        'x-myobapi-version': 'v2',
        'Authorization': 'Basic QWRtaW5pc3RyYXRvcjo='
        }

        data1 = db.session.query(MYOBACCOUNTRIGHTQboTokens).filter(MYOBACCOUNTRIGHTQboTokens.job_id == job_id).first()

        # keys = (
        #     db.session.query(Jobs, ToolSettings.keys, ToolSettings.values, ToolSettings.added_on, ToolSettings.id)
        #     .join(Tool, Jobs.input_account_id == Tool.id)
        #     .join(ToolSettings, ToolSettings.tool_id == Tool.id)
        #     .filter(Jobs.id == job_id)
        #     .all()
        # )
        
        base_url = f"http://localhost:8080/AccountRight/{data1.Myob_company_id}/"

        return payload, base_url, headers
        
    except Exception as ex:
        traceback.print_exc()
