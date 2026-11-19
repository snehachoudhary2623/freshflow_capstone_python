import numpy as np
import io

# FreshFlow Juice Company
FILE = "freshflow_sales.csv"

# Column positions in the CSV file
ID, DAY, OUTLET, PRODUCT, CATEGORY = 0, 1, 2, 3, 4
QTY, PRICE, COST, DISCOUNT = 5, 6, 7, 8
STOCK, PAYMENT, RATING = 9, 10, 11

outlet_names = ["", "Outlet A", "Outlet B", "Outlet C"]
product_names = ["", "Orange Juice", "Mango Juice", "Apple Juice",
                 "Watermelon Juice", "Banana Smoothie",
                 "Mixed Fruit Smoothie", "Lemonade", "Iced Tea"]
category_for_product = [0, 1, 1, 1, 1, 2, 2, 3, 4]


def heading(text):
    print("\\n" + "=" * 60)
    print(text)
    print("=" * 60)


def load_data():
    # Blank numeric fields are loaded as NaN.
    return np.genfromtxt(FILE, delimiter=",", skip_header=1, ndmin=2)


def percent(top, bottom):
    if bottom == 0:
        return 0
    return top / bottom * 100


def data_profile(data):
    heading("TASK A - DATA PROFILE")
    print("Rows:", data.shape[0])
    print("Columns:", data.shape[1])
    print("Shape:", data.shape)
    print("Data type:", data.dtype)
    print("Number of values:", data.size)
    print("Memory in bytes:", data.nbytes)
    print("Missing values by column:")
    for col in range(data.shape[1]):
        print(col, int(np.isnan(data[:, col]).sum()))


def make_flags(data):
    # A mask is an array of True and False values.
    ids = data[:, ID]
    day = data[:, DAY]
    outlet = data[:, OUTLET]
    product = data[:, PRODUCT]
    category = data[:, CATEGORY]
    qty = data[:, QTY]
    price = data[:, PRICE]
    cost = data[:, COST]
    discount = data[:, DISCOUNT]
    stock = data[:, STOCK]
    payment = data[:, PAYMENT]
    rating = data[:, RATING]

    unique_ids, counts = np.unique(ids[np.isfinite(ids)], return_counts=True)
    duplicate_ids = unique_ids[counts > 1]

    expected = np.zeros(len(data))
    for code in range(1, 9):
        expected[product == code] = category_for_product[code]

    flags = {}
    flags["invalid ID"] = (~np.isfinite(ids)) | (ids <= 0) | (ids != np.floor(ids))
    flags["duplicate ID"] = np.isin(ids, duplicate_ids)
    flags["invalid day"] = (day < 1) | (day > 30) | (day != np.floor(day))
    flags["unknown outlet"] = ~np.isin(outlet, [1, 2, 3])
    flags["unknown product"] = ~np.isin(product, np.arange(1, 9))
    flags["unknown payment"] = ~np.isin(payment, [1, 2, 3, 4])
    flags["category mismatch"] = (product >= 1) & (product <= 8) & (category != expected)
    flags["invalid quantity"] = (qty <= 0) | (qty != np.floor(qty))
    flags["missing price"] = np.isnan(price)
    flags["invalid price"] = np.isfinite(price) & (price <= 0)
    flags["missing cost"] = np.isnan(cost)
    flags["invalid cost"] = np.isfinite(cost) & (cost < 0)
    flags["invalid discount"] = (discount < 0) | (discount > 1)
    flags["zero stock"] = stock == 0
    flags["invalid rating"] = np.isfinite(rating) & ((rating < 1) | (rating > 5))

    heading("TASK B - INTEGRITY AUDIT")
    for name in flags:
        print(name + ":", int(flags[name].sum()))
    return flags


def clean_data(data, flags):
    # Never change raw data. Select usable records into a new array.
    bad = np.zeros(len(data), dtype=bool)
    exclude_names = ["invalid ID", "duplicate ID", "invalid day", "unknown outlet",
                     "unknown product", "unknown payment", "category mismatch",
                     "invalid quantity", "missing price", "invalid price",
                     "missing cost", "invalid cost", "invalid discount"]
    for name in exclude_names:
        bad = bad | flags[name]

    clean = data[~bad].copy()
    heading("TASK C - CLEANING")
    print("Original rows:", len(data))
    print("Rows retained:", len(clean))
    print("Rows excluded:", int(bad.sum()))
    print("Missing customer ratings are allowed.")
    print("High but valid discounts and zero stock are kept for review.")
    return clean


def get_metrics(data):
    qty = data[:, QTY]
    price = data[:, PRICE]
    cost = data[:, COST]
    discount = data[:, DISCOUNT]

    gross_sales = qty * price
    discount_amount = gross_sales * discount
    net_revenue = gross_sales - discount_amount
    cogs = qty * cost
    gross_profit = net_revenue - cogs
    return gross_sales, discount_amount, net_revenue, cogs, gross_profit


