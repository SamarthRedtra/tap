
import frappe
import tap

@frappe.whitelist(allow_guest=True)
def create_customer():
    data = {
        "first_name": 'test',
        "last_name": 'test',
        "email": 'test@test.com',
        "nationality": "Moroccan",
        "currency": "MAD"
    }

    customer = tap.Customer.create(**data)
    return customer



def create_token(card_number, exp_month, exp_year, cvc):
    """
    Create a token for a card using Tap API.

    Args:
        card_number (str): Card number.
        exp_month (int): Expiry month of the card.
        exp_year (int): Expiry year of the card.
        cvc (str): CVC of the card.

    Returns:
        dict: Token response from Tap API.
    """
    data = {
        "card": {
            "number": card_number,
            "exp_month": exp_month,
            "exp_year": exp_year,
            "cvc": cvc
        }
    }

    # Call the Tap API to create a token
    token = tap.Token.create(**data)
    return token


def get_customer(id):
    customer = tap.Customer.retrieve(id=id)
    return customer

def create_charge(customer_id):
    data = {
        "amount": 10,
        "currency": "KWD",
        "customer": {
            "id": customer_id
        },
        "source": {
            "id": "src_all"
        },
        "reference":{
            "order":"SINV-2233"
            
        },
        "post": {
            "url": "http://your_website.com/post_url"
        },
        "redirect": {
            "url": "http://your_website.com/redirect_url"
        }
    }

    charge = tap.Charge.create(**data)
    return charge



def create_card(customer_id, card_number, exp_month, exp_year, cvc):
    """
    Create a card for a customer using Tap API.

    Args:
        customer_id (str): Tap customer ID.
        card_number (str): Card number.
        exp_month (int): Expiry month of the card.
        exp_year (int): Expiry year of the card.
        cvc (str): CVC of the card.

    Returns:
        dict: Card response from Tap API.
    """
    # Generate a token for the card
    token = create_token(card_number, exp_month, exp_year, cvc)

    # Attach the card to the customer
    card = tap.Customer.create_card(customer_id, source=token["id"])
    return card


@frappe.whitelist(allow_guest=True)
def create_customer_with_card():
    # Create a customer
    data = {
        "first_name": 'John',
        "last_name": 'Doe',
        "email": 'john.doe@example.com',
        "nationality": "Kuwaiti",
        "currency": "KWD"
    }
    customer = tap.Customer.create(**data)

    # Create a card for the customer
    card = create_card(
        customer_id=customer["id"],
        card_number="4242424242424242",
        exp_month=12,
        exp_year=2025,
        cvc="123"
    )

    return {
        "customer": customer,
        "card": card
    }




@frappe.whitelist(allow_guest=True)
def list_charges(customer_id=None, limit=25, page=1):
    params = {
      "period": {
        "date": {
          "from": 1735603200000,
          "to": 1736541505514
        }
      },
      "status": "",
      "starting_after": "",
      "limit": 25
    }

    # Ensure that the Authorization header is set
    charges = tap.Charge.list(**params)
    return charges
    
@frappe.whitelist(allow_guest=True)
def create_charge_with_customer_and_card():
    # Create a customer
    customer = tap.Customer.create(**{
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "nationality": "Kuwaiti",
        "currency": "KWD"
    })

    # Create a card for the customer
    card = create_card(
        customer_id=customer["id"],
        card_number="5123450000000008",
        exp_month=1,
        exp_year=2039,
        cvc="100"
    )

    # Create a charge
    charge_data = {
        "amount": 50,
        "currency": "KWD",
        "customer": {"id": customer["id"]},
        "source": {"id": card["id"]},
        "post": {"url": "https://yourwebsite.com/post_url"},
        "redirect": {"url": "https://yourwebsite.com/redirect_url"}
    }
    charge = tap.Charge.create(**charge_data)

    return {
        "customer": customer,
        "card": card,
        "charge": charge
    }

@frappe.whitelist(allow_guest=True)
def create_charge_with_customer():
    customer = create_customer()
    print("customer", customer)
    customer_id = get_customer(customer.id)
    print("customer_id", customer_id)
    charge = create_charge(customer_id.id)
    return charge
