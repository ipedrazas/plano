from eve import Eve
from py2neo import Graph
from py2neo import Node, Relationship
from flask import request
from flask.ext.cors import CORS

graph = Graph("http://neo4j:7474/db/data/")



def after_insert_application(documents):
    for doc in documents:
        elem = graph.find_one(label="Application", property_key="fk", property_value=str(doc["_id"]))
        if not elem:
            app.logger.info("Adding Application node to neo4j")
            add_node(Node("Application", name=doc["name"], fk=str(doc["_id"])))


def after_insert_component(documents):
    for doc in documents:
        elem = graph.find_one(label="Component", property_key="fk", property_value=str(doc["_id"]))
        if not elem:
            app.logger.info("Adding Component node to neo4j")
            add_node(Node("Component", name=doc["name"], fk=str(doc["_id"])))


def add_node(node):
    graph.create(node)

app = Eve()
cors = CORS(app)
app.on_inserted_applications += after_insert_application
app.on_inserted_components += after_insert_component

@app.route("/version")
def version():
    return 'plano.io v0.0.1'

@app.route("/rel/ispart", methods=['POST'])
def rel_is_part():
    json = request.json
    if create_rels("Component", json["source"], "Application", json["target"], "IS_PART"):
        return "created", 201
    return "Relationship already exists", 409

@app.route("/rel/connects", methods=['POST'])
def rel_connects():
    json = request.json
    if create_rels("Component", json["source"], "Component", json["target"], "CONNECTS"):
        return "created", 201
    return "Relationship already exists", 409


def create_rels(source_label, source, target_label, target, relationship):

    source_elem = graph.find_one(label=source_label, property_key="fk", property_value=source)
    if source_elem:
        target_elem = graph.find_one(label=target_label, property_key="fk", property_value=target)
        if target_elem:
            if len(list(graph.match(start_node=source_elem, end_node=target_elem, rel_type=relationship))) > 0:
                app.logger.debug("Relationship already exists")
                return False
            rel = Relationship(source_elem, relationship, target_elem)
            graph.create(rel)
            return True
    return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


