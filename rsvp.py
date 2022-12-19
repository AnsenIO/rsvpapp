from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import socket
import os
import json

app = Flask(__name__)

LINK = os.environ.get('LINK', "www.iab.ai")
TEXT1 = os.environ.get('TEXT1', "IABAI")
TEXT2 = os.environ.get('TEXT2', "IT Solutions")
LOGO = os.environ.get('LOGO', "https://www.iab.ai/assets/iabai_logo_small.png")
COMPANY = os.environ.get('COMPANY', "IABAI SaS")

MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
client = MongoClient(MONGODB_HOST, 27017)
db = client.rsvpdata


class RSVP(object):
    """Simple Model class for RSVP"""

    def __init__(self, name, email, _id=None):
        self.name = name
        self.email = email
        self._id = _id

    def dict(self):
        _id = str(self._id)
        return {
            "_id": _id,
            "name": self.name,
            "email": self.email,
            "links": {
                "self": "{}api/rsvps/{}".format(request.url_root, _id)
            }
        }

    def delete(self):
        db.rsvpdata.find_one_and_delete({"_id": self._id})

    @staticmethod
    def find_all():
        return [RSVP(**doc) for doc in db.rsvpdata.find()]

    @staticmethod
    def find_one(ids):
        doc = db.rsvpdata.find_one({"_id": ObjectId(ids)})
        return doc and RSVP(doc['name'], doc['email'], doc['_id'])

    @staticmethod
    def new(name, email):
        doc = {"name": name, "email": email}
        result = db.rsvpdata.insert_one(doc)
        return RSVP(name, email, result.inserted_id)


@app.route('/')
def rsvp():
    _items = db.rsvpdata.find()
    items = [item for item in _items]
    count = len(items)
    hostname = socket.gethostname()
    return render_template('profile.html', counter=count, hostname=hostname,
                           items=items, TEXT1="", TEXT2=TEXT2, LOGO=LOGO,
                           COMPANY=COMPANY)


@app.route('/new', methods=['POST'])
def new():
    item_doc = {'name': request.form['name'], 'email': request.form['email']}
    db.rsvpdata.insert_one(item_doc)
    return redirect(url_for('rsvp'))


@app.route('/api/rsvps', methods=['GET', 'POST'])
def api_rsvps():
    if request.method == 'GET':
        docs = [r.dict() for r in RSVP.find_all()]
        return json.dumps(docs, indent=True)
    else:
        try:
            doc = json.loads(request.data)
        except ValueError:
            return '{"error": "expecting JSON payload"}', 400

        if 'name' not in doc:
            return '{"error": "name field is missing"}', 400
        if 'email' not in doc:
            return '{"error": "email field is missing"}', 400

        r = RSVP.new(name=doc['name'], email=doc['email'])
        return json.dumps(r.dict(), indent=True)


@app.route('/api/rsvps/<ids>', methods=['GET', 'DELETE'])
def api_rsvp(ids):
    rsvped = RSVP.find_one(ids)
    if not rsvped:
        return json.dumps({"error": "not found"}), 404

    if request.method == 'GET':
        return json.dumps(rsvped.dict(), indent=True)
    elif request.method == 'DELETE':
        rsvped.delete()
        return json.dumps({"deleted": "true"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
