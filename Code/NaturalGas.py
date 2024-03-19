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

    @staticmethod
    def natgas_export_data():

        plt.figure(figsize=(15, 8))
        colors = ["blue", "orange", "red"]

        natgas_export_all = pd.read_csv(
            "../Data/U.S._Natural_Gas_Exports_and_Re-Exports_by_Country.csv", skiprows=6
        )
        natgas_export_all.columns = [
            "Year",
            "LNG Export",
            "Pipeline Export",
            "Total Export",
        ]

        lng_export = natgas_export_all[["Year", "LNG Export"]]
        lng_export.columns = ["Year", "Amount"]

        pipeline_export = natgas_export_all[["Year", "Pipeline Export"]]
        pipeline_export.columns = ["Year", "Amount"]

        total_export = natgas_export_all[["Year", "Total Export"]]
        total_export.columns = ["Year", "Amount"]

        lng_export = lng_export[lng_export["Year"].isin(range(1973, 2022))]
        pipeline_export = pipeline_export[
            pipeline_export["Year"].isin(range(1973, 2022))
        ]
        total_export = total_export[total_export["Year"].isin(range(1973, 2022))]

        total_export["Typ Eksportu"] = "Eksport Całkowity"
        pipeline_export["Typ Eksportu"] = "Eksport Gazociągiem"
        lng_export["Typ Eksportu"] = "Eksport LNG"

        all_data = pd.concat([total_export, lng_export, pipeline_export])
        all_data["Amount"] = all_data["Amount"].values / 1000

        all_data = all_data.reset_index(drop=True)

        ax = sns.lineplot(
            data=all_data,
            x="Year",
            y="Amount",
            hue="Typ Eksportu",
            marker="o",
            linestyle="dashed",
            palette=colors,
        )

        plt.xlabel("Rok", size=16)
        plt.ylabel("Eksport w miliardach stóp sześciennych rocznie", size=16)
        plt.title("Eksport gazu ziemnego w USA z podziałem na gazociągi i LNG", size=18)

        years = list(range(1973, 2023, 7))
        plt.xticks(size=12)
        ax.set_xticks(years)

        plt.savefig("../Figs/fig5.png")

    @staticmethod
    def lng_export_data():

        colors = [
            "#e6194B",
            "#f58231",
            "#ffe119",
            "#3cb44b",
            "#42d4f4",
            "#4363d8",
            "#911eb4",
            "#fabebe",
            "#469990",
        ]
        plt.rcParams.update({"font.size": 12})
        plt.figure(figsize=(15, 8))

        lng_export = pd.read_csv("../Data/U.S._LNG_Exports_by_Country.csv", skiprows=6)
        lng_export = lng_export.fillna(0)

        country_names = lng_export.iloc[0][1:].index
        country_names_series = pd.Series(country_names)
        extracted_countries = country_names_series.str.extract(
            r"[U.S. Liquefied|Liquefied U.S.] Natural Gas Exports by Vessel[s]? to ([^,]+) MMcf"
        )
        cleaned_countries = extracted_countries.fillna(country_names_series)
        cleaned_countries_series = cleaned_countries[0]
        new_columns = ["Year"] + cleaned_countries_series.tolist()
        lng_export.columns = new_columns

        excluded_column = ["Year"]
        lng_export["Total"] = lng_export.loc[
            :, ~lng_export.columns.isin(excluded_column)
        ].sum(axis=1)

        def prepare_data(row_data):
            sorted_data = row_data.sort_values(ascending=False)
            top_8_data = sorted_data[:8]
            other_category_sum = sorted_data[8:].sum()
            result_data = top_8_data.append(
                pd.Series(other_category_sum, index=["Other"])
            )
            return result_data.index, result_data.values

        excluded = ["Year", "Total"]
        row_data = lng_export.loc[1, ~lng_export.columns.isin(excluded)]
        labels, sizes = prepare_data(row_data)

        plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
        plt.title("2022")

        plt.savefig("../Figs/fig6.png")
    