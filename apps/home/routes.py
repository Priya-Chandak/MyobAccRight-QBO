import os
import random
import string
import asyncio
import urllib.request, json
from redis import StrictRedis
from flask import render_template, redirect, request, url_for,jsonify,session,flash
from flask_login import login_required
from werkzeug.utils import secure_filename
import json
import requests
import webbrowser
import base64
from apps.authentication.forms import CreateJobForm, CreateSettingForm,CreateSelectidForm,CreateIdNameForm,CreateEmailForm,CreateauthcodeForm,FileNameForm,CreateCustomerInfoForm
from apps.home import blueprint
from apps.home.models import Jobs, JobExecutionStatus, Task, TaskExecutionStatus, TaskExecutionStep,ToolId,MYOBACCOUNTRIGHT,MYOBACCOUNTRIGHTQboTokens,CustomerInfo
from apps.tasks.myob_to_qbo_task import read_myob_write_qbo_task
from apps.mmc_settings.all_settings import *

from apps.myconstant import * 

redis = StrictRedis(host='localhost', port=6379, decode_responses=True)

@blueprint.route("/jobs")

def jobs():
    page = request.args.get('page', 1, type=int)
    tool1 = aliased(Tool)
    tool2 = aliased(Tool)
    jobs = (
        db.session.query(
            Jobs,
            tool1.tool_name.label("input_tool"),
            tool2.tool_name.label("output_tool"),
        )
        .join(tool1, Jobs.input_account_id == tool1.id)
        .join(tool2, Jobs.output_account_id == tool2.id)
    )

    jobs_data = jobs.paginate(page=page, per_page=100)
    # jobs_data.items.reverse()

    return render_template("home/jobs.html", segment="jobs", jobs=jobs_data)

@blueprint.route("/tasks/<int:job_id>")
def tasks_by_job(job_id):
    tasks = Task.query.filter(
        Task.job_id == job_id
    ).all()
    return render_template("home/tasks.html", segment="tasks", data=tasks, job_id=job_id)

@blueprint.route("/start_job/<int:job_id>")
def start_job(job_id):
    # read_myob_write_qbo_task.apply_async(args=[job_id])
    tasks = Task.query.filter(
        Task.job_id == job_id
    ).all()
    return render_template("home/tasks.html", segment="tasks", data=tasks)

@blueprint.route("/startJobByID", methods=["POST"])
def startJobByID():
    job_id=redis.get('my_key')
    asyncio.run(read_myob_write_qbo_task(job_id))
    return json.dumps({'status': 'success'})

@blueprint.route("/task_execution_details/<int:task_id>")
@login_required
def task_execution_details(task_id):
    task_steps = TaskExecutionStep.query.filter(
        TaskExecutionStep.task_id == task_id
    ).all()
    return render_template("home/task_execution_details.html", segment="task_steps", data=task_steps)

@blueprint.route("/job_execution_status/<int:job_id>")
@login_required
def Job_Execution_Status(job_id):
    job_execution_status = JobExecutionStatus.query.filter(
        JobExecutionStatus.job_id == job_id
    )
    return render_template(
        "home/job_status.html",
        segment="job_execution_status",
        data=job_execution_status,
    )

@blueprint.route("/task_execution_status/<int:job_id>")
@login_required
def Task_Execution_Status(task_id):
    task_execution_status = TaskExecutionStatus.query.filter(
        TaskExecutionStatus.task_id == task_id
    )
    return render_template(
        "home/job_status.html",
        segment="task_execution_status",
        data=task_execution_status,
    )

@blueprint.route("/upload_file_myobaccountright", methods=["GET", "POST"])

def upload_file_myobaccountright():

    if request.method == "GET":
                return render_template(
            "home/upload_file_myobaccountright.html",
        )

    if request.method == "POST":
        file_data=upload_file_accountright(request)
        print(file_data)

        return redirect(
            url_for(
                ".file_select_data",
               )
        )

@blueprint.route("/upload_accountright")

def upload_file_accountright(request):
    uploaded_file = request.files['file']

    if uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        
        upload_folder = r"C:\Users\dines\OneDrive\Documents\MYOB\My AccountRight Files"

        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, filename)
        uploaded_file.save(file_path)

        print(f"File '{filename}' uploaded successfully to: {file_path}")

        return "File uploaded successfully."
    
@blueprint.route("/file_select_data", methods=["GET", "POST"])

