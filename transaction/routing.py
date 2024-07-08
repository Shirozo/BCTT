from django.urls import path , include
from transaction.transact import Transaction

# Here, "" is routing to the URL ChatConsumer which 
# will handle the chat functionality.
websocket_urlpatterns = [
    path("" , Transaction.as_asgi()) , 
] 