def task_d(data):
    heading("TASK D - METRIC ENGINE")
    gross, discount, revenue, cogs, profit = get_metrics(data)
    print("Gross sales INR:", round(gross.sum(), 2))
    print("Discount amount INR:", round(discount.sum(), 2))
    print("Net revenue INR:", round(revenue.sum(), 2))
    print("Cost of goods sold INR:", round(cogs.sum(), 2))
    print("Gross profit INR:", round(profit.sum(), 2))
    print("Gross margin %:", round(percent(profit.sum(), revenue.sum()), 2))
    print("Average transaction value INR:", round(revenue.mean(), 2))
    return revenue, profit


def task_e(data, revenue, profit):
    heading("TASK E - OUTLET COMPARISON")
    for code in [1, 2, 3]:
        selected = data[:, OUTLET] == code
        print(outlet_names[code],
              "Revenue:", round(revenue[selected].sum(), 2),
              "Profit:", round(profit[selected].sum(), 2),
              "Units:", int(data[selected, QTY].sum()))

    heading("TASK E - PRODUCT COMPARISON")
    for code in range(1, 9):
        selected = data[:, PRODUCT] == code
        print(product_names[code],
              "Revenue:", round(revenue[selected].sum(), 2),
              "Profit:", round(profit[selected].sum(), 2),
              "Units:", int(data[selected, QTY].sum()))


def task_f(revenue):
    heading("TASK F - DESCRIPTIVE STATISTICS")
    print("Mean:", round(np.mean(revenue), 2))
    print("Median:", round(np.median(revenue), 2))
    print("Standard deviation:", round(np.std(revenue), 2))
    print("25th percentile:", round(np.percentile(revenue, 25), 2))
    print("75th percentile:", round(np.percentile(revenue, 75), 2))
    print("Minimum:", round(np.min(revenue), 2))
    print("Maximum:", round(np.max(revenue), 2))
    print("Range:", round(np.ptp(revenue), 2))
    print("Histogram counts:", np.histogram(revenue, bins=5)[0])


def task_g(data, revenue):
    heading("TASK G - DAILY TREND")
    daily = np.zeros(30)
    for day in range(1, 31):
        selected = data[:, DAY] == day
        daily[day - 1] = revenue[selected].sum()
    changes = np.diff(daily)
    moving_average = np.convolve(daily, np.ones(3) / 3, mode="valid")
    for i in range(30):
        if i == 0:
            print("Day", i + 1, "revenue:", round(daily[i], 2))
        else:
            print("Day", i + 1, "revenue:", round(daily[i], 2),
                  "change:", round(changes[i - 1], 2),
                  "change %:", round(percent(changes[i - 1], daily[i - 1]), 2))
    print("3-day moving average:", np.round(moving_average, 2))
    print("Total cumulative revenue:", round(np.cumsum(daily)[-1], 2))


def task_h(data, revenue, profit):
    heading("TASK H - DISCOUNT INVESTIGATION")
    bands = [(0, 0.01, "No discount"), (0.01, 0.11, "1-10%"),
             (0.11, 0.21, "11-20%"), (0.21, 0.31, "21-30%"),
             (0.31, 1.01, "Above 30%")]
    for low, high, name in bands:
        selected = (data[:, DISCOUNT] >= low) & (data[:, DISCOUNT] < high)
        if selected.sum() > 0:
            margin = percent(profit[selected].sum(), revenue[selected].sum())
            print(name, "count:", int(selected.sum()),
                  "quantity:", int(data[selected, QTY].sum()),
                  "revenue:", round(revenue[selected].sum(), 2),
                  "margin %:", round(margin, 2))
    print("Discount group differences do not prove cause and effect.")


def task_i(data, revenue, profit):
    heading("TASK I - ANOMALY REGISTER")
    price = data[:, PRICE]
    q1 = np.percentile(price, 25)
    q3 = np.percentile(price, 75)
    upper_limit = q3 + 1.5 * (q3 - q1)
    high_price = price > upper_limit
    high_discount = data[:, DISCOUNT] > 0.30
    zero_stock = data[:, STOCK] == 0
    std = revenue.std()
    if std == 0:
        z_score = np.zeros(len(revenue))
    else:
        z_score = (revenue - revenue.mean()) / std
    unusual_revenue = np.abs(z_score) > 2

    with open("anomaly_register.csv", "w") as file:
        file.write("transaction_id,reasons,net_revenue,gross_profit\\n")
        count = 0
        for i in range(len(data)):
            reasons = []
            if high_price[i]:
                reasons.append("high_price_IQR")
            if high_discount[i]:
                reasons.append("high_discount")
            if zero_stock[i]:
                reasons.append("zero_stock")
            if unusual_revenue[i]:
                reasons.append("unusual_revenue_zscore")
            if reasons:
                count += 1
                file.write(str(int(data[i, ID])) + ',"' + "|".join(reasons) + '",'
                           + str(round(revenue[i], 2)) + ','
                           + str(round(profit[i], 2)) + "\\n")
    print("Flagged records:", count)
    print("Details saved in anomaly_register.csv.")
    print("Outliers are review flags, not automatically errors.")


