import pandas as pd
from spyre import server
from datetime import datetime
from urllib.request import urlopen
import os

server.include_df_index = True

class DataViewer(server.App):
    # Створюємо заголовок/опис для сайту
    title = "NOAA Dara Visualization"

    # Список компонентів, які ми будемо використовувати для введення інформації
    # 1) Випадаючий список для регіонів України, де описом виступає назва регіону, а значення - ім'я файлу, де зберігаються дані
    # 2) Випадаючий список для вибору перегляду даних на графіку (певний індекс)
    # 3) Поле вводу для вибору року
    # 4) Поле вводу для вибору інтервалів тижнів
    inputs = [
        {
            "type": "dropdown",
            "id": "region_data",
            "label": "Region of Ukraine",
            "key": 'region_data',

            "options": [
                {"label": "Cherkasy", "value": '2023_12_13__10_10_58_vhi_id_1.csv'},
                {"label": "Chernihiv", "value": "2023_12_13__10_10_58_vhi_id_2.csv"},
                {"label": "Chernivtsi", "value": "2023_12_13__10_10_58_vhi_id_3.csv"},
                {"label": "Crimea", "value": "2023_12_13__10_10_58_vhi_id_4.csv"},
                {"label": "Dnipro", "value": "2023_12_13__10_10_58_vhi_id_5.csv"},
                {"label": "Donets'k", "value": "2023_12_13__10_10_58_vhi_id_6.csv"},
                {"label": "Ivano-Frankivs'k ", "value": "2023_12_13__10_10_58_vhi_id_7.csv"},
                {"label": "Kharkiv", "value": "2023_12_13__10_10_58_vhi_id_8.csv"},
                {"label": "Kherson", "value": "2023_12_13__10_10_58_vhi_id_9.csv"},
                {"label": "Khmel'nyts'kyy", "value": "2023_12_13__10_10_58_vhi_id_10.csv"},
                {"label": "Kyiv", "value": "2023_12_13__10_10_58_vhi_id_11.csv"},
                {"label": "Kyiv City", "value": "2023_12_13__10_10_58_vhi_id_12.csv"},
                {"label": "Kirovohrad", "value": "2023_12_13__10_10_58_vhi_id_13.csv"},
                {"label": "Luhans'k", "value": "2023_12_13__10_10_58_vhi_id_14.csv"},
                {"label": "L'viv", "value": "2023_12_13__10_10_58_vhi_id_15.csv"},
                {"label": "Mykolayiv", "value": "2023_12_13__10_10_58_vhi_id_16.csv"},
                {"label": "Odessa", "value": "2023_12_13__10_10_58_vhi_id_17.csv"},
                {"label": "Poltava", "value": "2023_12_13__10_10_58_vhi_id_18.csv"},
                {"label": "Rivne", "value": "2023_12_13__10_10_58_vhi_id_19.csv"},
                {"label": "Sevastopol'", "value": "2023_12_13__10_10_58_vhi_id_20.csv"},
                {"label": "Sumy", "value": "2023_12_13__10_10_58_vhi_id_21.csv"},
                {"label": "Ternopil'", "value": "2023_12_13__10_10_58_vhi_id_22.csv"},
                {"label": "Transcarpathia", "value": "2023_12_13__10_10_58_vhi_id_23.csv"},
                {"label": "Vinnytsya", "value": "2023_12_13__10_10_58_vhi_id_24.csv"},
                {"label": "Volyn", "value": "2023_12_13__10_10_58_vhi_id_25.csv"},
                {"label": "Zaporizhzhya", "value": "2023_12_13__10_10_58_vhi_id_26.csv"},
                {"label": "Zhytomyr", "value": "2023_12_13__10_10_58_vhi_id_27.csv"},
            ],

            "value": "2023_12_13__10_10_58_vhi_id_1.csv",
            "action_id": "update_data"
        },
        {
            "type": "dropdown",
            "id": "index_data",
            "label": "Index of Region",
            "options": [
                {"label": "VHI", "value": "VHI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VCI", "value": "VCI"},
                {"label": "SMT", "value": "SMT"},
                {"label": "SMN", "value": "SMN"},
            ],
            "key": "index_data",
            "action_id": "update_data"
        },
        {
            "type": "text",
            "id": "year",
            "label": "Year (1982 - 2023)",
            "value": "1982",
            "key": "year",
            "action_id": "update_data"
        },

        {
            "type": "text",
            "id": "week",
            "label": "Week (1-53) (format: from-to)",
            "value": "1-3",
            "key": "week",
            "action_id": "update_data"
        }

    ]

    # Компонент, а також один зі спосибів керування підгрузкою даних
    controls = [
        {
            "type": "button",
            "id": "update_data",
            "label": "Upload Data"
        }
    ]

    # Вкладки на сайті, на яких розміщуюється певна інформація
    tabs = ["Table", "Plot", "Description"]

    # Що ми маємо на виході для цих табів, а саме: табличка, графік і сторінка HTML з інфою про лабораторну і сам застосунок
    outputs = [
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": False
        },
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot",
            "on_page_load": False
        },
        {
            "type": "html",
            "id": "custom_html",
            "tab": "Description"
        }

    ]

    # Ініціалізація об'єкта класу DataViewer, завантаження CSV таблиць
    def __init__(self):
        self.downloadCsv()

    # Метод класу, який відповідає за те, щоб завантажувати CSV таблиці
    def downloadCsv(self):
        if not os.path.exists('csv_data'):
            os.mkdir('csv_data')

        directory = os.listdir('csv_data')

        if len(directory) == 0:
            date_time = datetime.now()
            separated_date_time = date_time.strftime('%Y_%m_%d__%H_%M_%S')

            for index_s in range(1, 28):
                url = f'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={index_s}&year1=1981&year2=2023&type=Mean'
                vhi_url = urlopen(url)

                with open(f'csv_data/{separated_date_time}_vhi_id_{index_s}.csv', 'w') as out:
                    dataset_s = vhi_url.read().decode('utf-8').replace('<br>', '').replace('<tt><pre>', '').replace(' ', '').split('\n')
                    dataset_s.pop(-1)
                    a = dataset_s.pop(0)
                    a = a.split(':')[1].split(',')[0]
                    out.write(f'{a}\n'+'\n'.join(dataset_s))
        
        else:
           print('Data has been added!'); 

    # Метод, який відповідає за отримання даних з файлу, нормалізацію їх, а також форматування таблички. Цей метод тісно пов'язаний з вкладкою "Table"
    # Після виконання коду, то він відповідає за завантаження туди даних. Для коректного відображення, ми видаляємо перші два рядки, для того, щоб залишались лише числові дані.
    # А також, ті числові дані, які нам треба ми переводимо із типу object в numeric (int, float) для корректної та відображення. 
    def getData(self, params):
        region = params["region_data"]
        year = int(params["year"])

        numbers = params["week"]
        numbers = numbers.split("-")
        week_from = int(numbers[0])
        week_to = int(numbers[1])

        df = pd.read_csv("csv_data/" + region, delimiter='\,\s+|\,|\s+', engine='python', index_col=False, names=["year", "week", "SMN", "SMT", "VCI", "TCI", "VHI"])

        df = df.drop(df.index[:2])
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df['week'] = pd.to_numeric(df['week'], errors='coerce')

        df = df.loc[df.year == year]
        filtered_data = df[(df.week >= week_from) & (df.week <= week_to)]

        return filtered_data

    # Метод, який відповідає за побудову графіку plot. Датафрейм отримує за допомогою методу getData(), також для корректної роботи ми переводу з object в float наші дані. 
    # Також трохи нормалізуємо її і будуємо графік з описом.
    def getPlot(self, params):
        df = self.getData(params).set_index(['week'])
        
        df['SMN'] = df['SMN'].astype("float")
        df['SMT'] = df['SMT'].astype("float")
        df['VCI'] = df['VCI'].astype("float")
        df['TCI'] = df['TCI'].astype("float")
        df['VHI'] = df['VHI'].astype("float")

        year = params["year"]
        
        data_week = params["week"]
        numbers = data_week.split("-")
        data_week = data_week.split("-")
        numbers[0] = int(numbers[0])
        numbers[1] = int(numbers[1])

        indexes = params["index_data"]

        df = df[[indexes]]
        plot_obj = df.plot()

        plot_obj.set_title(indexes + " for the selected year " + year)
        plot_obj.set_ylabel(indexes + ", %")
        plot_obj.set_xlabel("The selected period starting from week " + data_week[0] + " to " + data_week[1] + " for the year " + year)

        line_plot = plot_obj.get_figure()
        return line_plot

    # Сторінка з інфою про лабораторну роботу
    def getHTML(self, params):
        return "<h3>Third Work of Shelestov Laboratory</h3><span>In this laboratory work, I learned to create simple web tools that can help the researcher visualize data. I practiced with the following libraries: cherrypy, jinja2, spyre, matplotlib, pandas, numpy.<br> Web-based application for manual visualization of data, such as the need to reverse the river, the interval of the year, the index and the region that you need. <br>Next, the program will select the required file with data, and also make your adjustments from the displayed one.</span>"


app = DataViewer()
app.launch(port=8080)