import dearpygui.dearpygui as dpg
from transport import TransportCompany, Truck, Train, Client
import json

class TransportApp:
    def __init__(self):
        self.company = TransportCompany("Transport Company")
        self.setup_gui()
    
    def setup_gui(self):
        dpg.create_context()
        
        with dpg.window(label="Transport Company", tag="main_window", width=1000, height=700):
            with dpg.menu_bar():
                with dpg.menu(label="File"):
                    dpg.add_menu_item(label="Export Data", callback=self.export_data)
                    dpg.add_separator()
                    dpg.add_menu_item(label="Exit", callback=lambda: dpg.stop_dearpygui())
                
                with dpg.menu(label="Data"):
                    dpg.add_menu_item(label="Demo Data", callback=self.load_demo)
                    dpg.add_menu_item(label="Clear All", callback=self.clear_all)
                
                with dpg.menu(label="Help"):
                    dpg.add_menu_item(label="About", callback=self.show_about)
            
            with dpg.group(horizontal=True):
                dpg.add_button(label="+ Client", callback=lambda: dpg.show_item("client_window"))
                dpg.add_button(label="+ Vehicle", callback=lambda: dpg.show_item("vehicle_window"))
                dpg.add_button(label="Distribute", callback=self.distribute)
                dpg.add_button(label="Clear Loads", callback=self.clear_loads)
            
            with dpg.group(horizontal=True):
                with dpg.child_window(width=400, height=500):
                    dpg.add_text("Clients:")
                    with dpg.table(tag="client_table", header_row=True, borders_innerH=True, borders_outerH=True):
                        dpg.add_table_column(label="Name")
                        dpg.add_table_column(label="Weight")
                        dpg.add_table_column(label="VIP")
                
                with dpg.child_window(width=550, height=500):
                    dpg.add_text("Vehicles:")
                    with dpg.table(tag="vehicle_table", header_row=True, borders_innerH=True, borders_outerH=True):
                        dpg.add_table_column(label="ID")
                        dpg.add_table_column(label="Type")
                        dpg.add_table_column(label="Capacity")
                        dpg.add_table_column(label="Loaded")
                        dpg.add_table_column(label="Details")
            
            dpg.add_text("", tag="status_text")
        
        with dpg.window(label="New Client", tag="client_window", width=400, height=300, show=False, modal=True):
            dpg.add_input_text(label="Name", tag="client_name", width=200)
            dpg.add_input_float(label="Cargo Weight", tag="client_weight", default_value=1.0, min_value=0.1, max_value=10000, width=200)
            dpg.add_checkbox(label="VIP Client", tag="client_vip")
            with dpg.group(horizontal=True):
                dpg.add_button(label="Save", callback=self.save_client)
                dpg.add_button(label="Cancel", callback=lambda: dpg.hide_item("client_window"))
        
        with dpg.window(label="New Vehicle", tag="vehicle_window", width=400, height=350, show=False, modal=True):
            dpg.add_combo(["Truck", "Train"], label="Type", tag="vehicle_type", default_value="Truck", callback=self.vehicle_type_changed)
            dpg.add_input_float(label="Capacity", tag="vehicle_capacity", default_value=10.0, min_value=0.1, max_value=1000, width=200)
            dpg.add_input_text(label="Color", tag="vehicle_color", default_value="blue", width=200, show=True)
            dpg.add_input_int(label="Number of Cars", tag="vehicle_cars", default_value=5, min_value=1, max_value=100, width=200, show=False)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Save", callback=self.save_vehicle)
                dpg.add_button(label="Cancel", callback=lambda: dpg.hide_item("vehicle_window"))
        
        with dpg.window(label="About Program", tag="about_window", width=400, height=200, show=False, modal=True):
            dpg.add_text("Laboratory Work 11")
            dpg.add_text("Variant: 1")
            dpg.add_text("Developer: Student Name")
            dpg.add_button(label="OK", callback=lambda: dpg.hide_item("about_window"))
        
        dpg.create_viewport(title='Transport Company', width=1000, height=700)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)
        
        self.load_demo()
        self.update_tables()
    
    def vehicle_type_changed(self):
        vehicle_type = dpg.get_value("vehicle_type")
        if vehicle_type == "Truck":
            dpg.show_item("vehicle_color")
            dpg.hide_item("vehicle_cars")
        else:
            dpg.hide_item("vehicle_color")
            dpg.show_item("vehicle_cars")
    
    def save_client(self):
        name = dpg.get_value("client_name").strip()
        weight = dpg.get_value("client_weight")
        vip = dpg.get_value("client_vip")
        
        if not name or len(name) < 2:
            self.show_status("Name must be at least 2 characters", error=True)
            return
        
        if weight <= 0:
            self.show_status("Weight must be positive", error=True)
            return
        
        client = Client(name, weight, vip)
        self.company.add_client(client)
        dpg.hide_item("client_window")
        self.update_tables()
        self.show_status(f"Client '{name}' added")
    
    def save_vehicle(self):
        vtype = dpg.get_value("vehicle_type")
        capacity = dpg.get_value("vehicle_capacity")
        
        if capacity <= 0:
            self.show_status("Capacity must be positive", error=True)
            return
        
        if vtype == "Truck":
            color = dpg.get_value("vehicle_color")
            vehicle = Truck(capacity, color)
        else:
            cars = dpg.get_value("vehicle_cars")
            vehicle = Train(capacity, cars)
        
        self.company.add_vehicle(vehicle)
        dpg.hide_item("vehicle_window")
        self.update_tables()
        self.show_status(f"{vtype} added (ID: {vehicle.vehicle_id})")
    
    def distribute(self):
        self.company.optimize_cargo_distribution()
        self.update_tables()
        self.show_status("Cargo distributed")
    
    def clear_loads(self):
        self.company.clear_all_loads()
        self.update_tables()
        self.show_status("Cargo cleared")
    
    def load_demo(self):
        self.company.vehicles = [
            Truck(10, "blue"),
            Truck(8, "red"),
            Train(50, 10),
            Train(30, 6)
        ]
        
        self.company.clients = [
            Client("Ivan", 5, True),
            Client("Maria", 3),
            Client("Peter", 7, True),
            Client("Anna", 2),
            Client("Olga", 6)
        ]
        
        self.update_tables()
        self.show_status("Demo data loaded")
    
    def clear_all(self):
        self.company.vehicles.clear()
        self.company.clients.clear()
        self.update_tables()
        self.show_status("All data cleared")
    
    def show_about(self):
        dpg.show_item("about_window")
    
    def export_data(self):
        if not self.company.clients and not self.company.vehicles:
            self.show_status("No data to export", error=True)
            return
        
        data = {
            "company": self.company.name,
            "clients": [
                {
                    "name": c.name,
                    "weight": c.cargo_weight,
                    "vip": c.is_vip
                } for c in self.company.clients
            ],
            "vehicles": [
                {
                    "id": v.vehicle_id,
                    "type": v.type,
                    "capacity": v.capacity,
                    "load": v.current_load,
                    "clients": v.clients_list
                } for v in self.company.vehicles
            ]
        }
        
        with open("transport_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self.show_status("Data exported to transport_data.json")
    
    def update_tables(self):
        for table in ["client_table", "vehicle_table"]:
            children = dpg.get_item_children(table, 1)
            for child in children:
                dpg.delete_item(child)
        
        for client in self.company.clients:
            with dpg.table_row(parent="client_table"):
                dpg.add_text(client.name)
                dpg.add_text(f"{client.cargo_weight:.1f}t")
                dpg.add_text("Yes" if client.is_vip else "No")
        
        for vehicle in self.company.vehicles:
            with dpg.table_row(parent="vehicle_table"):
                dpg.add_text(str(vehicle.vehicle_id))
                dpg.add_text(vehicle.type)
                dpg.add_text(f"{vehicle.capacity:.1f}t")
                dpg.add_text(f"{vehicle.current_load:.1f}t")
                if isinstance(vehicle, Truck):
                    dpg.add_text(f"Color: {vehicle.color}")
                else:
                    dpg.add_text(f"Cars: {vehicle.number_of_cars}")
    
    def show_status(self, message, error=False):
        if error:
            dpg.configure_item("status_text", color=[255, 0, 0])
        else:
            dpg.configure_item("status_text", color=[0, 200, 0])
        dpg.set_value("status_text", message)
    
    def run(self):
        dpg.start_dearpygui()
        dpg.destroy_context()

if __name__ == "__main__":
    app = TransportApp()
    app.run()