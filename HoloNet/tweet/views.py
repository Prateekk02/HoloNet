from django.shortcuts import render
from .models import Tweet, EmailOTP
from .forms import TweetForm, UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import EmailOTP
import random
# Create your views here.

def index(request):
    return render(request, 'index.html')

#Read
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    for tweet in tweets:
        if tweet.photo and tweet.photo.file:
            tweet.photo_url = tweet.photo.url
        else:
            tweet.photo_url = None
    return render(request, 'tweet_list.html', {'tweets': tweets})

#Create
@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')        
    else:
        form = TweetForm()    
    return render(request, 'tweet_form.html', {'form': form})

#Edit
@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == "POST":
        form = TweetForm(request.POST , request.FILES, instance=tweet) 
        if form.is_valid():
            tweet = form.save(commit = False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')       
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})

#Delete
@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html',{'tweet':tweet})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            print("User saved successfully!")
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                print("User logged in:", request.user.is_authenticated)
                return redirect('tweet_list')
            else:
                print("Failed to log in")
        else:
            print("Form is not valid:", form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# OTP Verification Logic

# def generate_otp():
#     return str(random.randint(100000, 999999))

# def send_otp_email(request, user):
#     otp = generate_otp()
#     email_otp = EmailOTP.objects.create(user=user, otp=otp)
    
#     subject = "Your OTP Verification"
#     message = render_to_string("otp_email.html", {"otp": otp})
#     send_mail(subject, message, "from@example.com", [user.email])
    
# def verify_otp(request):
#     if request.method == "POST":
#         otp = request.POST.get("otp")
#         user = request.user

#         try:
#             email_otp = EmailOTP.objects.get(user=user, otp=otp)
#             # Check if OTP is expired (e.g., 15 minutes)
#             if # OTP is not expired:
#                 # Mark OTP as used
#                 email_otp.delete()
#                 return redirect("home")
#             else:
#                 return render(request, "verify_otp.html", {"error": "OTP expired"})
#         except EmailOTP.DoesNotExist:
#             return render(request, "verify_otp.html", {"error": "Invalid OTP"})

#     return render(request, "verify_otp.html")
    
    
    
    
    