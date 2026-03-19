from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
import random
from django.core.mail import send_mail
from .models import OTP
from django.views import View
from .models import Note


# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 =request.POST.get('password2')
        if password1 != password2:
            messages.error(request,'password does not match')
            return redirect('signup')
        if User.objects.filter(username = username).exists():
            messages.error(request,'username is already exists')
            return redirect('signup')
        else:
            user =User.objects.create_user(username = username, email=email,password=password1)
            user.save()
            return redirect('login')
    return render(request,'signup.html')


def login_view(request):
    if  request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username,password =password)
        if user is not None:
            login(request,user)
            messages.success(request,'login successfuly')
            return redirect('home')
        else:
            messages.error(request,'invalid username or password')
            return redirect('login')
    return render(request,'login.html')


    

# c
#


@login_required()
def create_note(request):
    if request.method == 'POST':
        title =request.POST.get('title')
        content =request.POST.get('content')
        if not title or not content :
            messages.error(request,'all field are requarid')
            return render(request,'create_note.html')
        else:
            Note.objects.create(title = title ,content = content ,user = request.user)
            messages.success(request ,'note created susseccfuly')
        return redirect('home')
    return render(request,'create_note.html')


@login_required()
def home_view(request):
    notes = Note.objects.filter(user = request.user)

    context = {
      "notes" : notes
    } 
    return render(request,'home.html',context)


@login_required
def note_detail(request ,id):
 notes = get_object_or_404( Note,id = id ,user = request.user)
 context = {
    "notes" : notes
    }
 return render (request,'note_detail.html' ,context)


@login_required
def update_note(request ,id):
    notes = get_object_or_404(Note,id = id ,user = request.user)
    if request.method == 'POST':
        title =  request.POST.get('title')
        content = request.POST.get('content')
        notes.title = title
        notes.content = content
        notes.save()
        return redirect('home')

    context ={
            'note':notes
        }
    return render(request,'update_note.html',context)
    
    
@login_required
def delete_note(request,id):
    notes = get_object_or_404(Note,id = id ,user = request.user)
    
    notes.delete()
    return redirect('home')

class SendOTPView(View):
    def get(self ,request):
       return render(request,'forgot_password.html')

    def post(self ,request):
        email = request.POST.get('email')
            
        try: 
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request,"forgot_password.html",{"error":"email not found"})
        # genrate OTP

        otp_code = str(random.randint(100000,999999))
        OTP.objects.create(user = user ,code = otp_code)

        print(f"your otp is {email} : {otp_code}")

        request.session['user_id'] = user.id

        return redirect('verify_otp')
    
class VerifyOTPView(View):
    def get(self,request):
        return render(request,'verify_otp.html') 
    def post(self,request):
        otp = request.POST.get('otp') 
        user_id = request.session.get('user_id')
        if OTP.objects.filter(user_id = user_id ,code = otp).exists():
            request.session['otp_verified'] = True
            return redirect('new_password')
        return render(request,'verify_otp.html',{"error":"invalid otp"})
    

class NewPasswordOTPView(View):
    def get(self, request):
        if not request.session.get('otp_verified'):
            return redirect('verify_otp')
        return render(request, 'new_password.html')

    def post(self, request):
        if not request.session.get('otp_verified'):
            return redirect('verify_otp')

        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password != confirm:
            return render(request, 'new_password.html', {'error': "password not match"})

        user = User.objects.get(id=request.session.get('user_id'))
        user.set_password(password)
        user.save()

        # cleanup
        request.session.pop('otp_verified', None)

        return redirect('login')

