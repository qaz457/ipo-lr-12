from transport import TransportCompany, Truck, Train, Client
import sys

def print_menu():
    print("ГЛАВНОЕ МЕНЮ:")
    print("1. Добавить транспортное средство")
    print("2. Добавить клиента")
    print("3. Просмотреть всю информацию")
    print("4. Распределить грузы (оптимизация)")
    print("5. Управление транспортом")
    print("6. Управление клиентами")
    print("7. Загрузить демо-данные")
    print("8. Очистить все данные")
    print("0. Выход")

def print_vehicle_menu():
    print("ВЫБЕРИТЕ ТИП ТРАНСПОРТА:")
    print("1. Грузовик")
    print("2. Поезд")
    print("0. Назад")

def print_control_menu():
    print("УПРАВЛЕНИЕ:")
    print("1. Удалить транспорт")
    print("2. Удалить клиента")
    print("3. Очистить все грузы")
    print("0. Назад")

def create_company():
    name = input("Введите название транспортной компании: ")
    return TransportCompany(name)

def vehicle_menu(company):
    while True:
        print_vehicle_menu()
        choice = input("Выберите действие: ")
        
        if choice == "1": 
            try:
                capacity = float(input("Введите грузоподъемность: "))
                color = input("Введите цвет грузовика: ")
                truck = Truck(capacity, color)
                company.add_vehicle(truck)
            except ValueError:
                print("введите корректное число для грузоподъемности")
        
        elif choice == "2": 
            try:
                capacity = float(input("Введите грузоподъемность: "))
                cars = int(input("Введите количество вагонов: "))
                train = Train(capacity, cars)
                company.add_vehicle(train)
            except ValueError:
                print("введите корректные числовые значения")
        
        elif choice == "0":
            break
        
        else:
            print("Неверный выбор")

def add_client_menu(company):
    print("ДОБАВЛЕНИЕ КЛИЕНТА:")
    name = input("Введите имя клиента: ")
    
    try:
        cargo = float(input("Введите вес груза: "))
        if cargo <= 0:
            print("Вес груза должен быть положительным числом")
            return
    except ValueError:
        print("введите корректное число для веса груза")
        return
    
    vip = input("VIP клиент? (да/нет): ").lower()
    is_vip = vip in ['да', 'yes', '1']
    
    client = Client(name, cargo, is_vip)
    company.add_client(client)

def all_info(company):
    company.show_statistics()

def manage_vehicles_menu(company):
    while True:
        print("СПИСОК ТРАНСПОРТА:")
        vehicles = company.list_vehicles()
        if not vehicles:
            print("  Нет транспортных средств")
            return
        
        for i, vehicle in enumerate(vehicles, 1):
            print(f"{i}. {vehicle}")
        
        print_control_menu()
        choice = input("Выберите действие: ")
        
        if choice == "1": 
            try:
                vehicle_id = int(input("Введите ID транспорта для удаления: "))
                company.remove_vehicle(vehicle_id)
            except ValueError:
                print("введите корректный ID")
        
        elif choice == "2": 
            name = input("Введите имя клиента для удаления: ")
            company.remove_client(name)
        
        elif choice == "3": 
            company.clear_all_loads()
        
        elif choice == "0":
            break
        
        else:
            print("Неверный выбор")

def load_data(company):
    
    vehicles = [
        Truck(10.0, "синий"),
        Truck(8.0, "красный"),
        Truck(15.0, "зеленый"),
        Train(50.0, 10),
        Train(30.0, 6)
    ]
    
    for vehicle in vehicles:
        company.add_vehicle(vehicle)
    

    clients = [
        Client("Андрей", 2.5),
        Client("Сергей", 1.4, is_vip=True),
        Client("Мария", 3.0),
        Client("Иван", 4.0, is_vip=True),
        Client("Ольга", 5.5),
        Client("Дмитрий", 2.0, is_vip=True),
        Client("Екатерина", 7.0)
    ]
    
    for client in clients:
        company.add_client(client)
    
    print("данные загружены успешно!")

def clear_all_data(company):
    confirm = input("Вы уверены, что хотите очистить все данные? (да/нет): ")
    if confirm.lower() in ['да', 'yes', '1']:
        company.vehicles.clear()
        company.clients.clear()
        print("Все данные очищены")
    else:
        print("Операция отменена")

def main():
    company = create_company()
    
    while True:
        print(f"Компания: {company.name}")
        print(f"Транспорт: {len(company.vehicles)} | Клиенты: {len(company.clients)}")
        
        print_menu()
        choice = input("Выберите действие (0-8): ")
        
        if choice == "1": 
            vehicle_menu(company)
        
        elif choice == "2": 
            add_client_menu(company)
        
        elif choice == "3":
            all_info(company)
        
        elif choice == "4":
            company.optimize_cargo_distribution()
        
        elif choice == "5":  
            manage_vehicles_menu(company)
        
        elif choice == "6": 
            print("СПИСОК КЛИЕНТОВ:")
            if not company.clients:
                print(" Нет клиентов")
            else:
                for i, client in enumerate(company.clients, 1):
                    vip = " [VIP]" if client.is_vip else ""
                    print(f"{i}. {client.name}{vip}: {client.cargo_weight}т")
            
  
            name = input("Введите имя клиента для удаления (или Enter для отмены): ")
            if name:
                company.remove_client(name)
        
        elif choice == "7":
            load_data(company)
        
        elif choice == "8": 
            clear_all_data(company)
        
        elif choice == "0":  
            print("end code")
      
            sys.exit(0)
        
        else:
            print("Неверный выбор. Попробуйте снова.")

        if choice not in ["0", "3", "4"]:
            input("Нажмите Enter для продолжения...")

main()