import os
import random
import string
import asyncio
import urllib.request, json
from redis import StrictRedis
from flask import render_template, redirect, request, url_for,jsonify,session,flash,Response
from flask_login import login_required
from werkzeug.utils import secure_filename
from sqlalchemy import desc
import json
import requests
import pdfkit
import webbrowser
from apps.util.db_mongo import get_mongodb_database
from apps.util.qbo_util import retry_payload_for_myob_to_qbo,get_pagination_for_records
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

@blueprint.route("/conversion_underway")
def conversion_underway():
    job_id = redis.get('my_key')
    return render_template(
        "home/conversion_underway.html",
        job_id=job_id

    )

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
     
        url = Accountright_uri
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
                        ".qbo_file_data", msg="Myob accountright Token added successfully!!!!.", success=True,
                        
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

        CLIENT_ID = QBO_CI
        CLIENT_SECRET = QBO_CS

        REDIRECT_URI = QBO_REDIRECT
        AUTHORIZATION_ENDPOINT = QBO_Authorization
        TOKEN_ENDPOINT = QBO_Token
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
    CLIENT_ID = QBO_CI
    CLIENT_SECRET = QBO_CS
    token_endpoint = QBO_Token
    # redirect_uri = "https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl"
    redirect_uri=QBO_REDIRECT
    clientIdSecret = CLIENT_ID + ':' + CLIENT_SECRET
    encoded_u = base64.b64encode(clientIdSecret.encode()).decode()
    auth_code = "%s" % encoded_u

    authorization_code = request.args.get("code")
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
     'Authorization': "Basic" "  " + f'{auth_code}',
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



# @blueprint.route("/customerinfo_email", methods=["GET", "POST"])
# def get_customerinfo_email():
#
#     customer_info_data = customer_info.query.filter(
#         customer_info.job_id == redis.get('my_key')).first()
#
#     print(customer_info_data.Email, "customer info email")
#     customer_email = customer_info_data.Email
#
#     return customer_email


# @blueprint.route("/sent_email_to_customer", methods=["GET", "POST"])
# def sent_email_to_customer():
#     # Specify your AWS access key and secret key directly
#     aws_access_key_id = aws_access_key_id1
#     aws_secret_access_key = aws_secret_access_key1
#     region_name = region_name1
#     # Initialize Boto3 SQS client with the credentials
#     sqs = boto3.client('sqs', region_name=region_name, aws_access_key_id=aws_access_key_id,
#                        aws_secret_access_key=aws_secret_access_key)
#     ses = boto3.client('ses', region_name=region_name, aws_access_key_id=aws_access_key_id,
#                        aws_secret_access_key=aws_secret_access_key)
#     queue_url = Queue_URI
#
#     customer_info_data = CustomerInfo.query.filter(
#         CustomerInfo.job_id == redis.get('my_key')).first()
#
#     file_name = customer_info_data.File_Name
#     first_name = customer_info_data.First_Name
#     # start_date = customer_info_data.start_date
#     # end_date = customer_info_data.end_date
#     start_date = 1/12/2022
#     end_date = 12/12/2023
#     subject = f"Check Status of {file_name} from {start_date} to {end_date}"
#     conversion_report_link = f"https://mmc.vishleshak.io/conversion_report/{redis.get('my_key')}"
#     html_body = f"<html><body><p>Dear {first_name},</p><p>I hope this email finds you well. I wanted to provide you with an update on the status of the file named <strong>{file_name}</strong> that you are associated with. To view the progress and details, please click on the following link:</p><p><a href=\"{conversion_report_link}\">Check Status</a></p>    <p>This link will redirect you to a page where you can check the status of <strong>{file_name}</strong> between the specified start date of <strong>{start_date}</strong> and the end date of <strong>{end_date}</strong>.</p><p>Thank you</p><p>Best regards,<br>Ankit Mehta<br></body></html>"
#     recipient = get_customerinfo_email()
#
#     response = ses.send_email(
#         Source='ankit@mmcconvert.com',
#         Destination={'ToAddresses': [recipient]},
#         Message={
#             'Subject': {'Data': subject},
#             'Body': {
#                 'Html': {'Data': html_body}
#             }
#         }
#     )
#
#     sqs.send_message(QueueUrl=queue_url, MessageBody=subject)
#
#     return response


