import pandas as pd
from datetime import datetime
from urllib.request import urlopen

# Функція для завантаження файлів таблиць данних та їх нормалізація
def download_csv():
    date_time = datetime.now()
    separated_date_time = date_time.strftime('%Y_%m_%d__%H_%M_%S')

    for index_s in range(1, 28):
        url = f'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={index_s}&year1=1981&year2=2023&type=Mean'
        vhi_url = urlopen(url)

        with open(f'{separated_date_time}_vhi_id_{index_s}.csv', 'w') as out:
            dataset_s = vhi_url.read().decode('utf-8').replace('<br>', '').replace('<tt><pre>', '').replace(' ', '').split('\n')
            dataset_s.pop(-1)
            a = dataset_s.pop(0)
            a = a.split(':')[1].split(',')[0]
            out.write(f'{a}\n'+'\n'.join(dataset_s))

# Функція читання файлу таблиці
def read_csv_file():
    tuple_NNAA_to_LW = {1: 22, 2: 24,  3: 23, 4: 25,  5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21, 11: 9, 12: 0, 13: 10, 14: 11, 15: 12, 16: 13, 17: 14, 18: 15, 19: 16, 20: 0, 21: 17, 22: 18, 23: 6,  24: 1, 25: 2, 26: 7, 27: 5}
    frames = []

    for index_f in range(1, 28):
        with open(f'2023_12_04__17_34_17_vhi_id_{index_f}.csv', "r") as dataset:
            df = dataset.readlines()
            df = [line.strip().split(',') for line in df]

            df = pd.DataFrame(df[2:], columns=['year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty'])
            df['index_region'] = tuple_NNAA_to_LW[index_f]

            frames.append(df)

    result_df = pd.concat(frames, ignore_index=True)

    return result_df

# Функція, яка визначає максимальний (мінімальний) індекс VHI
def min_max_VHI(year, index):
    max_VHI = read_csv_file()[(read_csv_file()["year"] == f'{year}') & (read_csv_file()["index_region"] == index) & (read_csv_file()['VHI'] != '-1.00')]
    min_VHI = read_csv_file()[(read_csv_file()["year"] == f'{year}') & (read_csv_file()["index_region"] == index) & (read_csv_file()['VHI'] != '-1.00')]
    return max_VHI['VHI'].max(), (min_VHI['VHI']).min()

# Функція, яка визначає екстремальні засухи
def extreme_drought(index):
    data_year = read_csv_file()[(read_csv_file()["index_region"] == index) & (read_csv_file()['VHI'] != '-1.00')]
    year = data_year[(data_year['VHI'] < '15.00') & data_year['year']]
    return year['year']

# Функція, яка визначає помірні засухи
def moderate_drought(index):
    data_year = read_csv_file()[(read_csv_file()["index_region"] == index) & (read_csv_file()['VHI'] != '-1.00')]
    year = data_year[(data_year['VHI'] < '35.00') & data_year['year']]
    year = year[(year['VHI'] > '15.00') & year['year']]
    return year['year'].head()


# download_csv()

max_VHI, min_VHI = min_max_VHI(1982, 2)[0], min_max_VHI(1982, 2)[1]
ex_dr = extreme_drought(2)
md_dr = moderate_drought(2)

print(f'Max VHI: {max_VHI} | Min VHI: {min_VHI}')
print(f"Extreme Drought: \n{ex_dr}")
print(f"Moderate Drought: \n{md_dr}")