from apps.home.models import Task
from apps.myob.myob_ledger_writer.add_bank_transfer_myobledger import (
    add_qbo_bank_transfer_to_myobledger,
)
from apps.myob.myob_ledger_writer.add_coa_myob import add_qbo_coa_to_myobledger

from apps.myob.myob_ledger_writer.add_customer import add_qbo_customer_to_myobledger
from apps.myob.myob_ledger_writer.add_job import add_qbo_job_to_myobledger
from apps.myob.myob_ledger_writer.add_invoice_as_journal import add_qbo_invoice_as_journal_to_myobledger
from apps.myob.myob_ledger_writer.add_journal_myobledger import (
    add_qbo_journal_to_myobledger,
)
from apps.myob.myob_ledger_writer.add_receive_money import (
    add_qbo_receive_money_to_myobledger,
)
from apps.myob.myob_ledger_writer.add_spend_money import (
    add_qbo_spend_money_to_myobledger,
)
from apps.myob.myob_ledger_writer.add_supplier import add_qbo_supplier_to_myobledger
from apps.myob.myob_ledger_writer.update_existing_coa import *
from apps.myob.myob_reader.chart_of_account import get_chart_of_account
from apps.myob.myob_reader.customer import get_customer
from apps.myob.myob_reader.job import get_myob_job
from apps.myob.myob_reader.myobledger_taxcode import get_taxcode_myob
from apps.myob.myob_reader.supplier import get_supplier
from apps.qbo.account.account_referrence import account_reference
from apps.qbo.reader.QBO_combined_tax import get_qbo_tax
from apps.qbo.reader.qbo_data_reader import read_qbo_data
from apps.qbo.reader.taxrate import get_qbo_taxrate
from apps.qbo.reader.taxcode import get_qbo_taxcode
from apps.xero.myob_ledger_writer.edit_chart_of_account import *
from apps.myob.delete_apis import delete_chart_of_account

from apps.home.data_util import update_task_execution_status, write_task_execution_step



