import dearpygui.dearpygui as dpg
from transport import TransportCompany, Truck, Train, Client
import json


class TransportGUI:
    def __init__(self):
        self.company = TransportCompany("Transport Company")
        self.load_demo()
        self.make_gui()

    def load_demo(self):
        v = [
            Truck(10.0, "blue"),
            Truck(8.0, "red"),
            Train(50.0, 10),
            Train(30.0, 6)
        ]
        for veh in v:
            self.company.add_vehicle(veh)

        c = [
            Client("Andrew", 2.5),
            Client("Sergey", 1.4, True),
            Client("Maria", 3.0),
            Client("Ivan", 4.0, True)
        ]
        for cl in c:
            self.company.add_client(cl)

    def reload_demo(self):
        self.company.vehicles.clear()
        self.company.clients.clear()

        v = [
            Truck(10.0, "blue"),
            Truck(8.0, "red"),
            Train(50.0, 10),
            Train(30.0, 6)
        ]
        for veh in v:
            self.company.add_vehicle(veh)

        c = [
            Client("Andrew", 2.5),
            Client("Sergey", 1.4, True),
            Client("Maria", 3.0),
            Client("Ivan", 4.0, True)
        ]
        for cl in c:
            self.company.add_client(cl)

        self.refresh_tables()
        self.show_msg("Demo data loaded")

    def make_gui(self):
        dpg.create_context()

        with dpg.window(label="Main Window", tag="main"):
            with dpg.menu_bar():
                with dpg.menu(label="File"):
                    dpg.add_menu_item(label="Export Result", callback=self.export)
                    dpg.add_menu_item(label="Exit", callback=lambda: dpg.stop_dearpygui())

                with dpg.menu(label="Data"):
                    dpg.add_menu_item(label="Demo Data", callback=self.reload_demo)
                    dpg.add_menu_item(label="Clear All", callback=self.clear_all)

                with dpg.menu(label="Help"):
                    dpg.add_menu_item(label="About", callback=self.show_about)

            with dpg.group(horizontal=True):
                dpg.add_button(label="Client +", callback=self.show_add_client)
                dpg.add_button(label="Vehicle +", callback=self.show_add_vehicle)
                dpg.add_button(label="Distribute", callback=self.distribute)
                dpg.add_button(label="Clear Loads", callback=self.clear_loads)

            with dpg.group(horizontal=True):
                with dpg.child_window(width=400, tag="client_window"):
                    dpg.add_text("Clients:")
                    with dpg.table(header_row=True, tag="client_table", policy=dpg.mvTable_SizingFixedFit):
                        dpg.add_table_column(label="Name")
                        dpg.add_table_column(label="Weight")
                        dpg.add_table_column(label="VIP")

                with dpg.child_window(width=600, tag="vehicle_window"):
                    dpg.add_text("Vehicles:")
                    with dpg.table(header_row=True, tag="vehicle_table", policy=dpg.mvTable_SizingFixedFit):
                        dpg.add_table_column(label="ID")
                        dpg.add_table_column(label="Type")
                        dpg.add_table_column(label="Capacity")
                        dpg.add_table_column(label="Loaded")
                        dpg.add_table_column(label="Details")

            dpg.add_text("", tag="status")

        self.make_client_window()
        self.make_vehicle_window()
        self.make_about_window()

        dpg.create_viewport(title='Transport Company', width=1200, height=700)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main", True)
        self.refresh_tables()

    def make_client_window(self):
        with dpg.window(label="Client", modal=True, show=False, tag="client_win", width=400, height=300):
            dpg.add_input_text(label="Name", tag="client_name")
            dpg.add_input_float(label="Cargo Weight", tag="client_weight", default_value=1.0, min_value=0.1,
                                max_value=10000)
            dpg.add_checkbox(label="VIP", tag="client_vip")
            with dpg.group(horizontal=True):
                dpg.add_button(label="Save", callback=self.save_client)
                dpg.add_button(label="Cancel", callback=lambda: dpg.hide_item("client_win"))

    def make_vehicle_window(self):
        with dpg.window(label="Vehicle", modal=True, show=False, tag="vehicle_win", width=400, height=350):
            dpg.add_combo(["Truck", "Train"], label="Type", tag="vehicle_type", default_value="Truck",
                          callback=self.vehicle_changed)
            dpg.add_input_float(label="Capacity", tag="vehicle_capacity", default_value=10.0, min_value=0.1,
                                max_value=1000)
            dpg.add_input_text(label="Color", tag="vehicle_color", default_value="blue", show=False)
            dpg.add_input_int(label="Cars", tag="vehicle_cars", default_value=5, min_value=1, max_value=100,
                              show=False)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Save", callback=self.save_vehicle)
                dpg.add_button(label="Cancel", callback=lambda: dpg.hide_item("vehicle_win"))

    def make_about_window(self):
        with dpg.window(label="About Program", modal=True, show=False, tag="about_win", width=400, height=200):
            dpg.add_text("Laboratory Work 13")
            dpg.add_text("Variant: 1")
            dpg.add_text("Developer: Anfrey")
            dpg.add_button(label="OK", callback=lambda: dpg.hide_item("about_win"))

    def vehicle_changed(self):
        t = dpg.get_value("vehicle_type")
        if t == "Truck":
            dpg.show_item("vehicle_color")
            dpg.hide_item("vehicle_cars")
        else:
            dpg.hide_item("vehicle_color")
            dpg.show_item("vehicle_cars")

    def show_add_client(self):
        dpg.set_value("client_name", "")
        dpg.set_value("client_weight", 1.0)
        dpg.set_value("client_vip", False)
        dpg.show_item("client_win")

    def show_add_vehicle(self):
        dpg.set_value("vehicle_type", "Truck")
        dpg.set_value("vehicle_capacity", 10.0)
        dpg.set_value("vehicle_color", "blue")
        dpg.set_value("vehicle_cars", 5)
        dpg.show_item("vehicle_color")
        dpg.hide_item("vehicle_cars")
        dpg.show_item("vehicle_win")

    def show_about(self):
        dpg.show_item("about_win")

    def save_client(self):
        name = dpg.get_value("client_name").strip()
        weight = dpg.get_value("client_weight")
        vip = dpg.get_value("client_vip")

        if not name or len(name) < 2:
            self.show_err("Name must be at least 2 characters")
            return

        if weight <= 0:
            self.show_err("Weight must be positive")
            return

        client = Client(name, weight, vip)
        self.company.add_client(client)
        dpg.hide_item("client_win")
        self.refresh_tables()
        self.show_msg(f"Client {name} added")

    def save_vehicle(self):
        t = dpg.get_value("vehicle_type")
        cap = dpg.get_value("vehicle_capacity")

        if cap <= 0:
            self.show_err("Capacity must be positive")
            return

        if t == "Truck":
            color = dpg.get_value("vehicle_color")
            v = Truck(cap, color)
        else:
            cars = dpg.get_value("vehicle_cars")
            v = Train(cap, cars)

        self.company.add_vehicle(v)
        dpg.hide_item("vehicle_win")
        self.refresh_tables()
        self.show_msg(f"Vehicle {v.vehicle_id} added")

    def distribute(self):
        self.company.optimize_cargo_distribution()
        self.refresh_tables()
        self.show_msg("Cargo distributed")

    def clear_loads(self):
        self.company.clear_all_loads()
        self.refresh_tables()
        self.show_msg("Cargo cleared")

    def clear_all(self):
        self.company.vehicles.clear()
        self.company.clients.clear()
        self.refresh_tables()
        self.show_msg("All data cleared")

    def refresh_tables(self):
        try:
            if dpg.does_item_exist("client_table"):
                children = dpg.get_item_children("client_table", 1)
                for child in children:
                    dpg.delete_item(child)

            if dpg.does_item_exist("vehicle_table"):
                children = dpg.get_item_children("vehicle_table", 1)
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

        except Exception as e:
            print(f"Error: {e}")

    def export(self):
        if not self.company.clients and not self.company.vehicles:
            self.show_err("No data to export")
            return

        data = {
            "company": self.company.name,
            "clients": [
                {"name": c.name, "weight": c.cargo_weight, "vip": c.is_vip}
                for c in self.company.clients
            ],
            "vehicles": [
                {
                    "id": v.vehicle_id,
                    "type": v.type,
                    "capacity": v.capacity,
                    "load": v.current_load,
                    "clients": v.clients_list
                }
                for v in self.company.vehicles
            ]
        }

        with open("transport_export.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.show_msg("Data exported to transport_export.json")

    def show_err(self, msg):
        dpg.configure_item("status", color=[255, 0, 0])
        dpg.set_value("status", f"Error: {msg}")

    def show_msg(self, msg):
        dpg.configure_item("status", color=[0, 200, 0])
        dpg.set_value("status", msg)

    def run(self):
        dpg.start_dearpygui()
        dpg.destroy_context()


if __name__ == "__main__":
    app = TransportGUI()
    app.run()