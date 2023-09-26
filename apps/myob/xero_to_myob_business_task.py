from apps.home.data_util import update_task_execution_status, write_task_execution_step

from apps.myob.myob_reader.all_bill import get_all_bill
from apps.myob.myob_reader.all_invoice import get_all_invoice
from apps.myob.myob_reader.all_bill_for_payment import get_all_bill_for_payments
from apps.myob.myob_reader.all_invoice_for_payment import get_all_invoice_for_payments
from apps.xero.reader.invoice import get_invoice_customers


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
from apps.xero.myob_ledger_writer.add_xero_bill_payment_to_myob import add_xero_bill_payment_to_myob
from apps.xero.myob_ledger_writer.add_xero_invoice_payment_as_journal import add_xero_invoicepayment_as_vendorcredit_to_myob
from apps.xero.myob_ledger_writer.add_xero_bill_payment_as_journal_to_myob import add_xero_billpayment_as_vendorcredit_to_myob
from apps.xero.myob_ledger_writer.add_xero_payment_to_myob import add_xero_payment_to_myob
from apps.xero.myob_ledger_writer.add_spend_overpayment import add_spend_overpayment_as_spend_money

from apps.xero.myob_ledger_writer.add_spend_overpayment_as_bill_credit import add_xero_spend_overpayment_as_billcredit_to_myob
from apps.xero.myob_ledger_writer.add_received_overpayment_as_credit_memo import add_xero_overpayment_as_credit_memo_to_myob
from apps.xero.myob_ledger_writer.add_bill_to_myob import add_xero_bill_to_myob
from apps.xero.myob_ledger_writer.add_archived_customer import add_xero_archived_customer_to_myobledger, get_used_archived_customers_myob
from apps.xero.myob_ledger_writer.add_archived_supplier import add_xero_archived_supplier_to_myobledger, get_used_archived_suppliers_myob
from apps.xero.myob_ledger_writer.add_bill_vendorcredite_to_myob import add_xero_vendorcredit_to_myob
from apps.xero.myob_ledger_writer.add_chart_of_account import (
    add_xero_chart_account_to_myobledger, add_xero_chart_of_account_as_default_myobledger,
)
from apps.xero.myob_ledger_writer.add_archived_chart_of_account import add_xero_archived_chart_account_to_myobledger

from apps.xero.myob_ledger_writer.add_customer import add_xero_customer_to_myobledger
from apps.xero.myob_ledger_writer.add_invoice_to_myob import add_xero_invoice_to_myob
from apps.xero.myob_ledger_writer.add_item_xero_to_myob import add_item_xero_to_myob
from apps.xero.myob_ledger_writer.add_job import add_xero_job_to_myobledger
from apps.xero.reader.receive_money import get_xero_receive_money
from apps.xero.reader.payment import get_xero_payment
from apps.xero.reader.invoice_payment import get_xero_invoice_payment
from apps.xero.reader.bill_payment import get_xero_bill_payment

from apps.xero.reader.customer_archived import get_xero_archived_customer
from apps.xero.reader.supplier_archived import get_xero_archived_supplier
from apps.xero.myob_ledger_writer.add_journal import add_xero_journal_to_myobledger
from apps.xero.myob_ledger_writer.add_received_money import (
    add_receive_money_from_xero_to_myobledger,
)
from apps.xero.myob_ledger_writer.add_bill_payment_as_bill_credit_myob import add_xero_bill_credit_to_myob
from apps.xero.myob_ledger_writer.add_bill_credit_refund_as_bill import add_xero_bill_credit_refund

from apps.xero.myob_ledger_writer.add_credit_memo_refund_as_invoice import add_xero_credite_memo_refund_as_invoice
from apps.xero.myob_ledger_writer.add_received_overpayment import (
    add_receive_overpayment_as_received_money,
)
from apps.xero.myob_ledger_writer.add_spend_money import (
    add_spend_money_from_xero_to_myobledger,
)
from apps.xero.myob_ledger_writer.add_supplier import add_xero_supplier_to_myobledger
from apps.xero.myob_ledger_writer.add_xero_creditnote_to_myob import (
    add_xero_creditnote_to_myob,
)
from apps.xero.myob_ledger_writer.edit_chart_of_account import *
from apps.xero.myob_ledger_writer.get_coa_classification import (
    get_xero_classified_coa_for_myobledger,
)

