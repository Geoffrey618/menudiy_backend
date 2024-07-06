import sqlite3

costs = [0.988, 0.5608, 0.7212, 0.532, 1.752, 1.540336, 2.532192, 2.672, 0.504, 4.72, 3.292, 0.6408, 6.608, 5.188, 4.172, 6.376, 2, 2.5224, 1.4, 1.044, 5.814, 1.0528, 4, 4, 13.664, 0.44, 0.172, 3.392277081, 0.256, 1.12, 1.560560224, 2.420168067, 2.384153661, 1.735716857, 0.731466987, 4, 0.672, 4.012868015, 6.972, 8.72, 3.5816, 5.6756, 4.7664, 4.043028434, 2.71, 3.29, 4.0008, 4.149271549, 11.76796401, 2.5056, 5.318, 5.716, 2.392, 3.436, 3.278160384, 4.727440576, 7.8316, 11.648, 12.317248, 7.6332, 10.28377911, 7.52795201, 7.075889076, 13.8144, 11.92, 14.4, 5.8568, 3.40120048, 5.6, 3.964, 5.736, 3.404, 5.289659064, 11.17993761, 2.003165447, 10.622, 4.1624, 3.5088, 4.0172, 3.903880024, 6.3852, 7.8452, 7.7248, 7.9256, 2.88, 1.68, 0.58, 1.22, 4.44, 5.46, 3.18, 2.16, 3.28, 4.46, 7.78, 10.46, 3.76, 2.74, 4.76, 1.74, 1.86, 4, 4, 5.12, 6, 4.6, 4.2, 9.74, 0.882, 0.58, 0.554, 0.776, 1.5, 0.78, 0.324, 0.446, 1.95, 3.762, 0.664, 1.144, 0.9, 0.5, 1.04, 0.96, 4.816, 0.6, 1.056, 0.41, 1.22, 4.708, 5.796, 7.466, 0.5623, 0.3223, 1.67, 0.5, 0.2, 0.22, 0.22, 0.22, 0.22, 0.22, 0.22, 0.22, 0.22]
weights = [ ... ]  # 请填入之前的 weights 数据
names = [ ... ]  # 请填入之前的 names 数据

# 连接到 SQLite 数据库
conn = sqlite3.connect('menu.db')
cursor = conn.cursor()

# 创建表格（如果不存在）
cursor.execute('''
CREATE TABLE IF NOT EXISTS food_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    cost REAL,
    calories REAL,
    carbs REAL,
    fiber REAL,
    protein REAL,
    fat REAL,
    cholesterol REAL,
    folate REAL,
    vitamin_a REAL,
    vitamin_b REAL,
    vitamin_c REAL,
    vitamin_d REAL,
    vitamin_e REAL,
    sodium REAL,
    potassium REAL,
    calcium REAL,
    phosphorus REAL,
    magnesium REAL,
    iron REAL,
    zinc REAL
)
''')
# 提交创建表格的更改
conn.commit()

# 插入数据
for i in range(len(names)):
    cursor.execute('''
    INSERT INTO food_data (
        name, cost, calories, carbs, fiber, protein, fat, cholesterol, folate,
        vitamin_a, vitamin_b, vitamin_c, vitamin_d, vitamin_e, sodium,
        potassium, calcium, phosphorus, magnesium, iron, zinc
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', [names[i], costs[i]] + weights[i])

# 提交插入的数据
conn.commit()

# 关闭游标和连接
cursor.close()
conn.close()

print("数据已成功插入到数据库。")