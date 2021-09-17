import pandas as pd


class Preprocessor:
    """
    This class prepares data with full features
    Don't use it if data don't contain some features
    """
    NonNanValuesCount = 14

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.data['delete'] = [True] * len(self.data)

    def delete_rows_with_nan(self):
        """
        This function removes records without physical address
        and records with non-nan data less than NonNanValuesCount
        """
        self.data.dropna(subset=['physical address'], inplace=True)
        #self.data.dropna(subset=['year of construction'], inplace=True)
        self.data.dropna(thresh=Preprocessor.NonNanValuesCount, inplace=True)

    def divide_address(self):
        """
        This function divides address into street and district
        """
        addresses = []
        districts = []
        for item in self.data['physical address']:
            divider_index = item.find("|")
            address = item[:divider_index]
            if "Пермский край, Пермь," in address:
                end_city_index = len("Пермский край, Пермь,")
                address = address[end_city_index:]
            addresses.append(address)
            district = item[divider_index + 2:]
            districts.append(district)
        self.data['address'] = addresses
        self.data['district'] = districts
        self.data.drop(columns=['physical address'], inplace=True)

        self.data['delete'] = self.data['district'].map(lambda x: x if len(x) < 25 else None)
        self.data.dropna(subset=['delete'], inplace=True)
        self.data.drop(columns=['delete'], inplace=True)

    def divide_area(self):
        """
        This function removes м² for area
        """
        self.data['area of apartment'] = self.data['area of apartment'].map(lambda x: x.replace(" м²", ""))

    def divide_garbage_chute(self):
        """
        This function divides garbage_chute into garbage chute and concierge
        """
        self.data["concierge"] = self.data['garbage chute'].map(str).map(lambda x: 'консьерж' in x)
        self.data["garbage chute"] = self.data['garbage chute'].map(str).map(lambda x: 'мусоропровод' in x)

    def correct_types(self):
        """
        This function corrects type following attributes:
        number of rooms, area of apartment, elevator
        """
        self.data["number of rooms"] = self.data["number of rooms"].map(lambda x: x if x.isdigit() else 1)
        self.data["number of rooms"] = self.data["number of rooms"].astype("int64")
        self.data["area of apartment"] = self.data["area of apartment"].astype("float64")
        self.data["elevator"] = self.data["elevator"].astype("bool")

    def filling_nan_values(self):
        """
        This function replaces nan-values from categorical-features into tops
        and replaces year of construction into top on region
        """
        table = self.data.describe(include="object")
        for column_name in table:
            self.data[column_name].fillna(value=table[column_name].top, inplace=True)

    def sort_column_names(self):
        """
        This function sorts column names
        """
        self.data = self.data[['address', 'district', 'number of floors', 'apartment floor',
                               'number of rooms', 'area of apartment', 'bathroom', 'repair',
                               'view from the windows', 'terrace', 'year of construction',
                               'garbage chute', 'type of house', 'parking', 'concierge',
                               'elevator', 'link', 'price']]

    def delete(self):
        self.delete_rows_with_nan()

    def form_new_attributes(self):
        self.divide_address()
        self.divide_area()
        self.divide_garbage_chute()
        self.correct_types()

    def change_structure(self):
        self.data = self.data.reindex(range(len(self.data)), method='ffill')
        self.sort_column_names()

    def get_data(self):
        """
        This function returns changed data
        """
        self.delete()
        self.form_new_attributes()
        self.filling_nan_values()
        self.change_structure()
        return self.data


class DataLoader:
    def __init__(self, path):
        self.path = path

    def load(self):
        return pd.read_csv(self.path, sep=';')


class DataSaver:
    def __init__(self, new_path, new_data):
        self.path = new_path
        self.data = new_data

    def save(self):
        self.data.to_csv(self.path, sep=';')
