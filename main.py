import pandas as pd

print("Script Start")

df = pd.read_csv("./bank_enriched_addresses.csv")
df.head()

# a. Remove all rows where pdays is -1
df = df.query('pdays != -1')

# b. Split name into first name and second name columns (drop name)
names = df["name"].str.split(" ", n=1, expand=True)
df["first_name"] = names[0]
df["second_name"] = names[1]
df.drop(columns=["name"], inplace=True)

# Replace the values in the age column with bucketed values, such that
df["age"] = df["age"] // 10

# d. Replace yes/no values with booleans
df["default"] = df["default"].replace({'yes': True, 'no': False})
df["housing"] = df["housing"].replace({'yes': True, 'no': False})
df["loan"] = df["loan"].replace({'yes': True, 'no': False})
df["y"] = df["y"].replace({'yes': True, 'no': False})

# e. Replace day and month with a single date column, of the form dd/MM
month_mapping = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
}

# Convert the "month" column to numerical values using the mapping
df["month_numeric"] = df["month"].str.lower().map(month_mapping)

# Create a new datetime column using "day" and "month_numeric" columns
df["date"] = pd.to_datetime(df['day'].astype(str) + '/' + df['month_numeric'].astype(str), format='%d/%m')

# Format the "date" column as "dd/MM" and store it in a new column "date"
df["date"] = df["date"].dt.strftime('%d/%m')

# Drop temp and old columns
df.drop(["month_numeric", "day", "month"], axis=1, inplace=True)

# f. Rename the y column to “outcome"
df = df.rename(columns={"y": "outcome"})

# Add a column which categorizes geographical features in the address, where present. Note the dirtiness of the
# address data and that the exact categories:
# a. “water”, where the address contains e.g. lake, creek
# b. “relief”, where the address contains e.g. hill, canyon
# c. “flat”, where the address contains e.g. plain


def categorize_geographical_feature(address):
    address = address.lower()
    if any(keyword in address for keyword in ["lake", "creek", "river"]):
        return "water"
    elif any(keyword in address for keyword in ["hill", "canyon"]):
        return "relief"
    elif any(keyword in address for keyword in ["plain"]):
        return "flat"
    else:
        return "unknown"


df["geographical_feature"] = df["address"].apply(categorize_geographical_feature)


# Group by the feature (if you created it, or by some other field if not) and filter out any empty values, sort by
# the age bucket (or age if you didn’t do the bucketing), and return a row count.
agg_df = df.dropna()
agg_df = agg_df.query('geographical_feature != "unknown"')
agg_df = agg_df.groupby(["geographical_feature", "age"]).size().reset_index(name='counts').sort_values("age")

# Write the row level data from step 2, and aggregated data from step 3 to both CSV and parquet formats.
df.to_csv('step_2.csv', index=False)
df.to_parquet('step_2.parquet.gzip', compression='gzip', index=False)

agg_df.to_csv('step_4.csv', index=False)
agg_df.to_parquet('step_4.parquet.gzip', compression='gzip', index=False)

print("Script End - Successfuly")
