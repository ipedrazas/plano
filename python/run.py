from eve import Eve
from flask import request
from flask.ext.cors import CORS
import plano_utils



def after_insert_application(documents):
    for doc in documents:
       plano_utils.add_application(doc)


def after_insert_component(documents):
    for doc in documents:
        plano_utils.add_component(doc)


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
    if plano_utils.create_rels("Component", json["source"], "Application", json["target"], "IS_PART"):
        return "created", 201
    return "Relationship already exists", 409

@app.route("/rel/connects", methods=['POST'])
def rel_connects():
    json = request.json
    if plano_utils.create_rels("Component", json["source"], "Component", json["target"], "CONNECTS"):
        return "created", 201
    return "Relationship already exists", 409


@app.route('/compose', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        application = request.form.get("application")
        file = request.files['file']
        if application and file and plano_utils.allowed_file(file.filename):
            object_app = plano_utils.get_or_create_app(app, application)
            nodes = plano_utils.parse_yaml(file)
            plano_utils.add_nodes(nodes, app, str(object_app['_id']), app.logger)
            return "Yaml parsed", 201
    return "Trouble", 409


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
