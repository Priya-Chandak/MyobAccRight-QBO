from apps.home.data_util import update_task_execution_status, write_task_execution_step
from apps.myob.delete_apis import *
from apps.myob.myob_reader.all_bill import get_all_bill
from apps.myob.myob_reader.all_invoice import get_all_invoice
from apps.myob.myob_reader.bank_transfer import get_bank_transfer
from apps.myob.myob_reader.bill_payment import get_bill_payment
# from apps.xero.qbo_writer.get_qbo_invoice_for_payments import get_qbo_invoice_for_payments,get_qbo_bill_for_payments 
from apps.myob.myob_reader.chart_of_account import get_chart_of_account
from apps.myob.myob_reader.currency import get_currency
from apps.myob.myob_reader.customer import get_customer
from apps.myob.myob_reader.employee import get_employee
from apps.myob.myob_reader.final_bill import (
    get_final_bill1,
    get_final_bill2,
    get_final_bill3,
    get_final_bill,
)
from apps.myob.myob_reader.item import get_item
from apps.myob.myob_reader.item_bill import get_item_bill
from apps.myob.myob_reader.item_invoice import get_item_invoice, get_classified_invoice
from apps.myob.myob_reader.item_purchase_order import get_item_purchase_order
from apps.myob.myob_reader.item_quotes import get_item_quote
from apps.myob.myob_reader.job import get_myob_job
from apps.myob.myob_reader.journal import get_journal
from apps.myob.myob_reader.misc_bill import get_miscellaneous_bill
from apps.myob.myob_reader.payment import get_invoice_payment
from apps.myob.myob_reader.professional_bill import get_professional_bill
from apps.myob.myob_reader.received_money import get_received_money
from apps.myob.myob_reader.service_bill import get_service_bill
from apps.myob.myob_reader.service_invoice import get_service_classified_invoice, get_service_invoice
from apps.myob.myob_reader.service_purchase_order import get_service_purchase_order
from apps.myob.myob_reader.spend_money import get_spend_money
from apps.myob.myob_reader.supplier import get_supplier
from apps.myob.myob_reader.taxcode import get_taxcode
from apps.qbo.account.add_chart_of_account import add_chart_account
from apps.qbo.account.add_duplicate_chart_of_account import (
    add_duplicate_chart_account,
    update_qbo_existing_chart_account,
)
from apps.qbo.account.add_item_bill import add_item_bill
from apps.qbo.account.add_service_bill1 import add_service_bill1
from apps.qbo.account.add_service_bill import add_service_bill
from apps.qbo.account.get_COA_classification import get_classified_coa
from apps.qbo.reader.QBO_combined_tax import get_qbo_tax
from apps.qbo.reader.qbo_data_reader import read_qbo_data
from apps.qbo.reader.taxrate import get_qbo_taxrate
from apps.qbo.reader.taxcode import get_qbo_taxcode
from apps.qbo.writer.add_bank_transfer import add_bank_transfer
from apps.qbo.writer.add_bill_payment import add_bill_payment
from apps.qbo.writer.add_credit_card_credit import add_credit_card_credit
from apps.qbo.writer.add_customer import add_customer
from apps.qbo.writer.add_employee import add_employee
from apps.qbo.writer.add_item import add_item
from apps.qbo.writer.add_item_quotes import add_item_quote
from apps.qbo.writer.add_job import add_job
from apps.qbo.writer.add_journal import add_journal
from apps.qbo.writer.add_multiple_item_invoice import add_multiple_item_invoice
from apps.qbo.writer.add_multiple_service_invoice import add_multiple_service_invoice
from apps.qbo.writer.add_payment import add_payment
from apps.qbo.writer.add_purchase_order import add_item_purchase_order
from apps.qbo.writer.add_received_money import add_received_money
from apps.qbo.writer.add_service_purchase_order import add_service_purchase_order
from apps.qbo.writer.add_single_item_invoice import add_single_item_invoice
from apps.qbo.writer.add_single_service_invoice import add_single_service_invoice
from apps.qbo.writer.add_spend_money import add_spend_money
from apps.qbo.writer.add_negative_spend_money import add_negative_spend_money
from apps.qbo.writer.add_supplier import add_supplier
from apps.qbo.writer.create_item_from_invoice import create_item_from_invoice, create_item_from_service_invoice, create_item_from_itemcode_acccode


