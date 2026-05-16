import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
import numpy as np

# ==============================================================================
# 1. ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ И ЗАГРУЗКА ДАННЫХ
# ==============================================================================

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="example",
        database="testdb"
    )
    print("✓ Подключение к БД установлено")

    # --- 1.1 Средний балл и количество сдач по курсам ---
    df_courses = pd.read_sql("""
        SELECT 
            c.course_name AS course,
            ROUND(AVG(e.grade)::numeric, 2) AS avg_grade,
            COUNT(e.enrollment_id) AS total_enrollments,
            STDDEV(e.grade) AS std_grade
        FROM enrollments e
        JOIN courses c ON e.course_id = c.course_id
        GROUP BY c.course_name
        ORDER BY avg_grade DESC
    """, connection)

    # --- 1.2 Студенты по годам поступления (для круговой диаграммы) ---
    df_years = pd.read_sql("""
        SELECT 
            enrollment_year AS year,
            COUNT(student_id) AS students
        FROM students
        GROUP BY enrollment_year
        ORDER BY enrollment_year
    """, connection)

    # --- 1.3 Все оценки (для гистограммы распределения) ---
    df_all = pd.read_sql("SELECT grade FROM enrollments", connection)

    # --- 1.4 Студенты без оценок (аномалия) ---
    df_missing = pd.read_sql("""
        SELECT 
            s.first_name || ' ' || s.last_name AS student,
            s.enrollment_year
        FROM students s
        LEFT JOIN enrollments e ON s.student_id = e.student_id
        WHERE e.enrollment_id IS NULL
        ORDER BY s.enrollment_year, s.last_name
    """, connection)

    print(f"✓ Загружено: {len(df_courses)} курсов, {len(df_all)} оценок")
    print(f"✓ Студентов без оценок: {len(df_missing)}")

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

# Словарь для сокращения длинных названий курсов
NAME_MAP = {
    "Основы программирования на Python": "Python",
    "Алгоритмы и структуры данных": "Алгоритмы",
    "Базы данных и SQL": "SQL",
    "Веб-разработка (Frontend)": "Frontend",
    "Администрирование Linux": "Linux",
    "Математический анализ": "Матанализ",
    "Дискретная математика": "Дискр. мат.",
    "Английский язык для IT": "Английский"
}
df_courses["short_name"] = df_courses["course"].map(NAME_MAP)

# Расчёт общей статистики по оценкам
mean_grade = df_all["grade"].mean()
median_grade = df_all["grade"].median()
std_grade = df_all["grade"].std()
total_grades = len(df_all)

# Цветовая схема для столбцов среднего балла (красный — если ниже среднего)
course_mean = df_courses["avg_grade"].mean()
bar_colors = ["#d9534f" if g < course_mean else "#4a90d9" for g in df_courses["avg_grade"]]

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

fig = plt.figure(figsize=(15, 10))
fig.suptitle("📊 Анализ успеваемости учебной базы данных", fontsize=16, fontweight="bold")

# Сетка 2x2
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)

# ------------------------------------------------------------
# ГРАФИК 1: Средний балл по курсам (горизонтальный bar chart)
# ------------------------------------------------------------
ax1 = fig.add_subplot(gs[0, 0])

bars1 = ax1.barh(df_courses["short_name"], df_courses["avg_grade"],
                  color=bar_colors, edgecolor="white", height=0.65)

# Подписи значений на концах столбцов
for bar, val in zip(bars1, df_courses["avg_grade"]):
    ax1.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
             f"{val:.2f}", va="center", fontsize=9)

ax1.axvline(course_mean, color="darkorange", linestyle="--", linewidth=1.5,
            label=f"Среднее по курсам: {course_mean:.2f}")
ax1.set_xlim(2.5, 5.2)
ax1.set_xlabel("Средний балл")
ax1.set_title("🏆 Средний балл по курсам", fontweight="bold")
ax1.legend(handles=[
    Patch(facecolor="#4a90d9", label="Выше или равно среднему"),
    Patch(facecolor="#d9534f", label="Ниже среднего")
], fontsize=8, loc="lower right")

# ------------------------------------------------------------
# ГРАФИК 2: Количество сдач по курсам (вертикальный bar chart)
# ------------------------------------------------------------
ax2 = fig.add_subplot(gs[0, 1])

bars2 = ax2.bar(df_courses["short_name"], df_courses["total_enrollments"],
                 color="#5cb85c", edgecolor="white", width=0.65)

for bar in bars2:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             str(int(bar.get_height())), ha="center", fontsize=9)

ax2.set_ylabel("Количество студентов")
ax2.set_title("📚 Количество сдач по курсам", fontweight="bold")
ax2.set_xticks(range(len(df_courses)))
ax2.set_xticklabels(df_courses["short_name"], rotation=40, ha="right", fontsize=8)

# ------------------------------------------------------------
# ГРАФИК 3: Распределение оценок (гистограмма + статистика)
# ------------------------------------------------------------
ax3 = fig.add_subplot(gs[1, 0])

grade_counts = df_all["grade"].value_counts().sort_index()
bars3 = ax3.bar(grade_counts.index, grade_counts.values,
                color="#f0ad4e", edgecolor="white", width=0.55)

# Подписи: количество и процент
for bar, (grade, cnt) in zip(bars3, grade_counts.items()):
    pct = cnt / total_grades * 100
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f"{cnt} ({pct:.0f}%)", ha="center", fontsize=9)

# Линии медианы и среднего
ax3.axvline(median_grade, color="crimson", linestyle="--", linewidth=1.5,
            label=f"Медиана: {median_grade}")
