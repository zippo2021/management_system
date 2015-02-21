from django.core.mail import EmailMessage
from django.template import loader,Context
import os

def send_regular_email(user,eid)
    try:
        template = loader.get_template(os.path.join(settings.DOWNLOAD_DIR,str(eid)), 'regular_email.txt')   
        price_group = PriceGroup.objects.get(user=user,event=eid)
        message = template.render(Context({'price':price_group.price,'date':'immmannotknow'}))
        mail = EmailMessage('Подтверждение заявки', message, settings.EMAIL_HOST_USER, [user.email])
        complete_mail = attach_files(event_id,mail)
        complete_mail.send() 
        return 'Sent'
    except:
        return 'Error'

def attach_files(eid,mail):
    import magic
    import glob
    from django.conf import settings
    file_list =  glob.glob(os.path.join(os.path.join(settings.EVENT_ATTACHMENTS_DIR,str(event_id)), '*'))
    for fname in file_list:
        item = file(fname)
        mimetype = magic.from_file(fname,mime = True)
        mail.attach(item.name,item.read(),mimetype)
    return mail
