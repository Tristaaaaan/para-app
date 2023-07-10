import sqlite3


class Database:
    def __init__(self):
        self.data_con = sqlite3.connect('fares.db')
        self.fare = self.data_con.cursor()
        self.create_database()

    def create_database(self):
        """Create expense table"""
        self.fare.execute(
            "CREATE TABLE IF NOT EXISTS history( \
                id integer PRIMARY KEY AUTOINCREMENT, \
                starting_place varchar(55) NOT NULL, \
                destination varchar(55) NOT NULL, \
                quantity integer NOT NULL, \
                minimum_fare integer NOT NULL, \
                distance integer NOT NULL, \
                total integer NOT NULL, \
                status varchar(20) NOT NULL, \
                date varchar(50) \
                ) \
        ")
        self.data_con.commit()

    def createFareInfo(self, starting_place, destination, minimum_fare, quantity, distance, total, status, date):
        """Create an expense"""
        self.fare.execute(
            "INSERT INTO history(starting_place, destination, distance, total, status, minimum_fare, quantity, date) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (starting_place, destination, distance, total, status, minimum_fare, quantity, date,))
        self.data_con.commit()

        # Obtaining the last item to insert in the list on the application
        select_expense = self.fare.execute(
            "SELECT * FROM history WHERE total = ?", (total,)).fetchall()

        return select_expense[-1]

    def all_data(self):
        history_data = self.fare.execute(
            "SELECT * FROM history").fetchall()

        return history_data

    def delete_expense(self, prim_key):
        """Delete a task"""
        self.fare.execute("DELETE FROM history WHERE id=?", (prim_key,))

        self.data_con.commit()

    def close_db_connection(self):
        self.data_con.close()
