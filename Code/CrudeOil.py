import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class CrudeOil:

    @staticmethod
    def all_data_chart():

        sns.set_style("darkgrid")
        plt.figure(figsize=(15, 8))
        colors = ["blue", "orange", "red"]

        # Prepare data for chart generation
        tight_oil_production = pd.read_csv("../Data/tight_oil_production.csv")

        crude_production = pd.read_csv(
            "../Data/U.S._Imports_of_Crude_Oil.csv", skiprows=4
        )
        crude_production.columns = ["Year", "Amount"]

        crude_import = pd.read_csv(
            "../Data/U.S._Field_production_of_Crude_Oil.csv", skiprows=4
        )
        crude_import.columns = ["Year", "Amount"]

        # Return only years between 1973 and 2022
        crude_production = crude_production[
            crude_production["Year"].isin(range(1973, 2022))
        ]
        crude_import = crude_import[crude_import["Year"].isin(range(1973, 2022))]

        # Add an indicator to each dataset
        crude_production["Źródło ropy"] = "Produkcja Krajowa"
        crude_import["Źródło ropy"] = "Import"
        tight_oil_production["Źródło ropy"] = "Ropa z Łupków"

        # Combine the data
        all_data = pd.concat([crude_production, crude_import, tight_oil_production])

        # Generate the chart
        ax = sns.lineplot(
            data=all_data,
            x="Year",
            y="Amount",
            hue="Źródło ropy",
            marker="o",
            linestyle="dashed",
            palette=colors,
        )

        # Label the chart
        plt.xlabel("Rok", size=16)
        plt.ylabel("Tysiąc baryłek ropy dziennie", size=16)
        plt.title(
            "Produkcja całkowita, produkcja z łupków i import ropy naftowej w USA",
            size=18,
        )

        # Set x ticks
        years = list(range(1973, 2023, 7))
        plt.xticks(size=12)
        ax.set_xticks(years)

        # Save the chart
        plt.savefig("../Figs/fig1.png")

    @staticmethod
    def crude_export_data():

        sns.set_style("darkgrid")
        plt.figure(figsize=(10, 8))

        # Prepare data for chart generation
        crude_export = pd.read_csv("../Data/U.S._Exports_of_Crude_oil.csv", skiprows=4)
        crude_export.columns = ["Year", "Amount"]
        crude_export = crude_export[crude_export["Year"].isin(range(1973, 2022))]

        # Generate the chart
        ax = sns.lineplot(
            data=crude_export,
            x="Year",
            y="Amount",
            marker="o",
            linestyle="dashed",
        )

        # Label the chart
        plt.xlabel("Rok", size=16)
        plt.ylabel("Tysiąc baryłek ropy dziennie", size=16)
        plt.title("Eksport ropy naftowej w USA", size=18)

        # Set x ticks
        years = list(range(1973, 2023, 7))
        plt.xticks(size=12)
        ax.set_xticks(years)

        # Save the chart
        plt.savefig("../Figs/fig2.png")

    @staticmethod
    def crude_import_by_country():

        plt.rcParams.update({"font.size": 12})
        colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2a1ff", "#a1fff4"]

        # Import dataset
        crude_import_by_country = pd.read_csv(
            "../Data/U.S._Imports_by_Country_of_Origin.csv", skiprows=6
        )

        # Display only country names as column names
        country_names = crude_import_by_country.iloc[0][1:].index
        country_names_series = pd.Series(country_names)
        extracted_countries = country_names_series.str.extract(
            r"U.S. Imports from ([^,]+) of Crude Oil Mbbl/d"
        )
        cleaned_countries = extracted_countries.fillna(country_names_series)
        cleaned_countries_series = cleaned_countries[0]
        new_columns = ["Year"] + cleaned_countries_series.tolist()
        crude_import_by_country.columns = new_columns

        # Calculate total imports in a given year
        excluded_column = ["Year"]
        crude_import_by_country["Total"] = crude_import_by_country.loc[
            :, ~crude_import_by_country.columns.isin(excluded_column)
        ].sum(axis=1)

        # Select data only from 1973, 2005, 2022 and fill all NaN with 0
        crude_import_by_country = crude_import_by_country[
            crude_import_by_country["Year"].isin([1973, 2005, 2022])
        ]
        crude_import_by_country = crude_import_by_country.fillna(0)

        # Method for preparing top5 countries with biggest export values and categorizing the rest as 'Other'
        def prepare_data(row_data):
            sorted_data = row_data.sort_values(ascending=False)
            top_5_data = sorted_data[:5]
            other_category_sum = sorted_data[5:].sum()
            result_data = top_5_data.append(
                pd.Series(other_category_sum, index=["Other"])
            )
            return result_data.index, result_data.values

        # Selecting desired data rows from dataset
        row_data_2022 = crude_import_by_country.loc[
            1, ~crude_import_by_country.columns.isin(["Year", "Total"])
        ]
        row_data_2005 = crude_import_by_country.loc[
            18, ~crude_import_by_country.columns.isin(["Year", "Total"])
        ]
        row_data_1973 = crude_import_by_country.loc[
            50, ~crude_import_by_country.columns.isin(["Year", "Total"])
        ]

        # Parsing the rows through prepare_data method
        labels2022, sizes2022 = prepare_data(row_data_2022)
        labels2005, sizes2005 = prepare_data(row_data_2005)
        labels1973, sizes1973 = prepare_data(row_data_1973)

        # Creating three pie charts side by side
        fig, axs = plt.subplots(1, 3, figsize=(18, 8))

        axs[0].pie(
            sizes2022,
            labels=labels2022,
            autopct="%1.1f%%",
            colors=colors,
            startangle=90,
        )
        axs[0].set_title("2022")

        axs[1].pie(
            sizes2005,
            labels=labels2005,
            autopct="%1.1f%%",
            colors=colors,
            startangle=90,
        )
        axs[1].set_title("2005")

        axs[2].pie(
            sizes1973,
            labels=labels1973,
            autopct="%1.1f%%",
            colors=colors,
            startangle=90,
        )
        axs[2].set_title("1973")

        plt.subplots_adjust(wspace=0.5)
        plt.tight_layout()

        # Save the chart
        plt.savefig("../Figs/fig3.png")
