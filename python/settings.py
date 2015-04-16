XML = False

MONGO_HOST = 'mongodb'
MONGO_PORT = 27017
MONGO_DBNAME = 'plano01'

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

logs = {
    'schema': {
        'user': {
            'type': 'string'
        },
        'source_id': {
            'type': 'string'
        },
        'action': {
            'type': 'string'
        },
        'value': {
            'type': 'string'
        }
    }
}

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
    'logs': logs,
    'applications': applications,
    'components': components,
    'runtimes': runtimes,
}

