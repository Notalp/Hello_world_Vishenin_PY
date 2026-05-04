import psycopg2

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="example",
        database="testdb"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT version();")

    result = cursor.fetchall()
    for row in result:
        print(row)

    cursor.close()
    connection.close()

except Exception as error:
    print(f"Произошла ошибка: {error}")