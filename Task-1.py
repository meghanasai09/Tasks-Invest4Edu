import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
 
def generate_report_cards(file_path):
    try:
        data = pd.read_excel(file_path)
        if not all(col in data.columns for col in ['Student ID', 'Name', 'Subject', 'Score']):
            raise ValueError("Missing required columns in the Excel file.")
        if data.isnull().any().any():
            raise ValueError("The Excel file contains missing data.")
        grouped = data.groupby('Student ID')
        student_data = {}
        for student_id, group in grouped:
            name = group['Name'].iloc[0]
            total_score = group['Score'].sum()
            avg_score = group['Score'].mean()
            scores = group[['Subject', 'Score']].values.tolist()
            student_data[student_id] = {'Name': name, 'Total': total_score, 'Average': avg_score, 'Scores': scores}
        styles = getSampleStyleSheet()  
        for student_id, info in student_data.items():
            pdf_file = f"report_card_{student_id}.pdf"
            doc = SimpleDocTemplate(pdf_file, pagesize=letter)
            elements = []
            elements.append(Paragraph(f"Report Card for {info['Name']}", styles['Title']))
            elements.append(Paragraph(f"Total Score: {info['Total']}", styles['Normal']))
            elements.append(Paragraph(f"Average Score: {info['Average']:.2f}", styles['Normal']))
            table_data = [['Subject', 'Score']] + info['Scores']
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)
            doc.build(elements)
        print("Report cards generated successfully!")
    except Exception as e:
        print(f"Error: {e}")
 
generate_report_cards('C:/Users/ASUS/OneDrive/Desktop/Task-1.xlsx')