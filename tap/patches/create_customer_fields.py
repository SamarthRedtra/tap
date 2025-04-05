from frappe.custom.doctype.custom_field.custom_field import create_custom_field
import frappe
from frappe import _

def execute():
    add_customer_custom_fields()
    add_for_user_custom_fields()
    add_custom_field_portal_user()
    
    
    


def add_custom_field_portal_user():
    
    custom_fields = [
         {
            'fieldname': 'role',
            'label': 'Portal User Role',
            'fieldtype': 'Select',
            'options': "Member\nAdmin\nGuest",
            'insert_after': 'user',
            'in_list_view':1,
            'description': 'Indicates if the portal user role in a customer portal'
        },
        
    ]
    
    for field in custom_fields:
        try:
            if not frappe.get_meta('Portal User').has_field(field['fieldname']):
                create_custom_field('Portal User', field)
                print(f"Custom field '{field['label']}' added successfully.")
            else:
                print(f"Custom field '{field['label']}' already exists.")
        except Exception as e:
            frappe.log_error(message=str(e), title=_("Custom Field Creation Error"))
            print(f"Error adding custom field '{field['label']}': {str(e)}")
            continue    
    

def add_for_user_custom_fields():
    custom_fields = [
        {
            'fieldname': 'customer_id',
            'label': 'Customer ID',
            'fieldtype': 'Data',
            'insert_after': 'username',
            'read_only': 1,
            'description': 'Indicates if the user is a member'
        },
        {
            'fieldname': 'stripe_customer_id',
            'label': 'Stripe Customer ID',
            'fieldtype': 'Data',
            'insert_after': 'username',
            'read_only': 1,
            'description': 'Indicates if the user is a member'
        },
        {
            'fieldname': 'onboarded',
            'label': 'Is Onboarded',
            'fieldtype': 'Check',
            'insert_after': 'stripe_customer_id',
            'read_only': 1
        },
        {
            'fieldname': 'contract_signed',
            'label': 'Contract Signed',
            'fieldtype': 'Check',
            'insert_after': 'username',
            'read_only': 1
        },
        {
            'fieldname': 'accepted_terms',
            'label': 'Accepted Terms',
            'fieldtype': 'Check',
            'insert_after': 'contract_signed',
            'read_only': 1
        }
        
    ]
    for field in custom_fields:
        try:
            if not frappe.get_meta('User').has_field(field['fieldname']):
                create_custom_field('User', field)
                print(f"Custom field '{field['label']}' added successfully.")
            else:
                print(f"Custom field '{field['label']}' already exists.")
        except Exception as e:
            frappe.log_error(message=str(e), title=_("Custom Field Creation Error"))
            print(f"Error adding custom field '{field['label']}': {str(e)}")
            continue    

def add_customer_custom_fields():
    custom_fields = [
        {
            'fieldname': 'customer_id',
            'label': 'Customer ID',
            'fieldtype': 'Data',
            'insert_after': 'customer_name',
            'read_only': 1,
            'description': 'Indicates if the user is a member'
        },
        {
            'fieldname': 'source_web',
            'label': 'Source Web',
            'fieldtype': 'Check',
            'insert_after': 'currency',
            'read_only': 1
            
        },
        {
            'fieldname': 'nationality',
            'label': 'Nationality',
            'fieldtype': 'Data',
            'insert_after': 'source_web',
            'read_only': 1
        }
    ]

    for field in custom_fields:
        try:
            if not frappe.get_meta('Customer').has_field(field['fieldname']):
                create_custom_field('Customer', field)
                print(f"Custom field '{field['label']}' added successfully.")
            else:
                print(f"Custom field '{field['label']}' already exists.")
        except Exception as e:
            frappe.log_error(message=str(e), title=_("Custom Field Creation Error"))
            print(f"Error adding custom field '{field['label']}': {str(e)}")
            continue