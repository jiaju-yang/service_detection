from . import db


class AdminModel(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    sign = db.Column(db.String(10))
    tip = db.Column(db.Text)
    updated_at = db.Column(db.DateTime)

    def __init__(self, username, password, updated_at, sign=None, tip=None):
        self.username = username
        self.password = password
        self.updated_at = updated_at
        self.sign = sign
        self.tip = tip

    def __repr__(self):
        return '<Admin {username}>'.format(username=self.username)


class HostModel(db.Model):
    __tablename__ = 'hosts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    detail = db.Column(db.Text)
    address = db.Column(db.Text, nullable=False)
    services = db.relationship('ServiceModel', backref='host')

    def __init__(self, name, detail, address, services=None):
        self.name = name
        self.detail = detail
        self.address = address
        self.services = services

    def __repr__(self):
        return '<Host {name}, {address}>'.format(name=self.name,
                                                 address=self.address)


class ServiceModel(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    detail = db.Column(db.Text)
    port = db.Column(db.Integer, nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'), nullable=False)

    def __init__(self, name, detail, port, host_id):
        self.name = name
        self.detail = detail
        self.port = port
        self.host_id = host_id

    def __repr__(self):
        return '<Service {name}, {port}>'.format(name=self.name, port=self.port)
