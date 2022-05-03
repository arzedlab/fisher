import requests
from app import db
from datetime import date
from user_agents import parse
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(10), unique=True, nullable=False)
    url = db.Column(db.String(2048), unique=False, nullable=False)
    endpoint_token = db.Column(db.String(120), unique=True, nullable=False)
    info = db.relationship('Target', backref='info', lazy=True)


today = date.today()
date = today.strftime("%B %d, %Y")

class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(32))

    # Adress By IP 
    ip_address = db.Column(db.String(120))
    country = db.Column(db.String(120))
    countryCode = db.Column(db.String(120))
    region = db.Column(db.String(120))
    regionName = db.Column(db.String(120))
    city = db.Column(db.String(120))
    zip = db.Column(db.String(120))
    geo = db.Column(db.String(120))
    timezone = db.Column(db.String(120))
    isp = db.Column(db.String(120))
    org = db.Column(db.String(120))

    browser = db.Column(db.String(240))
    operating_system = db.Column(db.String(120))
    device = db.Column(db.String(120))

    url_id = db.Column(db.Integer, db.ForeignKey('URL.id'), nullable=False)

    def __init__(self,ip_address, ua_string, url_id):
        self.time = date

        self.ip_address = ip_address
        self.country = ip_address_parser(ip_address)["country"]
        self.countryCode = ip_address_parser(ip_address)["countryCode"]
        self.region = ip_address_parser(ip_address)["region"]
        self.regionName = ip_address_parser(ip_address)["regionName"]
        self.city = ip_address_parser(ip_address)["city"]
        self.zip = ip_address_parser(ip_address)["zip"]
        self.geo = str(ip_address_parser(ip_address)["lat"]) + " " + str(ip_address_parser(ip_address)["lon"])
        self.timezone = ip_address_parser(ip_address)["timezone"]
        self.isp = ip_address_parser(ip_address)["isp"]
        self.org = ip_address_parser(ip_address)["org"]
        self.browser = user_agent_parser(ua_string).browser.family + " " + user_agent_parser(ua_string).browser.version_string
        self.operating_system = user_agent_parser(ua_string).os.family + " " + user_agent_parser(ua_string).os.version_string
        self.device = ua_string.split("(")[1].split(")")[0]
        self.url_id = url_id

def ip_address_parser(ip_address):
    if ip_address == "127.0.0.1":
        ip_address = "1.1.1.1"
    r = requests.get(f'http://ip-api.com/json/{ip_address}')
    return r.json()

def user_agent_parser(ua_string):
    user_agent = parse(ua_string)
    return user_agent

