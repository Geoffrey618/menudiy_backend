from flask import Flask, request, jsonify, render_template
import sqlite3
import pulp

app = Flask(__name__)

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def calculate_nutrition(data):
    height = float(data['height'])
    weight = float(data['weight'])
    gender = data['gender']
    age = float(data['age'])
    move = data['move']
    dgc = data['dgc']

    move_c = {'少': 1.2, '轻': 1.375, '中': 1.55, '高': 1.725}[move]
    dgc_c = 200 if dgc == '是' else 300

    bmi = calculate_bmi(weight, height)

    if gender == '男':
        bmr = 88.36 + (13.4 * weight) + (4.8 * height * 100) - (5.7 * age)
    else:
        bmr = 447.6 + (9.2 * weight) + (3.1 * height * 100) - (4.3 * age)

    tee = bmr * move_c
    fat = tee * 0.3 / 9

    if gender == '男':
        if 11 <= age < 14:
            protein, carbs, fiber, ga, mg, k, na, fe, p, va, vb, vb9, vc, ve, zn = 60, 150, 25, 1200, 300, 1900, 1400, 15, 600, 600, 2.9, 300, 90, 13, 7
        elif 14 <= age < 18:
            protein, carbs, fiber, ga, mg, k, na, fe, p, va, vb, vb9, vc, ve, zn = 75, 150, 30, 1100, 320, 2200, 1600, 16, 590, 900, 4, 400, 100, 14, 9.7
        elif 18 <= age < 50:
            protein, carbs, fiber, ga, mg, k, na, fe, p, va, vb, vb9, vc, ve, zn = 65, 120, 30, 800, 330, 2000, 1500, 12, 590, 900, 4, 400, 100, 14, 10.1
        else:
            protein, carbs, fiber, ga, mg, k, na, fe, p, va, vb, vb9, vc, ve, zn = 65, 120, 30, 1000, 330, 2000, 1400, 12, 590, 900, 4, 400, 100, 14, 10.1
    else:
        if 11 <= age < 14:
            protein, carbs, fiber, ga, mg, k, na, fe, p, va, vb, vb9, vc, ve, zn = 55, 150, 25, 1200, 300, 1900, 1400, 18, 600, 600, 2.9, 300, 90, 13, 6.3
        elif 14 <= age < 18:
            protein, carbs, fiber, ga, mg, k, na, fe, p, va, vb, vb9, vc, ve, zn = 60, 150, 30, 1100, 320, 2200, 1600, 18, 590, 700, 3.6, 400, 100, 14, 6.5
        elif 18 <= age < 50:
            protein, carbs, fiber, ga, mg, k, na, fe, p, va, vb, vb9, vc, ve, zn = 55, 120, 30, 800, 330, 2000, 1500, 20, 590, 700, 3.6, 400, 100, 14, 6.9
        else:
            protein, carbs, fiber, ga, mg, k, na, fe, p, va, vb, vb9, vc, ve, zn = 55, 120, 30, 1000, 330, 2000, 1400, 12, 590, 700, 3.6, 400, 100, 14, 6.9

    results = {
        "bmi": bmi,
        "tee": tee,
        "fat": fat,
        "protein": protein,
        "carbs": carbs,
        "fiber": fiber,
        "dgc": dgc_c,
        "ga": ga,
        "mg": mg,
        "k": k,
        "na": na,
        "fe": fe,
        "p": p,
        "va": va,
        "vb": vb,
        "vb9": vb9,
        "vc": vc,
        "ve": ve,
        "zn": zn
    }

    return results

def optimize_menu(min_weights):
    lastcosts = 0
    num_variables = 144

    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM food_data')
    rows = cursor.fetchall()
    conn.close()

    costs = []
    weights = []
    names = []

    for row in rows:
        name = row[1]
        cost = row[2]
        nutrients = row[3:]
        names.append(name)
        costs.append(cost)
        weights.append(list(nutrients))

    days_of_week = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    zongcaipu_array = []
    allcosts_array = []

    usage_counts = [0] * num_variables

    for _ in range(7):
        prob = pulp.LpProblem("Minimize_Costs_Problem", pulp.LpMinimize)
        x = pulp.LpVariable.dicts("x", range(num_variables), lowBound=0, upBound=1, cat='Integer')

        for i in range(num_variables):
            prob += x[i] <= max(0, 3 - usage_counts[i])

        prob += pulp.lpSum([costs[i] * x[i] for i in range(num_variables)])
        prob += pulp.lpSum([costs[i] * x[i] for i in range(num_variables)]) >= lastcosts + 0.1

        for j in range(len(min_weights)):
            prob += pulp.lpSum([weights[i][j] * x[i] for i in range(num_variables)]) >= min_weights[j]

        prob += pulp.lpSum([x[i] for i in range(132, 137)]) == 1
        prob += pulp.lpSum([x[i] for i in range(109, 127)]) == 1
        prob += pulp.lpSum([x[i] for i in range(128, 131)]) == 1
        prob += pulp.lpSum([x[i] for i in range(85, 108)]) == 1
        prob += pulp.lpSum([x[i] for i in range(39, 84)]) == 2
        prob += pulp.lpSum([x[i] for i in range(1, 38)]) == 2
        prob += pulp.lpSum([x[i] for i in range(138, 144)]) == 1

        for i in range(num_variables):
            prob += x[i] <= max(0, 3 - usage_counts[i])

        prob.solve()

        caipu_array = []

        if pulp.LpStatus[prob.status] == "Optimal":
            for v in prob.variables():
                if v.varValue == 1:
                    usage_counts[int(v.name.split('_')[1])] += 1
                    if usage_counts[int(v.name.split('_')[1])] > 3:
                        costs[int(v.name.split('_')[1])] = 1e9
                    caipu_array.append(names[int(v.name.split('_')[1])])

            zongcaipu_array.append(caipu_array)
            lastcosts = pulp.value(prob.objective)
            allcosts_array.append(lastcosts)

    menu = []
    for day, dailycaipu, dailycosts in zip(days_of_week, zongcaipu_array, allcosts_array):
        menu.append({"day": day, "menu": dailycaipu, "cost": dailycosts})

    return menu

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    nutrition_data = calculate_nutrition(data)
    return jsonify(nutrition_data)

@app.route('/optimize', methods=['POST'])
def optimize():
    min_weights = request.json.get('min_weights')
    optimized_menu = optimize_menu(min_weights)
    return jsonify(optimized_menu)

if __name__ == '__main__':
    app.run(debug=True)