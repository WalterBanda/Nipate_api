from .models import ProviderService
from locations.models import TownsModel

def createProviderService(data):
    service_obj, _ = ProviderService.objects.get_or_create(
        UserID_id=data["ProviderID"], ProviderServiceName=data["ProviderServiceName"],
        ProductID_id=data["ProductID"],
    )
    if data["LocationID"]:
        try:
            service_obj.LocationID_id = int(data["LocationID"])
        except:
            location, _ = TownsModel.objects.get_or_create(Name=data["LocationID"])
            service_obj.LocationID_id = location.id