from apps.xero.reader.bank_transfer import get_xero_bank_transfer
from apps.xero.reader.batchpayment import get_xero_invoice_batchpayment, get_xero_bill_batchpayment
from apps.xero.reader.chart_of_account import get_coa, get_archieved_coa
from apps.xero.reader.customer import get_xero_customer
from apps.xero.reader.bill_credit_note_refund_payment import get_xero_bill_credit_memo_refund_payment
from apps.xero.reader.credit_note_refund import get_xero_credit_memo_refund_payment
from apps.xero.reader.supplier import get_xero_supplier
from apps.xero.reader.creditnote import get_creditnote
from apps.xero.reader.vendorcredit import get_vendorcredit
from apps.xero.reader.invoice import get_invoice, get_all_xero_invoice_for_payment, get_all_xero_bill_for_payment
from apps.xero.reader.bill import get_xero_bill, get_bill_suppliers

from apps.xero.reader.items import get_items
from apps.xero.reader.job import get_xero_job
from apps.xero.reader.manual_journal import get_manual_journal
from apps.xero.reader.spend_money import get_xero_spend_money
from apps.xero.reader.tax import get_xero_tax
from apps.util.db_mongo import get_mongodb_database


class XeroToMyobBusiness(object):
    @staticmethod
    def read_data(job_id, task):

        step_name = None
        try:
            dbname = get_mongodb_database()

            if "Job" == task.function_name:

                update_task_execution_status(
                    task.id, status=2, task_type="read")
                step_name = "Reading data from job"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_job(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Customer" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")

                step_name = "Reading data from contact"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_customer(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Archieved Customer" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")

                step_name = "Reading Invoice data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_invoice_customers(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from Archieved Customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_archived_customer(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Archieved Supplier" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")

                step_name = "Reading bill suppliers data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_bill_suppliers(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from Archieved Supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_archived_supplier(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Supplier" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")

                step_name = "Reading data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_supplier(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Existing Chart of account" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_coa(job_id, task.id)

                step_name = "Reading data from myob_chart_of_account"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id, task.id)

                step_name = "Reading data from duplicate_chart_of_account"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_duplicate_chart_of_account_myob(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Chart of account" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_coa(job_id, task.id)

                step_name = "Reading data from classified coa"
                get_xero_classified_coa_for_myobledger(job_id, task.id)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_tax(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Archieved Chart of account" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")

                step_name = "Reading xero archieved chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_archieved_coa(job_id, task.id)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_coa(job_id, task.id)

                step_name = "Reading data from classified coa"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_classified_coa_for_myobledger(job_id, task.id)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_tax(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Item" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")

                step_name = "Reading data from item"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_items(job_id, task.id)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_coa(job_id, task.id)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_taxrate'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_xero_tax(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Bank Transfer" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")
                step_name = "Reading data from bank transfer"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_bank_transfer(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Spend Money" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")
                step_name = "Reading data from spend money"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_spend_money(job_id, task.id)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_coa(job_id, task.id)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_taxrate'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_xero_tax(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Receive Money" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")

                step_name = "Reading data from receive money"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_receive_money(job_id, task.id)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_coa(job_id, task.id)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_taxrate'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_xero_tax(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Journal" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")
                step_name = "Reading data from manual journal"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_manual_journal(job_id, task.id)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_taxrate'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_xero_tax(job_id, task.id)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_coa(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Invoice" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")
                step_name = "Reading data from invoice"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_invoice(job_id, task.id)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_taxrate'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_xero_tax(job_id, task.id)

                step_name = "Reading data from item"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_items'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_items(job_id, task.id)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_coa(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Invoice CreditNote" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")

                step_name = "Reading data from creaditnote"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_creditnote(job_id, task.id)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_taxrate'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_xero_tax(job_id, task.id)

                step_name = "Reading data from item"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_items'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_items(job_id, task.id)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_coa(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Bill" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")
                step_name = "Reading data from bill"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_bill(job_id, task.id)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_taxrate'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_xero_tax(job_id, task.id)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_coa(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Bill VendorCredit" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")

                step_name = "Reading data from Vendorcredit"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_vendorcredit(job_id, task.id)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_taxrate'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_xero_tax(job_id, task.id)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_coa(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Payment Allocation" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")

                step_name = "Reading data from payment"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_payment(job_id, task.id)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_coa(job_id, task.id)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_taxrate'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_xero_tax(job_id, task.id)

                step_name = "Reading data from invoice"
                write_task_execution_step(task.id, status=2, step=step_name)
                # get_all_xero_invoice_for_payment(job_id, task.id)
                get_invoice(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Invoice Payment" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")

                step_name = "Reading data from invoice payment"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_invoice_payment(job_id, task.id)

                step_name = "Reading xero archived chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_archieved_coa(job_id, task.id)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_coa(job_id, task.id)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_taxrate'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_xero_tax(job_id, task.id)

                step_name = "Reading data from xero all invoice"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_all_xero_invoice_for_payment(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Bill Payment" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")

                step_name = "Reading data from bill payment"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_bill_payment(job_id, task.id)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_coa(job_id, task.id)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_taxrate'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_xero_tax(job_id, task.id)

                step_name = "Reading data from xero all bill"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_xero_bill(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Invoice Credit Memo Refund" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")

                step_name = "Reading data from credit memo refund"
                write_task_execution_step(task.id, status=2, step=step_name)
                # get_xero_credit_memo_refund_payment(job_id, task.id)
                get_xero_payment(job_id,task.id)


                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_coa(job_id, task.id)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_taxrate'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_xero_tax(job_id, task.id)

                step_name = "Reading data from item"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_items(job_id, task.id)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_archieved_coa(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

            if "Bill Credit Memo Refund" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="read")

                step_name = "Reading data from  bill credit memo refund"
                write_task_execution_step(task.id, status=2, step=step_name)
                # get_xero_bill_credit_memo_refund_payment(job_id, task.id)
                get_xero_payment(job_id,task.id)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_coa'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_coa(job_id, task.id)

                step_name = "Reading data from taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['xero_taxrate'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_xero_tax(job_id, task.id)

                step_name = "Reading data from item"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_items(job_id, task.id)

                step_name = "Reading xero chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_archieved_coa(job_id, task.id)

                update_task_execution_status(
                    task.id, status=1, task_type="read")

        except Exception as ex:
            write_task_execution_step(task.id, status=0, step=step_name)
            update_task_execution_status(
                job_id, task.id, status=0, task_type="read")
            raise ex

    @staticmethod
    def write_data(job_id, task):
        step_name = None
        try:
            dbname = get_mongodb_database()

            if "Job" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")
                step_name = "Adding job"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_job_to_myobledger(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Customer" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['taxcode_myob'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_taxcode_myob(job_id, task.id)

                step_name = "Adding customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_customer_to_myobledger(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Supplier" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['taxcode_myob'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_taxcode_myob(job_id, task.id)

                step_name = "Adding supplier data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_supplier_to_myobledger(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Archieved Customer" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['taxcode_myob'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_taxcode_myob(job_id, task.id)

                step_name = "Adding data Archieved Customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_used_archived_customers_myob(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding data Archieved Customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_archived_customer_to_myobledger(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Archieved Supplier" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Get Archieved supplier data"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_used_archived_suppliers_myob(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['taxcode_myob'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_taxcode_myob(job_id, task.id)

                step_name = "Adding data Archieved Supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_archived_supplier_to_myobledger(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Chart of account" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Reading data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['chart_of_account'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_chart_of_account(job_id, task.id)

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['taxcode_myob'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_taxcode_myob(job_id, task.id)

                step_name = "Adding default chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_chart_of_account_as_default_myobledger(
                    job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_chart_account_to_myobledger(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Archieved Chart of account" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Reading data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['chart_of_account'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_chart_of_account(job_id, task.id)

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['taxcode_myob'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_taxcode_myob(job_id, task.id)

                step_name = "Adding archived chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_archived_chart_account_to_myobledger(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Existing Chart of account" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Updating existing chart_of_account data"
                write_task_execution_step(task.id, status=2, step=step_name)
                update_existing_chart_account_xero_myob(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Item" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Reading data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['chart_of_account'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_chart_of_account(job_id, task.id)

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['taxcode_myob'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_taxcode_myob(job_id, task.id)

                step_name = "Adding Item"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_item_xero_to_myob(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Bank Transfer" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Reading data from  myob chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id, task.id)

                step_name = "Adding bank transfer data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_bank_transfer_to_myobledger(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Spend Money" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")
                step_name = "Reading data from job"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['job'].count_documents({"job_id": job_id})
                if results == 0:

                    get_myob_job(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['chart_of_account'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_chart_of_account(job_id, task.id)

                step_name = "Reading data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['supplier'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_supplier(job_id, task.id)

                step_name = "Reading data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['customer'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_customer(job_id, task.id)

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['taxcode_myob'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_taxcode_myob(job_id, task.id)

                step_name = "Adding spend money data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_spend_money_from_xero_to_myobledger(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding spend money overpayment data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_spend_overpayment_as_billcredit_to_myob(
                    job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Receive Money" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")
                step_name = "Reading data from job"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['job'].count_documents({"job_id": job_id})
                if results == 0:

                    get_myob_job(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['chart_of_account'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_chart_of_account(job_id, task.id)

                step_name = "Reading data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['supplier'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_supplier(job_id, task.id)

                step_name = "Reading data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['customer'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_customer(job_id, task.id)

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['taxcode_myob'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_taxcode_myob(job_id, task.id)

                step_name = "Adding receive money data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_receive_money_from_xero_to_myobledger(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding receive money overpayment data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_overpayment_as_credit_memo_to_myob(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)
                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Journal" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Reading data from job"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['job'].count_documents({"job_id": job_id})
                if results == 0:

                    get_myob_job(job_id, task.id)

                step_name = "Reading data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['chart_of_account'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_chart_of_account(job_id, task.id)

                step_name = "Reading data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['supplier'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_supplier(job_id, task.id)

                step_name = "Reading data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['customer'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_customer(job_id, task.id)

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['taxcode_myob'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_taxcode_myob(job_id, task.id)

                step_name = "Adding journal "
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_journal_to_myobledger(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Invoice" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Reading data from job"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['job'].count_documents({"job_id": job_id})
                if results == 0:

                    get_myob_job(job_id, task.id)

                step_name = "Reading data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['chart_of_account'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_chart_of_account(job_id, task.id)

                step_name = "Reading data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['supplier'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_supplier(job_id, task.id)

                step_name = "Reading data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['customer'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_customer(job_id, task.id)

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['taxcode_myob'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_taxcode_myob(job_id, task.id)

                step_name = "Reading data from myob item"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['item'].count_documents({"job_id": job_id})
                if results == 0:

                    get_item(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding invoice data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_invoice_to_myob(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Invoice CreditNote" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Reading data from job"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['job'].count_documents({"job_id": job_id})
                if results == 0:

                    get_myob_job(job_id, task.id)

                step_name = "Reading data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['chart_of_account'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_chart_of_account(job_id, task.id)

                step_name = "Reading data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['supplier'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_supplier(job_id, task.id)

                step_name = "Reading data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['customer'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_customer(job_id, task.id)

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['taxcode_myob'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_taxcode_myob(job_id, task.id)

                step_name = "Reading data from myob item"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['item'].count_documents({"job_id": job_id})
                if results == 0:

                    get_item(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id, task.id)

                step_name = "Adding invoice credit-note data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_creditnote_to_myob(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Bill" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Reading data from job"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['job'].count_documents({"job_id": job_id})
                if results == 0:

                    get_myob_job(job_id, task.id)

                step_name = "Reading data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['chart_of_account'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_chart_of_account(job_id, task.id)

                step_name = "Reading data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['supplier'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_supplier(job_id, task.id)

                step_name = "Reading data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['customer'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_customer(job_id, task.id)

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['taxcode_myob'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_taxcode_myob(job_id, task.id)

                step_name = "Reading data from myob item"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['item'].count_documents({"job_id": job_id})
                if results == 0:

                    get_item(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding bill data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_bill_to_myob(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Bill VendorCredit" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Reading data from job"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['job'].count_documents({"job_id": job_id})
                if results == 0:

                    get_myob_job(job_id, task.id)

                step_name = "Reading data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['chart_of_account'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_chart_of_account(job_id, task.id)

                step_name = "Reading data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['supplier'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_supplier(job_id, task.id)

                step_name = "Reading data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['customer'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_customer(job_id, task.id)

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['taxcode_myob'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_taxcode_myob(job_id, task.id)

                step_name = "Reading data from myob item"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['item'].count_documents({"job_id": job_id})
                if results == 0:

                    get_item(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding vendor-credit data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_vendorcredit_to_myob(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Invoice Payment" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Reading data from all invoice "
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['all_invoice'].count_documents(
                    {"job_id": job_id})
                if results == 0:

                    get_all_invoice_for_payments(job_id, task.id)

                step_name = "Reading data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['chart_of_account'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_chart_of_account(job_id, task.id)

                step_name = "Reading data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['supplier'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_supplier(job_id, task.id)

                step_name = "Reading data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['customer'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_customer(job_id, task.id)

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['taxcode_myob'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_taxcode_myob(job_id, task.id)

                step_name = "Adding invoice payment data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_payment_to_myob(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding invoice payment as journal data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_invoicepayment_as_vendorcredit_to_myob(
                    job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Bill Payment" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Reading data from all bill"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['all_bill'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_all_bill(job_id, task.id)

                step_name = "Reading data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['chart_of_account'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_chart_of_account(job_id, task.id)

                step_name = "Reading data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['supplier'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_supplier(job_id, task.id)

                step_name = "Reading data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['customer'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_customer(job_id, task.id)

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['taxcode_myob'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_taxcode_myob(job_id, task.id)

                step_name = "Adding bill payment data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_bill_payment_to_myob(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding bill payment as vendor credit data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_billpayment_as_vendorcredit_to_myob(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Invoice Credit Memo Refund" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Reading data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['chart_of_account'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_chart_of_account(job_id, task.id)

                step_name = "Reading data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['customer'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_customer(job_id, task.id)

                step_name = "Reading data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['supplier'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_supplier(job_id, task.id)

                step_name = "Reading data from myob item"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['item'].count_documents({"job_id": job_id})
                if results == 0:

                    get_item(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['taxcode_myob'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_taxcode_myob(job_id, task.id)

                step_name = "Adding invoice credit memo refund data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_credite_memo_refund_as_invoice(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Bill Credit Memo Refund" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Reading data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['chart_of_account'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_chart_of_account(job_id, task.id)

                step_name = "Reading data from myob item"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['item'].count_documents({"job_id": job_id})
                if results == 0:

                    get_item(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['customer'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_customer(job_id, task.id)

                step_name = "Reading data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['supplier'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_supplier(job_id, task.id)

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                results = dbname['taxcode_myob'].count_documents(
                    {"job_id": job_id})
                if results == 0:
                    get_taxcode_myob(job_id, task.id)

                step_name = "Adding bill credit memo refund data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_bill_credit_refund(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(
                    task.id, status=1, task_type="write")

            if "Payment Allocation" == task.function_name:
                update_task_execution_status(
                    task.id, status=2, task_type="write")

                step_name = "Reading data from all invoice "
                write_task_execution_step(task.id, status=2, step=step_name)
                # get_all_invoice_for_payments(job_id, task.id)
                # get_all_invoice(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Reading data from all bill"
                write_task_execution_step(task.id, status=2, step=step_name)
                # get_all_bill_for_payments(job_id, task.id)
                get_all_bill(job_id, task.id)

                step_name = "Reading data from chart of account"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_chart_of_account(job_id, task.id)

                step_name = "Reading data from supplier"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_supplier(job_id, task.id)

                step_name = "Reading data from customer"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_customer(job_id, task.id)

                step_name = "Reading data from myob taxcode"
                write_task_execution_step(task.id, status=2, step=step_name)
                get_taxcode_myob(job_id, task.id)

                step_name = "Adding invoice payment data"
                write_task_execution_step(task.id, status=2, step=step_name)
                add_xero_payment_to_myob(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding bill payment data"
                write_task_execution_step(task.id, status=2, step=step_name)
                # add_xero_bill_payment_to_myob(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                step_name = "Adding bill payment as journal data"
                write_task_execution_step(task.id, status=2, step=step_name)
                # add_xero_billpayment_as_vendorcredit_to_myob(job_id, task.id)
                write_task_execution_step(task.id, status=1, step=step_name)

                update_task_execution_status(
                    task.id, status=1, task_type="write")

        except Exception as ex:
            write_task_execution_step(task.id, status=0, step=step_name)
            update_task_execution_status(
                job_id, task.id, status=0, task_type="write")
            raise ex
