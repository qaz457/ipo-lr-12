import random

class Client:
    def __init__(self, name, cargo_weight, is_vip=False):
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip

class Vehicle:
    def __init__(self, capacity):
        self.vehicle_id = random.randint(10000, 99999)
        self.capacity = capacity
        self.current_load = 0
        self.clients_list = []
    
    def load_cargo(self, client):
        if not isinstance(client, Client):
            raise TypeError("Ожидается объект класса Client")
        if self.current_load + client.cargo_weight > self.capacity:
            raise ValueError("Превышена грузоподъемность")
        
        self.current_load += client.cargo_weight
        self.clients_list.append(client.name)
    
    def __str__(self):
        return f"Vehicle ID: {self.vehicle_id}, Capacity: {self.capacity}, Current Load: {self.current_load}"

class Truck(Vehicle):
    def __init__(self, capacity, color):
        super().__init__(capacity)
        self.color = color

class Train(Vehicle):
    def __init__(self, capacity, number_of_cars):
        super().__init__(capacity)
        self.number_of_cars = number_of_cars

class TransportCompany:
    def __init__(self, name):
        self.name = name
        self.vehicles = []
        self.clients = []
    
    def add_vehicle(self, vehicle):
        if not isinstance(vehicle, Vehicle):
            raise TypeError("Ожидается объект класса Vehicle")
        self.vehicles.append(vehicle)
        print(f"Транспорт {vehicle.vehicle_id} добавлен в компанию {self.name}")
    
    def list_vehicles(self):
        return self.vehicles
    
    def add_client(self, client):
        if not isinstance(client, Client):
            raise TypeError("Можно добавлять только объекты класса Client")
        self.clients.append(client)
        print(f"Клиент {client.name} добавлен в компанию {self.name}")
    
    def optimize_cargo_distribution(self):

        sorted_clients = sorted(self.clients, key=lambda client: client.is_vip, reverse=True)

        sorted_vehicles = sorted(self.vehicles, key=lambda vehicle: vehicle.capacity, reverse=True)
        
        for client in sorted_clients:
            distributed = False
            for vehicle in sorted_vehicles:
           
                if vehicle.current_load + client.cargo_weight <= vehicle.capacity:
                    try:
                        vehicle.load_cargo(client)
                        distributed = True
                        print(f"Груз клиента {client.name} ({client.cargo_weight}т) размещен в транспорте {vehicle.vehicle_id}")
                        break
                    except ValueError:
                        continue
            if not distributed:
                print(f"Не удалось разместить груз клиента {client.name} ({client.cargo_weight}т)")

try:
    company = TransportCompany("Быстрая Доставка")
    
    truck1 = Truck(capacity=10.0, color="синий")
    truck2 = Truck(capacity=8.0, color="красный")
    
    company.add_vehicle(truck1)
    company.add_vehicle(truck2)
    
    client1 = Client("Андрей", 2.5)
    client2 = Client("Сергей", 1.4, is_vip=True)
    client3 = Client("Мария", 3.0)
    client4 = Client("Иван", 4.0, is_vip=True)
    
    company.add_client(client1)
    company.add_client(client2)
    company.add_client(client3)
    company.add_client(client4)
    
    company.optimize_cargo_distribution()
    
   
    print("\nСостояние транспорта после распределения:")
    for vehicle in company.vehicles:
        print(f"{vehicle}, Клиенты: {vehicle.clients_list}")
        
except (ValueError, TypeError) as e:
    print(f"Ошибка: {e}")