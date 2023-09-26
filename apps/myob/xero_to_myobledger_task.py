from apps.home.data_util import update_task_execution_status, write_task_execution_step
from apps.home.models import Task
from apps.myob.myob_ledger_writer.add_bank_transfer_myobledger import (
    add_qbo_bank_transfer_to_myobledger,
)
from apps.myob.myob_ledger_writer.add_coa_myob import (
    add_qbo_coa_to_myob,
    add_qbo_existing_chart_account_to_myob,
)
from apps.myob.myob_ledger_writer.add_customer import add_qbo_customer_to_myobledger
from apps.myob.myob_ledger_writer.add_item_myob_business import add_qbo_item_to_myob
from apps.myob.myob_ledger_writer.add_job import add_qbo_job_to_myobledger
from apps.myob.myob_ledger_writer.add_journal_myobledger import (
    add_qbo_journal_to_myobledger,
)
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
from apps.myob.myob_ledger_writer.update_existing_coa import *
from apps.myob.myob_reader.all_bill import get_all_bill
from apps.myob.myob_reader.all_invoice import get_all_invoice
# from apps.myob.myob_ledger_writer.add_Bank_Transfer import add_qbo_bank_transfer_to_myobledger
from apps.myob.myob_reader.chart_of_account import get_chart_of_account
from apps.myob.myob_reader.customer import get_customer
from apps.myob.myob_reader.item import get_item
from apps.myob.myob_reader.job import get_myob_job
from apps.myob.myob_reader.myobledger_taxcode import get_taxcode_myob
from apps.myob.myob_reader.supplier import get_supplier
from apps.myob.myob_to_qbo_task import MyobToQbo
from apps.xero.myob_ledger_writer.add_bank_transfer import (
    add_xero_bank_transfer_to_myobledger,
)
from apps.xero.myob_ledger_writer.add_bill import (
    add_xero_bill_as_journal_to_myobledger,
    add_xero_vendorcredit_as_journal_to_myobledger,
)
from apps.xero.myob_ledger_writer.add_bill_to_myob import add_xero_bill_to_myob
from apps.xero.myob_ledger_writer.add_chart_of_account import (
    add_xero_chart_account_to_myobledger,
)
from apps.xero.myob_ledger_writer.add_customer import add_xero_customer_to_myobledger
from apps.xero.myob_ledger_writer.add_invoice_to_myob import add_xero_invoice_to_myob
from apps.xero.myob_ledger_writer.add_spend_overpayment import add_spend_overpayment_as_spend_money

from apps.xero.myob_ledger_writer.add_item_xero_to_myob import add_item_xero_to_myob
from apps.xero.myob_ledger_writer.add_job import add_xero_job_to_myobledger
from apps.xero.myob_ledger_writer.add_journal import add_xero_journal_to_myobledger
from apps.xero.myob_ledger_writer.add_payment import (
    add_invoice_payment_as_receive_money,
)
from apps.xero.myob_ledger_writer.add_received_money import (
    add_receive_money_from_xero_to_myobledger,
)
from apps.xero.myob_ledger_writer.add_received_overpayment import (
    add_receive_overpayment_as_received_money,
)
from apps.xero.myob_ledger_writer.add_spend_money import (
    add_spend_money_from_xero_to_myobledger,
)

