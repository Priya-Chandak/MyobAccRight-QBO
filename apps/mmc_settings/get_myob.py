import traceback
from datetime import datetime

import requests

from apps import db
from apps.home.models import Jobs
from apps.home.models import Tool, ToolSettings


def get_myob_settings(job_id):
    try:
        
        payload={}
        headers = {
        'x-myobapi-version': 'v2',
        'Authorization': 'Basic QWRtaW5pc3RyYXRvcjo='
        }

        keys = (
            db.session.query(Jobs, ToolSettings.keys, ToolSettings.values, ToolSettings.added_on, ToolSettings.id)
            .join(Tool, Jobs.input_account_id == Tool.id)
            .join(ToolSettings, ToolSettings.tool_id == Tool.id)
            .filter(Jobs.id == job_id)
            .all()
        )

        for row in keys:
            if row[1] == "company_file_id":
                company_file_id = row[2]
        
        base_url = f"http://localhost:8080/AccountRight/{company_file_id}/"

        return payload, base_url, headers
        
    except Exception as ex:
        traceback.print_exc()
