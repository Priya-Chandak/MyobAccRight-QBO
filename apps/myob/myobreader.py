from apps.home.models import Task
from apps.myob.myob_to_qbo_task import MyobToQbo

from apps import db
from os import path
from apps.home.models import Jobs, Tool
from apps.myconstant import *
from sqlalchemy.orm import aliased
from apps.mmc_settings.all_settings import *
from apps.home.data_util import add_job_status

def read_data(job_id):
    try:
        # GET MYOB data
        # #job_details = db.session.query(Jobs).get(job_id)
        # tool1 = aliased(Tool)
        # tool2 = aliased(Tool)
        # read_result = db.session.execute("select t1.account_type as input ,t2.account_type as output from jobs inner join tool t1 on t1.id=jobs.input_account_id inner join tool t2 on t2.id=jobs.output_account_id where jobs.id=:job_id", {"job_id":job_id})
        # # Output the query result as JSON
        # for row in read_result:
        input_tool=1
        output_tool=2
        # Get list of tasks added in the job

        # TODO: Check if input tool is excel
        # If yes push data to mongodb in respective tables with job id and task id and some status flag
        # indicating whether the records is pushed or not

        read_tasks = Task.query.filter(Task.job_id == job_id).filter(Task.read != 1).all()
        add_job_status(job_id, status=2)

        for task in read_tasks:
            
            if input_tool == 1 and output_tool == 2:
                MyobToQbo.read_data(job_id, task)
           
           
            db.session.close()
        

        # write_result = db.session.execute("select t1.account_type as input ,t2.account_type as output from jobs inner join tool t1 on t1.id=jobs.input_account_id inner join tool t2 on t2.id=jobs.output_account_id where jobs.id=:job_id", {"job_id":job_id})
        # Output the query result as JSON
        # for row in write_result:
        #     input_tool=row
        #     output_tool=row[1]
        # Get list of tasks added in the job
        
        write_tasks = Task.query.filter(Task.job_id == job_id).filter(Task.write != 1).all()
        add_job_status(job_id, status=2)
        

        for task in write_tasks:
            print(task,"write task")
            
            if input_tool == 1 and output_tool == 2:
                MyobToQbo.write_data(job_id, task)

            
            db.session.close()

        
        # delete_result = db.session.execute("select t1.account_type as input ,t2.account_type as output from jobs inner join tool t1 on t1.id=jobs.input_account_id inner join tool t2 on t2.id=jobs.output_account_id where jobs.id=:job_id", {"job_id":job_id})
        # # Output the query result as JSON
        # for row in delete_result:
        #     input_tool=row[0]
        #     output_tool=row[1]
        # # Get list of tasks added in the job

        # delete_tasks = Task.query.filter(Task.job_id == job_id).filter(Task.delete != 1).all()

        # for task in delete_tasks:
        #     print("hasiixiax")
        #     if input_tool == DELETE and output_tool == MYOB:
        #         DeleteToMyob.delete_data(job_id, task)

        #     db.session.close()



    except Exception as ex:
        print(ex)
