from celery.schedules import crontab
from .worker import celery
from .models import Sponsor, Influencer, AdRequest, Campaign
from jinja2 import Template
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import smtplib

def sendMail(reciever, subject, message, type="html"):
    msg=MIMEMultipart()
    msg["From"] = "team@sc.com"
    msg["To"] = reciever
    msg["Subject"] = subject

    msg.attach(MIMEText(message, type))
    
    m = smtplib.SMTP(host="localhost", port=1025)
    m.login("team@sc.com","")
    m.send_message(msg)
    m.quit()
    return "Mail Sent"


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(30, daily_influencers_reminder.s()) 

    sender.add_periodic_task(30, monthly_report.s())

    sender.add_periodic_task(
        crontab(minute=0, hour=20), 
        daily_influencers_reminder.s(),
        name='Daily reminder'
    )

    sender.add_periodic_task(
        crontab(day_of_month=1, month_of_year='*'),  
        monthly_report.s(),
        name="Monthly Report"
    )


@celery.task()
def daily_influencers_reminder():
    influencers = Influencer.query.all()
    for i in influencers:
        sendMail(i.email, subject="Daily Reminder", message="Heyy! Checkout latest campaigns and ad requests.")

    return "Reminder sent."


@celery.task()
def monthly_report():
    sponsors = Sponsor.query.all()

    for s in sponsors:
        all_campaigns = Campaign.query.filter_by(sponsor_id = s.id).all()

        campaign_details = []
        for campaign in all_campaigns:
            ad_requests = AdRequest.query.filter_by(campaign_id = campaign.id).all()
            ad_details = [
                {
                    'requirements': ad.requirements,
                    'message': ad.message,
                    'payment_amount': ad.payment_amount,
                    'status': ad.status,
                    'influencer': ad.influencer.name
                }
                for ad in ad_requests
            ]
            campaign_info = {
                'name': campaign.name,
                'description': campaign.description,
                'budget': campaign.budget,
                'visibility': campaign.visibility,
                'ads': ad_details
            }
            campaign_details.append(campaign_info)

        with open("public/report.html") as fileTemp:
            template = Template(fileTemp.read())
            html_report = template.render(campaign_details=campaign_details, name=s.company_name)

            sendMail(s.email, subject="Monthly Report", message=html_report, type='html')
    
    return "Monthly reports sent!"

