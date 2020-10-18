import pandas as pd


def make_country_df(country):
    def make_df(condition):
        df = pd.read_csv(f"data/global_{condition}.csv")
        df = df.loc[df["Country/Region"] == country]
        df = (
            df.drop(columns=["Province/State", "Country/Region", "Lat", "Long"])
            .sum()
            .reset_index(name=condition)
        )
        df = df.rename(columns={"index": "date"})
        return df

    final_df = None
    for condition in conditions:
        condition_df = make_df(condition)
        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)
    return final_df


# Time Series Data preprocessor


def make_global_df():
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

totals_df = df[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(name="count")
totals_df = totals_df.rename(columns={"index": "condition"})

# Total by Country
countries_df = (
    df[["Country_Region", "Confirmed", "Deaths", "Recovered"]]
    .groupby("Country_Region")
    .sum()
    .sort_values(by="Confirmed", ascending=False)
    .reset_index()
)

dropdown_options = countries_df.sort_values("Country_Region").reset_index()
dropdown_options = dropdown_options["Country_Region"]

