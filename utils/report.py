from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import seaborn as sns

def generate_pdf_report(df, insights, filename="report.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(Paragraph("AI Data Analysis Report", styles['Title']))
    content.append(Spacer(1, 10))

    # Basic Info
    content.append(Paragraph(f"Rows: {df.shape[0]}", styles['Normal']))
    content.append(Paragraph(f"Columns: {df.shape[1]}", styles['Normal']))
    content.append(Spacer(1, 10))

    # Missing Values
    missing = df.isnull().sum().sum()
    content.append(Paragraph(f"Missing Values: {missing}", styles['Normal']))
    content.append(Spacer(1, 10))

    # Insights
    content.append(Paragraph("Insights:", styles['Heading2']))
    for i in insights:
        content.append(Paragraph(i["message"], styles['Normal']))
        content.append(Spacer(1, 5))

    # 🔥 Add Visualization (Seaborn Heatmap)
    try:
        plt.figure(figsize=(6,4))
        sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
        plt.title("Correlation Heatmap")

        img_path = "heatmap.png"
        plt.savefig(img_path)
        plt.close()

        content.append(Spacer(1, 10))
        content.append(Paragraph("Correlation Heatmap:", styles['Heading2']))
        content.append(Image(img_path, width=400, height=300))
    except:
        pass

    # 🔥 Distribution Plot
    try:
        num_cols = df.select_dtypes(include='number').columns[:1]

        if len(num_cols) > 0:
            plt.figure()
            sns.histplot(df[num_cols[0]], kde=True)
            plt.title(f"Distribution of {num_cols[0]}")

            img_path2 = "dist.png"
            plt.savefig(img_path2)
            plt.close()

            content.append(Spacer(1, 10))
            content.append(Paragraph("Distribution Plot:", styles['Heading2']))
            content.append(Image(img_path2, width=400, height=300))
    except:
        pass

    doc.build(content)

    return filename