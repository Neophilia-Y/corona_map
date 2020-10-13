import pandas as pd


def make_country_df():
    def country_data(condition, country):
        df = pd.read_csv(f"data/global_{condition}.csv")
        df = (
            df.loc[df["Country/Region"] == country, "1/22/20":]
            .sum()
            .reset_index(name=condition)
        )
        df = df.rename(columns={"index": "date"})
        return df

    df = pd.read_csv("data/global_confirmed.csv")
    countries = list(df["Country/Region"].unique())

    df_dict = {}
    for country in countries:
        for condition in conditions:
            df = country_data(condition, country)
            if country not in df_dict.keys():
                df_dict[country] = df
            else:
                df_dict[country] = df_dict[country].merge(df)
    return df_dict


# Time Series Data preprocessor


def time_series_total():
    def extract(condition):
        df = pd.read_csv(f"data/global_{condition}.csv")
        df = df.iloc[:, 4:].sum().reset_index(name=condition)
        # key, value값을 데이터프레임으로 바꾸기 위해 reset_index()
        df = df.rename(columns={"index": "date"})
        return df

    final_df = None
    for condition in conditions:
        df = extract(condition)
        if final_df is None:
            final_df = df
        else:
            final_df = final_df.merge(df)

    return final_df


conditions = ["confirmed", "recovered", "deaths"]

# Total Cases

df = pd.read_csv("data/daily_report.csv")

total_df = df[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(name="count")
total_df = total_df.rename(columns={"index": "condition"})

# Total by Country
countries_df = (
    df[["Country_Region", "Confirmed", "Deaths", "Recovered"]]
    .groupby("Country_Region")
    .sum()
    .reset_index()
)

