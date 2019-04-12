from flask import Flask, request, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

DEFAULT_LIMIT = "0/day, 0/minute"

# creating flask app
app = Flask(__name__)
# for data serialization/render json response
marsh_app = Marshmallow(app)

# creating db
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.sqlite')
db = SQLAlchemy(app)

# defining comapny model
class Company(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(100), unique=False)
    contact_email = db.Column(db.String(50), unique=True, default="")
    contact_no = db.Column(db.String(30), default="")
    limit = db.Column(db.String(50), default=DEFAULT_LIMIT)

    def __init__(self, name, address, contact_email, contact_no, limit):
        self.name = name
        self.address = address
        self.contact_email = contact_email
        self.contact_no = contact_email
        self.limit = limit


class CompanySchema(marsh_app.Schema):
    class Meta:
        fields = ('name', 'address', 'contact_email', 'contact_no', 'limit')

# for single company
company_schema = CompanySchema()
# for all companies
company_schema = CompanySchema(many=True)


def comp_exists():
    """
    method to check if company exists for given id
    Note: 'id' param is being used as test. It can be changed as needed like comapny name
    """
    return (Company.query.get(request.view_args['id']), 0)


# defining limiter
limiter = Limiter(
    app,
    key_func=comp_exists,
    default_limits=[DEFAULT_LIMIT] # this is default limit set for app
)


# create new company
@app.route("/company", methods=["POST"])
@limiter.limit("100/day, 2/minute", key_func= lambda : True if (request.method == "POST") else abort(403))
def create_company():
    """
    Method to create a company and insert into db
    """
    name = request.json['name']
    address = request.json['address']
    contact_email = request.json['contact_email']
    contact_no = request.json['contact_no']
    limit = request.json['limit']
    
    new_company = Company(name, address, contact_email, contact_no, limit)

    # add new company into db
    db.session.add(new_company)
    db.session.commit()

    return jsonify({
        'Company_name': new_company.name,
        'address': new_company.address,
        'email': new_company.contact_email,
        'Contact_number': new_company.contact_no,
        'limit': new_company.limit
    })


@app.route("/company/<c_id>", methods=["DELETE"])
@limiter.limit("100/day, 50/minute", key_func= lambda : True if (request.method == "DELETE") else abort(403))
def delete_company(c_id):
    try:
        company = Company.query.get(c_id)
        db.session.delete(company)
        db.session.commit()
        return "success"
    except:
        return abort(404)


@app.route("/company", methods=["GET"])
# for listing the companies, here limiter is being modified with new the limit and a new key_func
@limiter.limit("100/day, 5/minute", key_func= lambda : True if (request.method == "GET") else abort(403))
def list_companies():
    all_comp = Company.query.all()
    result = company_schema.dump(all_comp)
    return jsonify(result.data)


def get_company_limit():
    try:
        company = Company.query.get(request.view_args['id'])
        return company.limit
    except:
        abort(403)


@app.route("/check_company/<id>", methods=["GET"])
# to get dynamic limit value, a callable is provided to the decorator
@limiter.limit(limit_value=get_company_limit)
def check_company(id):
    return "success"




if __name__ == '__main__':
    app.run(debug=True)
