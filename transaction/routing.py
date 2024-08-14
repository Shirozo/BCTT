from django.urls import path , include
from transaction.transact import TransactionConsumer

# Here, "" is routing to the URL ChatConsumer which 
# will handle the chat functionality.
websocket_urlpatterns = [
    path("" , TransactionConsumer.as_asgi()) , 
] 