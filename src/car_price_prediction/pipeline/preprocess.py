import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3] # Goes to the root of the project
DATA_DIR = BASE_DIR / "data"

# print(DATA_DIR)


def clean_data():
    df = pd.read_csv(DATA_DIR / "Car_details.csv")
    print("---------------BEFORE CLEANING:---------------")
    print("Check for missing values: ")
    print(df.isnull().sum())
    print("-" * 50, "\n")
    print("Check for data types: ")
    print(df.dtypes)
    print("-" * 50, "\n")
    print()
    print("Check for info: ")
    print(df.info())
    print("-" * 50, "\n")
    print()
    print("display first 10 rows: ")
    print(df.head(10))
    print("-" * 50, "\n")
    print()
    print("Check for summary statistics: ")
    print(df.describe())
    print("-" * 50, "\n")
    print()

    # cleans the engine column by removing the CC and replaces missing values with the median
    df['engine'] = df['engine'].str.replace(' CC','').astype(float)
    df['engine'] = df['engine'].fillna(df['engine'].median()).astype(int)


    # cleans the mileage column by removing the kmpl and replaces missing values with the median
    # print(df['mileage'].unique())
    df['mileage'] = df['mileage'].str.replace(' kmpl| km/kg','', regex=True).astype(float) #? regex=True is used for pattern matching
    df['mileage'] = df['mileage'].fillna(df['mileage'].median()).astype(int)



    # cleans the torque column by converting kgm to Nm and replaces missing values with the median
    #* extract number
    df['torque_value'] = df['torque'].str.extract(r'(\d+\.?\d*)').astype(float)

    #* detect unit
    df['torque_unit'] = df['torque'].str.contains('kgm', case=False)

    #* convert kgm → Nm
    #? For rows where torque_unit == True, multiply the torque value.
    df.loc[df['torque_unit'], 'torque_value'] = df.loc[df['torque_unit'], 'torque_value'] * 9.80665

    #* final torque column
    df['torque'] = df['torque_value']

    # drop torque_value and torque_unit
    df.drop(columns=['torque_value','torque_unit'], inplace=True)

    df['torque'] = df['torque'].fillna(df['torque'].median()).astype(int)



    # cleans max_power by removing the bhp and replaces missing values with the median
    # print(df['max_power'].unique())
    df['max_power'] = df['max_power'].str.replace(' bhp','')
    df['max_power'] = pd.to_numeric(df['max_power'], errors='coerce')
    df['max_power'] = df['max_power'].fillna(df['max_power'].median()).astype(int)


    #clean seats by replacing missing values with the median and convert to int
    # print(df['seats'].unique())
    df['seats'] = df['seats'].fillna(df['seats'].median()).astype(int)

    print("---------------AFTER CLEANING:---------------")
    print()
    print("Check for missing values: ")
    print(df.isnull().sum())
    print("-" * 50, "\n")
    print()
    print("Check for data types: ")
    print(df.dtypes)
    print("-" * 50, "\n")
    print()
    print("Check for info: ")
    print(df.info())
    print("-" * 50, "\n")
    print()
    print("display first 10 rows: ")
    print(df.head(10))
    print("-" * 50, "\n")
    print()
    print(df.iloc[:, 8:].head(17))
    print(df.describe())
    print("-" * 50, "\n")


    df.to_csv(DATA_DIR / "cleaned_car_details.csv", index=False)

    return df



df = clean_data()
def remove_outliers():

    df_clean = df.copy()

    cols = ["mileage","engine","max_power","torque","selling_price","km_driven"]

    for col in cols:

        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)

        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        df_clean = df_clean[(df_clean[col] >= lower) & (df_clean[col] <= upper)]

    df_clean['car_age'] = 2026 - df_clean['year']
    df_clean.drop('year', axis=1, inplace=True)

    df_clean['km_driven_per_year'] = df_clean['km_driven'] / df_clean['car_age']
    df_clean.drop('km_driven', axis=1, inplace=True)

    df_clean.to_csv(DATA_DIR / "cleaned_car_out.csv", index=False)

    return df_clean

# remove_outliers()