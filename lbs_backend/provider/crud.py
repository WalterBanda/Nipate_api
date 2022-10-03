import requests
from .models import ProviderService
from locations.models import CenterLocation


def createProviderService(data, providerID):
    provider_service, _ = ProviderService.objects.get_or_create(
        ProviderID=providerID, ProviderServiceName=data["ProviderServiceName"],
        ProductID_id=data["ProductID"]
    )
    return provider_service


def pinProviderServiceCenter(service):
    headers, payload = {}, {}
    url = "https://nominatim.openstreetmap.org/reverse?lat={}&lon={}&format=json"\
        .format(service.Lattitude, service.Longitude)
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.json())
    print("\n")
    center = CenterLocation.objects.filter(DisplayName=response.json()["display_name"]).first()
    print(center)
    return center
