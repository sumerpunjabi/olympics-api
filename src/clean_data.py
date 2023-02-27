import pandas as pd


# script to clean irregular data in csv files, convert to title case
def main():
    files = ["../data/summer.csv", "../data/winter.csv"]

    for file in files:
        df = pd.read_csv(file)
        df["Name"] = df["Name"].apply(lambda x: x.title())  # convert to title case
        df.dropna(inplace=True)  # drop rows with missing values
        df.to_csv(file, index=False)


if __name__ == "__main__":
    main()