@blueprint.route("/User_info", methods=["GET", "POST"])
@login_required
def User_info():

    if request.method == "GET":

        all_customer_info = CustomerInfo.query.order_by(
            desc(CustomerInfo.id)).all()

        return render_template(
            "home/end_user.html",
            all_customer_info=all_customer_info
        )



@blueprint.route("/start_conversion_report/<int:job_id>")
def start_conversion_report(job_id):
    dbname = get_mongodb_database()

    job_id1 = job_id

    print(job_id, type(job_id))
    function_name = ["Existing COA","Chart of Account","Customer","Supplier", "Item", "Spend Money",
                     "Receive Money", "Bank Transfer", "Journal", "Invoice","Invoice Creditnote", "Bill","Bill Vendorcredit", "Invoice Payment", "Bill Payment"]
    table_name = [dbname['existing_coa'],dbname['xero_classified_coa'], dbname['xero_customer'], dbname['xero_supplier'], dbname['xero_items'], dbname['xero_spend_money'], dbname['xero_receive_money'],
                  dbname['xero_bank_transfer'], dbname['xero_manual_journal'], dbname['xero_invoice'],dbname['xero_creditnote'], dbname['xero_bill'],dbname['xero_vendorcredit'], dbname['xero_invoice_payment'], dbname['xero_bill_payment']]

    condition1 = {"job_id": f"{job_id}"}
    print(condition1)
    condition2 = {"job_id": f"{job_id}", "is_pushed": 1}
    condition3 = {"job_id": f"{job_id}", "is_pushed": 0}

    company_info = CustomerInfo.query.filter(
        CustomerInfo.job_id == job_id).first()

    company_name = company_info.File_Name,
    customer_email = company_info.Email,


    all_data = []
    pushed_data = []
    unpushed_data = []
    s1 = []
    f1 = []
    for k in range(0, len(table_name)):
        print(k)

        all_data1 = table_name[k].count_documents(condition1)
        pushed_data1 = table_name[k].count_documents(condition2)
        unpushed_data1 = table_name[k].count_documents(condition3)
        all_data.append(all_data1)
        pushed_data.append(pushed_data1)
        unpushed_data.append(unpushed_data1)
        if all_data1 != 0:
            success = pushed_data1/all_data1*100
            fail = unpushed_data1/all_data1*100
            s1.append(success)
            f1.append(fail)

        else:
            success = 0
            fail = 0
            s1.append(success)
            f1.append(fail)

        if all_data1 == 0:
            all_data1 = 100
    # return jsonify(all_data,function_name);
    return render_template("home/conversion_report_for_start_conversion.html", function_name=function_name, data1=all_data, data2=pushed_data, data3=unpushed_data, success=s1, fail=f1, job_id=job_id, company_name=company_name,
                           customer_email=customer_email,job_id1=job_id1)



@blueprint.route("/start_conversion_report_data/<int:job_id>")
def start_conversion_report_data(job_id):
    dbname = get_mongodb_database()

    function_name = ["Existing COA", "Chart of Account", "Customer", "Supplier", "Item", "Spend Money",
                     "Receive Money", "Bank Transfer", "Journal", "Invoice","Invoice CreditNote", "Bill","Bill VendorCredit", "Invoice Payment", "Bill Payment"]
    table_name = [dbname['existing_coa'], dbname['xero_classified_coa'], dbname['xero_customer'], dbname['xero_supplier'], dbname['xero_items'], dbname['xero_spend_money'], dbname['xero_receive_money'],
                  dbname['xero_bank_transfer'], dbname['xero_manual_journal'], dbname['xero_invoice'],dbname['xero_creditnote'], dbname['xero_bill'],dbname['xero_vendorcredit'], dbname['xero_invoice_payment'], dbname['xero_bill_payment']]

    condition1 = {"job_id": f"{job_id}"}
    # print(condition1)
    condition2 = {"job_id": f"{job_id}", "is_pushed": 1}
    condition3 = {"job_id": f"{job_id}", "is_pushed": 0}

    company_info = CustomerInfo.query.filter(
        CustomerInfo.job_id == job_id).first()

    all_data = []
    pushed_data = []
    unpushed_data = []
    s1 = []
    f1 = []
    for k in range(0, len(table_name)):
        all_data1 = table_name[k].count_documents(condition1)
        pushed_data1 = table_name[k].count_documents(condition2)
        unpushed_data1 = table_name[k].count_documents(condition3)
        all_data.append(all_data1)
        pushed_data.append(pushed_data1)
        unpushed_data.append(unpushed_data1)
        if all_data1 != 0:
            success = pushed_data1/all_data1*100
            fail = unpushed_data1/all_data1*100
            s1.append(success)
            f1.append(fail)

        else:
            success = 0
            fail = 0
            s1.append(success)
            f1.append(fail)

        if all_data1 == 0:
            all_data1 = 100

    data_list = []

    for i in range(len(function_name)):
        item_dict = {
            "company_name": company_info.File_Name,
            "customer_email": company_info.Email
             }

        item_dict['function_name'] = function_name[i]
        item_dict['values'] = s1[i]

        data_list.append(item_dict)

    return jsonify({'data': data_list})



