import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class NaturalGas:

    @staticmethod
    def all_data_chart():

        sns.set_style("darkgrid")
        plt.figure(figsize=(15, 8))
        colors = ["blue", "orange", "red"]

        natgas_production = pd.read_csv(
            "../Data/U.S._Dry_Natural_Gas_Production.csv", skiprows=4
        )
        natgas_production.columns = ["Year", "Amount"]
        natgas_imports = pd.read_csv("../Data/U.S._Natural_Gas_Imports.csv", skiprows=4)
        natgas_imports.columns = ["Year", "Amount"]
        natgas_shale_production = pd.read_csv(
            "../Data/dry-natgas-production-by-source-refcase.csv", skiprows=6
        )
        natgas_shale_production.columns = [
            "Year",
            "Alaska",
            "Lower 48 offshore",
            "other lower 48 onshore",
            "Amount",
        ]
        natgas_shale_production = natgas_shale_production[["Year", "Amount"]]

        natgas_production = natgas_production[
            natgas_production["Year"].isin(range(1973, 2022))
        ]
        natgas_imports = natgas_imports[natgas_imports["Year"].isin(range(1973, 2022))]
        natgas_shale_production = natgas_shale_production[
            natgas_shale_production["Year"].isin(range(1973, 2022))
        ]
        natgas_shale_production["Amount"] = natgas_shale_production["Amount"].apply(
            lambda x: x * 1000000
        )

        natgas_production["Źródło gazu"] = "Produkcja krajowa"
        natgas_imports["Źródło gazu"] = "Import"
        natgas_shale_production["Źródło gazu"] = "Gaz z łupków"
        all_data = pd.concat(
            [natgas_production, natgas_imports, natgas_shale_production]
        )
        all_data["Amount"] = all_data["Amount"].values / 1000

        ax = sns.lineplot(
            data=all_data,
            x="Year",
            y="Amount",
            hue="Źródło gazu",
            marker="o",
            linestyle="dashed",
            palette=colors,
        )
        plt.xlabel("Rok", size=16)
        plt.ylabel("Miliard stóp sześciennych rocznie", size=16)
        plt.title(
            "Produkcja całkowita, produkcja z łupków i import gazu ziemnego w USA",
            size=18,
        )

        years = list(range(1973, 2023, 7))
        plt.xticks(size=12)
        ax.set_xticks(years)

        plt.savefig("../Figs/fig4.png")
