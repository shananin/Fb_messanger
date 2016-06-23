from interfaces import IFBPayload


class Image(IFBPayload):
    def __init__(self, image_url):
        self.image_url = image_url

    def get_dict(self):
        return {
            'type': 'image',
            'payload': {
                'url': self.image_url,
            },
        }


class Buttons(IFBPayload):
    def __init__(self, text, buttons):
        self.text = text
        self.buttons = buttons

    def get_dict(self):
        button_dicts = []

        for button in self.buttons:
            button_dicts.append(button.get_dict())

        return {
            'type': 'template',
            'payload': {
                'template_type': 'button',
                'text': self.text,
                'buttons': button_dicts
            }
        }


class GenericElement(IFBPayload):
    def __init__(self, title, item_url=None, image_url=None, subtitle=None, buttons=None):
        self.title = title
        self.item_url = item_url
        self.image_url = image_url
        self.subtitle = subtitle
        self.buttons = buttons

    def get_dict(self):
        button_dicts = []

        data = {
            'title': self.title,
        }

        if self.item_url:
            data['item_url'] = self.item_url

        if self.image_url:
            data['image_url'] = self.image_url

        if self.subtitle:
            data['subtitle'] = self.subtitle

        if self.buttons:
            for button in self.buttons:
                button_dicts.append(button.get_dict())

            data['buttons'] = button_dicts

        return data


class Generic(IFBPayload):
    def __init__(self, elements):
        self.elements = elements

    def get_dict(self):
        element_dicts = []

        for element in self.elements:
            element_dicts.append(element.get_dict())

        return {
            'type': 'template',
            'payload': {
                'template_type': 'generic',
                'elements': element_dicts,
            },
        }


class Receipt(IFBPayload):
    """
    TODO: complete receipt attachment
    """
    def __init__(self, recipient_name, order_number, currency, payment_method, elements, summary,
                 timestamp=None, order_url=None, address=None, adjustments=None):
        self.recipient_name = recipient_name
        self.order_number = order_number
        self.currency = currency
        self.payment_method = payment_method
        self.elements = elements
        self.summary = summary
        self.timestamp = timestamp
        self.order_url = order_url
        self.address = address
        self.adjustments = adjustments

    def get_dict(self):
        element_dicts = []

        for elem in self.elements:
            element_dicts.append(elem.get_dict())

        data = {
            'type': 'template',
            'payload': {
                'template_type': 'receipt',
                'recipient_name': self.recipient_name,
                'order_number': self.order_number,
                'currency': self.currency,
                'payment_method': self.payment_method,
                'elements': element_dicts,
                'summary': self.summary.get_dict(),
            },
        }

        if self.timestamp:
            data['timestamp'] = self.timestamp

        if self.order_url:
            data['order_url'] = self.order_url

        if self.address:
            data['address'] = self.address.get_dict()

        if self.adjustments:
            adjustments_dicts = []

            for elem in self.adjustments:
                adjustments_dicts.append(elem.get_dict())

            data['adjustments'] = adjustments_dicts

        return data


class Summary(IFBPayload):
    def __init__(self, total_cost, subtotal=None, shipping_cost=None, total_tax=None):
        self.total_cost = total_cost
        self.subtotal = subtotal
        self.shipping_cost = shipping_cost
        self.total_tax = total_tax

    def get_dict(self):
        data = {
            'total_cost': self.total_cost,
        }

        if self.subtotal:
            data['subtotal'] = self.subtotal

        if self.shipping_cost:
            data['shipping_cost'] = self.shipping_cost

        if self.total_tax:
            data['total_tax'] = self.total_tax

        return data


class ReceiptElement(IFBPayload):
    def __init__(self, title, subtitle=None, quantity=None, price=None, currency=None, image_url=None):
        self.title = title
        self.subtitle = subtitle
        self.quantity = quantity
        self.price = price
        self.currency = currency
        self.image_url = image_url

    def get_dict(self):
        data = {
            'title': self.title,
        }

        if self.subtitle:
            data['subtitle'] = self.subtitle

        if self.quantity:
            data['quantity'] = self.quantity

        if self.price:
            data['price'] = self.price

        if self.currency:
            data['currency'] = self.currency

        if self.image_url:
            data['image_url'] = self.image_url

        return data