class QboToMyobLedger(object):
    @staticmethod
    def read_data(job_id, task):
        step_name = None
        try:

            if "Chart of account" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")

                step_name = "Reading chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of account")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from duplicate chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_duplicate_chart_account_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Taxcode")
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading data from taxrate"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
            
                step_name = "Reading data from tax"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
            
                
                step_name = "Reading myob data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
            
                update_task_execution_status(task.id, status=1, task_type="read")

            
            if "Customer" == task.function_name:

                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Customer")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                update_task_execution_status(task.id, status=1, task_type="read")

              
            if "Supplier" == task.function_name:
                
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from Supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Supplier")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                update_task_execution_status(task.id, status=1, task_type="read")
              
                
            if "Job" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from Job"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Job")
                write_task_execution_step(task.id, status=1, step=step_name)
                
                update_task_execution_status(task.id, status=1, task_type="read")
              
                
            if "Spend Money" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from Spend Money"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Spend Money")
                write_task_execution_step(task.id, status=1, step=step_name)
               
                step_name = "Reading supplier data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_supplier(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
                
                step_name = "Reading customer data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_customer(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
                
                step_name = "Reading job data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_myob_job(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                step_name = "Reading Myob tax"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_taxcode_myob(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
                
                step_name = "Reading data from taxrate"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
            
                step_name = "Reading data from taxcode"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                step_name = "Reading data from tax"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                
                step_name = "Reading chart of account data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_chart_of_account(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                step_name = "Reading data from Job "
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Job")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from COA "
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of account")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from Customer "
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Customer")
                write_task_execution_step(task.id, status=1, step=step_name)
               
                update_task_execution_status(task.id, status=1, task_type="read")
              

               
            if "Receive Money" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from Receive Money"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Receive Money")
                write_task_execution_step(task.id, status=1, step=step_name)
               
                step_name = "Reading data from Job "
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Job")
                write_task_execution_step(task.id, status=1, step=step_name)

                
                step_name = "Reading supplier data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_supplier(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                step_name = "Reading Customer data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_customer(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
                
                
                step_name = "Reading job data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_myob_job(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                step_name = "Reading Myob tax"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_taxcode_myob(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
                
                step_name = "Reading data from taxrate"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
            
                step_name = "Reading data from taxcode"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                step_name = "Reading data from tax"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                
                step_name = "Reading chart of account data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_chart_of_account(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                
                step_name = "Reading data from COA "
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of account")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from Customer "
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Customer")
                write_task_execution_step(task.id, status=1, step=step_name)
               
                update_task_execution_status(task.id, status=1, task_type="read")
              
            if "Bank Transfer" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from bank Transfer"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Bank Transfer")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from COA "
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of account")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading chart of account data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_chart_of_account(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                

                update_task_execution_status(task.id, status=1, task_type="read")
              
            if "Journal" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from Journal"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Journal")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from taxrate"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
            
                step_name = "Reading data from taxcode"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                step_name = "Reading data from tax"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
                
                step_name = "Reading QBO COA data"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of Account")
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading chart of account data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_chart_of_account(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                step_name = "Reading taxcode myob data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_taxcode_myob(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
                
                step_name = "Reading supplier data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_supplier(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
                
                step_name = "Reading customer data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_customer(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
                
                step_name = "Reading job data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_myob_job(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                
                update_task_execution_status(task.id, status=1, task_type="read")

            if "Invoice" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading QBO Invoice data"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Invoice")
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading data from taxrate"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
            
                step_name = "Reading data from taxcode"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                step_name = "Reading data from tax"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
                
                step_name = "Reading QBO COA data"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of Account")
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading chart of account data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_chart_of_account(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                step_name = "Reading taxcode myob data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_taxcode_myob(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
                
                step_name = "Reading myob customer data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_customer(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
                
                step_name = "Reading myob supplier data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_supplier(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
                
                step_name = "Reading myob job data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                get_myob_job(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
                
                update_task_execution_status(task.id, status=1, task_type="read")
                
            
        except Exception as ex:
            write_task_execution_step(task.id, status=0, step=step_name)
            update_task_execution_status(job_id, task.id, status=0, task_type="read")
            raise ex

    
    @staticmethod
    def write_data(job_id, task):
        step_name = None
        try:
            if "Chart of account" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")

                step_name = "Adding chart_of_account data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                # add_qbo_coa_to_myobledger(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                step_name = "Deleting chart_of_account data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                # delete_chart_of_account(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")
                
                
            if "Customer" == task.function_name:
                
                update_task_execution_status(task.id, status=2, task_type="write")
                
                step_name = "Adding customer data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                add_qbo_customer_to_myobledger(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")


            if "Supplier" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")
                
                step_name = "Adding Supplier data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                # add_qbo_supplier_to_myobledger(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")
            
            if "Job" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")
                
                step_name = "Adding job data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                add_qbo_job_to_myobledger(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")

            if "Spend Money" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")
                
                step_name = "Adding spend money data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                add_qbo_spend_money_to_myobledger(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")
                
            if "Receive Money" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")
                
                step_name = "Adding receive money data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                add_qbo_receive_money_to_myobledger(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")
                

            if "Bank Transfer" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")
                
                step_name = "Adding bank transfer data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                add_qbo_bank_transfer_to_myobledger(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")
                
            if "Journal" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")
                
                step_name = "Adding journal data"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                add_qbo_journal_to_myobledger(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")

            if "Invoice" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")
                
                step_name = "Adding Invoice as Journal"
                write_task_execution_step(
                    job_id, task.id, status=2, step=step_name)
                
                add_qbo_invoice_as_journal_to_myobledger(job_id,task.id)
                write_task_execution_step(
                    job_id, task.id, status=1, step=step_name)
                
                # add_job_status(job_id, "Credit Notes as Journal","write")
                # add_xero_creditnote_as_journal_to_myobledger(job_id)
                # add_job_status(job_id, "Credit Notes as Journal", "write",
                #                started_or_complete="complete")
                update_task_execution_status( task.id, status=1, task_type="write")


            
                    

        except Exception as ex:
            write_task_execution_step(task.id, status=0, step=step_name)
            update_task_execution_status(job_id, task.id, status=0, task_type="read")
            raise ex


