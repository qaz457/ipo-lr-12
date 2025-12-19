import random

class Client:
    def __init__(self, name, cargo_weight, is_vip=False):
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip
    
    def __str__(self):
        vip_status = "VIP" if self.is_vip else "обычный"
        return f"Клиент: {self.name}, Груз: {self.cargo_weight}т, Статус: {vip_status}"

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
            raise ValueError(f"Превышена грузоподъемность! Свободно: {self.capacity - self.current_load}т, требуется: {client.cargo_weight}т")
        
        self.current_load += client.cargo_weight
        self.clients_list.append(client.name)
    
    def clear_load(self):
        self.current_load = 0
        self.clients_list = []
    
    def get_free_capacity(self):
        return self.capacity - self.current_load
    
    def __str__(self):
        return f"ID: {self.vehicle_id}, Вместимость: {self.capacity}т, Загружено: {self.current_load}т, Клиенты: {self.clients_list}"

class Truck(Vehicle):
    def __init__(self, capacity, color):
        super().__init__(capacity)
        self.color = color
        self.type = "Грузовик"
    
    def __str__(self):
        return f"{self.type} {super().__str__()}, Цвет: {self.color}"

class Train(Vehicle):
    def __init__(self, capacity, number_of_cars):
        super().__init__(capacity)
        self.number_of_cars = number_of_cars
        self.type = "Поезд"
    
    def __str__(self):
        return f"{self.type} {super().__str__()}, Вагонов: {self.number_of_cars}"

class TransportCompany:
    def __init__(self, name):
        self.name = name
        self.vehicles = []
        self.clients = []
    
    def add_vehicle(self, vehicle):
        if not isinstance(vehicle, Vehicle):
            raise TypeError("Ожидается объект класса Vehicle")
        self.vehicles.append(vehicle)
        print(f"Транспорт {vehicle.vehicle_id} ({vehicle.type}) добавлен в компанию '{self.name}'")
    
    def remove_vehicle(self, vehicle_id):

        for i, vehicle in enumerate(self.vehicles):
            if vehicle.vehicle_id == vehicle_id:
                removed = self.vehicles.pop(i)
                print(f"✓ Транспорт {vehicle_id} удален")
                return removed
        print(f"Транспорт с ID {vehicle_id} не найден")
        return None
    
    def list_vehicles(self):
        return self.vehicles
    
    def list_available_vehicles(self):
        return [v for v in self.vehicles if v.get_free_capacity() > 0]
    
    def add_client(self, client):
        if not isinstance(client, Client):
            raise TypeError("Можно добавлять только объекты класса Client")
        self.clients.append(client)
        print(f"Клиент {client.name} добавлен в компанию '{self.name}'")
    
    def remove_client(self, name):
        for i, client in enumerate(self.clients):
            if client.name == name:
                removed = self.clients.pop(i)
                print(f"Клиент {name} удален")
                return removed
        print(f"Клиент с именем {name} не найден")
        return None
    
    def clear_all_loads(self):
        for vehicle in self.vehicles:
            vehicle.clear_load()
        print("Все грузы выгружены")
    
    def optimize_cargo_distribution(self):

        if not self.clients:
            print("Нет клиентов для распределения")
            return
        
        if not self.vehicles:
            print("Нет доступного транспорта")
            return

        self.clear_all_loads()
        

        sorted_clients = sorted(self.clients, key=lambda c: (not c.is_vip, c.cargo_weight), reverse=True)
        
        sorted_vehicles = sorted(self.vehicles, key=lambda v: v.capacity, reverse=True)
        
        distributed_count = 0
        not_distributed = []
        
        print("="*50)
        print("НАЧАЛО РАСПРЕДЕЛЕНИЯ ГРУЗОВ")
        print("="*50)
        
        for client in sorted_clients:
            distributed = False
            
            for vehicle in sorted_vehicles:
                if vehicle.get_free_capacity() >= client.cargo_weight:
                    try:
                        vehicle.load_cargo(client)
                        distributed = True
                        distributed_count += 1
                        vip_status = " (VIP)" if client.is_vip else ""
                        print(f"Груз клиента {client.name}{vip_status} ({client.cargo_weight}т) "
                              f"размещен в {vehicle.type}е ID: {vehicle.vehicle_id}")
                        break
                    except ValueError:
                        continue
            
            if not distributed:
                not_distributed.append(client)

        print("="*50)
        print("РЕЗУЛЬТАТЫ РАСПРЕДЕЛЕНИЯ")
        print("="*50)
        
        if distributed_count > 0:
            print(f"Успешно распределено грузов: {distributed_count}/{len(self.clients)}")
        
        if not_distributed:
            print(f"Не удалось разместить {len(not_distributed)} груз(ов):")
            for client in not_distributed:
                vip_status = "VIP " if client.is_vip else ""
                print(f"  - {vip_status}{client.name}: {client.cargo_weight}т")
        
        print("Состояние транспорта:")
        used_vehicles = [v for v in self.vehicles if v.current_load > 0]
        if used_vehicles:
            for i, vehicle in enumerate(used_vehicles, 1):
                utilization = (vehicle.current_load / vehicle.capacity) * 100
                print(f"{i}. {vehicle} (загрузка: {utilization}%)")
        else:
            print("  Транспорт не использован")
    
    def show_statistics(self):
        print("="*50)
        print(f"СТАТИСТИКА КОМПАНИИ '{self.name}'")
        print("="*50)
        
        print(f"\nКлиенты ({len(self.clients)}):")
        if self.clients:
            vip_count = sum(1 for c in self.clients if c.is_vip)
            total_cargo = sum(c.cargo_weight for c in self.clients)
            for i, client in enumerate(self.clients, 1):
                vip = " [VIP]" if client.is_vip else ""
                print(f"{i}. {client.name}{vip}: {client.cargo_weight}т")
            print(f"Итого: VIP клиентов: {vip_count}, Общий вес грузов: {total_cargo}т")
        else:
            print("Нет клиентов")
        
        print(f"Транспорт ({len(self.vehicles)}):")
        if self.vehicles:
            trucks = [v for v in self.vehicles if isinstance(v, Truck)]
            trains = [v for v in self.vehicles if isinstance(v, Train)]
            total_capacity = sum(v.capacity for v in self.vehicles)
            
            print(f" Грузовиков: {len(trucks)}")
            print(f" Поездов: {len(trains)}")
            print(f" Общая вместимость: {total_capacity}т")
            
            for i, vehicle in enumerate(self.vehicles, 1):
                free = vehicle.get_free_capacity()
                print(f"{i}. {vehicle}")
        else:
            print("Нет транспорта")