from apps.xero.myob_ledger_writer.add_payment import add_invoice_batchpayment_as_receive_money,add_bill_batchpayment_as_spend_money,add_bill_payment_as_spend_money,add_invoice_payment_as_receive_money
from apps.xero.myob_ledger_writer.add_invoice import add_xero_creditnote_as_journal_to_myobledger,add_xero_invoice_as_journal_to_myobledger
from apps.xero.myob_ledger_writer.add_supplier import add_xero_supplier_to_myobledger
from apps.xero.myob_ledger_writer.add_xero_creditnote_to_myob import (
    add_xero_creditnote_to_myob,
)
from apps.xero.myob_ledger_writer.edit_chart_of_account import *
from apps.xero.myob_ledger_writer.get_coa_classification import (
    get_xero_classified_coa_for_myobledger,
)
from apps.xero.qbo_writer.add_bank_transfer import add_xero_bank_transfer
from apps.xero.qbo_writer.add_customer import add_xero_customer
from apps.xero.qbo_writer.add_employee import add_xero_employee
from apps.xero.qbo_writer.add_item import *
from apps.xero.qbo_writer.add_item_purchase_order import add_xero_item_purchase_order
from apps.xero.qbo_writer.add_item_quotes import add_xero_item_quote
from apps.xero.qbo_writer.add_job import add_xero_job
from apps.xero.qbo_writer.add_payment import add_xero_invoice_payment
from apps.xero.qbo_writer.add_received_money import add_xero_receive_money
from apps.xero.qbo_writer.add_service_purchase_order import (
    add_service_xero_purchase_order,
)
from apps.xero.qbo_writer.add_spend_money import add_xero_spend_money
from apps.xero.qbo_writer.add_supplier import add_xero_supplier
# from apps.xero.qbo_writer.add_xero_invoice_1 import add_xero_invoice
from apps.xero.qbo_writer.add_xero_invoice import add_xero_invoice
from apps.xero.qbo_writer.get_COA_classification import get_xero_classified_coa
from apps.xero.qbo_writer.test_combined_bill import add_xero_bill
from apps.xero.reader.bank_transfer import get_xero_bank_transfer
from apps.xero.reader.batchpayment import get_xero_invoice_batchpayment,get_xero_bill_batchpayment
from apps.xero.reader.chart_of_account import get_coa
from apps.xero.reader.receive_money import get_xero_receive_money
from apps.xero.reader.payment import get_xero_payment
from apps.xero.reader.customer import get_xero_customer
from apps.xero.reader.supplier import get_xero_supplier
from apps.xero.reader.creditnote import get_creditnote
from apps.xero.reader.employee import get_xero_employee
from apps.xero.reader.invoice import get_invoice
from apps.xero.reader.items import get_items
from apps.xero.reader.job import get_xero_job
from apps.xero.reader.manual_journal import get_manual_journal
from apps.xero.reader.purchase_order import get_xero_purchase_order
from apps.xero.reader.quotes import get_xero_quotes
from apps.xero.reader.spend_money import get_xero_spend_money
from apps.xero.reader.tax import get_xero_tax