@blueprint.route("/Create_final_report", methods=["GET", "POST"])
def Create_final_report(job_id):
    dbname = get_mongodb_database()
    job_id1 = str(job_id)
    print(job_id1, "print job id create final")

    customer_info_data = CustomerInfo.query.filter(
        CustomerInfo.job_id == job_id).first()



    cust_data = list(dbname["xero_report_customer"].find({"job_id": job_id1}))
    supp_data = list(dbname["xero_report_supplier"].find({"job_id": job_id1}))
    coa_data = list(dbname["matched_trial_balance"].find({"job_id": job_id1}))

    img_name = "qbo_image.png"
    qbo_img = os.path.join('apps', 'static', 'assets', 'img', img_name)

    print(len(cust_data), "print len of cust_data")
    print(len(supp_data), "print len of supp_data")
    print(len(coa_data), "print len of coa_data")

    return render_template("home/final_conversion_report.html", cust_data=cust_data, supp_data=supp_data, coa_data=coa_data, qbo_img=qbo_img)



@blueprint.route("/report_generation/<int:job_id>", methods=["GET", "POST"])
def report_generation(job_id):

    create_final_report_response = Create_final_report(job_id)
    job_id = job_id
    print(job_id)
    if isinstance(create_final_report_response, Response):

        create_final_report_content = create_final_report_response.data.decode(
            'utf-8')
    else:
        create_final_report_content = str(create_final_report_response)

    options = {
        'page-size': 'A4',
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
        "enable-local-file-access": ""
    }
    try:
        file_name = f"Report_{job_id}.pdf"
        pdf_path = os.path.join('apps', 'static', 'reports', file_name)
        print(pdf_path)
        pdfkit.from_string(create_final_report_content,
                           pdf_path, options=options,)
    except Exception as e:
        print(f"Error generating PDF: {e}")

    return redirect(
        url_for(
            ".User_info"
        )
    )



@blueprint.route("/final_report_email_to_customer/<int:job_id>", methods=["GET", "POST"])
def final_report_email_to_customer(job_id):
    print(job_id, "final report email job id")
    cust_data = []
    supp_data = []


    ses_smtp_server = 'email-smtp.us-east-2.amazonaws.com'  
    ses_smtp_port = 587
    ses_smtp_username =  os.environ['aws_access_key_id2']
    ses_smtp_password = os.environ['aws_secret_access_key2']

   

    aws_access_key_id = os.environ['aws_access_key_id2']
    aws_secret_access_key = os.environ['aws_secret_access_key2']
    region_name = os.environ['region_name2']

    sqs = boto3.client('sqs', region_name=region_name, aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)

    ses_smtp_connection = smtplib.SMTP(ses_smtp_server, ses_smtp_port)
    ses_smtp_connection.starttls() 
    ses_smtp_connection.login(ses_smtp_username, ses_smtp_password)

    ses = boto3.client('ses', region_name=region_name, aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)
    
    customer_info_data = CustomerInfo.query.filter(
        CustomerInfo.job_id == job_id).first()

    file_name = customer_info_data.Company

    subject = f"Check Status of Final Report {file_name}"

    dbname = get_mongodb_database()

    recipient = get_customerinfo_email(job_id)

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'qboxero9@gmail.com'
    msg['To'] = recipient

    file_name = f"Report_{job_id}.pdf"
    pdf_path = os.path.join('apps', 'static', 'reports', file_name)

    attachment_path = pdf_path
    attachment_filename = f"{file_name}_Final_Report.pdf"

    with open(attachment_path, 'rb') as attachment_file:
        attachment_data = attachment_file.read()

    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(attachment_data)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition',
                          f'attachment; filename="{attachment_filename}"')
    msg.attach(attachment)

    # response = ses.send_raw_email(RawMessage={'Data': msg.as_string()})

    # sqs.send_message(QueueUrl=queue_url, MessageBody=subject)

    file_name = f"Report_{job_id}.pdf"
    pdf_path = os.path.join('apps', 'static', 'reports', file_name)

    if os.path.exists(pdf_path):
        response=ses_smtp_connection.sendmail('qboxero9@gmail.com', recipient, msg.as_string())
        ses_smtp_connection.quit()
        os.remove(pdf_path)
    else:
        flash('Please generate pdf before send mail', 'error')

    return response


