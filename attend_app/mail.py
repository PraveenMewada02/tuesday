import pandas as pd
from sqlalchemy import create_engine, exc
from sqlalchemy.dialects import postgresql  # Ensure PostgreSQL dialect is explicitly imported
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Database URL
database_url = "postgresql://default:uWiPqh7zO4SQ@ep-square-wood-a15wl9fx.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=require"

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
    try:
        # Attempt to connect to the database
        engine = create_engine(database_url)
        connection = engine.connect()

        # Query to fetch attendance data for the given date
        table_name = "attend_app_count_number"
        employee_details_table = "attend_app_employee_details"
        date_input = input("Enter the date (dd/mm/yyyy): ")

        # Validate the date format
        date_object = datetime.strptime(date_input, '%d/%m/%Y')
        formatted_date = date_object.strftime('%d/%m/%Y')

        query = f"""
            SELECT * FROM {table_name}
            WHERE DateString = '{formatted_date}'
        """
        df = pd.read_sql(query, connection)

        # Filter based on null or '--:--' entries in INTime
        filtered_df = df[(df['intime'].isnull()) | (df['intime'] == '--:--')]

        if filtered_df.empty:
            print(f"No people found with missing entries on {date_input}")
        else:
            emp_codes_with_issues = filtered_df['empcode'].tolist()
            print(f"Empcodes with missing entries on {date_input}: {emp_codes_with_issues}")

            # Query to fetch email addresses for the employees with missing INTime
            emp_codes_str = "','".join(emp_codes_with_issues)
            email_query = f"""
                SELECT emp_code, email FROM {employee_details_table}
                WHERE emp_code IN ('{emp_codes_str}')
            """
            email_df = pd.read_sql(email_query, connection)

            # Send emails to employees with missing INTime
            for index, row in email_df.iterrows():
                emp_code = row['emp_code']
                email = row['email']
                subject = "Missing In Time Alert"
                body = f"""Dear,\n\n
I hope this message finds you well. I am writing to bring to your attention a missing "In Time" entry on {date_input}.\n
I kindly request that you please rectify this issue as soon as possible.\n
Thank you for your prompt attention to this matter.\n\n
Best regards,\n OrnageDataTech Pvt Ltd"""
                send_email(email, subject, body)

            print(f"Emails sent to employees with missing INTime on {date_input}")

            # Print the DataFrame for verification
            print("Data for the specified date:")
            print(df)

    except exc.SQLAlchemyError as sql_error:
        print(f"SQLAlchemy error occurred: {sql_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if 'connection' in locals():
            connection.close()





















# import pandas as pd
# from sqlalchemy import create_engine, exc
# from sqlalchemy.dialects import postgresql  # Ensure PostgreSQL dialect is explicitly imported
# import smtplib
# import psycopg2
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from datetime import datetime
# from sqlalchemy import create_engine, exc
# from sqlalchemy.dialects.postgresql import psycopg2  # Explicitly import the PostgreSQL dialect


# # Database URL
# database_url = "postgres://default:uWiPqh7zO4SQ@ep-square-wood-a15wl9fx.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=require"

# # Email configuration
# smtp_server = 'smtp.gmail.com'
# smtp_port = 587
# smtp_username = 'pravinmewada1999@gmail.com'  # Your email address
# smtp_password = 'nczy qogr vofn kmcv'  # Your email password

# # Function to send email
# def send_email(to_address, subject, body):
#     msg = MIMEMultipart()
#     msg['From'] = smtp_username
#     msg['To'] = to_address
#     msg['Subject'] = subject

#     msg.attach(MIMEText(body, 'plain'))

#     try:
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()
#         server.login(smtp_username, smtp_password)
#         text = msg.as_string()
#         server.sendmail(smtp_username, to_address, text)
#         server.quit()
#         print(f"Email sent to {to_address}")
#     except Exception as e:
#         print(f"Failed to send email to {to_address}: {e}")

# # Main execution flow
# if __name__ == "__main__":
#     table_name = "attend_app_count_number"
#     employee_details_table = "attend_app_employee_details"
#     date_input = input("Enter the date (dd/mm/yyyy): ")

#     # Validate the date format
#     try:
#         date_object = datetime.strptime(date_input, '%d/%m/%Y')
#     except ValueError:
#         print("Incorrect date format, should be dd/mm/yyyy")
#     else:
#         formatted_date = date_object.strftime('%d/%m/%Y')

#         try:
#             # Attempt to connect to the database
#             engine = create_engine(database_url)
#             connection = engine.connect()

#             # Query to fetch attendance data for the given date
#             query = f"""
#                 SELECT * FROM {table_name}
#                 WHERE DateString = '{formatted_date}'
#             """
#             df = pd.read_sql(query, connection)

#             # Filter based on null or '--:--' entries in INTime
#             filtered_df = df[(df['intime'].isnull()) | (df['intime'] == '--:--')]

#             if filtered_df.empty:
#                 print(f"No people found with missing entries on {date_input}")
#             else:
#                 emp_codes_with_issues = filtered_df['empcode'].tolist()
#                 print(f"Empcodes with missing entries on {date_input}: {emp_codes_with_issues}")

#                 # Query to fetch email addresses for the employees with missing INTime
#                 emp_codes_str = "','".join(emp_codes_with_issues)
#                 email_query = f"""
#                     SELECT emp_code, email FROM {employee_details_table}
#                     WHERE emp_code IN ('{emp_codes_str}')
#                 """
#                 email_df = pd.read_sql(email_query, connection)

#                 # Send emails to employees with missing INTime
#                 for index, row in email_df.iterrows():
#                     emp_code = row['emp_code']
#                     email = row['email']
#                     subject = "Missing In Time Alert"
#                     body = f"""Dear,\n\n
#     I hope this message finds you well. I am writing to bring to your attention a missing "In Time" entry on {date_input}.\n
#     I kindly request that you please rectify this issue as soon as possible.\n
#     Thank you for your prompt attention to this matter.\n\n
#     Best regards,\n OrnageDataTech Pvt Ltd"""
#                     send_email(email, subject, body)

#                 print(f"Emails sent to employees with missing INTime on {date_input}")

#                 # Print the DataFrame for verification
#                 print("Data for the specified date:")
#                 print(df)

#         except exc.SQLAlchemyError as sql_error:
#             print(f"SQLAlchemy error occurred: {sql_error}")
#         except Exception as e:
#             print(f"An unexpected error occurred: {e}")
#         finally:
#             if 'connection' in locals():
#                 connection.close()


#                         #org
# # #Display the empcode whose intime is not present & also send the email
# # #Need view
# # import pandas as pd
# # from sqlalchemy import create_engine
# # import smtplib
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart
# # from datetime import datetime
# # from sqlalchemy.dialects import postgresql


# # # Database URL
# # database_url = "postgres://default:uWiPqh7zO4SQ@ep-square-wood-a15wl9fx.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=require"
# # engine = create_engine(database_url)

# # # Email configuration
# # smtp_server = 'smtp.gmail.com'
# # smtp_port = 587
# # smtp_username = 'pravinmewada1999@gmail.com'  # Your email address
# # smtp_password = 'nczy qogr vofn kmcv'  # Your email password

# # # Function to send email
# # def send_email(to_address, subject, body):
# #     msg = MIMEMultipart()
# #     msg['From'] = smtp_username
# #     msg['To'] = to_address
# #     msg['Subject'] = subject

# #     msg.attach(MIMEText(body, 'plain'))

# #     try:
# #         server = smtplib.SMTP(smtp_server, smtp_port)
# #         server.starttls()
# #         server.login(smtp_username, smtp_password)
# #         text = msg.as_string()
# #         server.sendmail(smtp_username, to_address, text)
# #         server.quit()
# #         print(f"Email sent to {to_address}")
# #     except Exception as e:
# #         print(f"Failed to send email to {to_address}: {e}")

# # # Main execution flow
# # if __name__ == "__main__":
# #     table_name = "attend_app_count_number"
# #     employee_details_table = "attend_app_employee_details"
# #     date_input = input("Enter the date (dd/mm/yyyy): ")

# #     # Validate the date format
# #     try:
# #         date_object = datetime.strptime(date_input, '%d/%m/%Y')
# #     except ValueError:
# #         print("Incorrect date format, should be dd/mm/yyyy")
# #     else:
# #         formatted_date = date_object.strftime('%d/%m/%Y')

# #         # Query to fetch attendance data for the given date
# #         query = f"""
# #             SELECT * FROM {table_name}
# #             WHERE DateString = '{formatted_date}'
# #         """
# #         df = pd.read_sql(query, engine)

# #         # Filter based on null or '--:--' entries in INTime
# #         filtered_df = df[(df['intime'].isnull()) | (df['intime'] == '--:--')]

# #         if filtered_df.empty:
# #             print(f"No people found with missing entries on {date_input}")
# #         else:
# #             emp_codes_with_issues = filtered_df['empcode'].tolist()
# #             print(f"Empcodes with missing entries on {date_input}: {emp_codes_with_issues}")

# #             # Query to fetch email addresses for the employees with missing INTime
# #             emp_codes_str = "','".join(emp_codes_with_issues)
# #             email_query = f"""
# #                 SELECT emp_code, email FROM {employee_details_table}
# #                 WHERE emp_code IN ('{emp_codes_str}')
# #             """
# #             email_df = pd.read_sql(email_query, engine)

# #             # Send emails to employees with missing INTime
# #             for index, row in email_df.iterrows():
# #                 emp_code = row['emp_code']
# #                 email = row['email']
# #                 subject = "Missing In Time Alert"
# #                 body = f"""Dear,\n\n
# # I hope this message finds you well. I am writing to bring to your attention a missing "In Time" entry on {date_input}.\n
# # I kindly request that you please rectify this issue as soon as possible.\n
# # Thank you for your prompt attention to this matter.\n\n
# # Best regards,\n OrnageDataTech Pvt Ltd"""
# #                 send_email(email, subject, body)

# #             print(f"Emails sent to employees with missing INTime on {date_input}")

# #             # Print the DataFrame for verification
# #             print("Data for the specified date:")
# #             print(df)
