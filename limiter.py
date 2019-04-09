from flask import Flask, request, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

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

    def __init__(self, name, address, contact_email, contact_no):
        self.name = name
        self.address = address
        self.contact_email = contact_email
        self.contact_no = contact_email


class CompanySchema(marsh_app.Schema):
    class Meta:
        fields = ('name', 'address', 'contact_email', 'contact_no')

# for single company
company_schema = CompanySchema()
# for all companies
company_schema = CompanySchema(many=True)


def comp_exists():
    """
    method to check if company exists for given id
    Note: 'id' param is being used as test. It can be changed as needed like comapny name
    """
    if Company.query.get(request.args['id']):
        return True
    return False


# defining limiter
limiter = Limiter(
    app,
    key_func=comp_exists,
    default_limits=["100/day, 2/minute"] # this is default limit set for app
)

@app.route("/company", methods=["POST"])
# create new company
def create_company():
    """
    Method to create a company and insert into db
    """
    name = request.json['name']
    address = request.json['address']
    contact_email = request.json['contact_email']
    contact_no = request.json['contact_no']
    
    new_company = Company(name, address, contact_email, contact_no)

    # add new company into db
    db.session.add(new_company)
    db.session.commit()

    return jsonify({
        'Company_name': new_company.name,
        'address': new_company.address,
        'email': new_company.contact_email,
        'Contact_number': new_company.contact_no
    })


def company_exists(comp_id):
    """
    method to check if company exists for given id
    """
    if Company.query.get(comp_id):
        return True
    return False

@app.route("/company", methods=["GET"])
def list_companies():
    all_comp = Company.query.all()
    result = company_schema.dump(all_comp)
    return jsonify(result.data)



@app.route("/check_company", methods=["GET"])
def check_company():
    return "success"


# @app.route("/check_company/<id>", methods=["GET"])
# def check_company(id):
#     if company_exists(id):
#         return "company found in database"
#     abort(403)




if __name__ == '__main__':
    app.run(debug=True)