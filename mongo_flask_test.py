from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

from flask import Flask, request, jsonify, abort
from pymongo import MongoClient
import json
import requests

from bson import ObjectId


# Define
MONGO_HOST = 'localhost' 
MONGO_PORT = 27017
MONGO_DB = 'vickie'

# Mongo connection
client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
db = client[MONGO_DB]

# Flask app
app = Flask(__name__)

def transform(d):
	d['_id'] = str(d['_id'])
	return d

# API route
## Get all people
@app.route('/people', methods=['GET'])
def get_people():
	coll = db['people']
	people = [transform(p) for p in coll.find()]
	return jsonify({'people': people})

## Get a person
@app.route('/people/<person_id>', methods=['GET'])
def get_people_id(person_id):
	coll = db['people']
	try:
		person = coll.find_one({'_id': ObjectId(person_id)})
		return jsonify({'person': transform(person)})
	except:
		abort(404)

## Create a person
@app.route('/people', methods=['POST'])
def create_person():
	coll = db['people']
	body = request.get_json()
	content = {}
	for prop in ['name', 'age']:
		if prop in body:
			content[prop] = body[prop]
	obj_id = coll.insert(content)
	return jsonify({'person_id': str(obj_id)}), 201

## Update a person
@app.route('/people/<person_id>', methods=['PUT'])
def update_people(person_id):
	coll = db['people']
	body = request.get_json()
	content = {}
	for prop in ['name', 'age']:
		if prop in body:
			content[prop] = body[prop]

	r = coll.update_one({'_id': ObjectId(person_id)}, {'$set': content})
	content['_id'] = person_id

	if r.matched_count > 0:
		return jsonify({'people': content})
	else:
		abort(404)

# Remove a person
@app.route('/people/<person_id>', methods=['DELETE'])
def remove_people(person_id):
	coll = db['people']
	s = coll.remove({'_id': ObjectId(person_id)})
	if s['n'] > 0:
		return jsonify({'result': True})
	else:
		abort(404)

@app.errorhandler(404)
def not_found(error):
	return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=True)