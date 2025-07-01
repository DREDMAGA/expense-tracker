from datetime import datetime
import sqlite3
import csv


class ExpenseTracker:

    def export_to_csv(self, filename="expenses.csv"):
        expenses = self.get_expenses()
        if not expenses:
            print("Нет данных для экспорта.")
            return

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["amount", "category", "date"])
            writer.writeheader()
            writer.writerows(expenses)

        print(f"✅ Данные экспортированы в файл {filename}")

    def __init__(self):
        self.conn = sqlite3.connect('expenses.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        amount REAL NOT NULL,
                        category TEXT NOT NULL,
                        date TEXT NOT NULL
                    )
                ''')
        self.conn.commit()

    def add_expense(self, amount, category):
        """
        Добавляет новый расход в список.

        """
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount должен быть числом больше 0.")
        if not isinstance(category, str) or not category.strip():
            raise ValueError("Category должна быть непустой строкой.")

        date = datetime.now().date().isoformat()
        self.cursor.execute(
            "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
            (float(amount), category.strip(), date)
        )
        self.conn.commit()

    def get_expenses(self):
        self.cursor.execute("SELECT amount, category, date FROM expenses")
        rows = self.cursor.fetchall()

        expenses = []
        for amount, category, date in rows:
            expenses.append({
                "amount": amount,
                "category": category,
                "date": date
            })
        return expenses

    def get_total(self):
        self.cursor.execute("SELECT SUM(amount) FROM expenses")
        result = self.cursor.fetchone()[0]
        return result if result is not None else 0

    def __repr__(self):
        expenses = self.get_expenses()
        return f"<ExpenseTracker: {len(expenses)} расходов, итого {self.get_total():.2f}>"

    def print_expenses(self):
        expenses = self.get_expenses()
        if not expenses:
            print("Расходы отсутствуют")
            return
        for expense in expenses:
            print(f"{expense['date']} | {expense['category']:<10} | {expense['amount']:.2f}")

    def close(self):
        self.conn.close()

tracker = ExpenseTracker()
tracker.add_expense(12.5, "еда")
tracker.add_expense(7.0, "транспорт")

# Экспорт в CSV
tracker.export_to_csv()
tracker.close()
