from django.urls import path
from .import views
from .views import  SendOTPView,VerifyOTPView,NewPasswordOTPView


urlpatterns = [
    path ('login/',views.login_view,name = 'login'),
    path('signup/',views.signup_view,name = 'signup'),
#     path("forgot-password/",SendOTPView.as_view(),name="forgot_password"),

# path("verify-otp/",VerifyOTPView.as_view(),name="verify_otp"),

# path("new-password/",NewPasswordView.as_view(),name="new_password"),
    path('home/',views.home_view,name='home'),
    path('create_note/',views.create_note,name = 'create_note'),
    path('note_detail/<int:id>/',views.note_detail,name = 'note_detail'),
    path('update_note/<int:id>/',views.update_note,name = 'update_note'),
    path('delete_note/<int:id>/',views.delete_note,name = 'delete_note'),

    # path('note_detail/<int:id>/', views.note_detail_view ,name ='note_detail'),
    # path('update_note/<int:id>/',views.update_note_view,name = 'update_note'),
    # path('delete_note/<int:id>/',views.delete_note_view,name='delete_note')
    path('forgot_password/', SendOTPView.as_view(),name = 'forgot_password'),
    path('verify_otp/',VerifyOTPView.as_view(),name='verify_otp'),
    path('new_password/', NewPasswordOTPView.as_view() ,name= 'new_password')

    
    
]