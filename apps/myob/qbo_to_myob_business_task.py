from apps.home.data_util import update_task_execution_status, write_task_execution_step
from apps.home.models import Task
from apps.myob.myob_ledger_writer.add_bank_transfer_myobledger import (
    add_qbo_bank_transfer_to_myobledger,
)
from apps.myob.myob_ledger_writer.add_coa_myob import (
    add_qbo_coa_to_myob,
    add_qbo_existing_chart_account_to_myob,
    add_qbo_chart_of_account_as_default_myob
)
from apps.myob.myob_ledger_writer.add_archived_coa_myob import add_qbo_archive_coa_to_myob
from apps.myob.myob_ledger_writer.add_customer import add_qbo_customer_to_myobledger
from apps.myob.myob_ledger_writer.add_item_myob_business import add_qbo_item_to_myob
from apps.myob.myob_ledger_writer.add_job import add_qbo_job_to_myobledger
from apps.myob.myob_ledger_writer.add_journal_myobledger import (
    add_qbo_journal_to_myobledger,
)
from apps.myob.myob_ledger_writer.edit_existing_coa import get_duplicate_chart_of_account_qbo, \
    update_existing_chart_account_qbo_myob
from apps.myob.myob_ledger_writer.add_qbo_bill_payment_to_myob import (
    add_qbo_bill_payment_to_myob,
)
from apps.myob.myob_ledger_writer.add_qbo_bill_to_myob import add_qbo_bill_to_myob
from apps.myob.myob_ledger_writer.add_qbo_credit_memo_to_myob import (
    add_qbo_credit_memo_to_myob,
)
from apps.myob.myob_ledger_writer.add_qbo_invoice_to_myob import add_qbo_invoice_to_myob
from apps.myob.myob_ledger_writer.add_qbo_payment_to_myob import add_qbo_payment_to_myob
from apps.myob.myob_ledger_writer.add_qbo_supplier_credit_to_myob import (
    add_qbo_supplier_credit_to_myob,
)
from apps.myob.myob_ledger_writer.add_receive_money import (
    add_qbo_receive_money_to_myobledger,
)
from apps.myob.myob_ledger_writer.add_spend_money import (
    add_qbo_spend_money_to_myobledger,
)
from apps.myob.myob_ledger_writer.add_supplier import add_qbo_supplier_to_myobledger
from apps.myob.myob_ledger_writer.add_archived_supplier import add_qbo_archived_supplier_to_myob
from apps.myob.myob_ledger_writer.add_archived_customer import add_qbo_archive_customer_to_myob
from apps.myob.myob_ledger_writer.update_existing_coa import *
from apps.myob.myob_reader.all_bill import get_all_bill
from apps.myob.myob_reader.all_invoice import get_all_invoice
# from apps.myob.myob_ledger_writer.add_Bank_Transfer import add_qbo_bank_transfer_to_myobledger
from apps.myob.myob_ledger_writer.add_bank_transfer_as_journal import add_qbo_bank_transfer_as_journal
from apps.myob.myob_reader.chart_of_account import get_chart_of_account
from apps.myob.myob_reader.customer import get_customer
from apps.myob.myob_reader.item import get_item
from apps.myob.myob_reader.job import get_myob_job
from apps.myob.myob_reader.myobledger_taxcode import get_taxcode_myob
from apps.myob.myob_reader.supplier import get_supplier

from apps.qbo.account.account_referrence import account_reference
from apps.qbo.reader.QBO_combined_tax import get_qbo_tax
from apps.qbo.reader.archived_coa import get_qbo_archived_coa
from apps.qbo.reader.archived_customer import get_qbo_archived_customer
from apps.qbo.reader.archived_supplier import get_qbo_archived_vendor
from apps.qbo.reader.qbo_data_reader import read_qbo_data
from apps.qbo.reader.taxrate import get_qbo_taxrate
from apps.qbo.reader.taxcode import get_qbo_taxcode


