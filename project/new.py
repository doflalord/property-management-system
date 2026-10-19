class Property:
    def __init__(self, id, city, neighborhood, price):
        self.id = id
        self.city = city
        self.neighborhood = neighborhood
        self.price = float(price)

    def display(self) -> None:
        print(f"ID: {self.id}")
        print(f"City: {self.city}")
        print(f"Neighborhood: {self.neighborhood}")
        print(f"Price: {self.price}")


class Land(Property):
    def __init__(self, id, city, neighborhood, price, size):
        super().__init__(id, city, neighborhood, price)
        self.size = size

    def display(self) :
        super().display()
        print(f"Size: {self.size}")


class House(Property):
    def __init__(self, id ,city, neighborhood, price, floors, apartments):
        super().__init__(id, city, neighborhood, price)
        self.floors = floors
        self.apartments = apartments

    def display(self) :
        super().display()
        print(f"Floors: {self.floors}")
        print(f"Number of apartments: {self.apartments}")


class Apartment(Property):
    def __init__(self, id, city, neighborhood, price, floor, rooms):
        super().__init__(id, city, neighborhood, price)
        self.floor = floor
        self.rooms = rooms

    def display(self) :
        super().display()
        print(f"Floor: {self.floor}")
        print(f"Number of rooms: {self.rooms}")
lands = []
houses = []
apartments = []

class PropertyManager:
    
    # إضافة عقار
    def add_property(self, prop: Property):
        if isinstance(prop,Land):
            lands.append(prop)
            print(f"{prop.id} has added successfully")
        if isinstance(prop,House):
            houses.append(prop)
            print(f"{prop.id} has added successfully")
        if isinstance(prop,Apartment):
            apartments.append(prop)
            print(f"{prop.id} has added successfully")

