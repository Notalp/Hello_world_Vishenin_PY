import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
import numpy as np

# ==============================================================================
# 1. ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ nastya (порт 5434)
# ==============================================================================

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5434",
        user="nastya",
        password="example",
        database="nastya"
    )
    print("✓ Подключение к БД установлено")

    # --- 1.1 Данные о товарах и ценах ---
    df_products_prices = pd.read_sql("""
        SELECT 
            pr.name AS product_name,
            pr.category,
            p.price,
            p.created_at
        FROM products pr
        JOIN prices p ON pr.id = p.product_id
        ORDER BY pr.category, pr.name;
    """, connection)

    # --- 1.2 Статистика по категориям (средняя цена, количество) ---
    df_category_stats = pd.read_sql("""
        SELECT 
            pr.category,
            COUNT(p.id) AS price_count,
            ROUND(AVG(p.price)::numeric, 2) AS avg_price,
            ROUND(MIN(p.price)::numeric, 2) AS min_price,
            ROUND(MAX(p.price)::numeric, 2) AS max_price,
            ROUND(STDDEV(p.price)::numeric, 2) AS std_price
        FROM products pr
        JOIN prices p ON pr.id = p.product_id
        GROUP BY pr.category
        ORDER BY avg_price DESC;
    """, connection)

    # --- 1.3 Количество товаров по категориям ---
    df_products_by_category = pd.read_sql("""
        SELECT 
            category,
            COUNT(id) AS product_count
        FROM products
        GROUP BY category
        ORDER BY product_count DESC;
    """, connection)

    # --- 1.4 Товары без цен (аномалия) ---
    df_missing_prices = pd.read_sql("""
        SELECT 
            pr.name AS product_name,
            pr.category
        FROM products pr
        LEFT JOIN prices p ON pr.id = p.product_id
        WHERE p.id IS NULL
        ORDER BY pr.category, pr.name;
    """, connection)

    # --- 1.5 Поставщики по категориям ---
    df_suppliers_by_category = pd.read_sql("""
        SELECT 
            pr.category,
            COUNT(s.id) AS supplier_count
        FROM products pr
        JOIN suppliers s ON pr.id = s.product_id
        GROUP BY pr.category
        ORDER BY supplier_count DESC;
    """, connection)

    print(f"✓ Загружено записей о ценах: {len(df_products_prices)}")
    print(f"✓ Уникальных товаров: {df_products_prices['product_name'].nunique()}")
    print(f"✓ Уникальных категорий: {df_products_prices['category'].nunique()}")
    print(f"✓ Товаров без цен (аномалия): {len(df_missing_prices)}")

except Exception as error:
    print(f"❌ Ошибка подключения: {error}")
    raise SystemExit

finally:
    if 'connection' in locals():
        connection.close()
        print("✓ Соединение закрыто\n")

# ==============================================================================
# 2. ПОДГОТОВКА ДАННЫХ ДЛЯ ГРАФИКОВ
# ==============================================================================

# Объединяем данные для графика 2 (чтобы категории совпадали)
df_combined = df_category_stats[['category', 'price_count']].merge(
    df_suppliers_by_category[['category', 'supplier_count']],
    on='category',
    how='outer'
).fillna(0)

# Сортируем по средней цене (как в графике 1)
df_combined = df_combined.merge(
    df_category_stats[['category', 'avg_price']],
    on='category'
).sort_values('avg_price', ascending=False)

# Расчёт общей статистики по ценам
all_prices = df_products_prices['price']
mean_price = all_prices.mean()
median_price = all_prices.median()
std_price = all_prices.std()
q1_price = all_prices.quantile(0.25)
q3_price = all_prices.quantile(0.75)
iqr_price = q3_price - q1_price

# Выбросы по методу 1.5 * IQR
lower_fence = q1_price - 1.5 * iqr_price
upper_fence = q3_price + 1.5 * iqr_price
outliers = all_prices[(all_prices < lower_fence) | (all_prices > upper_fence)]

# Цветовая схема для столбцов средней цены
category_mean_global = df_category_stats['avg_price'].mean()
bar_colors = ["#d9534f" if g < category_mean_global else "#4a90d9"
              for g in df_category_stats['avg_price']]

# ==============================================================================
# 3. ПОСТРОЕНИЕ ГРАФИКОВ
# ==============================================================================

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
})

fig = plt.figure(figsize=(15, 12))
fig.suptitle("📊 Анализ товаров, цен и поставщиков",   # ← УБРАНО "база данных nastya"
             fontsize=16, fontweight="bold")

gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.35)

