#!flask/bin/python
# derived from https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
from flask import Flask, jsonify, abort, make_response
from flask import request

app = Flask(__name__)

answerqs = [
    {
        'userid': 0,
        'username': u'admin',
    }
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/answerqs', methods=['GET'])
def get_answerqs():
    return jsonify({'answerqs': answerqs})

@app.route('/answerqs/<int:answerq_userid>', methods=['GET'])
def get_answerq(answerq_userid):
    answerq = [answerq for answerq in answerqs if answerq['userid'] == answerq_userid]
    if len(answerq) == 0:
        abort(404)
    return jsonify({'answerq': answerq[0]})

@app.route('/answerqs', methods=['POST'])
def create_answerq():
    if not request.json or not 'username' in request.json:
        abort(400)
    answerq = {
        'userid': answerqs[-1]['userid'] + 1,
        'username': request.json['username'],
    }
    answerqs.append(answerq)
    return jsonify({'answerq': answerq}), 201

@app.route('/answerqs/<int:answerq_userid>', methods=['DELETE'])
def delete_answerq(answerq_userid):
    answerq = [answerq for answerq in answerqs if answerq['userid'] == answerq_userid]
    if len(answerq) == 0:
        abort(404)
    answerqs.remove(answerq[0])
    return jsonify({'result': True})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)