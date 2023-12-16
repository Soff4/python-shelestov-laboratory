# Імпортуємо необхідні нам бібліотеки для роботи з датасетом
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr

# Створюємо вхідні дані (шлях до файлу, шлях для збереження, конфіг для встановлення типів даних)
path = 'csv_data/household_power_consumption.txt'
out_path = 'csv_data/household_power_consumption.csv'
config = {
    'Date' : object,
    'Time' : object,
    'Global_active_power': float,
    'Global_reactive_power' : float,
    'Voltage' : float,
    'Global_intensity' : float,
    'Sub_metering_1' : float,
    'Sub_metering_2' : float,
    'Sub_metering_3' : float,
}

# На основі поставленних завдань був створенний спеціальний клас PowerConsumption
class PowerConsumption:

    # Ініціалізація (конструктор) класу, який має 3 вхідних властивості (шлях, параметр для читання файлів та датафрейм в який ми одразу записуємо дані за допомогою метода)
    def __init__(self, path):
        self.path = path
        self.delimeter = ";"
        self.df = self.read_data()

    # Метод, який повертає дані, які ми зчитуємо з файлу, додаючи певні параметри
    def read_data(self):
        return pd.read_csv(self.path, delimiter=self.delimeter, skiprows=[0])
    
    # Метод, який виводить дані, де output_data моде бути або "Data", або "Type"
    # num_rows - кількість рядків для виводу
    def output_data(self, output_type = "Data", num_rows = 5):
        if output_type == "Data":
            print(self.df.head(num_rows))
        else:
            print(self.df.dtypes)

    #  Метод, який встановлює певні типи даних використовуючи конфіг
    def set_dtype_data(self, config):
        self.df = pd.read_csv(self.path, delimiter=self.delimeter, dtype=config, na_values="?")

    # Метод для чистки даних
    def clean_data(self):
        self.df.dropna(inplace=True)

    # Метод для збереження фалйу в форматі таблички
    def save_data(self, to_path):
        self.df.to_csv(to_path, index=False, sep=self.delimeter)

    # Метод який фільтрує по потужності
    def filter_by_active_power(self, active_power):
        return self.df[self.df['Global_active_power'] > float(active_power)]
    
    # Метод, який філтрує дані по вольтажу
    def filter_by_voltage(self, voltage):
        return self.df[self.df['Voltage'] > voltage]
    
    # Метод, який фільтрує дані по силі струму
    def filter_by_intensity(self, min_intens, max_intens):
        return self.df[(self.df['Global_intensity'] >= min_intens) & (self.df['Global_intensity'] <= max_intens)]

    # Метод, який вибирає n кількість даних з таблички, випадково 
    def filter_by_random(self, size):
        random = np.random.choice(self.df.index, size=size, replace=False)
        return self.df.loc[random]

    # Метод, який фільтрує по часу і потужності
    def filter_by_time_power(self, time, power):
        return self.df[(self.df['Time'] > time) & (self.df['Global_active_power'] > float(power))]

    # Метод, який визначиє ті, у яких основне споживання електроенергії припадає на пральну машину, сушарку, холодильник та освітлення
    def filter_by_sub_metering(self, df, group):
        return df[(df[group[1]] > df[[group[0], group[2]]].max(axis=1))]

    # Метод, який вираховує середнє значення споживання електроенергії
    def average_energy_consumption(self, group):
        return self.df[group].mean()
    
    # Метод, яким можна обрати кожен n елемент з першої половини та кожний n елемент з другої половини
    def selected_each_n(self, n_first_half, n_second_half):
        filter_by_time = self.filter_by_time_power('18:00', 6)
        select_group = self.filter_by_sub_metering(filter_by_time, group=['Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3'])
       
        mid_list = len(select_group) // 2
        first_half = select_group[:mid_list]
        second_half = select_group[mid_list:]

        return pd.concat([first_half.iloc[2::int(n_first_half)], second_half.iloc[3::int(n_second_half)]])
    
    # Метод
    def count_columns(self):
        numeric_columns = self.df.select_dtypes(include=['number']).columns
        categorical_columns = self.df.select_dtypes(exclude=['number']).columns
        
        self.df[numeric_columns] = self.df[numeric_columns].fillna(self.df[numeric_columns].median())
        self.df[categorical_columns] = self.df[categorical_columns].fillna("Unknown")

        missing_numeric = self.df[numeric_columns].isna().sum()
        missing_categorical = self.df[categorical_columns].isna().sum()
        total_missing = self.df.isna().sum()
        
        print("Кількість незаповнених значень для числових стовпців:")
        print(missing_numeric)
        print("\nКількість незаповнених значень для рядкових стовпців:")
        print(missing_categorical)
        print("\nЗагальна кількість незаповнених значень:")
        print(total_missing)
    
    def standardize_data(self):
        numeric_data = self.df.select_dtypes(include=[float, int])
        mean_vals = numeric_data.mean()
        standardized_data = (numeric_data - mean_vals) / numeric_data.std()
        
        return standardized_data
    
    def plot_histogram(self, column):
        plt.figure(figsize=(10, 6))
        plt.hist(self.df[column], bins=10, edgecolor='green')
        plt.xlabel('ID')
        plt.ylabel(column)
        plt.title(f'Діаграма залежності {column} за ID')
        plt.show()
    
    def plot_scatter(self, x_column, y_column):
        plt.figure(figsize=(10, 6))
        sns.regplot(x=self.df[x_column], y=self.df[y_column])
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(f'Графік залежності {x_column} від {y_column}')
        plt.show()
    
    def calculate_correlation(self, attribute1, attribute2):
        data_attribute1 = self.df[attribute1]
        data_attribute2 = self.df[attribute2]
        
        pearson_coefficient, _ = pearsonr(data_attribute1, data_attribute2)
        spearman_coefficient, _ = spearmanr(data_attribute1, data_attribute2)
        
        return pearson_coefficient, spearman_coefficient
    
    def pair_plot(self, selected_features):
        pp = sns.pairplot(self.df[selected_features], hue='SUR3')
        plt.show()
    
    def apply_one_hot_encoding(self, column_name):
        df_one_hot = pd.get_dummies(self.df, columns=[column_name])
        selected_columns = df_one_hot.columns[:20]
        df_one_hot_selected = df_one_hot[selected_columns]
        ar_one_hot = df_one_hot_selected.values
        
        return df_one_hot_selected, ar_one_hot