@blueprint.route("/update_task_flag/<int:task_id>/<function_name>", methods=["GET", "POST"])
def update_task_flag(task_id, function_name):
    print(task_id, "task id print -----")
    print(function_name, "function name print")
    dbname = get_mongodb_database()

    if function_name == "Chart of account":
        table_data = dbname['xero_classified_coa']

    elif function_name == 'AR-AP':
        table_data = dbname['AR']

    elif function_name == 'Archieved Chart of account':
        table_data = dbname['xero_classified_archived_coa']

    elif function_name == 'Existing Chart of account':
        table_data = dbname['existing_coa']

    elif function_name == 'Deleted Chart Of Account':
        table_data = dbname['xero_deleted_coa']

    elif function_name == 'Archieved Customer':
        table_data = dbname['xero_archived_customer_in_invoice']

    elif function_name == 'Archieved Supplier':
        table_data = dbname['xero_archived_supplier']

    elif function_name == 'Customer':
        table_data = dbname['xero_customer']

    elif function_name == 'Supplier':
        table_data = dbname['xero_supplier']

    elif function_name == 'Item':
        table_data = dbname['xero_items']

    elif function_name == 'Job':
        table_data = dbname['xero_job']

    elif function_name == 'Spend Money':
        table_data = dbname['xero_spend_money']

    elif function_name == 'Receive Money':
        table_data = dbname['xero_receive_money']

    elif function_name == 'Invoice':
        table_data = dbname['xero_invoice']

    elif function_name == 'Invoice CreditNote':
        table_data = dbname['xero_creditnote']

    elif function_name == 'Bill':
        table_data = dbname['xero_bill']

    elif function_name == 'Bill VendorCredit':
        table_data = dbname['xero_vendorcredit']

    elif function_name == 'Invoice Credit Memo Refund':
        table_data = dbname['xero_credit_memo_refund_payment']

    elif function_name == 'Bill Credit Memo Refund':
        table_data = dbname['xero_supplier_credit_cash_refund']

    elif function_name == 'Journal':
        table_data = dbname['xero_manual_journal']

    elif function_name == 'Invoice Payment':
        table_data = dbname['xero_invoice_payment']

    elif function_name == 'Bill Payment':
        table_data = dbname['xero_bill_payment']

    elif function_name == 'Bank Transfer':
        table_data = dbname['xero_bank_transfer']

    table_data.update_many({'task_id': task_id}, {'$set': {'is_pushed': 1}})

    return "Updated data"




@blueprint.route("/retryPayload", methods=["POST"])

