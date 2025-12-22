import random

class Client:
    def __init__(self, name, cargo_weight, is_vip=False):
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip
    
    def __str__(self):
        vip = "VIP" if self.is_vip else "обычный"
        return f"{self.name}: {self.cargo_weight}т ({vip})"

class Vehicle:
    def __init__(self, capacity):
        self.vehicle_id = random.randint(10000, 99999)
        self.capacity = capacity
        self.current_load = 0
        self.clients_list = []
    
    def load_cargo(self, client):
        if self.current_load + client.cargo_weight > self.capacity:
            return False
        self.current_load += client.cargo_weight
        self.clients_list.append(client.name)
        return True
    
    def get_free_capacity(self):
        return self.capacity - self.current_load
    
    def clear_load(self):
        self.current_load = 0
        self.clients_list = []
    
    def __str__(self):
        return f"{self.vehicle_id}: {self.current_load}/{self.capacity}т"

class Truck(Vehicle):
    def __init__(self, capacity, color):
        super().__init__(capacity)
        self.color = color
        self.type = "Грузовик"
    
    def __str__(self):
        return f"{self.type} {super().__str__()}, цвет: {self.color}"

class Train(Vehicle):
    def __init__(self, capacity, number_of_cars):
        super().__init__(capacity)
        self.number_of_cars = number_of_cars
        self.type = "Поезд"
    
    def __str__(self):
        return f"{self.type} {super().__str__()}, вагонов: {self.number_of_cars}"

class TransportCompany:
    def __init__(self, name):
        self.name = name
        self.vehicles = []
        self.clients = []
    
    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
    
    def add_client(self, client):
        self.clients.append(client)
    
    def remove_vehicle(self, vehicle_id):
        for i, v in enumerate(self.vehicles):
            if v.vehicle_id == vehicle_id:
                self.vehicles.pop(i)
                return True
        return False
    
    def remove_client(self, name):
        for i, c in enumerate(self.clients):
            if c.name == name:
                self.clients.pop(i)
                return True
        return False
    
    def list_vehicles(self):
        return self.vehicles
    
    def clear_all_loads(self):
        for v in self.vehicles:
            v.clear_load()
    
    def optimize_cargo_distribution(self):
        self.clear_all_loads()
        
        if not self.clients or not self.vehicles:
            print("Нет данных для распределения")
            return
        
        vip_clients = [c for c in self.clients if c.is_vip]
        regular_clients = [c for c in self.clients if not c.is_vip]
        
        vip_clients.sort(key=lambda c: c.cargo_weight, reverse=True)
        regular_clients.sort(key=lambda c: c.cargo_weight, reverse=True)
        
        sorted_clients = vip_clients + regular_clients
        sorted_vehicles = sorted(self.vehicles, key=lambda v: v.capacity, reverse=True)
        
        for client in sorted_clients:
            placed = False
            for vehicle in sorted_vehicles:
                if vehicle.get_free_capacity() >= client.cargo_weight:
                    if vehicle.load_cargo(client):
                        placed = True
                        break
            if not placed:
                print(f"Не удалось разместить: {client.name}")
    
    def show_statistics(self):
        print(f"=== {self.name} ===")
        print(f"Клиенты: {len(self.clients)}")
        for c in self.clients:
            vip = " [VIP]" if c.is_vip else ""
            print(f"  {c.name}: {c.cargo_weight}т{vip}")
        
        print(f"Транспорт: {len(self.vehicles)}")
        for v in self.vehicles:
            print(f"  {v}")
        
        total_load = sum(v.current_load for v in self.vehicles)
        total_capacity = sum(v.capacity for v in self.vehicles)
        if total_capacity > 0:
            print(f"Загрузка: {total_load}/{total_capacity}т ({total_load/total_capacity*100:.1f}%)")