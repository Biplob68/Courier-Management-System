
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("contact/", views.contact, name="contact"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("productview/", views.productView, name="ProductView"),
    path("order/",views.order,name="order"),
    path("login/",views.signin,name="login"),
    path("signup/",views.signup,name="signup"),
    path("logout/",views.user_logout,name="logout"),
    path("thank/",views.thank,name="thank"),
    path("change_password/",views.change_password,name="change_password"),

    path("emp_home/",views.emp_index,name="emp_home"),
    path("pending_order/<int:order_id>/",views.pending_order,name="pending_order"),
    path("add_order/",views.add_order,name="add_order"),
    path("voucher/",views.voucher,name="voucher"),
    path("update_order/",views.update_order,name="update_order"),
    path("report/",views.report,name="report"),

]