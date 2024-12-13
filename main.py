import csv
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QTabWidget, QLabel, QPushButton, QMessageBox, QLineEdit, QComboBox, QFormLayout
from PyQt5.QtCore import Qt

# för att installera PyQt5 - pip install PyQt5
    
app = QApplication(sys.argv)

    
with open('style.qss', 'r') as f:
    app.setStyleSheet(f.read())


class AddCardDialog(QDialog):   # klass för att skapa ett "add card" fönster för att lägga in kort i csv filen
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Card")

        self.layout = QFormLayout(self)

        self.name_input = QLineEdit(self)
        self.desc_input = QLineEdit(self)
        self.type_input = QLineEdit(self)
        self.energy_input = QLineEdit(self)

        self.classtype_input = QComboBox()
        self.classtype_input.addItems(['The Ironclad', 'The Silent', 'The Defect', 'The Watcher'])

        self.layout.addRow(QLabel("Card name: "), self.name_input)
        self.layout.addRow(QLabel("Description: "), self.desc_input)
        self.layout.addRow(QLabel("Type: "), self.type_input)
        self.layout.addRow(QLabel("Energy: "), self.energy_input)
        self.layout.addRow(QLabel("Classtype: "), self.classtype_input)


        self.add_button = QPushButton("Add Card", self)
        self.add_button.clicked.connect(self.add_card)
        self.layout.addWidget(self.add_button)


        self.setLayout(self.layout)

    def add_card(self):

        name = self.name_input.text()
        desc = self.desc_input.text()
        type = self.type_input.text()
        energy = self.energy_input.text()
        classtype = self.classtype_input.currentText()

        if not name or not type or not desc or not energy or not classtype:
            print("Fill out all fields or no card :C")
            return
            
        new_card = {
            'id': None,
            'name': name,
            'type': type,
            'desc': desc,
            'energy': int(energy),
            'classtype': classtype
        }
        self.accept()

        self.parent().add_card_to_csv(new_card)



