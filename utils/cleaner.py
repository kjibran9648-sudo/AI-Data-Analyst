def get_nulls(df):
    return df.isnull().sum()

def remove_nulls(df):
    return df.dropna()

def fill_nulls(df):
    return df.fillna(df.mean(numeric_only=True))

def remove_duplicates(df):
    return df.drop_duplicates()