class QboToMyobBusiness(object):
    @staticmethod
    def read_data(job_id, task):
        step_name = None
        try:


            if "Chart of account" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")

                step_name = "Reading chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Chart of account")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
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

                update_task_execution_status( task.id, status=1, task_type="read")

            if "Archieved Chart of account" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="read")

                step_name = "Reading archived chart_of_account qbo data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_archived_coa(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
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

                update_task_execution_status( task.id, status=1, task_type="read")



            if "Existing Chart of account" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")

                step_name = "Reading chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Chart of account")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from duplicate chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_duplicate_chart_of_account_qbo(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

               
                update_task_execution_status( task.id, status=1, task_type="read")

            
            if "Customer" == task.function_name:


                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Customer")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                update_task_execution_status( task.id, status=1, task_type="read")

            if "Archieved Customer" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")

                step_name = "Reading data from Archieved Customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_archived_customer(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="read")

            if "Archieved Supplier" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from Archieved Supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_archived_vendor(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                

                update_task_execution_status(task.id, status=1, task_type="read")

              
            if "Supplier" == task.function_name:
                
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from Supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Supplier")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                update_task_execution_status( task.id, status=1, task_type="read")
              
                
            if "Job" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from Job"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Job")
                write_task_execution_step(task.id, status=1, step=step_name)
                
                update_task_execution_status( task.id, status=1, task_type="read")
              
                

            if "Spend Money" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from Spend Money"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Spend Money")
                write_task_execution_step(task.id, status=1, step=step_name)
               
                step_name = "Reading data from Job "
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Job")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from Customer "
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Customer")
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Chart of account")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from qbo taxrate"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from qbo taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from qbo tax"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_tax(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)


                step_name = "Reading myob data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="read")
              
               
            if "Receive Money" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from Receive Money"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Receive Money")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Chart of account")
                write_task_execution_step(task.id, status=1, step=step_name)
               
                step_name = "Reading data from Job "
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Job")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from Customer "
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Customer")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from qbo taxrate"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from qbo taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from qbo tax"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_tax(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

               
                update_task_execution_status( task.id, status=1, task_type="read")
              
            if "Bank Transfer" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from bank Transfer"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Bank Transfer")
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="read")
              
            if "Journal" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from Journal"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Journal")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Chart of account")
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="read")

            if "Invoice" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from Invoice"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Invoice")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Chart of account")
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="read")

            if "Bill" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from Bill"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Bill")
                write_task_execution_step(task.id, status=1, step=step_name)
                 
                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from taxrate"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from tax"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                
                step_name = "Reading data from Chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Chart of account")
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="read")
                
            if "Item" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from Item"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Item")
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading data from Chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Chart of account")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from qbo taxrate"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from qbo taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from qbo tax"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_tax(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from Account reference"
                write_task_execution_step(task.id, status=2, step=step_name)
                account_reference(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="read")


            if "Payment Allocation" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from Payment Allocation"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Payment Allocation")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from Chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Chart of account")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from taxrate"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from tax"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                
                step_name = "Reading data from Invoice"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Invoice")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from Bill"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Bill")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from Supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Supplier")
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="read")

            if "Bill Payment" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from Payment Allocation"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Bill Payment")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from Chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Chart of account")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from taxrate"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from tax"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)


                step_name = "Reading myob data from chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading data from Bill"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Bill")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from Supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Supplier")
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="read")

            if "Invoice Payment" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from Payment Allocation"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Invoice Payment")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from Chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Chart of account")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading data from Invoice"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Invoice")
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from Supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                read_qbo_data(job_id, task.id, "Supplier")
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="read")


        except Exception as ex:
            write_task_execution_step(task.id, status=0, step=step_name)
            update_task_execution_status(job_id, task.id, status=0, task_type="read")
            raise ex

    @staticmethod
    def write_data(job_id, task):
        step_name = None
        try:
            if "Chart of account" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Adding chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_coa_to_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding default chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_chart_of_account_as_default_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                # # delete_chart_of_account(job_id)
                # get_chart_of_account(job_id)

                update_task_execution_status( task.id, status=1, task_type="write")

            if "Archieved Chart of account" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Adding archived chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_archive_coa_to_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")

            if "Existing Chart of account" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Updating existing chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                update_existing_chart_account_qbo_myob(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                # # delete_chart_of_account(job_id)
                # get_chart_of_account(job_id)

                update_task_execution_status( task.id, status=1, task_type="write")
                
                
            if "Customer" == task.function_name:
                
                update_task_execution_status( task.id, status=2, task_type="write")
                
                step_name = "Adding customer data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_customer_to_myobledger(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")


            if "Supplier" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")
                
                step_name = "Adding Supplier data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_supplier_to_myobledger(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")

            if "Archieved Customer" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Adding data Archieved Customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_archive_customer_to_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Archieved Supplier" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")
        
                step_name = "Adding data Archieved Supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_archived_supplier_to_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                update_task_execution_status(task.id, status=1, task_type="write")
            
            if "Job" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")
                
                step_name = "Adding job data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_job_to_myobledger(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")

            if "Spend Money" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")
                
                step_name = "Reading supplier data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_supplier(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading customer data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_customer(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading job data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_myob_job(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading chart of account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding spend money data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_spend_money_to_myobledger(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")
                
            if "Receive Money" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")
                
                step_name = "Reading supplier data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_supplier(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading customer data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_customer(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading job data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_myob_job(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading chart of account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding receive money data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_receive_money_to_myobledger(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")
                

            if "Bank Transfer" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")
                
                step_name = "Reading myob taxcode data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
               
                step_name = "Reading chart of account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Adding bank transfer data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_bank_transfer_to_myobledger(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Adding bank transfer as journal data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_bank_transfer_as_journal(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)


                update_task_execution_status( task.id, status=1, task_type="write")
                
            if "Journal" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")
                
                
                step_name = "Reading myob data from chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from qbo taxrate"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from qbo taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from qbo tax"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_tax(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

 
                step_name = "Reading job data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_myob_job(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding journal data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_journal_to_myobledger(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")
                

            if "Invoice" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")
                
                step_name = "Reading supplier data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_supplier(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading myob data from chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from qbo taxrate"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from qbo taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from qbo tax"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_qbo_tax(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading customer data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_customer(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading job data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_myob_job(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading item data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_item(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding invoice data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_invoice_to_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                
                step_name = "Adding credit memo data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_credit_memo_to_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")
                

            if "Bill" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")
                
                step_name = "Reading supplier data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_supplier(job_id,task.id)   
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading myob data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading customer data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_customer(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                    
                step_name = "Reading myob data from chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                
                step_name = "Reading job data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_myob_job(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading item data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_item(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading all bill data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_all_bill(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding bill data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_bill_to_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding supplier credit data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_supplier_credit_to_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")
            
            if "Item" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")
                
                step_name = "Adding item data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_item_to_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")
                
            if "Payment Allocation" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")
                
                step_name = "Reading supplier data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_supplier(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading customer data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_customer(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading job data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_myob_job(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading item data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_item(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading all bill data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_all_bill(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
            
                step_name = "Reading all invoice data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_all_invoice(job_id,task.id)
               
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding invoice payment data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_payment_to_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding bill payment data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_bill_payment_to_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")
                
            if "Bill Payment" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")
                
                step_name = "Reading supplier data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_supplier(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading myob data from chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading customer data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_customer(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading job data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_myob_job(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading item data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_item(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading all bill data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_all_bill(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
            
                step_name = "Adding bill payment data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_bill_payment_to_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")
           
            if "Invoice Payment" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")
                
                step_name = "Reading supplier data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_supplier(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading customer data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_customer(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading job data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_myob_job(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading item data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_item(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading all invoice data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_all_invoice(job_id,task.id)
               
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding invoice payment data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_qbo_payment_to_myob(job_id,task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="write")
           
                
               

        except Exception as ex:
            write_task_execution_step(task.id, status=0, step=step_name)
            update_task_execution_status(job_id, task.id, status=0, task_type="read")
            raise ex


