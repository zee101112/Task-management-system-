from django.core.mail import send_mail
from django.conf import settings

def send_forget_password_email(request, email, token):
    subject = 'Your Password Reset Link'
    reset_url = request.build_absolute_uri(f'/change-password/{token}')
    message = f'Hi, Click on the following link to reset your password: {reset_url}'
    
    mail_from = settings.EMAIL_HOST_USER
    recipient_mail = [email]
    
    send_mail(subject, message, mail_from, recipient_mail)
    return True


def send_register_email(request, email, user_name, token):
    subject = 'Thanks for Registering - Verify Your Account'
    verify_url = request.build_absolute_uri(f'/verify/{token}')
    message = f'Hi {user_name},\n\nWe are very happy to have you on our Task Management System.\nClick the link to verify your account: {verify_url}'
    
    mail_from = settings.EMAIL_HOST_USER
    recipient_mail = [email]
    
    send_mail(subject, message, mail_from, recipient_mail)
    return True


def send_account_verification_email(email, u_name, f_name):
    subject = 'Your Account Has Been Verified'
    message = f'Hi {f_name},\n\nYour account has been verified by the admin. You can now log in and use your account. For more info, feel free to contact us.'
    
    mail_from = settings.EMAIL_HOST_USER
    recipient_mail = [email]

    try:
        send_mail(subject, message, mail_from, [recipient_mail])
        return True
    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")
        return False