import psycopg2


class Database:
    def __init__(self):
        # Connection details
        hostname = "silly.db.elephantsql.com"
        port = 5432
        database = "ejimkndj"
        username = "ejimkndj"
        password = "gcHA1CYttWXBR6ZKCyCCr6Y8i7mMvFR-"

        # Create a connection
        self.data_con = psycopg2.connect(
            host=hostname,
            port=port,
            database=database,
            user=username,
            password=password
        )

        self.fare = self.data_con.cursor()
        self.create_database()

    def create_database(self):
        """Create expense table"""
        self.fare.execute(
            "CREATE TABLE IF NOT EXISTS history( \
                id SERIAL PRIMARY KEY, \
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
            "INSERT INTO history(starting_place, destination, distance, total, status, minimum_fare, quantity, date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (starting_place, destination, distance, total, status, minimum_fare, quantity, date,))
        self.data_con.commit()

    def all_data(self):
        self.fare.execute(
            "SELECT * FROM history")

        history_data = self.fare.fetchall()

        return history_data

    def delete_expense(self, prim_key):
        """Delete a task"""
        self.fare.execute("DELETE FROM history WHERE id=%s", (prim_key,))

        self.data_con.commit()

    def expenses_sum(self):
        """Getting the sum of expenses"""
        self.fare.execute(
            "SELECT sum(total) FROM history")

        spent_sum = self.fare.fetchall()

        expense_sum = sum(res[0] for res in spent_sum)

        return expense_sum

    def close_db_connection(self):
        self.data_con.close()
