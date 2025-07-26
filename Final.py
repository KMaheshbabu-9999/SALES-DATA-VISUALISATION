import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    cnx = mysql.connector.connect(
        user='root',
        password='root',
        host='127.0.0.1',
        database='automobile_sales',
        auth_plugin='mysql_native_password'
    )

    cursor = cnx.cursor()

    print("Choose a chart type:")
    print("1. Bar chart")
    print("2. Heatmap")
    print("3. Histogram")
    print("4. Line chart")
    print("5. Circle chart")

    choice = input("Enter your choice (1-5): ")

    print("Choose a year:")
    years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
    for i, year in enumerate(years):
        print(f"{i + 1}. {year}")

    year_choice = int(input("Enter the number of the year(enter index of year): "))
    year = years[year_choice - 1]

    if choice == "1":
        query = "SELECT Manufacturer, SUM(sales) as sales FROM car_sales WHERE year = %s GROUP BY Manufacturer"
        cursor.execute(query, (year,))
        data = cursor.fetchall()
        if not data:
            print(f"No data found for year {year}")
        else:
            df = pd.DataFrame(data, columns=['manufacturer', 'sales'])
            plt.figure(figsize=(12, 6))
            sns.barplot(x='manufacturer', y='sales', data=df, palette='viridis')
            plt.title(f'Sales by Manufacturer in {year}', pad=20, size=14)
            plt.xlabel('Manufacturer', labelpad=10)
            plt.ylabel('Total Sales', labelpad=10)
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()

    elif choice == "2":
        query = """
            SELECT 
                Manufacturer,
                model,
                CAST(SUM(sales) AS SIGNED) as total_sales 
            FROM car_sales 
            WHERE year = %s 
            GROUP BY Manufacturer, model 
            ORDER BY Manufacturer, model
        """
        cursor.execute(query, (year,))
        data = cursor.fetchall()

        if not data:
            print(f"No data found for year {year}")
        else:
            df = pd.DataFrame(data, columns=['manufacturer', 'model', 'total_sales'])
            df['total_sales'] = pd.to_numeric(df['total_sales'], errors='coerce')

            pivot_table = df.pivot_table(
                index='manufacturer',
                columns='model',
                values='total_sales',
                fill_value=0.0,
                aggfunc='sum'
            ).astype(float)

            plt.figure(figsize=(15, 10))
            sns.heatmap(pivot_table,
                        annot=True,
                        cmap='YlOrRd',
                        fmt='.0f',
                        cbar_kws={'label': 'Sales Volume'},
                        square=True)

            plt.title(f'Sales Distribution by Manufacturer and Model in {year}', pad=20)
            plt.xlabel('Model', labelpad=10)
            plt.ylabel('Manufacturer', labelpad=10)
            plt.xticks(rotation=45, ha='right')
            plt.yticks(rotation=0)
            plt.tight_layout()
            plt.show()

    elif choice == "3":
        query = "SELECT sales FROM car_sales WHERE year = %s"
        cursor.execute(query, (year,))
        data = cursor.fetchall()
        if not data:
            print(f"No data found for year {year}")
        else:
            df = pd.DataFrame(data, columns=['sales'])
            plt.figure(figsize=(12, 6))
            sns.histplot(df['sales'], bins=15, kde=True, color='skyblue')
            plt.title(f'Sales Distribution in {year}', pad=20, size=14)
            plt.xlabel('Sales Volume', labelpad=10)
            plt.ylabel('Frequency', labelpad=10)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()

    elif choice == "4":
        query = "SELECT year, SUM(sales) as sales FROM car_sales WHERE year <= %s GROUP BY year ORDER BY year"
        cursor.execute(query, (year,))
        data = cursor.fetchall()
        if not data:
            print(f"No data found up to year {year}")
        else:
            df = pd.DataFrame(data, columns=['year', 'sales'])
            plt.figure(figsize=(12, 6))
            sns.lineplot(x='year', y='sales', data=df, marker='o', linewidth=2)
            plt.title(f'Sales Trend Over Time up to {year}', pad=20, size=14)
            plt.xlabel('Year', labelpad=10)
            plt.ylabel('Total Sales', labelpad=10)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()

    elif choice == "5":
        query = "SELECT Manufacturer, SUM(sales) as sales FROM car_sales WHERE year = %s GROUP BY Manufacturer"
        cursor.execute(query, (year,))
        data = cursor.fetchall()
        if not data:
            print(f"No data found for year {year}")
        else:
            df = pd.DataFrame(data, columns=['manufacturer', 'sales'])
            plt.figure(figsize=(12, 8))
            plt.pie(df['sales'],
                    labels=df['manufacturer'],
                    autopct='%1.1f%%',
                    startangle=90,
                    shadow=True)
            plt.title(f'Market Share by Manufacturer in {year}', pad=20, size=14)
            plt.axis('equal')
            plt.show()

    else:
        print("Invalid choice. Please try again.")

except mysql.connector.Error as err:
    print(f"Database Error: {err}")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'cnx' in locals():
        cnx.close()