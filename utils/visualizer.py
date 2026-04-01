import matplotlib.pyplot as plt
import seaborn as sns

def auto_visualize(df):
    plots = []

    for col in df.columns:
        plt.figure()

        if df[col].dtype == 'object':
            df[col].value_counts().head(10).plot(kind='bar')
            plt.title(f"Top Categories in {col}")

        else:
            sns.histplot(df[col], kde=True)
            plt.title(f"Distribution of {col}")

        plots.append(plt.gcf())
        plt.close()

    return plots