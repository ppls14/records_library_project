from flask import Flask, jsonify, abort, make_response, request
from models import cds

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/api/v1/cds/", methods=["GET"])
def cds_list_api_v1():
    return jsonify(cds.all())

@app.route("/api/v1/cds/<int:cd_id>", methods=["GET"])
def get_cd(cd_id):
    cd = cds.get(cd_id)
    if not cd:
        abort(404)
    return jsonify({"cds": cd})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.route("/api/v1/cds/", methods=["POST"])
def create_cd():
    if not request.json or not 'title' in request.json:
        abort(400)
    cd = {
        'id': cds.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'artist': request.json['artist'],
        'genre': request.json['genre'],
        'released': request.json['released']
    }
    cds.create(cd)
    return jsonify({'cd': cd}), 201

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

@app.route("/api/v1/cds/<int:cd_id>", methods=['DELETE'])
def delete_todo(cd_id):
    result = cds.delete(cd_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/cds/<int:cd_id>", methods=["PUT"])
def update_cd(cd_id):
    cd = cds.get(cd_id)
    if not cd:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'artist' in data and not isinstance(data.get('artist'), str),
        'genre' in data and not isinstance(data.get('genre'), str),
        'released' in data and not isinstance(data.get('released'), str),
    ]):
        abort(400)
    todo = {
        'title': data.get('title', cd['title']),
        'artist': data.get('artist', cd['artist']),
        'genre': data.get('genre', cd['genre']),
        'released': data.get('release', cd['released'])
    }
    cds.update(cd_id, cd)
    return jsonify({'cd': cd})

if __name__ == "__main__":
    app.run(debug=True)