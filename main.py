
from transport.company import TransportCompany, Truck, Client

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