class MyobToQbo(object):
    @staticmethod
    def read_data(job_id, task):
        step_name = None
        try:

            if "Chart of account" == task.function_name:
                update_task_execution_status(
                     task.id, status=2, task_type="read")
                step_name = "Reading data from chart_of_account"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_chart_of_account(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from classified_coa"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_classified_coa(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from taxcode"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_taxcode(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Chart of account"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of Account")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                # step_name = "Reading data from currency"
                # write_task_execution_step(
                #     task.id, status=2, step=step_name)
                # get_currency(job_id,task.id)
                # write_task_execution_step(
                #     task.id, status=1, step=step_name)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Bank Transfer" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")

                step_name = "Reading data from Bank Transfer"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_bank_transfer(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from QBO chart of account"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_chart_of_account(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from classified_coa"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_classified_coa(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                
                step_name = "Reading data from chart of account"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of account")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Job" == task.function_name:
                update_task_execution_status(
                   task.id, status=2, task_type="read")

                step_name = "Reading data from Job"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_myob_job(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(
                     task.id, status=1, task_type="read")

            if "Employee" == task.function_name:
                update_task_execution_status(
                   task.id, status=2, task_type="read")

                step_name = "Reading data from Employee"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_employee(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(
                   task.id, status=1, task_type="read")

            if "Customer" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")

                step_name = "Reading data from Customer"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_customer(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(
                   task.id, status=1, task_type="read")

            if "Supplier" == task.function_name:
                update_task_execution_status(
                   task.id, status=2, task_type="read")

                step_name = "Reading data from Supplier"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_supplier(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(
                   task.id, status=1, task_type="read")

            if "Item" == task.function_name:
                update_task_execution_status(
                   task.id, status=2, task_type="read")

                step_name = "Reading data from Item"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_item(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Myob Chart of Account"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_chart_of_account(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                
                step_name = "Reading data from QBO Chart of account"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of Account")
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                
                update_task_execution_status(
                   task.id, status=1, task_type="read")

            if "Quotes" == task.function_name:
                update_task_execution_status(
                   task.id, status=2, task_type="read")

                step_name = "Reading data from Quotes"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_item_quote(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(
                   task.id, status=1, task_type="read")

            if "Purchase Order" == task.function_name:
                update_task_execution_status(
                 task.id, status=2, task_type="read")

                step_name = "Reading data from Purchase Order"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_item_purchase_order(job_id,task.id)
                get_service_purchase_order(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from service purchase Order"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_service_purchase_order(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading qbo data from chart of account"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of account")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading qbo data from supplier"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Supplier")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading qbo data from taxrate"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                
                step_name = "Reading qbo data from taxrate"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)


                step_name = "Reading qbo data from tax"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading qbo data from job"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Job")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading qbo data from Employee"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Employee")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading qbo data from customer"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Customer")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading qbo data from Item"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Item")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(
                     task.id, status=1, task_type="read")

            if "Spend Money" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")

                step_name = "Reading data from Spend Money"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_spend_money(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from chart of account"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of account")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from supplier"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Supplier")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from taxrate"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                
                step_name = "Reading data from taxcode"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from tax"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from job"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Job")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Customer"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Customer")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Item"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Item")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                
                update_task_execution_status(
                  task.id, status=1, task_type="read")

            if "Receive Money" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")

                step_name = "Reading data from Receive Money"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_received_money(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                
                step_name = "Reading data from chart of account"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of account")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from supplier"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Supplier")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from taxrate"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                
                step_name = "Reading data from taxcode"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from tax"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                # step_name = "Reading data from job"
                # write_task_execution_step(
                #     task.id, status=2, step=step_name)
                # read_qbo_data(job_id,task.id, "Job")
                # write_task_execution_step(
                #     task.id, status=1, step=step_name)

                # step_name = "Reading data from Employee"
                # write_task_execution_step(
                #     task.id, status=2, step=step_name)
                # read_qbo_data(job_id,task.id, "Employee")
                # write_task_execution_step(
                #     task.id, status=1, step=step_name)

                step_name = "Reading data from Customer"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Customer")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Item"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Item")
                write_task_execution_step(
                    task.id, status=1, step=step_name)


                update_task_execution_status( task.id, status=1, task_type="read")

            if "Invoice" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")

                step_name = "Reading data from all Invoice"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_all_invoice(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from item invoice"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_item_invoice(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from classified invoice"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_classified_invoice(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from service invoice"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_service_invoice(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from chart of account"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of account")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from taxrate"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                
                step_name = "Reading data from taxcode"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from tax"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                
                step_name = "Reading data from Item"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Item")
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                step_name = "Reading data from supplier"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Supplier")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from job"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Job")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Customer"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Customer")
                write_task_execution_step(
                    task.id, status=1, step=step_name)


                update_task_execution_status( task.id, status=1, task_type="read")

            if "Bill" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")

                step_name = "Reading data from all bill"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_all_bill(job_id,task.id)

                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from item bill"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_item_bill(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from service bill"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_service_bill(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                
                step_name = "Reading data from miscellaneous bill"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_miscellaneous_bill(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                
                step_name = "Reading data from professional bill"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_professional_bill(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from final bill1"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_final_bill1(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from final bill2"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_final_bill2(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from final bill3"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_final_bill3(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from final bill"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_final_bill(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

              
                step_name = "Reading data from chart of account"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of account")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from supplier"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Supplier")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from taxrate"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                
                step_name = "Reading data from taxcode"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from tax"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from job"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Job")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Employee"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Employee")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Customer"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Customer")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Delete item data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                delete_item(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Item"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Item")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading myob job"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_myob_job(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                
                update_task_execution_status( task.id, status=1, task_type="read")

            if "Journal" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")

                step_name = "Reading data from Bill"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_journal(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from chart of account"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of account")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from supplier"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Supplier")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from taxrate"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from taxcode"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                
                step_name = "Reading data from tax"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from job"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Job")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Employee"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Employee")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Customer"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Customer")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Item"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Item")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading myob job"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_myob_job(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)


                update_task_execution_status( task.id, status=1, task_type="read")

            if "Payment Allocation" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")

                step_name = "Reading data from invoice payments"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_invoice_payment(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Bill payments"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                # get_bill_payment(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

            if "Bill Payment" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")
                
                step_name = "Reading data from Bill payments"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_bill_payment(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from chart of account"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of account")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from supplier"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Supplier")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from taxrate"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                
                step_name = "Reading data from taxcode"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                

                step_name = "Reading data from tax"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from job"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Job")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Employee"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Employee")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Customer"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Customer")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Item"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Item")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading qbo Invoice"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_bill_for_payments(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
   
                step_name = "Reading data from Myob Bill"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_all_bill(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)


                update_task_execution_status( task.id, status=1, task_type="read")

            if "Invoice Payment" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="read")

                step_name = "Reading data from invoice payments"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_invoice_payment(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from chart of account"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of account")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from supplier"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Supplier")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from taxrate"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                
                step_name = "Reading data from taxcode"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                

                step_name = "Reading data from tax"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from job"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Job")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Employee"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Employee")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Customer"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Customer")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Item"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Item")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading qbo Invoice"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_invoice_for_payments(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
   
                step_name = "Reading all invoice"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_all_invoice(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status( task.id, status=1, task_type="read")


        except Exception as ex:
            write_task_execution_step(
                job_id, task.id, status=0, step=step_name)
            update_task_execution_status(
                job_id, task.id, status=0, task_type="read")
            raise ex

    @staticmethod
    def write_data(job_id, task):
        step_name = None
        try:

            if "Chart of account" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Updating existing chart_of_account data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                update_qbo_existing_chart_account(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Adding duplicate chart_of_account data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_duplicate_chart_account(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Adding chart_of_account data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_chart_account(job_id,task.id)
                read_qbo_data(job_id,task.id, "Chart of account")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Delete coa data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                delete_coa(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Bank Transfer" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Add Bank Transfer Data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_bank_transfer(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Job" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Add Job Data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_job(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Employee" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Add Employee Data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_employee(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Customer" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Add Customer Data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_customer(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Supplier" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Add Supplier Data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_supplier(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Item" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                # step_name = "Add Item Data"
                # write_task_execution_step(
                #     task.id, status=2, step=step_name)
                # add_item(job_id,task.id)
                # write_task_execution_step(
                #     task.id, status=1, step=step_name)

                step_name = "Reading data from Item"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Item")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from all Invoice"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_all_invoice(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from item invoice"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_item_invoice(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Create Item From Invoice using Accountcode"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                create_item_from_invoice(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                
                # step_name = "Reading data from Service invoice"
                # write_task_execution_step(
                #     task.id, status=2, step=step_name)
                # get_service_invoice(job_id,task.id)
                # write_task_execution_step(
                #     task.id, status=1, step=step_name)

                # step_name = "Create Item From Service Invoice"
                # write_task_execution_step(
                #     task.id, status=2, step=step_name)
                # create_item_from_service_invoice(job_id,task.id)
                # write_task_execution_step(
                #     task.id, status=1, step=step_name)

                
                # step_name = "Create Item From Invoice Itemcode and Accountcode"
                # write_task_execution_step(
                #     task.id, status=2, step=step_name)
                # create_item_from_itemcode_acccode(job_id,task.id)
                # write_task_execution_step(
                #     task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Quotes" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Reading data from chart of account"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of account")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from supplier"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Supplier")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from taxrate"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
            
                step_name = "Reading data from taxcode"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from tax"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from job"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Job")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Employee"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Employee")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Customer"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Customer")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Item"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Item")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Add Quotes Data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_item_quote(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Purchase Order" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Reading data from chart of account"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of account")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from supplier"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Supplier")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from taxrate"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                
                step_name = "Reading data from taxcode"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from tax"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from job"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Job")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Employee"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Employee")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Customer"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Customer")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Item"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Item")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Add Item Purchase Order Data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_item_purchase_order(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Add Item Service Purchase Order Data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_service_purchase_order(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Spend Money" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Add Spend Money Data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_spend_money(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Add Negative Spend Money Data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_negative_spend_money(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)


                update_task_execution_status(task.id, status=1, task_type="write")

            if "Receive Money" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                
                step_name = "Add Received Money Data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                # add_received_money(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Add Credit Card Credit Data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_credit_card_credit(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Invoice" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Add Multiple Item Invoice"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_multiple_item_invoice(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Add Multiple Service Invoice"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_multiple_service_invoice(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Bill" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Add Item Bill"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_item_bill(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Add Service Bill"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_service_bill(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                # add_service_bill1(job_id,task.id)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Journal" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Add Journal data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_journal(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Payment Allocation" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Reading data from chart of account"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Chart of account")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from supplier"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Supplier")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from taxrate"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxrate(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                
                step_name = "Reading data from taxcode"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_taxcode(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)
                

                step_name = "Reading data from tax"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_qbo_tax(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from job"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Job")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Employee"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Employee")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Customer"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Customer")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Item"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Item")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Bill"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Bill")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading data from Invoice"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                read_qbo_data(job_id,task.id, "Invoice")
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Reading all invoice"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                get_all_invoice(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Add Invoice Payment Data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_payment(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                step_name = "Add Bill Payment Data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_bill_payment(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Invoice Payment" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Add Invoice Payment Data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_payment(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Bill Payment" == task.function_name:
                update_task_execution_status( task.id, status=2, task_type="write")

                step_name = "Add Bill Payment Data"
                write_task_execution_step(
                    task.id, status=2, step=step_name)
                add_bill_payment(job_id,task.id)
                write_task_execution_step(
                    task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")


        except Exception as ex:
            write_task_execution_step(
                job_id, task.id, status=0, step=step_name)
            update_task_execution_status(task.id, status=0, task_type="write")
            raise ex
