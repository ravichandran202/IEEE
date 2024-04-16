from django.urls import path
from . import views

urlpatterns = [
    path("login",views.login_page, name="login_page"),
    path("register",views.register_page, name="register_page"),
    path("logout",views.logout, name="logout"),
    path("forgot-pasword",views.forgot_password_page, name="forgot_password"),
    path("home",views.home_page, name="home_page"),
    path("contact",views.contact_page, name="contact_page"),
    path("about",views.about_page, name="about_page"),
    path("pricing",views.pricing_page, name="pricing_page"),
    path("faq",views.faq_page, name="faq_page"),
    path("vendors",views.vendors_page, name="vendors_page"),
    path("vendor/<int:id>",views.vendor_page, name="vendor_page"),
    path("annnounce",views.announce_page, name="announce_page"),
]
