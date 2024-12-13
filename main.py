import csv
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QTabWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt


    # app
app = QApplication(sys.argv)

    # qss stylesheet aka css
with open('style.qss', 'r') as f:
    app.setStyleSheet(f.read())

class App(QWidget):  
        def __init__(self):
            super().__init__()
            self.setWindowTitle("DECK")

            # data 
            self.products = self.collection('cards.csv')  
            self.inventory = []

            # tabs
            self.tabs_widget = Tabs(self, self.products, self.inventory, self.view_selected)

            # main layout
            main_layout = QVBoxLayout(self)  
            main_layout.addWidget(self.tabs_widget)  

            # sätter layout i ett fönster
            self.setLayout(main_layout)
            self.show()

        def collection(self, filename):
            """ läs data från databas(csv fil) """
            products = []
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    id = int(row['id'])
                    name = row['name']
                    type = row['type']
                    desc = row['desc']
                    energy = int(row['energy'])
                    classtype = row['classtype']

                    products.append({
                        "id": id,
                        "name": name,
                        "type": type,
                        "desc": desc,
                        "energy": energy,
                        "classtype": classtype
                    })
            return products
        
        def view_selected(self):
            
            print("view selected")

class ViewCard(QDialog):
        def __init__(self, card):
            super().__init__()
            
            self.setWindowTitle(f"Card: {card['name']}")

            
            layout = QVBoxLayout()
            
            
            name_label = QLabel(f"Name: {card['name']}")
            type_label = QLabel(f"Type: {card['type']}")
            desc_label = QLabel(f"Description: {card['desc']}")
            energy_label = QLabel(f"Energy: {card['energy']}")
            classtype_label = QLabel(f"Class: {card['classtype']}")

            layout.addWidget(name_label)
            layout.addWidget(type_label)
            layout.addWidget(desc_label)
            layout.addWidget(energy_label)
            layout.addWidget(classtype_label)

            self.setLayout(layout)
            self.exec_()  
            
