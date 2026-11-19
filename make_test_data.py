import numpy as np

rng = np.random.default_rng(42)
n = 500

ids = np.arange(1, n + 1).astype(float)
day = rng.integers(1, 31, n).astype(float)
outlet = rng.integers(1, 4, n).astype(float)
product = rng.integers(1, 9, n).astype(float)

category_list = np.array([0, 1, 1, 1, 1, 2, 2, 3, 4])
category = category_list[product.astype(int)].astype(float)

price_list = np.array([0, 80, 90, 70, 85, 120, 130, 50, 60])
price = np.round(price_list[product.astype(int)] * rng.uniform(0.97, 1.03, n), 2)
cost = np.round(price * rng.uniform(0.35, 0.55, n), 2)
qty = rng.integers(1, 7, n).astype(float)
discount = rng.choice([0, 0, 0.05, 0.10, 0.15, 0.20], n).astype(float)
stock = rng.integers(5, 60, n).astype(float)
payment = rng.integers(1, 5, n).astype(float)
rating = rng.integers(1, 6, n).astype(float)

# Inject intentional data-quality examples. Some issues can overlap.
order = rng.permutation(n)
pos = 0
def take(count):
    global pos
    selected = order[pos:pos + count]
    pos += count
    return selected

price[take(4)] = np.nan
cost[take(4)] = np.nan
rating[take(20)] = np.nan
rows = take(4)
qty[rows[:2]] = 0
qty[rows[2:]] = -1
price[take(2)] = -50
cost[take(2)] = -10
discount[take(2)] = 1.5
rating[take(3)] = [0, 6, 9]
rows = take(4)
category[rows] = (category[rows] % 4) + 1
outlet[take(2)] = 9
rows = take(3)
price[rows] = price[rows] * 3
discount[take(5)] = 0.45
stock[take(5)] = 0
rows = take(5)
ids[rows[1]] = ids[rows[0]]
ids[rows[2]] = ids[rows[0]]
ids[rows[4]] = ids[rows[3]]

header = "transaction_id,day_index,outlet_id,product_code,category_code,quantity,unit_price,unit_cost,discount_rate,stock_before_units,payment_code,customer_rating"
table = np.column_stack([ids, day, outlet, product, category, qty, price, cost, discount, stock, payment, rating])

with open("freshflow_sales.csv", "w") as file:
    file.write(header + "\n")
    for row in table:
        values = []
        for value in row:
            if np.isnan(value):
                values.append("")
            else:
                values.append(str(round(float(value), 4)))
        file.write(",".join(values) + "\n")

print("Created freshflow_sales.csv with", n, "data rows.")
