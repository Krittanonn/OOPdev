from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.scatter import ScatterPlane
from datetime import datetime
import os
import csv
import matplotlib.pyplot as plt
from kivy.uix.image import Image as KivyImage
from kivy.core.image import Image as CoreImage
from io import BytesIO

resource_add_path(os.path.abspath('.'))
LabelBase.register(name='THSarabunNew', fn_regular='THSarabunNew.ttf')

class MainScreen(Screen):
    # func build
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.layout.size)

        self.layout.bind(size=self._update_rect)

        self.header_label = Label(text='Expense Tracker', font_size='24sp', size_hint_y=None, height=50)
        self.header_label.color = (0, 0, 0, 1)
        self.layout.add_widget(self.header_label)

        self.form_layout = GridLayout(cols=2, row_default_height=40, row_force_default=True, spacing=10, size_hint_y=None)
        self.form_layout.bind(minimum_height=self.form_layout.setter('height'))

        self.form_layout.add_widget(Label(text='Entry Type:', size_hint_y=None, height=40, color=(0, 0, 0, 1)))
        self.entry_type_input = Spinner(values=('Income', 'Expense'), size_hint_y=None, height=40)
        self.form_layout.add_widget(self.entry_type_input)

        self.form_layout.add_widget(Label(text='Category:', size_hint_y=None, height=40, color=(0, 0, 0, 1)))
        self.category_input = Spinner(values=('Food', 'Transport', 'Utilities', 'Entertainment', 'Others'), size_hint_y=None, height=40)
        self.form_layout.add_widget(self.category_input)

        self.form_layout.add_widget(Label(text='Item Name:', size_hint_y=None, height=40, color=(0, 0, 0, 1)))
        self.item_input = TextInput(multiline=False, font_name='THSarabunNew', size_hint_y=None, height=40)
        self.form_layout.add_widget(self.item_input)

        self.form_layout.add_widget(Label(text='Amount:', size_hint_y=None, height=40, color=(0, 0, 0, 1)))
        self.amount_input = TextInput(multiline=False, input_filter='float', size_hint_y=None, height=40)
        self.form_layout.add_widget(self.amount_input)

        self.layout.add_widget(self.form_layout)

        self.button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.submit_button = Button(text='Add Entry', size_hint_x=0.5, background_color=(0.2, 0.8, 0.2, 1))
        self.submit_button.bind(on_press=self.add_entry)
        self.button_layout.add_widget(self.submit_button)

        self.clear_button = Button(text='Clear', size_hint_x=0.5, background_color=(0.8, 0.2, 0.2, 1))
        self.clear_button.bind(on_press=self.clear_fields)
        self.button_layout.add_widget(self.clear_button)

        self.layout.add_widget(self.button_layout)

        self.filter_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.filter_label = Label(text='Filter by Category:', size_hint_x=None, width=150, color=(0, 0, 0, 1))
        self.filter_layout.add_widget(self.filter_label)

        self.filter_spinner = Spinner(values=('All', 'Food', 'Transport', 'Utilities', 'Entertainment', 'Others', 'Income'), size_hint_x=None, width=150)
        self.filter_spinner.bind(text=self.filter_entries)
        self.filter_layout.add_widget(self.filter_spinner)

        self.layout.add_widget(self.filter_layout)

        self.scroll_view = ScrollView(size_hint=(1, 0.5))
        self.grid = GridLayout(cols=2, spacing=5, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll_view.add_widget(self.grid)
        self.layout.add_widget(self.scroll_view)

        self.total_income_label = Label(text='Total Income: 0.00 THB.', size_hint_y=None, height=40, color=(0, 0, 0, 1))
        self.layout.add_widget(self.total_income_label)

        self.total_expense_label = Label(text='Total Expense: 0.00 THB.', size_hint_y=None, height=40, color=(0, 0, 0, 1))
        self.layout.add_widget(self.total_expense_label)

        self.compare_button = Button(text='Compare Expenses', size_hint_y=None, height=50, background_color=(0.1, 0.5, 0.8, 1))
        self.compare_button.bind(on_press=self.switch_to_comparison)
        self.layout.add_widget(self.compare_button)

        self.load_entries()

        self.add_widget(self.layout)

    # func _update_rect 
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    # func add_entry
    def add_entry(self, instance):
        entry_type = self.entry_type_input.text
        category = self.category_input.text
        item_name = self.item_input.text
        amount = self.amount_input.text
        date = str(datetime.now().date())

        if item_name and amount:
            entry_label = f"{date} | {entry_type} | {category} | {item_name} | {amount} THB."
            label = Label(text=entry_label, font_name='THSarabunNew', size_hint_y=None, height=40, size_hint_x=0.8, color=(0, 0, 0, 1))
            delete_button = Button(
                text="Delete", 
                size_hint=(None, None), 
                size=(60, 40),
                background_color=(1, 0, 0, 1)
            )
            delete_button.bind(on_press=lambda btn: self.delete_entry(label, delete_button, date, entry_type, category, item_name, amount))
            
            self.grid.add_widget(label, index=0)
            self.grid.add_widget(delete_button, index=0)

            self.save_to_csv(date, entry_type, category, item_name, amount)

            self.item_input.text = ''
            self.amount_input.text = ''

            self.update_totals()

            print(f"Added new entry: {entry_label}")


    def clear_fields(self, instance):
        self.item_input.text = ''
        self.amount_input.text = ''
        self.category_input.text = 'Food'
        self.entry_type_input.text = 'Income'
        self.filter_spinner.text = 'All'

    def save_to_csv(self, date, entry_type, category, item_name, amount):
        filename = "expenses.csv"
        file_exists = os.path.isfile(filename)

        with open(filename, mode='a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Date', 'Entry Type', 'Category', 'Item Name', 'Amount'])
            writer.writerow([date, entry_type, category, item_name, amount])

    def load_entries(self):
        self.grid.clear_widgets()
        filename = "expenses.csv"
        if os.path.isfile(filename):
            with open(filename, mode='r', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                entries = list(reader)

                if entries:
                    print(f"Found {len(entries) - 1} entries in CSV")
                    for entry in reversed(entries[1:]):
                        if entry and len(entry) == 5:
                            date, entry_type, category, item_name, amount = entry
                            entry_label = f"{date} | {entry_type} | {category} | {item_name} | {amount} THB."
                            label = Label(text=entry_label, font_name='THSarabunNew', size_hint_y=None, height=40, size_hint_x=0.8, color=(0, 0, 0, 1))
                            delete_button = Button(
                                text="Delete", 
                                size_hint=(None, None), 
                                size=(60, 40),
                                background_color=(1, 0, 0, 1)
                            )
                            delete_button.bind(on_press=lambda btn, l=label, d=delete_button, dt=date, et=entry_type, c=category, i=item_name, a=amount: self.delete_entry(l, d, dt, et, c, i, a))
                            
                            self.grid.add_widget(label)
                            self.grid.add_widget(delete_button)
                            print(f"Loaded entry: {entry_label}")
                        else:
                            print(f"Skipped invalid entry: {entry}")
                else:
                    print("No entries found in CSV")
        else:
            print(f"CSV file not found: {filename}")

        self.update_totals()

    def delete_entry(self, label, delete_button, date, entry_type, category, item_name, amount):
        self.grid.remove_widget(label)
        self.grid.remove_widget(delete_button)

        self.remove_from_csv(date, entry_type, category, item_name, amount)

        self.update_totals()

    def remove_from_csv(self, date, entry_type, category, item_name, amount):
        filename = "expenses.csv"
        temp_filename = "temp_expenses.csv"

        with open(filename, 'r', newline='', encoding='utf-8') as csvfile, \
             open(temp_filename, 'w', newline='', encoding='utf-8') as temp_csvfile:
            reader = csv.reader(csvfile)
            writer = csv.writer(temp_csvfile)

            for row in reader:
                if row != [date, entry_type, category, item_name, amount]:
                    writer.writerow(row)

        os.remove(filename)
        os.rename(temp_filename, filename)

    def filter_entries(self, spinner, text):
        print(f"Filtering entries by: {text}")
        self.load_entries()

        filtered_entries = []
        for label, button in zip(self.grid.children[1::2], self.grid.children[::2]):
            entry_text = label.text
            if text == 'All' or \
            (text == 'Others' and all(category not in entry_text for category in ['Food', 'Transport', 'Utilities', 'Entertainment']) and 'Income' not in entry_text) or \
            (text == 'Income' and 'Income' in entry_text) or \
            (text in entry_text):
                filtered_entries.append((label, button))

        self.grid.clear_widgets()
        for label, button in reversed(filtered_entries):
            self.grid.add_widget(label)
            self.grid.add_widget(button)

        print(f"Filtered entries count: {len(filtered_entries)}")

        self.update_totals(text)

    def update_totals(self, filter_category=None):
        filename = "expenses.csv"
        total_income = 0.0
        total_expense = 0.0

        if os.path.isfile(filename):
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)

                for row in reader:
                    entry_type = row[1]
                    category = row[2]
                    amount = float(row[4])

                    if filter_category == 'Others':
                        if entry_type == 'Expense' and category not in ['Food', 'Transport', 'Utilities', 'Entertainment']:
                            total_expense += amount
                    elif filter_category == 'Income' and entry_type == 'Income':
                        total_income += amount
                    elif filter_category == category or filter_category == 'All' or filter_category is None:
                        if entry_type == 'Income':
                            total_income += amount
                        elif entry_type == 'Expense':
                            total_expense += amount

        self.total_income_label.text = f"Total Income: {total_income:.2f} THB."
        self.total_expense_label.text = f"Total Expense: {total_expense:.2f} THB."

    def switch_to_comparison(self, instance):
        self.manager.current = 'comparison_screen'

