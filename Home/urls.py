from django.urls import path 
from .import views  

urlpatterns = [

    path("Index",views.Index,name="Index"),
    path("SignUp",views.SignUp,name="SignUp"),
    path("",views.SignIn,name="SignIn"),
    path("SignOut",views.SignOut,name="SignOut"),
    path("AdminIndex",views.AdminIndex,name="AdminIndex"),
    path("AddStaff",views.AddStaff,name="AddStaff"),
    path("Mystaff",views.Mystaff,name="Mystaff"),
    path("Deletestaff/<int:pk>",views.Deletestaff,name="Deletestaff"),
    path("Fuelstock",views.Fuelstock,name="Fuelstock"),
    path("AddFuelstock",views.AddFuelstock,name="AddFuelstock"),
    path("UpdateStock/<int:pk>",views.UpdateStock,name="UpdateStock"),
    path("deleteStock/<int:pk>",views.deleteStock,name="deleteStock"),
    path("FuelRequests",views.FuelRequests,name="FuelRequests"),
    path("PurchaseHistory",views.PurchaseHistory,name="PurchaseHistory"),
    path("StaffIndex",views.StaffIndex,name="StaffIndex"),
    path("CustomerFuelRequest",views.CustomerFuelRequest,name="CustomerFuelRequest"),
    path("OrderTaken/<int:pk>",views.OrderTaken,name="OrderTaken"),
    path("OrderDeliveryChange/<int:pk>",views.OrderDeliveryChange,name="OrderDeliveryChange"),
    path("OrderDelivered/<int:pk>",views.OrderDelivered,name="OrderDelivered"),
    path("DeliveryHistory",views.DeliveryHistory,name="DeliveryHistory"),
    path("ViewInMap/<int:pk>",views.ViewInMap,name="ViewInMap"),
    path("FuelPriceUpdate",views.FuelPriceUpdate,name="FuelPriceUpdate"),
    path("AdminViewFuelRequests",views.AdminViewFuelRequests,name="AdminViewFuelRequests"),
    path("paymenthandler",views.paymenthandler,name="paymenthandler"),
    path("DeleteOrderByCustomer/<int:pk>",views.DeleteOrderByCustomer,name="DeleteOrderByCustomer"),




    
]