XML = False

MONGO_HOST = 'mongodb'
MONGO_PORT = 27017
MONGO_DBNAME = 'plano01'

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

applications = {
    'schema': {
        'name': {
            'type': 'string'
        }
    }
}

components = {
    'schema': {
        'name': {
            'type': 'string'
        }
    }
}

runtimes = {
    'schema': {
        'name': {
            'type': 'string'
        }
    }
}

DOMAIN = {
    'applications': applications,
    'components': components,
    'runtimes': runtimes,
}

