import requests
from .models import ProviderService
from locations.models import CenterLocation


def createProviderService(data, provider_id):
    provider_service, _ = ProviderService.objects.get_or_create(
        providerID=provider_id, productID_id=data["productID"],
    )
    provider_service.serviceTitle = data["serviceTitle"]
    provider_service.serviceDescription = data["serviceDescription"]
    provider_service.longitude = data["longitude"]
    provider_service.lattitude = data["lattitude"]
    provider_service.CenterLocationID_id = data["centerLocationID"]
    provider_service.save()

    return provider_service


def pinProviderServiceCenter(lattitude, longitude):
    headers, payload = {}, {}
    url = "https://nominatim.openstreetmap.org/reverse?lat={}&lon={}&format=json" \
        .format(lattitude, longitude)
    response = requests.request("GET", url, headers=headers, data=payload)

    center = CenterLocation.objects.filter(displayName=response.json()["display_name"]).first()
    if center:
        return center
    else:
        return createNewCenterLocation(response.json())


state = ["region", "state", "state_district", "county"]
town = ["municipality", "city", "town", "village"]
suburb = ["city_district", "district", "borough", "suburb", "subdivision"]
block = ["city_block", "residential", "farm", "farmyard", "industrial", "commercial", "retail"]
landmark = [
    "emergency", "historic", "military", "natural", "landuse", "place", "railway", "man_made", "aerialway",
    "boundary", "amenity", "aeroway", "club", "craft", "leisure", "office", "mountain_pass", "shop",
    "tourism", "bridge", "tunnel", "waterway"
]


def createNewCenterLocation(center):
    center_obj = CenterLocation(displayName=center["display_name"])
    for x in state:
        if x in center["address"]:
            center_obj.state = center["address"][x]
    for x in town:
        if x in center["address"]:
            center_obj.town = center["address"][x]
    for x in suburb:
        if x in center["address"]:
            center_obj.suburb = center["address"][x]

    for x in landmark:
        if x in center["address"]:
            center_obj.landmark = center["address"][x]
    for x in block:
        if x in center["address"]:
            center_obj.centerBlock = center["address"][x]
    if "road" in center["address"]:
        center_obj.road = center["address"]["road"]
    center_obj.save()

    return center_obj

