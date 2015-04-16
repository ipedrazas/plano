from eve import Eve
from py2neo import Graph
from py2neo import Node, Relationship
from flask import request

graph = Graph("http://neo4j:7474/db/data/")



def after_insert_application(documents):
    for doc in documents:
        add_node(Node("Application", name=doc["name"], fk=str(doc["_id"])))


def after_insert_component(documents):
    for doc in documents:
        add_node(Node("Component", name=doc["name"], fk=str(doc["_id"])))


def add_node(node):
    graph.create(node)

app = Eve()
app.on_inserted_applications += after_insert_application
app.on_inserted_components += after_insert_component

@app.route("/version")
def version():
    return 'plano.io v0.0.1'


@app.route("/ispart", methods=['POST'])
def component_is_part_application(component=None, application=None):

    json = request.json
    component = graph.find_one(label="Component", property_key="fk", property_value=json["component"])
    application = graph.find_one(label="Application", property_key="fk", property_value=json["application"])
    print component
    print application

    if component:
        if application:
            rel = Relationship(component, "IS_PART", application)
            graph.create(rel)
            return "Relationship created"
        else:
            return 'Relationship not found'

    else:
        return "Component not found"

    return "Impossible is nothing"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