def task_j(data):
    heading("TASK J - DISCOUNT SCENARIOS")
    qty = data[:, QTY]
    price = data[:, PRICE]
    cost = data[:, COST]
    old_discount = data[:, DISCOUNT]
    base_revenue = (qty * price * (1 - old_discount)).sum()
    base_profit = base_revenue - (qty * cost).sum()
    for rate in [0.05, 0.10, 0.15]:
        new_revenue = (qty * price * (1 - rate)).sum()
        new_profit = new_revenue - (qty * cost).sum()
        print("Assumed discount:", rate * 100, "%")
        print("Revenue:", round(new_revenue, 2),
              "change:", round(new_revenue - base_revenue, 2))
        print("Gross profit:", round(new_profit, 2),
              "change:", round(new_profit - base_profit, 2))
    print("Quantity and unit cost are held constant. This is not a forecast.")


def task_k(data):
    heading("TASK K - VALIDATION TESTS")
    gross, discount, revenue, cogs, profit = get_metrics(data)
    for i in range(min(5, len(data))):
        hand_value = data[i, QTY] * data[i, PRICE] * (1 - data[i, DISCOUNT])
        assert np.isclose(hand_value, revenue[i])
    print("Five sample rows checked.")

    assert data.shape[1] == 12
    print("Shape check passed.")

    assert percent(10, 0) == 0
    print("Zero denominator check passed.")

    test_array = np.array([1.0, np.nan, 3.0])
    assert np.isnan(test_array[1])
    print("NaN check passed.")

    wrong_shape = False
    try:
        np.array([1, 2, 3]) * np.array([1, 2])
    except ValueError:
        wrong_shape = True
    assert wrong_shape
    print("Invalid shape check passed.")

    np.testing.assert_allclose(gross - discount, revenue)
    np.testing.assert_allclose(revenue - cogs, profit)
    print("Metric consistency checks passed.")
    print("Bug fix: duplicate IDs are checked using the ID column, not complete rows.")


def task_l(data, profit):
    heading("TASK L - FINDINGS AND RECOMMENDATIONS")
    outlet_profit = []
    for code in [1, 2, 3]:
        outlet_profit.append(profit[data[:, OUTLET] == code].sum())
    best = int(np.argmax(outlet_profit)) + 1
    worst = int(np.argmin(outlet_profit)) + 1
    print("Finding 1: Highest gross-profit outlet:", outlet_names[best])
    print("Action: compare its practices with", outlet_names[worst])
    print("Monitor: weekly gross profit and margin.")
    print("Limitation: rent and salaries are not included.")

    units = []
    product_profit = []
    for code in range(1, 9):
        selected = data[:, PRODUCT] == code
        units.append(data[selected, QTY].sum())
        product_profit.append(profit[selected].sum())
    top_units = int(np.argmax(units)) + 1
    top_profit = int(np.argmax(product_profit)) + 1
    print("\\nFinding 2: Most units sold:", product_names[top_units])
    print("Highest product gross profit:", product_names[top_profit])
    print("Action: plan product stock using demand and profit.")
    print("Monitor: units and gross profit by product.")
    print("Limitation: only 30 days are included.")

    print("\\nFinding 3: Review discounts using margin and quantity together.")
    print("Action: test promotions carefully.")
    print("Monitor: gross margin by discount band.")
    print("Limitation: the data does not prove demand response.")
    print("\\nFindings use synthetic practice data.")


def main():
    raw = load_data()
    original = raw.copy()

    heading("DATA DICTIONARY")
    print("Columns:", "transaction_id, day_index, outlet_id, product_code, category_code,")
    print("quantity, unit_price, unit_cost, discount_rate, stock_before_units,")
    print("payment_code, customer_rating")
    clean_example = np.loadtxt(io.StringIO("1,2\n3,4"), delimiter=",")
    print("Clean example loaded with np.loadtxt:")
    print(clean_example)

    data_profile(raw)
    flags = make_flags(raw)
    clean = clean_data(raw, flags)
    revenue, profit = task_d(clean)
    task_e(clean, revenue, profit)
    task_f(revenue)
    task_g(clean, revenue)
    task_h(clean, revenue, profit)
    task_i(clean, revenue, profit)
    task_j(clean)
    task_k(clean)
    task_l(clean, profit)

    np.testing.assert_array_equal(np.nan_to_num(raw, nan=-999),
                                  np.nan_to_num(original, nan=-999))
    print("\\nAll analysis steps completed successfully.")


if __name__ == "__main__":
    main()