def file_select_data():
    create_customer_info_form = CreateCustomerInfoForm(request.form)
    if request.method == "GET":
        return render_template("home/file_data.html", form=create_customer_info_form)
    if request.method == "POST":
    
        job_functions=['Customer','Supplier']
        # job_functions=['Chart of account','Job','Customer','Supplier','Journal','Spend Money','Receive Money','Bank Transfer','Bill','Invoice','Bill Payment','Invoice Payment']
        job = Jobs()
        # job.functions = "Chart of account,Job,Customer,Supplier,Journal,Spend Money,Receive Money,Bank Transfer,Bill,Invoice,Bill Payment,Invoice Payment"
        job.functions="Customer,Supplier"
        length = 10 # You can change this to your desired length
        job.name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))  
        print(job.name)    
        job.description = "description1"
        job.input_account_id = 1
        job.output_account_id = 2
        job.start_date = ""
        job.end_date = ""
        db.session.add(job)
        db.session.commit()
        for fun in range(0, len(job_functions)):
            print('inside for loop',job.id)
            task = Task()
            task.function_name = job_functions[fun]
            task.job_id = job.id
            db.session.add(task)
            db.session.commit()

            key_to_clear = 'my_key'
            redis.delete(key_to_clear)

            redis.set('my_key', job.id)
            print(redis.get('my_key'),"request data same function ")

        customer_info= CustomerInfo()
        print("inside customer info table")
        customer_info.job_id=job.id
        customer_info.File_Name = request.form["inputCompany"]
        customer_info.Email = request.form["inputEmail"]
        customer_info.First_Name = request.form["inputFirstName"]
        customer_info.Last_Name = request.form["inputLastName"]
        db.session.add(customer_info)
        db.session.commit()

        myob_company_name = CustomerInfo.query.filter(CustomerInfo.job_id == redis.get('my_key')).first()
        print(myob_company_name.File_Name,"print company name ")
        url = "http://localhost:8080/AccountRight"
        response = urllib.request.urlopen(url)
        data = response.read()
        dict = json.loads(data)
        print(dict)
        file_name_data=myob_company_name.File_Name
        
        for item in dict:
            if item['Name'].lower() == file_name_data.lower() and item["ProductVersion"] == ProductVersion:
                myob_file=MYOBACCOUNTRIGHTQboTokens()
                myob_file.job_id=redis.get('my_key')
                myob_file.Myob_company_id=item["Id"]
                db.session.add(myob_file)
                db.session.commit()
                flash("File select successfully")
                return redirect(
                    url_for(
                        ".qbo_file_data", msg="Myob accountright Token added successfully!!!!.", success=True
                    )
                        )
            else:
                flash("Please enter correct file name","error")
                return redirect(
                    url_for(
                        ".file_select_data"
                    )
                        )
                


        

@blueprint.route("/qbo_file_data", methods=["GET", "POST"])

def qbo_file_data():

    if request.method == "GET":
        return render_template(
            "home/qbo_file_data.html",
        )

@blueprint.route("/file_data", methods=["GET"])

def file_data():
    if request.method == "GET":
        return render_template(
            "home/file_data.html",
        )

@blueprint.route("/qbo_auth", methods=["GET", "POST"])
def qbo_auth():

    if request.method == "POST":
    
        # CLIENT_ID = 'ABAngR99FX2swGqJy3xeHfeRfVtSJjHqlowjadjeGIg4W0mIdz'
        # CLIENT_SECRET = 'EC2abKy1uhHQcEpIDZy7EerH8i8hKl9gJ1ARGILE'

        CLIENT_ID = 'ABpWOUWtcEG1gCun5dQbQNfc7dvyalw5qVF97AkJQcn5Lh09o6'
        CLIENT_SECRET = 'LepyjXTADW592Dq5RYUP8UbGLcH5xtqDQhrf2xJN'

        REDIRECT_URI = 'http://localhost:5000/data_access'
        AUTHORIZATION_ENDPOINT = 'https://appcenter.intuit.com/connect/oauth2'
        TOKEN_ENDPOINT = 'https://oauth.platform.intuit.com/oauth2/v1/tokens'

    #     auth_url = f'{AUTHORIZATION_ENDPOINT}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=com.intuit.quickbooks.accounting&state=12345'
        auth_url = f'{AUTHORIZATION_ENDPOINT}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=com.intuit.quickbooks.accounting&state=12345'
        print(auth_url,"print auth url")
        # window.location.replace(auth_url,"_self")
        webbrowser.open(auth_url,"_self")

@blueprint.route("/data_access", methods=["GET", "POST"])
def data_access():
    auth_code1=request.args.get('code')
    realme_id=request.args.get('realmId')
    print(auth_code1 ,"print data auth code")
    CLIENT_ID = 'ABpWOUWtcEG1gCun5dQbQNfc7dvyalw5qVF97AkJQcn5Lh09o6'
    CLIENT_SECRET = 'LepyjXTADW592Dq5RYUP8UbGLcH5xtqDQhrf2xJN'
    token_endpoint = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
    # redirect_uri = "https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl"
    redirect_uri='http://localhost:5000/data_access'
    authorization_code = auth_code1
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
      "Authorization": "Basic QUJwV09VV3RjRUcxZ0N1bjVkUWJRTmZjN2R2eWFsdzVxVkY5N0FrSlFjbjVMaDA5bzY6TGVweWpYVEFEVzU5MkRxNVJZVVA4VWJHTGNINXh0cURRaHJmMnhKTg==",
    }

    response = requests.post(token_endpoint, data=data, headers=headers)
    print(response.json())
    if response.status_code == 200:
        token_data = MYOBACCOUNTRIGHTQboTokens.query.filter_by(job_id=redis.get('my_key')).first()
        print(token_data)
        token_data.qbo_access_token=response.json().get("access_token")
        token_data.qbo_refresh_token=response.json().get("refresh_token")
        token_data.qbo_company_id=realme_id
        db.session.commit()

    else:
        print("Token failed data")

    return render_template(
            "home/start_job_account_right.html",
        )
        

@blueprint.route("/jobs/create", methods=["GET", "POST"])

def create_job_for_accountright():
    job = Jobs()
    job.functions = ["Chart of account","Customer","Supplier","Item"]
    job.name = "job1"
    job.description = "description1"
    job.input_account_id = "1"
    job.output_account_id = "2"
    job.start_date = ""
    job.end_date = ""
    # TODO: Create job and tasks in same transaction, rollback if anything fails
    db.session.add(job)
    db.session.commit()

        
   


