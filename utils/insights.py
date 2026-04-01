def generate_insights(df):
    insights = []

    # 🔹 Missing values (ANY level)
    null_counts = df.isnull().sum()
    for col, val in null_counts.items():
        if val > 0:
            insights.append({
                "type": "missing",
                "message": f"⚠️ Column '{col}' has {val} missing values",
                "column": col,
                "count": val
            })

    # 🔹 Duplicate rows
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        insights.append({
            "type": "duplicate",
            "message": f"⚠️ Dataset contains {duplicate_count} duplicate rows",
            "count": duplicate_count
        })

    # 🔹 Correlation check
    try:
        corr = df.corr(numeric_only=True)
        for col in corr.columns:
            for row in corr.index:
                if col != row and abs(corr.loc[col, row]) > 0.8:
                    insights.append({
                        "type": "correlation",
                        "message": f"📊 High correlation between '{col}' and '{row}' ({corr.loc[col,row]:.2f})"
                    })
    except:
        pass

    return insights


def data_quality_score(df):
    total_cells = df.size

    missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()

    score = 100 - ((missing / total_cells) * 50 + (duplicates / len(df)) * 50)

    return round(score, 2)