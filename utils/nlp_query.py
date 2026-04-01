def process_query(query, df):
    query = query.lower()

    if "null" in query:
        return df.isnull().sum()

    elif "correlation" in query:
        return df.corr(numeric_only=True)

    elif "summary" in query:
        return df.describe()

    elif "columns" in query:
        return df.columns.tolist()

    elif "shape" in query:
        return df.shape

    elif "duplicates" in query:
        return df.duplicated().sum()

    else:
        return "❌ Sorry, I didn't understand the query"