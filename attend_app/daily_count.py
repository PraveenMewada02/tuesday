# #working well good.
# import pandas as pd
# from sqlalchemy import create_engine, text
# import requests
# import base64
# from datetime import datetime


# # Database URL
# database_url = "postgres://default:uWiPqh7zO4SQ@ep-square-wood-a15wl9fx.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=require"
# engine = create_engine(database_url)

# # API credentials
# api_url_template = "https://api.etimeoffice.com/api/DownloadInOutPunchData?Empcode=ALL&FromDate={}&ToDate={}"
# api_key = "ORANGEDATATECH:HR@Orange:UY7g2#!gWEA6kB8:true"

# # Encode the API key in base64
# base64_api_key = base64.b64encode(api_key.encode()).decode()

# headers = {
#     "Authorization": f"Basic {base64_api_key}",
#     "Content-Type": "application/json",
# }

# # Function to fetch data from the API
# def fetch_data_from_api(date):
#     formatted_date = date.strftime('%d/%m/%Y')
#     api_url = api_url_template.format(formatted_date, formatted_date)
#     try:
#         response = requests.get(api_url, headers=headers)
#         if response.status_code == 200:
#             return response.json().get('InOutPunchData', [])
#         else:
#             print(f"Error: {response.status_code} - {response.text}")
#             return []
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return []

# # Function to store data in PostgreSQL database
# def store_data(df, table_name):
#     df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
#     print(f"DataFrame successfully stored in table '{table_name}'")

# # Function to create or clear the daily table
# def create_or_clear_daily_table(table_name, date_str):
#     with engine.connect() as connection:
#         # Ensure the table exists with correct column names
#         connection.execute(text(f"""
#             CREATE TABLE IF NOT EXISTS {table_name} (
#                 empcode TEXT,
#                 intime TEXT,
#                 outtime TEXT,
#                 worktime TEXT,
#                 overtime TEXT,
#                 breaktime TEXT,
#                 status TEXT,
#                 datestring TEXT,
#                 remark TEXT,
#                 erl_out TEXT,
#                 late_in TEXT,
#                 name TEXT,
#                 PRIMARY KEY (empcode, datestring)
#             );
#         """))
        
#         # Clear data that is not for the specified date
#         connection.execute(text(f"TRUNCATE TABLE {table_name}"))
#         connection.commit()
        
#         print(f"Table '{table_name}' is ready to store/update data for date {date_str}")

# # Function to analyze the data
# def analyze_data(df):
#     df['INTime'] = pd.to_datetime(df['INTime'], errors='coerce').dt.time
#     df['OUTTime'] = pd.to_datetime(df['OUTTime'], errors='coerce').dt.time
#     reference_time = datetime.strptime('10:15', '%H:%M').time()

#     ontime_count = df[df['INTime'] <= reference_time].shape[0]
#     latein_count = df[df['INTime'] > reference_time].shape[0]
#     absent_count = df[df['INTime'].isna() & df['OUTTime'].isna()].shape[0]

#     print(f"ONTime: {ontime_count}")
#     print(f"LateIN: {latein_count}")
#     print(f"Absent: {absent_count}")

# # Main execution flow
# #TABLE NAME
# daily_table_name = "daily_count" 
# date_input = input("Enter the date (dd/mm/yyyy): ") #datetime.today().strftime('%d/%m/%Y') #

# # Validate the date format
# try:
#     date_object = datetime.strptime(date_input, '%d/%m/%Y')
#     date_str = date_object.strftime('%d/%m/%Y')
# except ValueError:
#     print("Incorrect date format, should be dd/mm/yyyy")
# else:
#     # Fetch data from API
#     data = fetch_data_from_api(date_object)
#     if not data:
#         print(f"No data found for the entered date: {date_input}")
#     else:
#         # Create a DataFrame with the desired columns
#         df = pd.DataFrame(data, columns=[
#             'Empcode', 'INTime', 'OUTTime', 'WorkTime', 'OverTime', 'BreakTime', 
#             'Status', 'DateString', 'Remark', 'Erl_Out', 'Late_In', 'Name'
#         ])
#         # Ensure the DateString column is consistent
#         df['DateString'] = date_str
        
#         # Create or clear the daily table before inserting new data
#         create_or_clear_daily_table(daily_table_name, date_str)
        
#         # Store the data in the daily table
#         store_data(df, daily_table_name)
        
#         # Perform the analysis on the data
#         analyze_data(df)
        
#         print("Data for the specified date:")
#         print(df)


import pandas as pd
from sqlalchemy import create_engine
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Database URL
database_url = "postgres://default:uWiPqh7zO4SQ@ep-square-wood-a15wl9fx.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=require"
engine = create_engine(database_url)

# Email configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'pravinmewada1999@gmail.com'  # Your email address
smtp_password = 'nczy qogr vofn kmcv'  # Your email password

# Function to send email
def send_email(to_address, subject, body):
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username, to_address, text)
        server.quit()
        print(f"Email sent to {to_address}")
    except Exception as e:
        print(f"Failed to send email to {to_address}: {e}")

# Main execution flow
if __name__ == "__main__":
    table_name = "attend_app_count_number"
    employee_details_table = "attend_app_employee_details"
    date_input = input("Enter the date (dd/mm/yyyy): ")

    # Validate the date format
    try:
        date_object = datetime.strptime(date_input, '%d/%m/%Y')
    except ValueError:
        print("Incorrect date format, should be dd/mm/yyyy")
    else:
        formatted_date = date_object.strftime('%d/%m/%Y')

        # Query to fetch attendance data for the given date
        query = f"""
            SELECT * FROM {table_name}
            WHERE DateString = '{formatted_date}'
        """
        df = pd.read_sql(query, engine)

        # Filter based on null or '--:--' entries in INTime
        filtered_df = df[(df['INTime'].isnull()) | (df['INTime'] == '--:--')]

        if filtered_df.empty:
            print(f"No people found with missing entries on {date_input}")
        else:
            emp_codes_with_issues = filtered_df['Empcode'].tolist()
            print(f"Empcodes with missing entries on {date_input}: {emp_codes_with_issues}")

            # Query to fetch email addresses for the employees with missing INTime
            emp_codes_str = "','".join(emp_codes_with_issues)
            email_query = f"""
                SELECT emp_code, email FROM {employee_details_table}
                WHERE emp_code IN ('{emp_codes_str}')
            """
            email_df = pd.read_sql(email_query, engine)

            # Send emails to employees with missing INTime
            for index, row in email_df.iterrows():
                emp_code = row['emp_code']
                email = row['email']
                subject = "Missing In Time Alert"
                body = f"""Hi,\n\nYou have a missing In time entry on {date_input}. Please rectify this as soon as possible.\n\nThank you."""
                send_email(email, subject, body)

            print(f"Emails sent to employees with missing INTime on {date_input}")

            # Print the DataFrame for verification
            print("Data for the specified date:")
            print(df)