# ЧАСТИНА 1
# Створюємо об'єкт на основі класу PowerConsumption, одразу надаємо шлях до файлу
# Встановлюємо типи даних для датасету за допомогою конфігу
# Чистимо дані, нашого датасету
# Зберігаємо дані у таблицю CSV, використовуючи певний шлях для цього
analyzer = PowerConsumption(path=path)
analyzer.set_dtype_data(config=config)
analyzer.clean_data()
analyzer.save_data(out_path)

# Отримуємо дані з наших методів та виводимо їх
df_active_power = analyzer.filter_by_active_power(5)
print('Filter by Active Power: \n', df_active_power[['Date', 'Time', 'Global_active_power']])

df_voltage = analyzer.filter_by_voltage(235)
print('Filter by Voltage: \n', df_voltage[['Date', 'Time', 'Voltage']])

df_selected_current = analyzer.filter_by_intensity(19, 20)
print('Filter by Intensity: \n', df_selected_current[['Date', 'Time', 'Global_intensity', 'Sub_metering_2', 'Sub_metering_3']])

df_average_consumption = analyzer.average_energy_consumption('Sub_metering_1')
print(f'Avarage energy consumption: {df_average_consumption}\n')

df_select_el = analyzer.selected_each_n(3, 4)
print('Selected Elements: \n', df_select_el[['Date', 'Time', 'Global_active_power', 'Sub_metering_2']].to_string(index=False))

# ЧАСТИНА 2
# Створюємо об'єкт на основі класу PowerConsumption, одразун надаємо шлях до файлу
path = 'csv_data/dataset_amp.csv'

processor = PowerConsumption(path=path)
processor.count_columns()

standardized_data = processor.standardize_data()

processor.plot_histogram('FR')
processor.plot_scatter('SUR1', 'SUR3')

pearson, spearman = processor.calculate_correlation('SUR1', 'SUR3')
print(f"Pearson Coefficient: {pearson}")
print(f"Spearman Coefficient: {spearman}")

processor.pair_plot(['SUR1', 'SUR2', 'SUR3', 'UR', 'FR'])

one_hot_df, one_hot_array = processor.apply_one_hot_encoding('SUR3')
print(one_hot_df.head())
print(one_hot_array[:5, :])