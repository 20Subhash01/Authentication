# Import necessary modules/classes
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.conf import settings
from . tokens import generate_token

# Define view functions for different URLs

# View function for the home page
def home(request):
    return render(request, "myapp/index.html")

# View function for user signup
def signup(request):
    if request.method == 'POST':
        # Retrieve form data
        uname = request.POST['uname']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Verify form data meets criteria
        if not uname.isalnum() or User.objects.filter(username=uname) or User.objects.filter(email=email) or pass1 != pass2:
            # Set error messages for invalid data
            if not uname.isalnum():
                messages.error(request, "Username must be alphanumeric i.e. Combination of alphabets and numbers")
            if User.objects.filter(username=uname):
                messages.error(request, "Username already exists please choose another username")
            if User.objects.filter(email=email):
                messages.error(request, "This Email already exists please choose another Email or signin using username and password")
            if pass1 != pass2:
                messages.error(request, "Password and Confirm Password did not match")
            return redirect('signup')

        # If form data is valid, create New user using the provided data
        else:
            myuser = User.objects.create_user(uname, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname

            # set the activation status of the user as inactive 
            myuser.is_active = False
            # save the user
            myuser.save()
            # show message that user has successfully registered
            messages.success(request, "You are successfully registered. We have sent you a mail. Please check and activate your account.")
            
            # for sennding normal welcome email

            # subject = 'Welcome to my website.'
            # message = 'Hello ' +  myuser.first_name + ' !! \n Welcome to my website \n Thankyou for registering \n We have sent a confirmation email with confirmation link \n Please verify and activate your account for signin \n \n Thank You!! '
            # email_from = settings.EMAIL_HOST_USER
            # to_list = [myuser.email]
            # send_mail(subject,message,email_from,to_list ) 


            # Sending email for account activation using the file confirmation_mail.html
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account Now!'
            message1 = render_to_string(
                'confirmation_mail.html',
                {
                    'name': myuser.first_name,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                    'token': generate_token.make_token(myuser),
                }
            )
            email = EmailMessage(
                email_subject,
                message1,
                settings.EMAIL_HOST_USER,
                [myuser.email],
            )
            email.fail_silently = True
            email.content_subtype = 'html'
            email.send()
            return redirect('signin')
    return render(request, "myapp/signup.html")

# View function for user signin
def signin(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pass1 = request.POST['pass1']
        # authenticate user
        user = authenticate(username=uname, password=pass1)
        # check if the user is authenticated, log them in and render the home page
        if user is not None:
            login(request, user)
            fname = user.first_name
            messages.success(request, "You are successfully Signed In")
            return render(request, "myapp/index.html", {'fname': fname})
        
        # if the authentication fails, display an error message
        else:
            messages.error(request, "You are not registered yet please register")
            return redirect('signup')
    return render(request, "myapp/signin.html")

# View function for user signout
def signout(request):
    logout(request)
    messages.success(request, "You are successfully Signed Out")
    return redirect('home')

# View function for account activation
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    # Check if the user exists and the token is valid
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True  # activate the user
        myuser.save()
        messages.success(request, "Congratulations! Your account has been successfully activated. You can now access all the features and services available to you.")

        # Sending email notification for successful account activation
        subject = 'Account Activation Notification'
        message = 'Dear ' + myuser.first_name + ' \n We are pleased to inform you that your account has been successfully activated. You can now access all the features and services associated with your account. \n Please proceed to log in using your credentials, and feel free to explore the various functionalities available to you. \n If you encounter any issues or require further assistance, please do not hesitate to reach out to our support team at XXXXXXXXXX \n Thank you for choosing Subhash authentication web app. We look forward to serving you. \n'
        email_from = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, email_from, to_list)
        return redirect('signin')
    else:
        messages.error(request, "We're sorry, but we couldn't activate your account at this time. Please double-check the activation link or contact our support team for assistance")
        return redirect('signup')