# ============================================================
# ГРАФИК 1: Средняя цена по категориям
# ============================================================
ax1 = fig.add_subplot(gs[0, 0])

bars1 = ax1.barh(df_category_stats['category'], df_category_stats['avg_price'],
                  color=bar_colors, edgecolor="white", height=0.65)

for bar, val in zip(bars1, df_category_stats['avg_price']):
    ax1.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
             f"{val:,.0f} руб.", va="center", fontsize=9)

ax1.axvline(category_mean_global, color="darkorange", linestyle="--", linewidth=1.5,
            label=f"Среднее по категориям: {category_mean_global:,.0f} руб.")
ax1.set_xlabel("Средняя цена (руб.)")
ax1.set_title("💰 Средняя цена по категориям товаров", fontweight="bold")
ax1.legend(handles=[
    Patch(facecolor="#4a90d9", label="Выше или равно среднему"),
    Patch(facecolor="#d9534f", label="Ниже среднего")
], fontsize=8, loc="lower right")

# ============================================================
# ГРАФИК 2: Количество цен и поставщиков по категориям
# ============================================================
ax2 = fig.add_subplot(gs[0, 1])

x = np.arange(len(df_combined['category']))
width = 0.35

bars_prices = ax2.bar(x - width/2, df_combined['price_count'], width,
                      label='Количество цен', color="#5cb85c", edgecolor="white")
bars_suppliers = ax2.bar(x + width/2, df_combined['supplier_count'], width,
                          label='Количество поставщиков', color="#f0ad4e", edgecolor="white")

for bar in bars_prices:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             str(int(bar.get_height())), ha="center", fontsize=8)
for bar in bars_suppliers:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             str(int(bar.get_height())), ha="center", fontsize=8)

ax2.set_xticks(x)
ax2.set_xticklabels(df_combined['category'], rotation=40, ha="right", fontsize=8)
ax2.set_ylabel("Количество")
ax2.set_title("📦 Количество цен и поставщиков по категориям", fontweight="bold")
ax2.legend(fontsize=8)
ax2.grid(axis="y", alpha=0.3)

# ============================================================
# ГРАФИК 3: Распределение цен
# ============================================================
ax3 = fig.add_subplot(gs[1, 0])

ax3.hist(all_prices, bins=20, color="#f0ad4e", edgecolor="white", alpha=0.7)

ax3.axvline(median_price, color="crimson", linestyle="--", linewidth=1.8,
            label=f"Медиана: {median_price:,.0f} руб.")
ax3.axvline(mean_price, color="#2a9d8f", linestyle=":", linewidth=1.8,
            label=f"Среднее: {mean_price:,.0f} руб.")
ax3.axvline(q1_price, color="#4a90d9", linestyle=":", linewidth=1.2, alpha=0.7,
            label=f"Q1: {q1_price:,.0f} руб.")
ax3.axvline(q3_price, color="#4a90d9", linestyle=":", linewidth=1.2, alpha=0.7,
            label=f"Q3: {q3_price:,.0f} руб.")

ax3.set_xlabel("Цена (руб.)")
ax3.set_ylabel("Количество записей")
ax3.set_title("📈 Распределение цен на товары", fontweight="bold")
ax3.legend(fontsize=8)

stats_text = (f"n = {len(all_prices)}\n"
              f"Среднее = {mean_price:,.0f} руб.\n"
              f"Медиана = {median_price:,.0f} руб.\n"
              f"Q1 = {q1_price:,.0f} руб.\n"
              f"Q3 = {q3_price:,.0f} руб.\n"
              f"IQR = {iqr_price:,.0f} руб.\n"
              f"σ = {std_price:,.0f} руб.")
