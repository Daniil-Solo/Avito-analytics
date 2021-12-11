import json
from math import sin, cos, asin, sqrt, pi
import torch
import torch.nn as nn


class BestModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.seq = nn.Sequential(
            nn.BatchNorm1d(37),
            nn.Linear(37, 8),
            nn.ReLU(),
            nn.Linear(8, 1)
        )

    def forward(self, x):
        res = self.seq(x)
        return res


def get_dist(llong1, llat1, llong2, llat2):
    rad = 6372795
    lat1 = llat1 * pi / 180.
    lat2 = llat2 * pi / 180.
    long1 = llong1 * pi / 180.
    long2 = llong2 * pi / 180.
    delta_long = long2 - long1
    delta_lat = lat2 - lat1
    ad = 2 * asin(sqrt(sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_long / 2) ** 2))
    dist = ad * rad
    return dist


def get_amenities(lat, lon):
    with open("../amenities.json", 'r') as f:
        amenities = json.load(f)

    amenities_dict = dict()
    for cat_id, category in enumerate(amenities):
        amenities_dict[category] = 0
        for coordinates in amenities[category]:
            object_lat = coordinates[0]
            object_lon = coordinates[1]
            dist = get_dist(
                llong1=lon,
                llat1=lat,
                llong2=object_lon,
                llat2=object_lat
            )
            if dist < 5000:
                amenities_dict[category] += 1
    return amenities_dict


def get_price(data):
    perm_esplanade_lat = 58.010455
    perm_esplanade_lon = 56.229443

    lat = data[-2]
    lon = data[-1]
    amenities_dict = get_amenities(lat, lon)
    distance = get_dist(
        llong1=lon,
        llat1=lat,
        llong2=perm_esplanade_lon,
        llat2=perm_esplanade_lat
    )
    data.append(amenities_dict['edu'])
    data.append(amenities_dict['health'])
    data.append(amenities_dict['culture'])
    data.append(amenities_dict['eat'])
    data.append(distance)

    tensor = torch.tensor(data, dtype=torch.float32)
    model = BestModel()
    model.load_state_dict(torch.load('../best_model.pkl'))
    model.eval()
    predict = model(tensor.reshape(1, -1))
    return int(predict)
