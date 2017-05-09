from flask import Flask, request
from flask_restplus import Resource, Api, fields, marshal
from flask_sqlalchemy import SQLAlchemy
import json
from gtfsdb import Route, Agency

# load the data
# bin/gtfsdb-load --database_url postgresql://localhost/gtfsdb data/gtfs_rail.zip

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/gtfsdb'
db = SQLAlchemy(app)
api = Api(app)

agencies = db.session.query(Agency).all()
metrorail = db.session.query(Agency).first()
# metrorail.session.query(Agency).first()

@api.route('/agencies')
class ListAgencies(Resource):
    def get(self):
        myfields = {'agency_id': fields.String}
        return marshal(agencies,myfields)

# /agency
@api.route('/agencies/<string:agency_id>')
class AgencyName(Resource):
    def get(self,agency_id):
        myagency = db.session.query(Agency).filter_by(agency_id=agency_id).first()
        myfields = {'agency_id': fields.String,'agency_name': fields.String}
        return marshal(myagency,myfields)

# /agencies/<agency_id>/routes/
@api.route('/agencies/<string:agency_id>/routes/')
class AgencyRoutes(Resource):
    def get(self,agency_id):
        myroutes = db.session.query(Route).filter_by(agency_id=agency_id).all()
        myfields = {'route_id': fields.String,'route_short_name': fields.String,'route_long_name': fields.String, }
        return marshal(myroutes,myfields)


# /hello
@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}




if __name__ == '__main__':
    app.run(debug=True)




# @api.route('/<string:todo_id>')
# class TodoSimple(Resource):
#     def get(self, todo_id):
#         return {todo_id: todos[todo_id]}
#
#     def put(self, todo_id):
#         todos[todo_id] = request.form['data']
#         return {todo_id: todos[todo_id]}