class App(QWidget):  
        def __init__(self):
            super().__init__()
            self.setWindowTitle("DECK")

            
            self.products = self.collection('cards.csv')  
            self.inventory = []

            
            self.tabs_widget = Tabs(self, self.products, self.inventory)

            
            main_layout = QVBoxLayout(self)  
            main_layout.addWidget(self.tabs_widget)  

           
            self.setLayout(main_layout)
            self.show()

        def collection(self, filename):
            
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
        def __init__(self, parent, products, inventory):
            super(QWidget, self).__init__(parent)
            self.layout = QVBoxLayout(self)  

            self.products = products
            self.inventory = inventory
            

            
            self.tabs = QTabWidget()
            self.tabs.tabBar().setExpanding(True)

            
            self.tab1 = QWidget() 
            self.tab2 = QWidget()  # inventory
            self.tab3 = QWidget()  # the ironclad
            self.tab4 = QWidget()  # the silent
            self.tab5 = QWidget()  # the defect
            self.tab6 = QWidget()  # the watcher
            
            
            self.tabs.addTab(self.tab1, "Cards")
            self.tabs.addTab(self.tab2, "Inventory")
            self.tabs.addTab(self.tab3, "The Ironclad")
            self.tabs.addTab(self.tab4, "The Silent")
            self.tabs.addTab(self.tab5, "The Defect")
            self.tabs.addTab(self.tab6, "The Watcher")

        
            self.create_table(self.tab3, self.filter_by_classtype('The Ironclad'), "table3")
            self.create_table(self.tab4, self.filter_by_classtype('The Silent'), "table4")
            self.create_table(self.tab5, self.filter_by_classtype('The Defect'), "table5")
            self.create_table(self.tab6, self.filter_by_classtype('The Watcher'), "table6")

            self.create_table(self.tab1, self.products, "table1")
            self.create_inventory(self.tab2)

            self.tab1_layout = self.get_or_create_layout(self.tab1)
            self.tab2_layout = self.get_or_create_layout(self.tab2)

            remove_button_tab1 = QPushButton("Remove?")
            remove_button_tab1.clicked.connect(self.remove_from_tab1)
            remove_button_tab2 = QPushButton("Remove?")
            remove_button_tab2.clicked.connect(self.remove_from_inventory)

            self.tab1_layout.addWidget(remove_button_tab1)
            self.tab2_layout.addWidget(remove_button_tab2)
            
                                           
            self.view_button_tab1 = QPushButton("View?")
            self.view_button_tab1.clicked.connect(self.view_selected_cards)
            self.view_button_tab2 = QPushButton("View?")
            self.view_button_tab2.clicked.connect(self.view_selected_inventory)

            self.add_card_button = QPushButton("Add Card")
            self.add_card_button.clicked.connect(self.open_add_card_dialog)
            self.tab1.layout().addWidget(self.add_card_button)

            self.add_view_to_tab(self.tab1, self.view_button_tab1)
            self.add_view_to_tab(self.tab2, self.view_button_tab2)
        
            self.layout.addWidget(self.tabs)
            self.setLayout(self.layout)
            self.populate_cards_table()

            self.current_view_dialog = None


        def get_or_create_layout(self, tab):
            layout = tab.layout()
            if layout is None:
                layout = QVBoxLayout(tab)
                tab.setLayout(layout)
            return layout


        def remove_from_tab1(self): # funktion för remove knappen i tab1
            selected_indexes = list(set(index.row() for index in self.table1.selectedIndexes()))
            
            if selected_indexes:
                for row in reversed(selected_indexes):
                    removed_card = self.products[row]
                    print(f"Removing card from Cards: {removed_card['name']}")
                    
                    self.products.pop(row)
                    print(f"card removed: {removed_card['name']}")
                
                self.populate_cards_table()

                self.update_csv()


        def update_csv(self):
            with open('cards.csv', mode='w', newline='') as file:                    
                writer = csv.DictWriter(file, fieldnames=['id', 'name', 'type', 'desc', 'energy', 'classtype'])

                writer.writeheader()

                for product in self.products:
                    writer.writerow(product)
                
            print("csv file updated")
           
        
        def populate_cards_table(self):
            self.table1.clearContents()
            self.table1.setRowCount(len(self.products))

            for row, product in enumerate(self.products):
                self.table1.setItem(row, 0, QTableWidgetItem(str(row + 1)))
                self.table1.setItem(row, 1, QTableWidgetItem(product['name']))
                self.table1.setItem(row, 2, QTableWidgetItem(product['type']))
                self.table1.setItem(row, 3, QTableWidgetItem(product['desc']))
                self.table1.setItem(row, 4, QTableWidgetItem(str(product['energy'])))
                self.table1.setItem(row, 5, QTableWidgetItem(product['classtype']))
            
            tab_layout = self.tab1.layout()
            if tab_layout is None:
                tab_layout = QVBoxLayout(self.tab1)
            
            if not tab_layout.indexof(self.table1):
                tab_layout.addWidget(self.table1)

            


        


        def remove_from_inventory(self): # funktion för "remove" knappen
            
            selected_rows = list(set(index.row() for index in self.inventory_table.selectedIndexes()))

            if selected_rows:
                for row in reversed(selected_rows):
                    removed_card = self.inventory.pop(row)
                    print(f"Removed card from inventory: {removed_card['name']}")

                print(f"Updated Inventory: {self.inventory}")  
                self.populate_inventory_table()
                


        
        def open_add_card_dialog(self): # funktion för att öppna "addcarddialog" klassen, aka fönstret för att skapa nytt kort
            dialog = AddCardDialog(self)
            dialog.exec_()


        def add_card_to_csv(self, new_card): # funktion för att lägga till kort i csv filen
            next_id = max([product['id'] for product in self.products], default=0) + 1
            new_card['id'] = next_id

            self.products.append(new_card)

            with open('cards.csv', 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['id', 'name', 'type', 'desc', 'energy', 'classtype'])
                writer.writerow(new_card)

            print(f"Added card: {new_card['name']} to CSV!")


            self.create_table(self.tab1, self.products, "table1")

        def add_view_to_tab(self, tab, view_button): # funktion för att lägga till "view" knapp till både inventory och cards tab

            tab_layout = tab.layout() if tab.layout() else QVBoxLayout(tab)
            tab_layout.addWidget(view_button)
            tab.setLayout(tab_layout)
        
        
        def view_selected_cards(self): # funktion för att veta vilket kort som "view" ska visa 
            selected_indexes = self.table1.selectedIndexes()

            if selected_indexes:
                row = selected_indexes[0].row()
                card = {
                    "id": int(self.table1.item(row, 0).text()),
                    "name": self.table1.item(row, 1).text(),
                    "type": self.table1.item(row, 2).text(),
                    "desc": self.table1.item(row, 3).text(),
                    "energy": int(self.table1.item(row, 4).text()),
                    "classtype": self.table1.item(row, 5).text()
                }
                self.current_view_dialog = ViewCard(card)
                self.current_view_dialog.finished.connect(self.reset_dialog_reference)
                self.current_view_dialog.exec_()
            else:
                print("card 0")


        def view_selected_inventory(self):
            selected_indexes = self.inventory_table.selectedIndexes()
            if selected_indexes:
                row = selected_indexes[0].row()
                card = {
                    "id": int(self.inventory_table.item(row, 0).text()),
                    "name": self.inventory_table.item(row, 1).text(),
                    "type": self.inventory_table.item(row, 2).text(),
                    "desc": self.inventory_table.item(row, 3).text(),
                    "energy": int(self.inventory_table.item(row, 4).text()),
                    "classtype": self.inventory_table.item(row, 5).text()
                }
                self.current_view_dialog = ViewCard(card)
                self.current_view_dialog.finished.connect(self.reset_dialog_reference)
                self.current_view_dialog.exec_()
            else:
                print("card 0")

        def create_card_from_table(self, table, row): # backup, använde innan men behövs inte längre. har kvar den ändå
            return {
                    "id": int(table.item(row, 0).text()),
                    "name": table.item(row, 1).text(),
                    "type": table.item(row, 2).text(),
                    "desc": table.item(row, 3).text(),
                    "energy": int(table.item(row, 4).text()),
                    "classtype": table.item(row, 5).text()
            }
    
        def reset_dialog_reference(self): # reset dialog för om window poppar upp två gånger när man trycker på "view", WIP
            self.current_view_dialog = None

        
        def show_error(self, title, message): # ska visa en error när något händer med "view" fönstret
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText(message)
            error_dialog.setWindowTitle(title)
            error_dialog.exec_()

        def filter_by_classtype(self, classtype): # filtrerar korten av "classtype"
            
            return [product for product in self.products if product['classtype'] == classtype]
        
        
        def create_table(self, tab, products, table_name): # skapar main lista i gränssnittet
            
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


        def create_inventory(self, tab2): # skapar inventory tab
    
            self.inventory_table = QTableWidget(len(self.inventory), 6)
            self.inventory_table.setHorizontalHeaderLabels(["#", "Name", "Type", "Description", "Energy", "Classtype"])

   
            print(f"Initial Inventory: {self.inventory}")

   
            self.populate_inventory_table()

    
            inventory_layout = QVBoxLayout()
            inventory_layout.addWidget(self.inventory_table)

            
            

            tab2.setLayout(inventory_layout)


        def add_to_inventory(self): # funktion för "add to inventory" knappen
           
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

        

        def populate_cards_table(self):
            self.table1.clearContents()
            self.table1.setRowCount(len(self.products))

            for row, product in enumerate(self.products):
                self.table1.setItem(row, 0, QTableWidgetItem(str(row +1 )))
                self.table1.setItem(row, 1, QTableWidgetItem(product['name']))
                self.table1.setItem(row, 2, QTableWidgetItem(product['type']))
                self.table1.setItem(row, 3, QTableWidgetItem(product['desc']))
                self.table1.setItem(row, 4, QTableWidgetItem(str(product['energy'])))
                self.table1.setItem(row, 5, QTableWidgetItem(product['classtype']))




        def populate_inventory_table(self): # funktion för att reload inventory när du lägger till
            
            
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

            self.inventory_table.viewport().update()   

if __name__ == "__main__":
    window = App()
    sys.exit(app.exec_())
