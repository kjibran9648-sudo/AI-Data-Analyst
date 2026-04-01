from ydata_profiling import ProfileReport

def generate_profile(df):
    profile = ProfileReport(df, explorative=True)
    return profile