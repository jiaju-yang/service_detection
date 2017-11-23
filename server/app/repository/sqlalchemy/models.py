from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AdminModel(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    sign = db.Column(db.String(10))
    tip = db.Column(db.Text)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<Admin {username}>'.format(username=self.username)


class HostModel(db.Model):
    __tablename__ = 'hosts'

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    detail = db.Column(db.Text)
    address = db.Column(db.Text, nullable=False)
    services = db.relationship('ServiceModel', lazy='joined', backref='host')

    def __repr__(self):
        return '<Host {name}, {address}>'.format(name=self.name,
                                                 address=self.address)


class ServiceModel(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    detail = db.Column(db.Text)
    port = db.Column(db.Integer, nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'), nullable=False)

    def __repr__(self):
        return '<Service {name}, {port}>'.format(name=self.name, port=self.port)