class ComparisonScreen(Screen):                                                                                                                               
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.layout.size)

        self.layout.bind(size=self._update_rect)

        self.header_label = Label(text='Expense Comparison', font_size='24sp', size_hint_y=None, height=50)
        self.header_label.color = (0, 0, 0, 1)
        self.layout.add_widget(self.header_label)

        self.date_layout_1 = GridLayout(cols=2, row_default_height=40, row_force_default=True, spacing=10, size_hint_y=None)
        self.date_layout_1.bind(minimum_height=self.date_layout_1.setter('height'))

        self.date_layout_1.add_widget(Label(text='Start Date Period 1 (YYYY-MM-DD):', size_hint_y=None, height=40, color=(0, 0, 0, 1)))
        self.start_date_input_1 = TextInput(multiline=False, size_hint_y=None, height=40)
        self.date_layout_1.add_widget(self.start_date_input_1)

        self.date_layout_1.add_widget(Label(text='End Date Period 1 (YYYY-MM-DD):', size_hint_y=None, height=40, color=(0, 0, 0, 1)))
        self.end_date_input_1 = TextInput(multiline=False, size_hint_y=None, height=40)
        self.date_layout_1.add_widget(self.end_date_input_1)

        self.layout.add_widget(self.date_layout_1)

        self.date_layout_2 = GridLayout(cols=2, row_default_height=40, row_force_default=True, spacing=10, size_hint_y=None)
        self.date_layout_2.bind(minimum_height=self.date_layout_2.setter('height'))

        self.date_layout_2.add_widget(Label(text='Start Date Period 2 (YYYY-MM-DD):', size_hint_y=None, height=40, color=(0, 0, 0, 1)))
        self.start_date_input_2 = TextInput(multiline=False, size_hint_y=None, height=40)
        self.date_layout_2.add_widget(self.start_date_input_2)

        self.date_layout_2.add_widget(Label(text='End Date Period 2 (YYYY-MM-DD):', size_hint_y=None, height=40, color=(0, 0, 0, 1)))
        self.end_date_input_2 = TextInput(multiline=False, size_hint_y=None, height=40)
        self.date_layout_2.add_widget(self.end_date_input_2)

        self.layout.add_widget(self.date_layout_2)

        self.compare_button = Button(text='Compare', size_hint_y=None, height=50, background_color=(0.2, 0.8, 0.2, 1))
        self.compare_button.bind(on_press=self.compare_expenses)
        self.layout.add_widget(self.compare_button)

        self.scroll_view = ScrollView(size_hint=(1, 0.5))
        self.grid = GridLayout(cols=1, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll_view.add_widget(self.grid)
        self.layout.add_widget(self.scroll_view)

        self.back_button = Button(text='Back to Main Screen', size_hint_y=None, height=50, background_color=(0.1, 0.5, 0.8, 1))
        self.back_button.bind(on_press=self.switch_to_main)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def compare_expenses(self, instance):
        start_date_1 = self.start_date_input_1.text
        end_date_1 = self.end_date_input_1.text
        start_date_2 = self.start_date_input_2.text
        end_date_2 = self.end_date_input_2.text

        expenses_by_category_1 = self.get_expenses_by_category(start_date_1, end_date_1)
        expenses_by_category_2 = self.get_expenses_by_category(start_date_2, end_date_2)

        self.plot_comparison(expenses_by_category_1, expenses_by_category_2)

    def get_expenses_by_category(self, start_date, end_date):
        filename = "expenses.csv"
        expenses_by_category = {}

        if os.path.isfile(filename):
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)

                for row in reader:
                    date = row[0]
                    entry_type = row[1]
                    category = row[2]
                    amount = float(row[4])

                    if start_date <= date <= end_date and entry_type == 'Expense':
                        if category not in expenses_by_category:
                            expenses_by_category[category] = 0.0
                        expenses_by_category[category] += amount

        return expenses_by_category

    def plot_comparison(self, expenses_1, expenses_2):
        categories = list(set(expenses_1.keys()).union(expenses_2.keys()))
        amounts_1 = [expenses_1.get(category, 0) for category in categories]
        amounts_2 = [expenses_2.get(category, 0) for category in categories]

        fig, ax = plt.subplots(figsize=(16, 12))

        bar_width = 0.35
        index = range(len(categories))

        bar1 = ax.bar(index, amounts_1, bar_width, label='Period 1')
        bar2 = ax.bar([i + bar_width for i in index], amounts_2, bar_width, label='Period 2')

        ax.set_xlabel('Category', fontsize=14)
        ax.set_ylabel('Amount (THB)', fontsize=14)
        ax.set_title('Expense Comparison by Category', fontsize=18)
        ax.set_xticks([i + bar_width / 2 for i in index])
        ax.set_xticklabels(categories, rotation=45, ha='right', fontsize=12)
        ax.legend(fontsize=12)

        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=300)
        buf.seek(0)
        im = CoreImage(buf, ext='png')

        self.grid.clear_widgets()

        graph_image = KivyImage(texture=im.texture, size_hint=(1, None), height=700)
        self.grid.add_widget(graph_image)

        plt.close(fig)

    def switch_to_main(self, instance):
        self.manager.current = 'main_screen'

class ExpenseApp(App):
    def build(self):
        sm = ScreenManager()
        self.main_screen = MainScreen(name='main_screen')
        self.comparison_screen = ComparisonScreen(name='comparison_screen')
        self.main_screen.build()
        self.comparison_screen.build()

        sm.add_widget(self.main_screen)
        sm.add_widget(self.comparison_screen)
        return sm

if __name__ == '__main__':
    ExpenseApp().run()
