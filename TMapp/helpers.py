from django.core.mail import send_mail

from django.conf import settings


def send_forget_password_email(email,token):
    subject = 'Your Forget Password Link'
    message = f'Hi, Click on the following link to rest your password http://127.0.0.1:8000/change-password/{token}'
    mailfrom = settings.EMAIL_HOST_USER
    receipt_mail = [email]
    send_mail(subject,message,mailfrom,receipt_mail)
    return True


def send_Register_email(email, user_name,token):
    
    subject = 'Thanks For Registering With Us Verify your Account'
    message = f'Hi, {user_name} We are Very happy To see you here at our Task Managemant System. Click the link to verify your account: http://127.0.0.1:8000/verify/{token}'
    mailfrom = settings.EMAIL_HOST_USER
    receipt_mail = [email]
    send_mail(subject, message, mailfrom, receipt_mail)
    return True

def send_Account_Verification_email(email, u_name, f_name):
    subject = 'Verification of your Account'
    message = f'Hi, {f_name} your account was Verified By the admin you can now use your account. For more info, Contact us.'
    mailfrom = settings.EMAIL_HOST_USER
    receipt_mail = email

    try:
        send_mail(subject, message, mailfrom, [receipt_mail])
        return True
    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")
        return False