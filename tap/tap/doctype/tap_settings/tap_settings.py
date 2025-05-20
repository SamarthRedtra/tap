# Copyright (c) 2025, Samarth Upare and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.integrations.utils import create_request_log, make_get_request
from frappe.utils import call_hook_method, cint, flt, get_url
from payments.utils import create_payment_gateway
from frappe import _ 
from frappe.utils import get_url
import tap
from tap.util import get_tap
currency_wise_minimum_charge_amount = {
	"KWD": 0.50,
	"OMR": 0.50,
	"QAR": 0.50,
	"SAR": 0.50,
	"USD": 0.50,
	"AED": 0.50
}

class TapSettings(Document):
	supported_currencies = (
		"KWD",
		"BHD",
		"OMR",
		"QAR",
		"SAR",
		"USD",
		"AED",
		)
	def validate_transaction_currency(self, currency):
		if currency not in self.supported_currencies:
			frappe.throw(
				_(
					"Please select another payment method. Tap does not support transactions in currency '{0}'"
				).format(currency)
			)

	# def validate_minimum_transaction_amount(self, currency, amount):
	# 	if currency in self.currency_wise_minimum_charge_amount:
	# 		if flt(amount) < self.currency_wise_minimum_charge_amount.get(currency, 0.0):
	# 			frappe.throw(
	# 				_("For currency {0}, the minimum transaction amount should be {1}").format(
	# 					currency, self.currency_wise_minimum_charge_amount.get(currency, 0.0)
	# 				)
	# 			)
 
	# {'amount': 450.0, 'title': 'Redtra', 'description': 'Payment Request for SAL-ORD-2025-00006', 'reference_doctype': 'Payment Request', 'reference_docname': 'ACC-PRQ-2025-00010', 'payer_email': 'Administrator', 'payer_name': 'Administrator', 'order_id': 'ACC-PRQ-2025-00010', 'currency': 'AED', 'payment_gateway': 'Tap'}
    
	def get_payment_url(self, **kwargs):
		tap = get_tap()
		order_id = kwargs.get("description").split("Payment Request for ")[1]
    
		payload  = {
			"amount": kwargs.get("amount"),
			"currency": kwargs.get("currency"),
			"live_mode": tap.live_mode,
			"save_card": False,
			"customer": {
				"first_name": kwargs.get("payer_name"),
				"last_name": kwargs.get("payer_name"),
				"email": kwargs.get("payer_email"),
			},
			"source": {
				"id": "src_all"
			},
			"receipt": {
				"email": True,
				"sms": True
			},
			"reference": {
				"order": order_id,
				"description": kwargs.get("description"),
				"transaction": kwargs.get("reference_docname"),
			},
			"post": {
				"url": get_url("/") + "api/method/tap.tap.doctype.tap_settings.tap_settings.tap_charge_webhook",
			},
			"redirect": {
				"url": get_url("/orders/{0}".format(order_id)),
			}
    	}
		self.integration_request = create_request_log( payload, service_name="Tap")
		self.integration_request.db_set("status", "Queued", update_modified=False)
		if self.integration_request.name:
			payload["reference"]["internal_reference"] = self.integration_request.name
		
		charge = tap.Charge.create(
			**payload
		)
		if charge.status.upper() == "INITIATED":
			return charge.transaction.url
		else:
			frappe.throw(_("Payment failed"))
			return {
				"redirect_to": frappe.redirect_to_message(
					_("Server Error"),
					_(
						"It seems that there is an issue with the server's Tap configuration. In case of failure, the amount will get refunded to your account."
					),
				),
				"status": 401,
			}
   

@frappe.whitelist(allow_guest=True)
def tap_charge_webhook(**kwargs):
	"""Webhook to handle Tap payment status updates"""
	try:
		data = frappe.parse_json(kwargs)
		event_type = data.get("type")
		charge = data.get("object", {}).get("charge") or data.get("object", {})
		status = charge.get("status")
		payment_request_id = charge.get("metadata", {}).get("payment_request_id") or charge.get("reference", {}).get("transaction")
		integration_request_id = charge.get("metadata", {}).get("integration_request_id") or charge.get("reference", {}).get("internal_reference")
		

		if not payment_request_id:
			frappe.log_error(str(data), "Tap Webhook: Missing payment_request_id")
			return

		doc = frappe.get_doc("Payment Request", payment_request_id)
		doc.flags.ignore_permissions = True

		if status in ("CAPTURED", "SUCCEEDED"):
			doc.set_as_paid()
			frappe.db.set_value("Integration Request", integration_request_id, "status", "Completed", update_modified=False)

			frappe.logger().info(f"[Tap] Payment succeeded for {payment_request_id}")

		elif status in ("FAILED", "DECLINED", "EXPIRED", "CANCELLED"):
			doc.set_as_failed()
			upstates = "Cancelled" if status == "CANCELLED" else "Failed"
			frappe.db.set_value("Integration Request", integration_request_id, "status",upstates, update_modified=False)

			frappe.logger().info(f"[Tap] Payment failed or cancelled for {payment_request_id} with status: {status}")

		frappe.db.commit()

	except Exception:
		frappe.log_error(frappe.get_traceback(), "Tap Charge Webhook Error")   
		
        
    
    
