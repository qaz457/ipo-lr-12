import sys
from transport import TransportCompany, Truck, Train, Client

def menu():
    print("\n=== МЕНЮ ===")
    print("1. Добавить транспорт")
    print("2. Добавить клиента")
    print("3. Показать всё")
    print("4. Распределить грузы")
    print("5. Управление")
    print("6. Демо данные")
    print("7. Очистить всё")
    print("0. Выход")

def car_menu(company):
    while True:
        print("\nДобавить транспорт:")
        print("1. Грузовик")
        print("2. Поезд")
        print("0. Назад")
        choice = input("Выбор: ")
        
        if choice == "1":
            try:
                cap = float(input("Грузоподъемность: "))
                color = input("Цвет: ")
                truck = Truck(cap, color)
                company.add_vehicle(truck)
                print(f"Добавлен грузовик {truck.vehicle_id}")
            except:
                print("Ошибка")
        
        elif choice == "2":
            try:
                cap = float(input("Грузоподъемность: "))
                cars = int(input("Вагонов: "))
                train = Train(cap, cars)
                company.add_vehicle(train)
                print(f"Добавлен поезд {train.vehicle_id}")
            except:
                print("Ошибка")
        
        elif choice == "0":
            break

def client_menu(company):
    print("\nДобавить клиента:")
    name = input("Имя: ")
    try:
        weight = float(input("Вес груза: "))
        if weight <= 0:
            print("Вес должен быть > 0")
            return
    except:
        print("Ошибка")
        return
    
    vip = input("VIP? (да/нет): ").lower()
    is_vip = vip in ['да', 'yes', 'y', '1']
    
    client = Client(name, weight, is_vip)
    company.add_client(client)
    print(f"Добавлен клиент {name}")

def manage_menu(company):
    while True:
        print("\nУправление:")
        print("1. Удалить транспорт")
        print("2. Удалить клиента")
        print("3. Очистить грузы")
        print("0. Назад")
        choice = input("Выбор: ")
        
        if choice == "1":
            try:
                vid = int(input("ID транспорта: "))
                if company.remove_vehicle(vid):
                    print("Удалено")
                else:
                    print("Не найден")
            except:
                print("Ошибка")
        
        elif choice == "2":
            name = input("Имя клиента: ")
            if company.remove_client(name):
                print("Удалено")
            else:
                print("Не найден")
        
        elif choice == "3":
            company.clear_all_loads()
            print("Грузы очищены")
        
        elif choice == "0":
            break

def demo_data(company):
    company.vehicles = [
        Truck(10, "синий"),
        Truck(8, "красный"),
        Truck(15, "зеленый"),
        Train(50, 10),
        Train(30, 6)
    ]
    
    company.clients = [
        Client("Иван", 5, True),
        Client("Мария", 3),
        Client("Петр", 7, True),
        Client("Анна", 2),
        Client("Сергей", 4),
        Client("Ольга", 6)
    ]
    
    print("Демо данные загружены")

def main():
    name = input("Название компании: ")
    company = TransportCompany(name)
    
    while True:
        print(f"{company.name}")
        print(f"Транспорт: {len(company.vehicles)}, Клиенты: {len(company.clients)}")
        menu()
        choice = input("Выбор: ")
        
        if choice == "1":
            car_menu(company)
        
        elif choice == "2":
            client_menu(company)
        
        elif choice == "3":
            company.show_statistics()
        
        elif choice == "4":
            company.optimize_cargo_distribution()
            print("Грузы распределены")
        
        elif choice == "5":
            manage_menu(company)
        
        elif choice == "6":
            demo_data(company)
        
        elif choice == "7":
            confirm = input("Очистить всё? (да/нет): ")
            if confirm.lower() in ['да', 'yes', 'y']:
                company.vehicles.clear()
                company.clients.clear()
                print("Данные очищены")
        
        elif choice == "0":
            print("Выход")
            sys.exit(0)
        
        if choice not in ["0", "3"]:
            input("Нажмите Enter...")

if __name__ == "__main__":
    main()