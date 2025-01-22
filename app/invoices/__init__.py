import os
from flask import Blueprint, request
from flask_restx import Api

from .controller import api as invoice_ns


invoice_bp = Blueprint("invoice", __name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;apikey&gt;'**, where apikey is the your "
                       "access_token "
    },
}

api = Api(
        invoice_bp,
        # authorizations=authorizations,
        # security='apikey',
        title=f'{os.environ.get("APPNAME")} Invoices Rest API',
        version='1.0',
        description="Invoices routes."
    )

api.add_namespace(invoice_ns)