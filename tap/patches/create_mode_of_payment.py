import frappe

def execute():
    if frappe.db.exists("DocType", "Mode of Payment"):
        if not frappe.db.exists("Mode of Payment", "Online"):
            frappe.db.sql("""insert into `tabMode of Payment` (`name`, `mode_of_payment`, `type`) values ('Online', 'Online', 'Bank')""")
    