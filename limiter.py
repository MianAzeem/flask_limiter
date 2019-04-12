from flask import request, jsonify, abort
from config import app, db, DEFAULT_LIMIT, cache
from models import Company, company_schema
from flask_limiter import Limiter



def get_company_key():
    """
    method to return company id as key
    Note: 'id' param is being used as test. It can be changed as needed like comapny name
    """
    return (Company.query.get(request.view_args['id']), 0)

@cache.memoize(timeout=300) # applying cache on this method for 5 mins
def get_company_limit():
    try:
        company = Company.query.get(request.view_args['id'])
        return company.limit
    # if company not found raise forbidden 403
    except:
        abort(403)


# defining limiter
limiter = Limiter(
    app,
    key_func=get_company_key,
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
@cache.memoize(timeout=600)  # cache for 10 mins on route
# for listing the companies, here limiter is being modified with new the limit and a new key_func
@limiter.limit("100/day, 5/minute", key_func= lambda : True if (request.method == "GET") else abort(403))
def list_companies():
    all_comp = Company.query.all()
    result = company_schema.dump(all_comp)
    return jsonify(result.data)



def company_limit_str():
    return get_company_limit()


@app.route("/check_company/<id>", methods=["GET"])
@limiter.limit(limit_value=company_limit_str) # to get dynamic limit value, a callable is provided to the decorator
def check_company(id):
    return "success"




if __name__ == '__main__':
    app.run(debug=True)
