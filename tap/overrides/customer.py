import frappe
from tap.util import get_tap
from erpnext.selling.doctype.customer.customer import Customer

class CustomCustomer(Customer):
    def before_insert(self):
        if self.get('source_web',None) == 1:
            tap = get_tap()
            resp = tap.Customer.create(**{
                "first_name": self.customer_name.split(' ')[0],
                "last_name": self.customer_name.split(' ')[1],
                "email": self.email_id,
                "nationality": self.nationality,
                "currency": self.billing_currency,
                "phone":{
                    "country_code": self.mobile_no.split('-')[0][1:],
                    "number": self.mobile_no.split('-')[1]
                }
            })
            self.customer_id = resp["id"]
            frappe.db.set_value('User',self.email_id,'customer_id',self.customer_id)


