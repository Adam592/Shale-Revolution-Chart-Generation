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
