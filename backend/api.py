from flask import request, jsonify, current_app as app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_caching import Cache
from datetime import datetime
from .models import db, Sponsor, Influencer, Campaign, AdRequest

cache = Cache(app)

# Admin Login API
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    password = data.get('password')

    if password == 'admin2024':
        access_token = create_access_token(identity={"id": 0, "role": "admin"})
        return jsonify({"msg": "Login successful", 'token': access_token}), 200
    return jsonify({"msg": "Invalid credentials"}), 400


# Admin Dashboard API
@app.route('/api/admin/dashboard', methods=['GET'])
@jwt_required()
@cache.memoize(180)
def admin_dashboard():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"msg": "Permission denied"}), 403

    campaigns = Campaign.query.filter_by().all()
    total_sponsors = Sponsor.query.count()
    total_influencers = Influencer.query.count()
    total_ads = AdRequest.query.count()
    campaigns = Campaign.query.all()
    campaign_list = [{"id": c.id, "name": c.name, "description": c.description, 'budget': c.budget, 'visibility': c.visibility, 'flagged': c.flagged} for c in campaigns]
    return {'campaigns': campaign_list, 'total_sponsors': total_sponsors, 'total_influencers': total_influencers, 'total_ads': total_ads}, 200

# Admin flag API
@app.route('/api/campaign/<int:id>/flag', methods=['POST'])
@jwt_required()
def campaign_flag(id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"msg": "Permission denied"}), 403
    
    campaign = Campaign.query.get(id)
    if not campaign:
        return jsonify({"msg": "Campaign not found."}), 404

    flag = campaign.flagged
    campaign.flagged = not flag
    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Campaign status updated"}), 200

# Sponsor Registration API
@app.route('/api/sponsor/register', methods=['POST'])
def sponsor_register():
    data = request.json
    company_name = data.get('company_name')
    email = data.get('email')
    industry = data.get('industry')
    password = data.get('password')

    s = Sponsor.query.filter_by(email=email).first()
    if s:
        return jsonify({"msg": "Company already exists!"}), 400

    new_s = Sponsor(company_name=company_name, password=password, industry=industry, email=email)
    db.session.add(new_s)
    db.session.commit()
    cache.clear()
    return jsonify(msg="Registered successfully!"), 201

# Sponsor Login API
@app.route('/api/sponsor/login', methods=['POST'])
def sponsor_login():
    data = request.json
    company_name = data.get('company_name')
    password = data.get('password')

    s = Sponsor.query.filter_by(company_name=company_name).first()
    if s and s.password == password:
        access_token = create_access_token(identity={"id": s.id, "role": "sponsor"})
        return jsonify({"msg": "Login successful", 'token': access_token}), 200
    return jsonify({"msg": "Invalid credentials"}), 401

# Sponsor Dashboard API
@app.route('/api/sponsor/dashboard', methods=['GET'])
@jwt_required()
@cache.memoize(180)
def sponsor_dashboard():
    current_user = get_jwt_identity()
    if current_user['role'] != 'sponsor':
        return jsonify({"msg": "Permission denied"}), 403

    campaigns = Campaign.query.filter_by(sponsor_id=current_user['id']).all()
    campaign_list = [{"id": c.id, "name": c.name, "description": c.description, 'budget': c.budget, 'visibility': c.visibility, 'flagged': c.flagged} for c in campaigns]
    return jsonify(campaign_list), 200

