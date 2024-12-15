from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Sponsor(db.Model):
    __tablename__ = 'sponsors'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200))
    industry = db.Column(db.String(120))

class Influencer(db.Model):
    __tablename__ = 'influencers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200))
    niche = db.Column(db.String(120))
    reach = db.Column(db.String(120))

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Float)
    flagged = db.Column(db.Boolean, default = False)
    visibility = db.Column(db.String(50), default='Private')  # 'public' or 'private'
    sponsor = db.relationship('Sponsor', backref=db.backref('campaigns', cascade='all, delete-orphan', lazy=True))

class AdRequest(db.Model):
    __tablename__ = 'ad_requests'
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id', ondelete='CASCADE'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.id'), nullable=False)
    message = db.Column(db.String(500))
    requirements = db.Column(db.String(500))
    payment_amount = db.Column(db.Float)
    negotiation = db.Column(db.String(500))
    status = db.Column(db.String(50), default='Pending')  # 'Pending', 'Accepted', 'Rejected', 'Negotiated', 'Completed'
    campaign = db.relationship('Campaign', backref=db.backref('ad_requests', cascade='all, delete-orphan', lazy=True))
    influencer = db.relationship('Influencer', backref=db.backref('ad_requests', lazy=True))


class InfluencerRequest(db.Model):
    __tablename__ = 'influencer_requests'
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id', ondelete='CASCADE'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.id'), nullable=False)
    status = db.Column(db.String(50), default='Pending')  # 'Pending', 'Accepted', 'Rejected', 'Completed'
    campaign = db.relationship('Campaign', backref=db.backref('influencer_requests', cascade='all, delete-orphan', lazy=True))
    influencer = db.relationship('Influencer', backref=db.backref('influencer_requests', lazy=True))
