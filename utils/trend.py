import matplotlib.pyplot as plt
import seaborn as sns

def trend_analysis(df):
    plots = []

    for col in df.select_dtypes(include="number").columns[:2]:
        plt.figure()
        sns.lineplot(data=df[col])
        plt.title(f"Trend of {col}")
        plots.append(plt.gcf())
        plt.close()

    return plots