import traceback
from apps import db
from apps.home.models import Tool, ToolSettings,MYOBACCOUNTRIGHTQboTokens

def get_myob_settings(job_id):
    try:
        
        payload={}
        headers = {
        'x-myobapi-version': 'v2',
        'Authorization': 'Basic QWRtaW5pc3RyYXRvcjo='
        }
        data1 = db.session.query(MYOBACCOUNTRIGHTQboTokens).filter(MYOBACCOUNTRIGHTQboTokens.job_id == job_id).first()
        base_url = f"http://localhost:8080/AccountRight/{data1.Myob_company_id}/"

        return payload, base_url, headers
        
    except Exception as ex:
        traceback.print_exc()
