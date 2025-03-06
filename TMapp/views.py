from django.shortcuts import render, redirect ,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .models import *
from .helpers import *
from django.contrib import messages
from .models import User, UserProfile
from django.contrib.auth.decorators import login_required
import uuid


def login_user(request):
    try:
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")

            user_object = User.objects.filter(email=email).first()
            if not user_object:
                messages.error(request, "User not found.")
                return render(request, "accounts/auth-login.html")

            user_profile = UserProfile.objects.filter(user=user_object).first()
            if not user_profile or not user_profile.is_verified:
                messages.error(request, "Account is not verified.")
                return render(request, "accounts/auth-login.html")

            user_ = authenticate(request, email=email, password=password)
            if user_ is None:
                messages.error(request, "Wrong password.")
                return render(request, "accounts/auth-login.html")

            login(request, user_)
            return redirect("home")

    except Exception as e:
        print(e)
        messages.error(request, "An error occurred. Please try again.")

    return render(request, "accounts/auth-login.html")


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect("login_user")


def Register(request):
    try:
        if request.method == "POST":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            password = request.POST.get("password")

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already taken.")
                return render(request, "accounts/auth-register.html")

            # Create user
            user = User.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )

            # Generate token for verification
            token = str(uuid.uuid4())
            UserProfile.objects.create(user=user, auth_token=token)

            # Send verification email
            send_Register_email(email, first_name, token)

            messages.success(request, "User registered successfully! Please verify your email.")
            return redirect("login_user")

    except Exception as e:
        print(e)
        messages.error(request, "Registration failed. Try again.")

    return render(request, "accounts/auth-register.html")


def verify(request, token):
    try:
        user_profile = UserProfile.objects.filter(auth_token=token).first()
        if user_profile:
            if user_profile.is_verified:
                messages.info(request, "Your account is already verified.")
            else:
                user_profile.is_verified = True
                user_profile.save()
                messages.success(request, "Your account has been verified. You can now log in.")
            return redirect("login_user")

    except Exception as e:
        print(e)
        messages.error(request, "Invalid verification link.")

    return redirect("login_user")


def reset_password(request):
    try:
        if request.method == "POST":
            email = request.POST.get("email")
            user = User.objects.filter(email=email).first()

            if not user:
                messages.error(request, "No user found with this email.")
                return render(request, "accounts/auth-forgot-password.html")

            # Generate reset token
            token = str(uuid.uuid4())
            user_profile = UserProfile.objects.get(user=user)
            user_profile.forget_password_token = token
            user_profile.save()

            send_forget_password_email(user.email, token)
            messages.success(request, "An email has been sent for password reset.")
            return redirect("login_user")

    except Exception as e:
        print(e)
        messages.error(request, "An error occurred. Please try again.")

    return render(request, "accounts/auth-forgot-password.html")


def change_password(request, token):
    try:
        user_profile = UserProfile.objects.filter(forget_password_token=token).first()
        if not user_profile:
            messages.error(request, "Invalid token.")
            return redirect("login_user")

        if request.method == "POST":
            new_password = request.POST.get("password")
            confirm_password = request.POST.get("confirm-password")

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, "accounts/auth-reset-password.html", {"token": token})

            user = user_profile.user
            user.set_password(new_password)
            user.save()

            # Clear token after password reset
            user_profile.forget_password_token = None
            user_profile.save()

            messages.success(request, "Password changed successfully. You can now log in.")
            return redirect("login_user")

    except Exception as e:
        print(e)
        messages.error(request, "An error occurred while changing the password.")

    return render(request, "accounts/auth-reset-password.html", {"token": token})


# @login_required(login_url = 'login_user')
def home(request):
    if not request.user.is_authenticated:
        messages.success(request, "Login is required to access this page.")
        return redirect("login_user")

    return render(request, "dashboard.html")

# =========Users============= 
def Users(request):
    
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user_name = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        img = request.FILES.get('image')  
        phoneno = request.POST.get("phoneno")  
        password = request.POST.get("password")

        if user_id is None:
        
            user_obj = User.objects.filter(email=email)
            if user_obj.exists():
                messages.error(request, "User with this email already exists")
            else:
                create_user = User(
                    first_name=first_name,
                    username=user_name,
                    last_name=last_name,
                    email=email,
                    phone_no=phoneno,
                    image=img,
                )
                create_user.set_password(password)
    
                create_user.save()

                token = str(uuid.uuid4())

                user_profile = UserProfile.objects.create(user=create_user)

                user_profile.auth_token = token

                # save the profile
                user_profile.save()

                # send_Added_email(email, username, token)

                messages.success(request, 'User Added Successfully')
        else:
         
            user = get_object_or_404(User, pk=user_id)
            user.first_name = first_name
            user.last_name = last_name
            user.user_name = user_name
            user.email = email
            user.phone_no = phoneno

            if img:
                user.image = img  

            user.save()
            messages.success(request, 'User Updated Successfully')

        return redirect('users')


    list_user = User.objects.all()
    list_user_status = UserProfile.objects.all()
    zipped_data = zip(list_user, list_user_status)
    context = {'zipped_data': zipped_data}
    return render(request, "users/users.html", context)


def get_user_data(request, user_id):
    try:
        user = get_object_or_404(User, pk=user_id)
        user_data = {
            'aj_id': user_id,
            'first_name': user.first_name,
            'username': user.user_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_no': user.phone_no,
            'password':user.password,
            'image_url': user.image.url if user.image else None,
        }
        print(user_data)
        return JsonResponse(user_data)
    
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
def delete_user(request):
    try:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, pk=user_id)
            user.delete()
            return JsonResponse({'success': True, 'message': 'User Deleted Successfully'})
    except Exception as e:

        return JsonResponse({'success': False, 'message': 'An error occurred while deleting the User'})
    
def verify_user(request):
    try:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            user = get_object_or_404(UserProfile, user_id=user_id)
            user.is_verified = True
            user.save()
            user_info = get_object_or_404(User, pk=user_id)
            # mail data to be sent 
            u_name = user_info.first_name
            f_name = user_info.last_name
            email_ = user_info.email
            print(email_)
            send_Account_Verification_email(email_, u_name, f_name)
            print('mail sent')
            return JsonResponse({'success': True, 'message': 'User Account Verified Successfully'})
    except Exception as e:

        return JsonResponse({'success': False, 'message': 'An error occurred while Verifing the User Account'})
    
def profile_setting(request):

    try:
        if request.method == "POST":
            user_id = request.POST.get('user_id')
            username = request.POST.get("username")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            img = request.FILES.get('image')  
            phoneno = request.POST.get("phoneno")  
            update_cmd = request.POST.get("update_profile")
            passrest_cmd = request.POST.get("pass_reset")
            new_password = request.POST.get("password")
            confirm_password = request.POST.get("confirm-password")

            if(update_cmd == "update_profile"):
                user = get_object_or_404(User, pk=user_id)
                user.first_name = first_name
                user.user_name = username
                user.last_name = last_name
                user.email = email
                user.phone_no = phoneno

                if img:
                    user.image = img  

                user.save()
                messages.success(request, 'User info Updated Successfully')


                return redirect('profile')
            
            if(passrest_cmd == "pass_reset"):
                user = get_object_or_404(User, pk=user_id)
                if new_password != confirm_password:
                    messages.error(request, "Passwords do not match.")
                    return redirect('profile') 
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully. Please Login Again..!")
                return redirect("login_user")        
 
        profile = User.objects.all()
        context = {
        'users':profile,
        }
        return render(request, "profile/profile.html", context)
    except Exception as e:
       print(e)
       return render(request, "profile/profile.html", e)