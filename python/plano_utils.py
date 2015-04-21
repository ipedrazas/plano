from py2neo import Graph
from py2neo import Node, Relationship
import yaml
from pymongo import MongoClient
import re


ALLOWED_EXTENSIONS = set(['yml', 'yaml'])


graph = Graph("http://neo4j:7474/db/data/")



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def parse_yaml(file):
    nodes = []
    mult_attrs = ['links', 'ports', 'volumes', 'volumes_from']
    attrs = ['command', 'image', 'build']
    compose = yaml.load(file)
    for k, v in compose.iteritems():
        node = {'name': k}
        if v:
            for attr in attrs:
                if v.get(attr):
                    node[attr] = v.get(attr)
            for attr in mult_attrs:
                if v.get(attr):
                    node[attr] = get_compose_list(v, attr)
        nodes.append(node)
    return nodes

def get_compose_list(doc, attr):
    elems = []
    for l in doc.get(attr):
        elems.append(l)
    return elems

def add_nodes(nodes, app, application, logger):
    '''
        To add nodes we have to create the nodes and then
        set the links between nodes. Otherwise, you might
        want to link to a node that it has not been processed yet
    '''
    updated_nodes = []
    for n in nodes:
        updated_nodes.append(get_or_create_component(app, n, application))

    for n in updated_nodes:
        set_links(app, n)

def get_or_create_component(app, component, application_id):
    components = app.data.driver.db['components']
    node = components.find_one({'name': re.compile(component['name'], re.IGNORECASE)})
    if node:
        component = node
    if application_id:
        app.logger.debug(component)
        component['_id'] = components.save(component)
        add_component(component)
    res = create_rels("Component", str(component['_id']), "Application", application_id, "IS_PART")
    return component

def set_links(app, component):
    components = app.data.driver.db['components']
    app.logger.debug(component)
    if component.get('links'):
        for link in component.get('links'):
            link_node = link.split(':')[0]
            linked = components.find_one({'name': re.compile(link_node, re.IGNORECASE)})
            if linked:
                create_rels("Component", str(component['_id']), "Component", str(linked['_id']), "CONNECTS")
    if component.get('volumes_from'):
        for link in component.get('volumes_from'):
            linked = components.find_one({'name': re.compile(link, re.IGNORECASE)})
            app.logger.debug(linked)
            if linked:
                create_rels("Component", str(component['_id']), "Component", str(linked['_id']), "CONNECTS")


def get_or_create_app(app, application):
    applications = app.data.driver.db['applications']
    node = applications.find_one({'name': re.compile(application, re.IGNORECASE)})
    if not node:
        node = {'name': application}
        node['_id'] = applications.save(node)
        add_application(node)
    return node

def create_rels(source_label, source, target_label, target, relationship):
    source_elem = graph.find_one(label=source_label, property_key="fk", property_value=source)
    if source_elem:
        target_elem = graph.find_one(label=target_label, property_key="fk", property_value=target)
        if target_elem:
            if len(list(graph.match(start_node=source_elem, end_node=target_elem, rel_type=relationship))) > 0:
                return False
            rel = Relationship(source_elem, relationship, target_elem)
            graph.create(rel)
            return True
    return False


def add_application(doc):
    add_node_to_neo4j('Application', {'fk': str(doc["_id"]), 'name': doc['name']})


def add_component(doc):
     add_node_to_neo4j('Component', {'fk': str(doc["_id"]), 'name': doc['name']})


def add_node_to_neo4j(label, properties):
    elem = graph.find_one(label=label, property_key='fk', property_value=properties.get('fk'))
    if not elem:
        graph.create(Node(label, name=properties.get('name'), fk=properties.get('fk')))
