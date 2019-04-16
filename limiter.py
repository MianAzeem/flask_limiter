from flask import request, jsonify, abort

from flask_limiter import Limiter
from manage import app, db, Company, DEFAULT_LIMIT
from config import company_schema, cache

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)



def generate_access_token(identity):
    # create an access token with no expiry date
    return create_access_token(identity=identity, expires_delta=False)


def get_company_key():
    """
    key_func: method to return company's identity(uuid string)
    """
    return (get_jwt_identity(), 0)


# defining limiter
limiter = Limiter(
    app,
    key_func=get_company_key,
    default_limits=[DEFAULT_LIMIT] # this is default limit set for app
)

###############################
# Endpoints
###############################

# create new company
@app.route("/company", methods=["POST"])
@limiter.limit("100/day, 10/minute", key_func= lambda : True if (request.method == "POST") else abort(403))
def create_company():
    """
    Method to create a company and insert into db
    """
    name = request.json['name']
    limit = request.json['limit']
    
    new_company = Company(name=name, limit=limit)
    try:
        # add new company into db
        db.session.add(new_company)
        db.session.commit()

        # creating jwt_access_token
        access_token = generate_access_token(new_company.identity)

        return jsonify({
            'Company_name': new_company.name,
            'limit': new_company.limit,
            'access_token': access_token
        })
    except:
        return "something went wrong"


# delete company by id
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


# list all companies
@app.route("/company", methods=["GET"])
# for listing the companies, here limiter is being modified with new the limit and a new key_func
@limiter.limit("100/day, 5/minute", key_func= lambda : True if (request.method == "GET") else abort(403))
def list_companies():
    all_comp = Company.query.all()
    result = company_schema.dump(all_comp)
    return jsonify(result.data)


@cache.memoize(timeout=300) # applying cache on this method for 5 mins
def get_company_limit():
    """
    Method returns company's limit using it's identity
    """
    c_identity = get_jwt_identity()
    try:
        company = Company.query.filter_by(identity=c_identity).first()
        return company.limit
    # if company not found raise forbidden 403
    except:
        abort(403)


@app.route("/get_limit", methods=["GET"])
@jwt_required
@limiter.limit(limit_value=get_company_limit)
def get_company_limit():
    return "success"



if __name__ == '__main__':
    app.run(debug=True)