class Tabs(QWidget):
        def __init__(self, parent, products, inventory, view_selected):
            super(QWidget, self).__init__(parent)
            self.layout = QVBoxLayout(self)  

            self.products = products
            self.inventory = inventory
            self.view_selected = view_selected

            # skapa tabs och widget
            self.tabs = QTabWidget()
            self.tabs.tabBar().setExpanding(True)

            # tabs
            self.tab1 = QWidget() 
            self.tab2 = QWidget()  # inventory
            self.tab3 = QWidget()  # the ironclad
            self.tab4 = QWidget()  # the silent
            self.tab5 = QWidget()  # the defect
            self.tab6 = QWidget()  # the watcher
            self.tab7 = QWidget()  # view selected card
            
            # lägg till tabbar i "tabs"
            self.tabs.addTab(self.tab1, "Cards")
            self.tabs.addTab(self.tab2, "Inventory")
            self.tabs.addTab(self.tab3, "The Ironclad")
            self.tabs.addTab(self.tab4, "The Silent")
            self.tabs.addTab(self.tab5, "The Defect")
            self.tabs.addTab(self.tab6, "The Watcher")
            self.tabs.addTab(self.tab7, "View Card")

            # skapa "tables" för alla tabs
            self.create_table(self.tab1, self.products, "table1")
            self.create_inventory(self.tab2)
            self.create_table(self.tab3, self.filter_by_classtype('The Ironclad'), "table3")
            self.create_table(self.tab4, self.filter_by_classtype('The Silent'), "table4")
            self.create_table(self.tab5, self.filter_by_classtype('The Defect'), "table5")
            self.create_table(self.tab6, self.filter_by_classtype('The Watcher'), "table6")
            
            self.view_button = QPushButton("View?")
            self.view_button.clicked.connect(self.view_selected)  

        
            self.tab7_layout = QVBoxLayout()
            self.tab7_layout.addWidget(self.view_button)

            self.tab7.setLayout(self.tab7_layout)

        
            self.layout.addWidget(self.tabs)
            self.setLayout(self.layout)
        
        
        def view_selected(self):
            selected_indexes = None
        
            if self.tabs.currentIndex() == 0:
                selected_indexes = self.table1.selectedIndexes()
            elif self.tabs.currentIndex() == 1:
                selected_indexes = self.inventory_table.selectedIndexes()

            if selected_indexes:
                row = selected_indexes[0].row()

            if self.tabs.currentIndex() == 0:  # Cards tab
                card = {
                    "id": int(self.table1.item(row, 0).text()),
                    "name": self.table1.item(row, 1).text(),
                    "type": self.table1.item(row, 2).text(),
                    "desc": self.table1.item(row, 3).text(),
                    "energy": int(self.table1.item(row, 4).text()),
                    "classtype": self.table1.item(row, 5).text()
                }
            elif self.tabs.currentIndex() == 1:  
                card = {
                    "id": int(self.inventory_table.item(row, 0).text()),
                    "name": self.inventory_table.item(row, 1).text(),
                    "type": self.inventory_table.item(row, 2).text(),
                    "desc": self.inventory_table.item(row, 3).text(),
                    "energy": int(self.inventory_table.item(row, 4).text()),
                    "classtype": self.inventory_table.item(row, 5).text()
                }

            
                self.view_card = ViewCard(card)
            else:
                print("No card selected!")
                
            




        def filter_by_classtype(self, classtype):
            """filtrerar alla kort för att separera de i deras klasser/tabs"""
            return [product for product in self.products if product['classtype'] == classtype]
        
        
        def create_table(self, tab, products, table_name):
            """skapa "table" för main cards listan"""
            table = QTableWidget(len(products), 6)
            table.setHorizontalHeaderLabels(["#", "Name", "Type", "Description", "Energy", "Classtype"])
            table.setSelectionMode(QTableWidget.SingleSelection)

            for row, product in enumerate(products):
                table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
                table.setItem(row, 1, QTableWidgetItem(product['name']))
                table.setItem(row, 2, QTableWidgetItem(product['type']))
                table.setItem(row, 3, QTableWidgetItem(product['desc']))
                table.setItem(row, 4, QTableWidgetItem(str(product['energy'])))
                table.setItem(row, 5, QTableWidgetItem(product['classtype']))

            setattr(self, table_name, table)

            # layout för tab1
            tab_layout = QVBoxLayout()
            tab_layout.addWidget(table)

            if tab == self.tab1:
                add_button = QPushButton("Add to inventory?")
                add_button.setFixedSize(100, 40)
                add_button.clicked.connect(self.add_to_inventory)
                tab_layout.addWidget(add_button)

            tab.setLayout(tab_layout)


        def create_inventory(self, tab2):
    
            self.inventory_table = QTableWidget(len(self.inventory), 6)
            self.inventory_table.setHorizontalHeaderLabels(["#", "Name", "Type", "Description", "Energy", "Classtype"])

   
            print(f"Initial Inventory: {self.inventory}")

   
            self.populate_inventory_table()

    
            inventory_layout = QVBoxLayout()
            inventory_layout.addWidget(self.inventory_table)

    
            remove_button = QPushButton("Remove?")
            remove_button.clicked.connect(self.remove_from_inventory)
            inventory_layout.addWidget(remove_button)

            tab2.setLayout(inventory_layout)


        def add_to_inventory(self):
            """lägg till valda kort i inventory"""
            selected_indexes = self.table1.selectedIndexes()

            if selected_indexes:
                for index in selected_indexes:
                    row = index.row()
                    card = {
                        "id": int(self.table1.item(row, 0).text()),
                        "name": self.table1.item(row, 1).text(),
                        "type": self.table1.item(row, 2).text(),
                        "desc": self.table1.item(row, 3).text(),
                        "energy": int(self.table1.item(row, 4).text()),
                        "classtype": self.table1.item(row, 5).text()
                    }
                    self.inventory.append(card)

                print(f"Added card to inventory: {card['name']}")  
                self.populate_inventory_table()  

        def remove_from_inventory(self):
            """ta bort valda kort från inventory"""
            selected_rows = list(set(index.row() for index in self.inventory_table.selectedIndexes()))

            if selected_rows:
                for row in reversed(selected_rows):
                    del self.inventory[row]

                print(f"Updated Inventory: {self.inventory}")  
                self.populate_inventory_table()  

        def populate_inventory_table(self):
            """lägg om alla kort till inventory för att 'refresh'"""
            # skapa om själva "table" för att uppdatera
            self.inventory_table.clearContents()
            self.inventory_table.setRowCount(len(self.inventory))

            # Debug: Check how many items in the inventory
            print(f"Populating Inventory Table: {len(self.inventory)} items")

            for row, product in enumerate(self.inventory):
                self.inventory_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
                self.inventory_table.setItem(row, 1, QTableWidgetItem(product['name']))
                self.inventory_table.setItem(row, 2, QTableWidgetItem(product['type']))
                self.inventory_table.setItem(row, 3, QTableWidgetItem(product['desc']))
                self.inventory_table.setItem(row, 4, QTableWidgetItem(str(product['energy'])))
                self.inventory_table.setItem(row, 5, QTableWidgetItem(product['classtype']))

            self.inventory_table.viewport().update()  # tvinga "table" att uppdatera 

if __name__ == "__main__":
    window = App()
    sys.exit(app.exec_())
