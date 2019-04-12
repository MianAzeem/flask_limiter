from config import db, marsh_app, DEFAULT_LIMIT


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