ax3.text(0.97, 0.95, stats_text, transform=ax3.transAxes,
         va="top", ha="right", fontsize=7,
         bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", edgecolor="lightgray"))

if len(outliers) > 0:
    ax3.annotate(f"⚠️ Выбросы:\n{len(outliers)} значений",
                 xy=(0.02, 0.95), xycoords='axes fraction',
                 fontsize=8, color="#d9534f",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#d9534f"))

# ============================================================
# ГРАФИК 4: Круговая диаграмма
# ============================================================
ax4 = fig.add_subplot(gs[1, 1])

pie_colors = ["#7b68ee", "#4a90d9", "#2ecc71", "#f0ad4e", "#d9534f", "#5bc0de"]
pie_labels = [f"{row.category}\n({row.product_count} шт.)"
              for _, row in df_products_by_category.iterrows()]

wedges, texts, autotexts = ax4.pie(
    df_products_by_category['product_count'],
    labels=None,
    autopct="%1.0f%%",
    colors=pie_colors[:len(df_products_by_category)],
    startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    pctdistance=0.7
)

for autotext in autotexts:
    autotext.set_fontsize(9)
    autotext.set_fontweight("bold")

ax4.set_title("📊 Товары по категориям", fontweight="bold")
ax4.legend(wedges, pie_labels, loc="lower center", bbox_to_anchor=(0.5, -0.15),
           fontsize=8, frameon=False)

# ==============================================================================
# 4. ВЫВОД АНОМАЛИЙ
# ==============================================================================

anomaly_text = ""
if len(df_missing_prices) > 0:
    anomaly_text = (f"⚠️ АНОМАЛИЯ: {len(df_missing_prices)} товаров не имеют цен! "
                    f"Примеры: {', '.join(df_missing_prices['product_name'].head(3).tolist())}")
elif len(outliers) > 0:
    anomaly_text = (f"⚠️ АНОМАЛИЯ: Обнаружено {len(outliers)} выбросов в ценах "
                    f"(за пределами ±1.5×IQR от Q1/Q3)")
else:
    anomaly_text = "✅ Аномалий не обнаружено: все товары имеют цены, выбросов нет"

fig.text(0.5, -0.02, anomaly_text, ha="center", fontsize=9,
         color="#8b0000" if (len(df_missing_prices) > 0 or len(outliers) > 0) else "#2ecc71",
         bbox=dict(boxstyle="round,pad=0.4",
                   facecolor="#fff3f3" if (len(df_missing_prices) > 0 or len(outliers) > 0) else "#f0fff0",
                   edgecolor="#d9534f" if (len(df_missing_prices) > 0 or len(outliers) > 0) else "#2ecc71"))

plt.tight_layout()
OUTPUT_FILE = "task_7_analysis_products_prices.png"
plt.savefig(OUTPUT_FILE, bbox_inches="tight", dpi=150)
print(f"\n✓ График сохранён: {OUTPUT_FILE}")
plt.show()

# ==============================================================================
# 5. ВЫВОДЫ ПО ГРАФИКАМ
# ==============================================================================

print("\n" + "="*60)
print("📌 ВЫВОДЫ ПО ГРАФИКАМ")
print("="*60)

print("\n📊 ГРАФИК 1 — Средняя цена по категориям:")
print(f"   • Самая дорогая категория: '{df_category_stats.iloc[0]['category']}' "
      f"({df_category_stats.iloc[0]['avg_price']:,.0f} руб.)")
print(f"   • Самая дешёвая категория: '{df_category_stats.iloc[-1]['category']}' "
      f"({df_category_stats.iloc[-1]['avg_price']:,.0f} руб.)")
print(f"   • Общая средняя цена по категориям: {category_mean_global:,.0f} руб.")

print("\n📊 ГРАФИК 2 — Количество цен и поставщиков по категориям:")
print("   • Данные объединены по всем категориям")

print("\n📊 ГРАФИК 3 — Распределение цен:")
print(f"   • Всего цен: {len(all_prices)}")
print(f"   • Средняя цена: {mean_price:,.0f} руб.")
print(f"   • Медиана: {median_price:,.0f} руб.")
print(f"   • Стандартное отклонение: {std_price:,.0f} руб.")
print(f"   • IQR: {iqr_price:,.0f} руб.")
print(f"   • Выбросов: {len(outliers)}")
if mean_price > median_price:
    print("   • Среднее > медианы → распределение скошено вправо (есть дорогие товары)")

print("\n📊 ГРАФИК 4 — Товары по категориям:")
total_products = df_products_by_category['product_count'].sum()
for _, row in df_products_by_category.iterrows():
    pct = row['product_count'] / total_products * 100
    print(f"   • {row['category']}: {row['product_count']} товаров ({pct:.0f}%)")

print("\n" + "="*60)
print("⚠️ АНОМАЛИИ В ДАННЫХ")
print("="*60)

if len(df_missing_prices) > 0:
    print(f"\n   • ТОВАРЫ БЕЗ ЦЕН: {len(df_missing_prices)} шт.")
    print(f"     Список: {', '.join(df_missing_prices['product_name'].tolist()[:5])}")
else:
    print("\n   • ✅ Все товары имеют хотя бы одну цену.")

if len(outliers) > 0:
    print(f"\n   • ЦЕНОВЫЕ ВЫБРОСЫ: {len(outliers)} значений")
    print(f"     Границы: {lower_fence:.0f} — {upper_fence:.0f} руб.")
else:
    print("\n   • ✅ Ценовых выбросов не обнаружено.")

print("\n" + "="*60)
print("✅ Анализ завершён.")