class XeroToMyobledger(object):
    @staticmethod
    def read_data(self, job_id, task):
        step_name = None
        try:
            dbname = get_mongodb_database()

            if "Chart of account" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="read")
                step_name = "Reading data from myob_chart_of_account"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from chart_of_account"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_coa(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from classified coa"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_classified_coa_for_myobledger(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_tax(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from myob_taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(task.id, status=1, task_type="read")

            if "Job" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="read")
                step_name = "Reading data from job"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_job(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(task.id, status=1, task_type="read")

            if "Customer" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="read")
                step_name = "Reading data from contact"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_customer(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(task.id, status=1, task_type="read")

            if "Supplier" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="read")
                step_name = "Reading data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_supplier(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(task.id, status=1, task_type="read")

            if "Bank Transfer" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="read")

                step_name = "Reading data from bank transfer"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_bank_transfer(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="read")

            if "Spend Money" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="read")

                step_name = "Reading data from spend money"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_spend_money(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents({"job_id": job_id})
                if results == 0:
                    get_coa(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from xero_taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_tax(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="read")

            if "Receive Money" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="read")

                step_name = "Reading data from receive money"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_receive_money(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents({"job_id": job_id})
                if results == 0:
                    get_coa(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading xero tax"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_taxrate'].count_documents({"job_id": job_id})
                if results == 0:
                    get_xero_tax(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="read")

            if "Journal" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="read")

                step_name = "Reading data from manual journal"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_manual_journal(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading xero tax"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_taxrate'].count_documents({"job_id": job_id})
                if results == 0:
                    get_xero_tax(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents({"job_id": job_id})
                if results == 0:
                    get_coa(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="read")

            if "Invoice" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="read")
                step_name = "Reading data from invoice"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_invoice(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from credit-note"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_creditnote(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading xero tax"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_taxrate'].count_documents({"job_id": job_id})
                if results == 0:
                    get_xero_tax(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from item"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_items(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents({"job_id": job_id})
                if results == 0:
                    get_coa(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="read")

            if "Bill" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="read")
                step_name = "Reading data from bill"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_invoice(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from credit-note"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_creditnote(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading xero tax"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_taxrate'].count_documents({"job_id": job_id})
                if results == 0:
                    get_xero_tax(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents({"job_id": job_id})
                if results == 0:
                    get_coa(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="read")

            if "Payment Allocation" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="read")
                step_name = "Reading data from invoice batch-payment"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_invoice_batchpayment(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)
    
                step_name = "Reading data from bill batch-payment"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_bill_batchpayment(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)
                
                step_name = "Reading data from payment"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_payment(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading xero tax"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_taxrate'].count_documents({"job_id": job_id})
                if results == 0:
                    get_xero_tax(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents({"job_id": job_id})
                if results == 0:
                    get_coa(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from invoice"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_invoice(job_id)
                get_all_invoice(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from all bill"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_all_bill(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(task.id, status=1, task_type="read")


        except Exception as ex:
            write_task_execution_step(task.id, status=0, step=step_name)
            update_task_execution_status(job_id, task.id, status=0, task_type="read")
            raise ex

    @staticmethod
    def write_data(self, job_id, task):
        step_name = None
        try:
            if "Chart of account" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")

                step_name = "Adding chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_chart_account_to_myobledger(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(task.id, status=1, task_type="write")

            if "Job" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")

                step_name = "Adding job data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_job_to_myobledger(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Customer" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")

                step_name = "Adding customer data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_customer_to_myobledger(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Supplier" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")

                step_name = "Adding supplier data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_supplier_to_myobledger(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Bank Transfer" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")

                step_name = "Reading myob data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding bank transfer data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_bank_transfer_to_myobledger(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Spend Money" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")

                step_name = "Reading myob data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_supplier(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_customer(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from job"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_myob_job(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding spend money data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_spend_money_from_xero_to_myobledger(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding spend money overpayment data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_spend_overpayment_as_spend_money(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(task.id, status=1, task_type="write")

            if "Receive Money" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")
                step_name = "Reading myob data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_supplier(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_customer(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from job"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_myob_job(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding receive money data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_receive_money_from_xero_to_myobledger(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding receive money overpayment data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_receive_overpayment_as_received_money(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(task.id, status=1, task_type="write")

            if "Journal" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")

                step_name = "Reading myob data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_supplier(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_customer(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from job"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_myob_job(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding journal data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_journal_to_myobledger(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(task.id, status=1, task_type="write")

            if "Invoice" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")
                step_name = "Reading myob data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_supplier(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_customer(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from job"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_myob_job(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding invoice data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_invoice_as_journal_to_myobledger(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding credit-note"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_creditnote_as_journal_to_myobledger(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(task.id, status=1, task_type="write")

            if "Bill" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")

                step_name = "Reading myob data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_supplier(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_customer(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from job"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_myob_job(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding bill data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_bill_as_journal_to_myobledger(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding vendor-credit data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_vendorcredit_as_journal_to_myobledger(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(task.id, status=1, task_type="write")

            if "Payment Allocation" == task.function_name:
                update_task_execution_status(task.id, status=2, task_type="write")
                step_name = "Reading myob data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_supplier(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_customer(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from job"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_myob_job(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading myob data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding invoice payment as receive money data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_invoice_payment_as_receive_money(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding invoice batch-payment as receive money data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_invoice_batchpayment_as_receive_money(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding bill payment as spend money data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_bill_payment_as_spend_money(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding bill batch-payment as spend money"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_bill_batchpayment_as_spend_money(job_id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(task.id, status=1, task_type="write")

        except Exception as ex:
            write_task_execution_step(task.id, status=0, step=step_name)
            update_task_execution_status(job_id, task.id, status=0, task_type="read")
            raise ex
