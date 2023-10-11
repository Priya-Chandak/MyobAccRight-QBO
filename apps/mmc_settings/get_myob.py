import traceback
from datetime import datetime

import requests
from flask import session

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

        # keys = (
        #     db.session.query(Jobs, ToolSettings.keys, ToolSettings.values, ToolSettings.added_on, ToolSettings.id)
        #     .join(Tool, Jobs.input_account_id == Tool.id)
        #     .join(ToolSettings, ToolSettings.tool_id == Tool.id)
        #     .filter(Jobs.id == job_id)
        #     .all()
        # )

        if "myob_company_id" in session:
            company_file_id =session["myob_company_id"] 
        else:
            company_file_id="0282c77d-b037-4cca-9d18-25d0abfd7d97"
        
           
        

        base_url = f"http://localhost:8080/AccountRight/{company_file_id}/"

        return payload, base_url, headers
        
    except Exception as ex:
        traceback.print_exc()
