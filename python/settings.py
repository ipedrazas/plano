XML = False

MONGO_HOST = 'mongodb'
MONGO_PORT = 27017
MONGO_DBNAME = 'plano01'

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

# Enable CORS for all domains
X_DOMAINS = "*"
X_HEADERS = "Content-Type, Accept, Authorization, X-Requested-With, " \
    " Access-Control-Request-Headers, Access-Control-Allow-Origin, " \
    " Access-Control-Allow-Credentials, X-HTTP-Method-Override, mozSystem, " \
    " Access-Control-Allow-Methods, If-Match "

UPLOAD_FOLDER = '/app/uploads'

applications = {
    'schema': {
        'name': {
            'type': 'string',
            'unique': True
        }
    }
}

components = {
    'schema': {
        'name': {
            'type': 'string',
            'unique': True
        }
    }
}

runtimes = {
    'schema': {
        'name': {
            'type': 'string',
            'unique': True
        }
    }
}

DOMAIN = {
    'applications': applications,
    'components': components,
    'runtimes': runtimes,
}