# Sponsor Campaign detail API
@app.route('/api/sponsor/campaign/<int:id>', methods=['GET'])
@jwt_required()
@cache.memoize(180)
def sponsor_campaign(id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'sponsor':
        return jsonify({"msg": "Permission denied"}), 403

    c = Campaign.query.filter_by(sponsor_id=current_user['id'], id = id).first()
    if not c:
        return jsonify({"msg": "Campaign not found"}), 404
    requests = AdRequest.query.filter_by(campaign_id = id).all()
    campaign_dict = {"id": c.id, "name": c.name, "description": c.description, 'budget': c.budget, 'visibility': c.visibility}
    ad_list = [{"id": r.id, "requirements": r.requirements, "payment_amount": r.payment_amount, 'status': r.status, 
                'influencer': r.influencer.name, 'negotiation': r.negotiation, 'message': r.message} for r in requests]
    return {'campaign': campaign_dict, 'requests': ad_list}, 200

    
# Sponsor request influencers API
@app.route('/api/influencers', methods=['GET'])
@jwt_required()
@cache.memoize(180)
def influencer_details():
    current_user = get_jwt_identity()
    if current_user['role'] != 'sponsor':
        return jsonify({"msg": "Permission denied"}), 403

    influencers = Influencer.query.all()
    influencer_list = [{"id": i.id, "name": i.name, "niche": i.niche, 'reach': i.reach} for i in influencers]
    return jsonify(influencer_list), 200

# Campaign details GET API
@app.route('/api/campaign/<int:id>')
@jwt_required()
@cache.memoize(180)
def campaign(id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'sponsor':
        return jsonify({"msg": "Permission denied"}), 403

    c = Campaign.query.get(id)
    if not c or c.sponsor_id != current_user['id']:
        return jsonify({"msg": "Campaign not found or unauthorized access"}), 404

    return jsonify({"id": c.id, "name": c.name, "description": c.description, 
                    'budget': c.budget, 'visibility': c.visibility,
                    'start_date': c.start_date, 'end_date': c.end_date, 'flagged': c.flagged}), 200

# Campaign Create API
@app.route('/api/campaign/create', methods=['POST'])
@jwt_required()
def campaign_create():
    current_user = get_jwt_identity()
    if current_user['role'] != 'sponsor':
        return jsonify({"msg": "Permission denied"}), 403

    data = request.json
    name = data.get('name')
    description = data.get('description')
    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
    end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
    budget = data.get('budget')
    visibility = data.get('visibility')

    new_c = Campaign(
        sponsor_id=current_user['id'],
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        visibility=visibility
    )

    db.session.add(new_c)
    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Campaign created successfully"}), 201

# Campaign Update API
@app.route('/api/campaign/update/<int:id>', methods=['PUT'])
@jwt_required()
def campaign_update(id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'sponsor':
        return jsonify({"msg": "Permission denied"}), 403

    campaign = Campaign.query.get(id)
    if not campaign or campaign.sponsor_id != current_user['id']:
        return jsonify({"msg": "Campaign not found or unauthorized access"}), 404

    data = request.json
    campaign.name = data.get('name')
    campaign.description = data.get('description')
    campaign.start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
    campaign.end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
    campaign.budget = data.get('budget')

    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Campaign updated successfully"}), 200

# Campaign Delete API
@app.route('/api/campaign/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def campaign_delete(id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'sponsor':
        return jsonify({"msg": "Permission denied"}), 403

    campaign = Campaign.query.get(id)
    if not campaign or campaign.sponsor_id != current_user['id']:
        return jsonify({"msg": "Campaign not found or unauthorized access"}), 404

    db.session.delete(campaign)
    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Campaign deleted successfully"}), 200

# Sponsor Ad detail API
@app.route('/api/sponsor/ad/<int:id>', methods=['GET'])
@jwt_required()
@cache.memoize(180)
def campaign_ad(id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'sponsor':
        return jsonify({"msg": "Permission denied"}), 403

    r = AdRequest.query.filter_by(id = id).first()
    if not r:
        return jsonify({"msg": "Ad Request not found"}), 404
    
    ad = {"id": r.id, "requirements": r.requirements, "payment_amount": r.payment_amount, 'status': r.status, 
                'influencer': r.influencer.name, 'negotiation': r.negotiation, 'message': r.message, 'campaign': r.campaign.name}
    return {'ad': ad}, 200

# Create Ad Request API
@app.route('/api/ad/create/<int:id>', methods=['POST'])
@jwt_required()
def ad_create(id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'sponsor':
        return jsonify({"msg": "Permission denied"}), 403

    data = request.json
    c = Campaign.query.get(id)
    if not c:
        jsonify({"msg": "Campaign not found"}), 404
        
    influencer_id = data['influencer_id']
    message = data['message']
    requirements = data['requirements']
    payment_amount = data['payment_amount']

    new_r = AdRequest(campaign_id = id, influencer_id = influencer_id, message = message,
                    requirements = requirements, payment_amount = payment_amount)
    
    db.session.add(new_r)
    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Request sent successfully"}), 201

# Update Ad Request by sponsor API
@app.route('/api/sponsor/ad/<int:id>', methods=['PUT'])
@jwt_required()
def ad_update(id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'sponsor':
        return jsonify({"msg": "Permission denied"}), 403

    data = request.json
    ad = AdRequest.query.get(id)
    if not ad:
        jsonify({"msg": "Ad not found"}), 404
        
    message = data['message']
    requirements = data['requirements']
    payment_amount = data['payment_amount']

    ad.message = message
    ad.requirements = requirements
    ad.payment_amount = payment_amount
    
    db.session.commit()  
    cache.clear()  
    return jsonify({"msg": "Ad updated successfully"}), 200

# Sponsor Delete Ad API
@app.route('/api/sponsor/ad/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_ad(id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'sponsor':
        return jsonify({"msg": "Permission denied"}), 403

    r = AdRequest.query.filter_by(id = id).first()
    if not r:
        return jsonify({"msg": "Ad Request not found"}), 404

    db.session.delete(r)
    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Ad deleted successfully"}), 200

# Influencer Registration API
@app.route('/api/influencer/register', methods=['POST'])
def influencer_register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    niche = data.get('niche')
    reach = data.get('reach')

    i = Influencer.query.filter_by(email=email).first()
    if i:
        return jsonify({"msg": "Email already exists!"}), 400

    new_i = Influencer(name=name, email=email, password=password, niche=niche, reach=reach)
    db.session.add(new_i)
    db.session.commit()
    cache.clear()
    access_token = create_access_token(identity={"id": new_i.id, "role": "influencer"})
    return jsonify(access_token=access_token, msg="Registered successfully"), 201

# Influencer Login API
@app.route('/api/influencer/login', methods=['POST'])
def influencer_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    i = Influencer.query.filter_by(email=email).first()
    if i and i.password == password:
        access_token = create_access_token(identity={"id": i.id, "role": "influencer"})
        return jsonify({"msg": "Login successful", 'token': access_token}), 200
    return jsonify({"msg": "Invalid credentials"}), 401

# Influencer Profile API
@app.route('/api/influencer/profile', methods = ['GET','POST'])
@jwt_required()
def influencer_profile():
    current_user = get_jwt_identity()
    if current_user['role'] != 'influencer':
        return jsonify({"msg": "Permission denied"}), 403

    i = Influencer.query.get(current_user['id'])
    if not i:
        return jsonify({"msg": "Profile not found"}), 404
     
    if request.method == 'POST':
        data = request.json
        name = data['name']
        niche = data['niche']
        reach = data['reach']
        
        i.name = name
        i.niche = niche
        i.reach = reach
        db.session.commit()
        cache.clear()
        return jsonify({"msg": "Profile updated"}), 200
    elif request.method == 'GET':
        return jsonify({'email': i.email, 'name': i.name, 'niche': i.niche, 'reach': i.reach}), 200
    
# Influencer Dashboard API
@app.route('/api/influencer/dashboard', methods=['GET'])
@jwt_required()
@cache.memoize(180)
def influencer_dashboard():
    current_user = get_jwt_identity()
    if current_user['role'] != 'influencer':
        return jsonify({"msg": "Permission denied"}), 403

    requests = AdRequest.query.filter_by(influencer_id=current_user['id']).all()
    request_list = [{"id": r.id, "campaign_id": r.campaign_id, "status": r.status, "payment_amount": r.payment_amount,
                     "message": r.message, "negotiation": r.negotiation, "requirements": r.requirements, 'flagged': r.campaign.flagged,
                     "campaign_description": r.campaign.description, "campaign_name": r.campaign.name} for r in requests]

    campaigns = Campaign.query.filter_by(visibility='Public').all()
    campaign_list = [{"id": c.id, "name": c.name, "description": c.description, 
                      'budget': c.budget, 'visibility': c.visibility, 
                      'industry': c.sponsor.industry, 'flagged': c.flagged} for c in campaigns]
    
    return jsonify(requests=request_list, campaigns=campaign_list), 200

# Ad Request Creation (Influencer Requests to Join Campaign)
@app.route('/api/adrequest/create/<int:id>', methods=['POST'])
@jwt_required()
def adrequest_create(id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'influencer':
        return jsonify({"msg": "Permission denied"}), 403

    # Check if the campaign exists and is public
    campaign = Campaign.query.get(id)
    if not campaign or campaign.visibility != 'Public':
        return jsonify({"msg": "Campaign not found or not public"}), 404

    existing_request = AdRequest.query.filter_by(influencer_id=current_user['id'], campaign_id=id).first()
    if existing_request:
        return jsonify({"msg": "Request already exists"}), 400

    new_request = AdRequest(influencer_id=current_user['id'], campaign_id=id, status='Self Requested', payment_amount = 0,
                            message = "This is a public campaign.",requirements = "Everything required for the campaign.")
    db.session.add(new_request)
    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Request sent successfully"}), 201

#Handle Campaign Requests API
@app.route('/api/campaign/request/<int:request_id>', methods=['PUT', 'PATCH', 'DELETE'])
@jwt_required()
def campaign_request_handler(request_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'sponsor':
        return jsonify({"msg": "Permission denied"}), 403

    ad_request = AdRequest.query.get(request_id)
    if not ad_request:
        return jsonify({"msg": "Request not found"}), 404

    if request.method == 'PATCH':
        ad_request.status = 'Accepted(Self)'
        db.session.commit()
        cache.clear()
        return jsonify({"msg": "Request accepted"}), 200
    
    if request.method == 'PUT':
        ad_request.status = 'Rejected(Self)'
        db.session.commit()
        cache.clear()
        return jsonify({"msg": "Request rejected"}), 200
    
    if request.method == 'DELETE':
        db.session.delete(ad_request)
        db.session.commit()
        cache.clear()
        return jsonify({"msg": "Request deleted"}), 200

# Accept Ad Request API
@app.route('/api/adrequest/accept/<int:request_id>', methods=['PUT'])
@jwt_required()
def adrequest_accept(request_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'influencer':
        return jsonify({"msg": "Permission denied"}), 403

    ad_request = AdRequest.query.get(request_id)
    if not ad_request:
        return jsonify({"msg": "Request not found"}), 404

    ad_request.status = 'Accepted'
    db.session.commit()
    cache.clear()
    
    return jsonify({"msg": "Request accepted"}), 200

# Reject Ad Request API
@app.route('/api/adrequest/reject/<int:request_id>', methods=['PUT'])
@jwt_required()
def adrequest_reject(request_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'influencer':
        return jsonify({"msg": "Permission denied"}), 403

    ad_request = AdRequest.query.get(request_id)
    if not ad_request:
        return jsonify({"msg": "Request not found"}), 404

    ad_request.status = 'Rejected'
    db.session.commit()
    cache.clear()
    
    return jsonify({"msg": "Request rejected"}), 200

# Complete Ad Request API
@app.route('/api/adrequest/complete/<int:request_id>', methods=['PUT'])
@jwt_required()
def adrequest_complete(request_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'influencer':
        return jsonify({"msg": "Permission denied"}), 403

    ad_request = AdRequest.query.get(request_id)
    if not ad_request:
        return jsonify({"msg": "Request not found"}), 404

    ad_request.status = 'Completed'
    db.session.commit()
    cache.clear()
    
    return jsonify({"msg": "Request completed"}), 200

# Negotiate Ad Request API
@app.route('/api/adrequest/negotiate/<int:request_id>', methods=['POST'])
@jwt_required()
def adrequest_negotiate(request_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'influencer':
        return jsonify({"msg": "Permission denied"}), 403

    ad_request = AdRequest.query.get(request_id)
    if not ad_request or ad_request.influencer_id != current_user['id']:
        return jsonify({"msg": "Request not found or unauthorized access"}), 404

    data = request.json
    ad_request.negotiation = data.get('message', ad_request.message)
    ad_request.status = 'Pending'  

    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Request updated successfully"}), 200
 