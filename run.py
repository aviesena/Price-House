from flask import Flask, render_template
import pandas as pd
from collections import defaultdict

app = Flask(__name__, template_folder='Template', static_folder='Static')
 
@app.route('/')
def index():
    data = pd.read_csv('cleansing_data.csv')
    data_dict = data.to_dict(orient='records')
    
    chart1_labels, chart1_values = chart1(data_dict)
    chart2_labels, chart2_values = chart2(data_dict)
    chart3_labels, chart3_values = piechart(data_dict)
    chart4_labels, chart4_values = avg_saleprice_by_condition(data_dict)
    return render_template('index.html', chart1_labels=chart1_labels, chart1_values=chart1_values, chart2_labels=chart2_labels, chart2_values=chart2_values, chart3_labels=chart3_labels, chart3_values=chart3_values, chart4_labels=chart4_labels, chart4_values=chart4_values)



def chart1(data_dict):
    sales_by_year = defaultdict(int)

    for row in data_dict:
        year_sold = row['YrSold']
        sales_by_year[year_sold] += 1
 
    labels = list(sales_by_year.keys())
    values = list(sales_by_year.values())

    return labels, values

def chart2(data_dict):
    sales_by_year = defaultdict(int)
    total_sales_by_year = defaultdict(int)

    for row in data_dict:
        year_sold = row['YrSold']
        sales_by_year[year_sold] += 1
        total_sales_by_year[year_sold] += row['SalePrice']  # Gantilah 'TotalSales' dengan nama kolom yang sesuai

    labels = list(sales_by_year.keys())
    values = list(total_sales_by_year.values())

    return labels, values

def piechart(data_dict):
    total_cond = defaultdict(int)
    total_entries = len(data_dict)

    for row in data_dict:
        overall_cond = row['OverallCond']
        total_cond[overall_cond] += 1

    labels = list(total_cond.keys())
    values = list(total_cond.values())

    # Menghitung persentase untuk setiap kategori
    percentages = [(count / total_entries) * 100 for count in values]

    return labels, percentages

def avg_saleprice_by_condition(data_dict):
    avg_saleprice_by_condition = defaultdict(list)

    for row in data_dict:
        overall_cond = row['OverallCond']
        saleprice = row['SalePrice']
        avg_saleprice_by_condition[overall_cond].append(saleprice)

    # Hitung rata-rata untuk setiap kondisi
    for condition, prices in avg_saleprice_by_condition.items():
        avg_saleprice_by_condition[condition] = sum(prices) / len(prices)

    # Urutkan kondisi berdasarkan nilai rata-rata
    sorted_conditions = sorted(avg_saleprice_by_condition.keys())
    sorted_avg_saleprice = [avg_saleprice_by_condition[cond] for cond in sorted_conditions]

    return sorted_conditions, sorted_avg_saleprice

@app.route('/EDA')
def EDA():
    # Lakukan pemrosesan data atau logika bisnis yang diperlukan di sini
    # Kemudian, render template Dashboard 2
    return render_template('eda.html')

if __name__=='__main__':
    app.run(debug=True)