ax3.axvline(mean_grade, color="#2a9d8f", linestyle=":", linewidth=1.5,
            label=f"Среднее: {mean_grade:.2f}")

ax3.set_xticks([2, 3, 4, 5])
ax3.set_xlabel("Оценка")
ax3.set_ylabel("Количество записей")
ax3.set_title("📈 Распределение оценок", fontweight="bold")
ax3.legend(fontsize=8)

# Блок со статистикой прямо на графике
stats_text = f"n = {total_grades}\nСреднее = {mean_grade:.2f}\nМедиана = {median_grade:.1f}\nσ = {std_grade:.2f}"
ax3.text(0.97, 0.95, stats_text, transform=ax3.transAxes,
         va="top", ha="right", fontsize=8,
         bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", edgecolor="lightgray"))

# ------------------------------------------------------------
# ГРАФИК 4: Студенты по году поступления (круговая диаграмма)
# ------------------------------------------------------------
ax4 = fig.add_subplot(gs[1, 1])

pie_colors = ["#7b68ee", "#4a90d9", "#2ecc71"]
pie_labels = [f"{int(row.year)} ({row.students} чел.)" for _, row in df_years.iterrows()]

wedges, texts, autotexts = ax4.pie(
    df_years["students"],
    labels=None,
    autopct="%1.0f%%",
    colors=pie_colors,
    startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    pctdistance=0.7
)
for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight("bold")

ax4.set_title("👥 Студенты по году набора", fontweight="bold")
ax4.legend(wedges, pie_labels, loc="lower center", bbox_to_anchor=(0.5, -0.15),
           fontsize=8, frameon=False)

# ==============================================================================
# 4. ВЫВОД АНОМАЛИЙ И АНАЛИЗ
# ==============================================================================

# Текст об аномалиях под всей фигурой
if len(df_missing) > 0:
    anomaly_text = (f"⚠️ АНОМАЛИЯ: {len(df_missing)} студентов не имеют ни одной оценки! "
                    f"Список: {', '.join(df_missing['student'].tolist()[:5])}")
    if len(df_missing) > 5:
        anomaly_text += f" и ещё {len(df_missing)-5}..."
else:
    anomaly_text = "✅ Аномалий не обнаружено: все студенты имеют хотя бы одну оценку."

fig.text(0.5, -0.02, anomaly_text, ha="center", fontsize=9,
         color="#8b0000" if len(df_missing) > 0 else "#2ecc71",
         bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff3f3" if len(df_missing) > 0 else "#f0fff0",
                   edgecolor="#d9534f" if len(df_missing) > 0 else "#2ecc71"))

# Сохранение
plt.tight_layout()
OUTPUT_FILE = "task_7_analysis.png"
plt.savefig(OUTPUT_FILE, bbox_inches="tight", dpi=150)
print(f"\n✓ График сохранён: {OUTPUT_FILE}")
plt.show()

# ==============================================================================
# 5. ВЫВОДЫ ПО ГРАФИКАМ (печатаются в консоль)
# ==============================================================================

print("\n" + "="*60)
print("📌 АНАЛИЗ ПОЛУЧЕННЫХ ГРАФИКОВ")
print("="*60)

print("\n📊 ГРАФИК 1 — Средний балл по курсам:")
print(f"   • Лучший курс: '{df_courses.iloc[0]['course']}' ({df_courses.iloc[0]['avg_grade']} баллов)")
print(f"   • Худший курс: '{df_courses.iloc[-1]['course']}' ({df_courses.iloc[-1]['avg_grade']} баллов)")
print(f"   • Общий средний балл по курсам: {course_mean:.2f}")
print("   • Курсы, отмеченные красным, находятся ниже среднего уровня успеваемости.")

print("\n📊 ГРАФИК 2 — Количество сдач по курсам:")
max_course = df_courses.loc[df_courses['total_enrollments'].idxmax()]
min_course = df_courses.loc[df_courses['total_enrollments'].idxmin()]
print(f"   • Самый популярный курс: '{max_course['course']}' ({max_course['total_enrollments']} сдач)")
print(f"   • Самый непопулярный курс: '{min_course['course']}' ({min_course['total_enrollments']} сдач)")
print("   • Курс 'Python' лидирует, что может говорить о его обязательности или востребованности.")

print("\n📊 ГРАФИК 3 — Распределение оценок:")
print(f"   • Всего оценок: {total_grades}")
print(f"   • Средний балл: {mean_grade:.2f}")
print(f"   • Медиана: {median_grade}")
print(f"   • Стандартное отклонение: {std_grade:.2f} — {'небольшой разброс' if std_grade < 1 else 'существенный разброс'}")
print("   • Большинство оценок — 4 и 5. Оценок 2 очень мало — редкая аномалия.")

if 2 in grade_counts.index:
    print(f"   • ⚠️ Обнаружено {grade_counts[2]} оценок '2' — выбросы, требующие внимания.")

print("\n📊 ГРАФИК 4 — Студенты по году поступления:")
for _, row in df_years.iterrows():
    print(f"   • {int(row['year'])} год: {row['students']} студентов ({row['students']/df_years['students'].sum()*100:.0f}%)")
print("   • Наблюдается рост набора студентов от 2023 к 2025 году.")

if len(df_missing) > 0:
    print(f"\n⚠️ АНОМАЛИЯ В ДАННЫХ: {len(df_missing)} студентов не имеют записей об успеваемости.")
    print("   Возможные причины: не внесены данные, студенты на академическом отпуске.")
else:
    print("\n✅ Аномалий в данных не обнаружено.")

print("\n" + "="*60)
print("✅ Анализ завершён.")