def retryPayload():

    print("inside retry function")

    dbname = get_mongodb_database()
    task_id = request.form['task_id']
    _id = request.form['_id']
    payload1 = request.form['payload']
    payload = json.loads(payload1)
    print(_id,"id-----------------")
    print(payload1,"payload1--------------")
    print(payload,"payload------------------------------")

    task_details = db.session.query(Task).get(task_id)
    job_id = task_details.job_id
    # jobs, input_tool, output_tool = db.session.query(Jobs, tool1.account_type.label('input_tool'),
    #                                                  tool2.account_type.label(
    #                                                      'output_tool')
    #                                                  ).join(tool1, Jobs.input_account_id == tool1.id
    #                                                         ).join(tool2, Jobs.output_account_id == tool2.id
    #                                                                ).filter(Jobs.id == job_id).first()

    function_name = task_details.function_name
    output_tool = 2
    input_tool = 1

    
    if output_tool == 2:
        if input_tool == 1:
            base_url, headers, company_id, minorversion, get_data_header, report_headers = get_settings_qbo_for_report(
                job_id)
            status = retry_payload_for_myob_to_qbo(
                job_id, payload, _id, task_id, function_name)

            if status == 'success':
                return json.dumps({'status': 'success'})
            else:
                return json.dumps({'status': 'error'})
   
   

