import psycopg2
import pandas as pd

try:
    # Подключение к контейнеру PostgreSQL
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="example",
        database="testdb"
    )
    print("✓ Подключение установлено\n")

    # 2. JOIN таблиц prices и products, загрузка в DataFrame
    query = """
    SELECT 
        p.product_id,
        pr.name AS product_name,
        pr.category,
        p.price,
        p.created_at AS date
    FROM prices p
    JOIN products pr ON p.product_id = pr.product_id
    ORDER BY pr.category, pr.name, p.created_at;
    """

    df = pd.read_sql(query, connection)

    print(f"Загружено записей: {len(df)}")
    print(df.head(), "\n")

    # 3. Основные статистики по цене
    print("=== Пункт 3. Основные статистики ===")
    print(f"Средняя цена: {df['price'].mean():.2f} руб.")
    print(f"Медианная цена: {df['price'].median():.2f} руб.")
    print(f"Стандартное отклонение: {df['price'].std():.2f} руб.")
    print(f"Минимальная цена: {df['price'].min():.2f} руб.")
    print(f"Максимальная цена: {df['price'].max():.2f} руб.\n")

    # 4. Квартили, IQR и товары с ценой выше Q3
    q1 = df['price'].quantile(0.25)
    q2 = df['price'].quantile(0.50)
    q3 = df['price'].quantile(0.75)
    iqr = q3 - q1

    print("=== Пункт 4. Квартили и IQR ===")
    print(f"Q1 (25%): {q1:.2f} руб.")
    print(f"Q2 (50%): {q2:.2f} руб.")
    print(f"Q3 (75%): {q3:.2f} руб.")
    print(f"IQR (Q3 - Q1): {iqr:.2f} руб.\n")

    # Товары с ценой выше Q3
    expensive = df[df['price'] > q3][['product_name', 'category', 'price']]
    print("Товары с ценой выше Q3:")
    if not expensive.empty:
        print(expensive.to_string(index=False))
    else:
        print("Нет таких товаров.")
    print()

    # 5. Группировка по категориям
    print("=== Пункт 5. Статистика по категориям ===")
    category_stats = df.groupby('category')['price'].agg(
        count='count',
        mean='mean',
        median='median',
        std='std'
    ).round(2).sort_values('mean', ascending=False)

    print(category_stats.to_string())
    print()

    # 6. Разброс цен по товарам
    print("=== Пункт 6. Товары с наибольшим разбросом цен ===")
    price_span = df.groupby('product_name')['price'].agg(
        min_price='min',
        max_price='max'
    )
    price_span['span'] = price_span['max_price'] - price_span['min_price']
    top5 = price_span.sort_values('span', ascending=False).head(5)

    print(top5.to_string())

except Exception as error:
    print(f"Ошибка: {error}")

finally:
    if 'connection' in locals() and connection:
        connection.close()
        print("\nСоединение закрыто.")