@blueprint.route("/records/<int:task_id>/<function_name>")
def records(task_id, function_name):
    dbname = get_mongodb_database()
    page = request.args.get('page', 1, type=int)
    input_tool = 1

    if input_tool == 1:
        if function_name == 'AR-AP':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["AR"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='AR-AP')

        if function_name == 'Archieved Chart of account':

            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_classified_archived_coa"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Archieved Chart of account')

        if function_name == 'Chart of account':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_classified_coa"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Chart of account')

        if function_name == 'Existing Chart of account':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["existing_coa"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Existing Chart of account')

        if function_name == 'Deleted Chart Of Account':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_deleted_coa"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Deleted Chart Of Account')

        if function_name == 'Archieved Customer':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_archived_customer_in_invoice"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Archieved Customer')

        if function_name == 'Archieved Supplier':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_archived_supplier"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Archieved Supplier')

        if function_name == 'Customer':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_customer"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Customer')

        if function_name == 'Supplier':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_supplier"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Supplier')

        if function_name == 'Item':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_items"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Item')

        if function_name == 'Job':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_job"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Job')

        if function_name == 'Spend Money':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_spend_money"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Spend Money')

        if function_name == 'Receive Money':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_receive_money"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Receive Money')

        if function_name == 'Invoice':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_invoice"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Invoice')

        if function_name == 'Invoice CreditNote':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_creditnote"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Invoice CreditNote')

        if function_name == 'Bill':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_bill"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Bill')

        if function_name == 'Bill VendorCredit':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_vendorcredit"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Bill VendorCredit')

        if function_name == 'Invoice Credit Memo Refund':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_credit_memo_refund_payment"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Invoice Credit Memo Refund')

        if function_name == 'Bill Credit Memo Refund':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_supplier_credit_cash_refund"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Bill Credit Memo Refund')

        if function_name == 'Journal':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_manual_journal"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Journal')

        if function_name == 'Invoice Payment':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_invoice_payment"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Invoice Payment')

        if function_name == 'Bill Payment':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_bill_payment"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Bill Payment')

        if function_name == 'Bank Transfer':
            page, per_page, total_records, successful_count, error_count, data = get_pagination_for_records(
                task_id, dbname["xero_bank_transfer"])
            data1 = []
            for i in data:
                data1.append(i)
            return render_template("home/records.html", data1=data1, page=page, per_page=per_page, total_records=total_records, successful_count=successful_count, error_count=error_count, task_id=task_id, function_name='Bank Transfer')



@blueprint.route("/conversion_report/<int:job_id>")
def conversion_report(job_id):
    dbname = get_mongodb_database()
    job_id = redis.get('my_key')
    print(job_id, type(job_id))

    function_name = ["Existing COA","Chart of Account","Customer","Supplier", "Item", "Spend Money",
                     "Receive Money", "Bank Transfer", "Journal", "Invoice","Invoice Creditnote", "Bill","Bill Vendorcredit", "Invoice Payment", "Bill Payment"]
    table_name = [dbname['existing_coa'],dbname['xero_classified_coa'], dbname['xero_customer'], dbname['xero_supplier'], dbname['xero_items'], dbname['xero_spend_money'], dbname['xero_receive_money'],
                  dbname['xero_bank_transfer'], dbname['xero_manual_journal'], dbname['xero_invoice'],dbname['xero_creditnote'], dbname['xero_bill'],dbname['xero_vendorcredit'], dbname['xero_invoice_payment'], dbname['xero_bill_payment']]

    condition1 = {"job_id": f"{job_id}"}
    print(condition1)
    condition2 = {"job_id": f"{job_id}", "is_pushed": 1}
    condition3 = {"job_id": f"{job_id}", "is_pushed": 0}

    company_info = CustomerInfo.query.filter(
        CustomerInfo.job_id == job_id).first()


    customer_email = company_info.Email

    all_data = []
    pushed_data = []
    unpushed_data = []
    s1 = []
    f1 = []
    for k in range(0, len(table_name)):
        print(k)

        all_data1 = table_name[k].count_documents(condition1)
        pushed_data1 = table_name[k].count_documents(condition2)
        unpushed_data1 = table_name[k].count_documents(condition3)
        all_data.append(all_data1)
        pushed_data.append(pushed_data1)
        unpushed_data.append(unpushed_data1)
        if all_data1 != 0:
            success = pushed_data1/all_data1*100
            fail = unpushed_data1/all_data1*100
            s1.append(success)
            f1.append(fail)

        else:
            success = 0
            fail = 0
            s1.append(success)
            f1.append(fail)

        if all_data1 == 0:
            all_data1 = 100
    # return jsonify(all_data,function_name);
    return render_template("home/conversion_report.html", function_name=function_name, data1=all_data, data2=pushed_data, data3=unpushed_data, success=s1, fail=f1, job_id=job_id,customer_email=customer_email)


@blueprint.route("/conversion_report_data/<int:job_id>")
def conversion_report_data(job_id):
    dbname = get_mongodb_database()

    job_id = redis.get('my_key')
    # print(job_id,type(job_id))

    function_name = ["Existing COA", "Chart of Account", "Customer", "Supplier", "Item","Class", "Spend Money",
                     "Receive Money", "Bank Transfer", "Journal", "Invoice", "Bill", "Open Invoice", "Open Bill", "Open Creditnote", "Open Vendorcredit", "Invoice Payment", "Bill Payment"]
    table_name = [dbname['existing_coa'], dbname['xero_classified_coa'], dbname['xero_customer'], dbname['xero_supplier'], dbname['xero_items'],dbname['xero_job'], dbname['xero_spend_money'], dbname['xero_receive_money'],
                  dbname['xero_bank_transfer'], dbname['xero_manual_journal'], dbname['xero_invoice'], dbname['xero_bill'], dbname['xero_open_invoice'], dbname['xero_open_bill'], dbname['xero_open_creditnote'], dbname['xero_open_suppliercredit'], dbname['xero_invoice_payment'], dbname['xero_bill_payment']]

    condition1 = {"job_id": f"{job_id}"}
    # print(condition1)
    condition2 = {"job_id": f"{job_id}", "is_pushed": 1}
    condition3 = {"job_id": f"{job_id}", "is_pushed": 0}

    company_info = CustomerInfo.query.filter(
        CustomerInfo.job_id == redis.get('my_key')).first()
    print(company_info, "print company_info data")

    all_data = []
    pushed_data = []
    unpushed_data = []
    s1 = []
    f1 = []
    for k in range(0, len(table_name)):
        # print(k)

        all_data1 = table_name[k].count_documents(condition1)
        pushed_data1 = table_name[k].count_documents(condition2)
        unpushed_data1 = table_name[k].count_documents(condition3)
        all_data.append(all_data1)
        pushed_data.append(pushed_data1)
        unpushed_data.append(unpushed_data1)
        if all_data1 != 0:
            success = pushed_data1/all_data1*100
            fail = unpushed_data1/all_data1*100
            s1.append(success)
            f1.append(fail)

        else:
            success = 0
            fail = 0
            s1.append(success)
            f1.append(fail)

        if all_data1 == 0:
            all_data1 = 100

    data_list = []

    # print(function_name)
    # print(s1)
    # print(f1)

    for i in range(len(function_name)):
        item_dict = {

            "customer_email": company_info.Email
           }

        item_dict['function_name'] = function_name[i]
        item_dict['values'] = s1[i]

        data_list.append(item_dict)

    return jsonify({'data': data_list})
