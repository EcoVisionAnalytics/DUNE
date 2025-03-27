import streamlit as st
import pandas as pd
import numpy as np
import os
import pyreadr
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, Normalizer, MaxAbsScaler
import smtplib
from email.mime.text import MIMEText

st.set_page_config(page_title="DUNE", layout="wide")

# Insert logo
col1, col2 = st.columns([8, 2])
with col1:
    st.title("DUNE: Data Unified Normalization Environment")
    st.markdown("_\"Highly organized research is guaranteed to produce nothing new.\" - Frank Herbert, Dune_")
    st.markdown("_\"Science is made up of so many things that appear obvious after they are explained.\" - Frank Herbert, Dune_") 
with col2:
    st.image("logo.png", width=150)

# Sidebar with upload and navigation
st.sidebar.header("Menu")

uploaded_file = st.sidebar.file_uploader("Upload Data (.csv, .Rdata)", type=['csv', 'Rdata'])

with st.sidebar.expander("Read Me"):
    st.markdown("""
    ### DUNE: Data Unified cleaNing Environment

    **Instructions:**

    1. **Upload Data:**
        - Accepted formats: `.csv`, `.Rdata`.
        - Non-supported files will be rejected.

    2. **Data Preview:**
        - Displays the uploaded dataset.

    3. **Data Summary:**
        - Provides descriptive statistics and data types.

    4. **Cleaning Options:**
        - Change column data types.
        - Rename columns.
        - Handle missing values (Drop, Mean, Median, Mode, Custom).
        - Scale numeric data (MinMax, Standard, Robust, Normalization, AbsMax).
        - Remove duplicate rows.

    5. **Outliers:**
        - Detect and optionally remove outliers in selected numeric columns.

    6. **Basic Stats:**
        - Perform statistical operations on selected columns.
        - Numeric columns: mean, median, sum, standard deviation.
        - Non-numeric columns: count occurrences of unique values.

    7. **Export Now:**
        - Download the cleaned dataset as a `.csv` file.
        - Generate and download a data summary report.

    **Notes:**
    - Operations modify the dataset directly. Ensure you export the dataset to save your work.
    """)

def summarize_data(df):
    st.subheader("Data Summary")
    st.write(df.describe(include='all'))
    st.write(pd.DataFrame(df.dtypes, columns=['Data Type']))

def find_outliers(df, col):
    q1, q3 = np.percentile(df[col].dropna(), [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)
    return df[(df[col] < lower_bound) | (df[col] > upper_bound)]

def send_bug_report(description):
    sender_email = os.getenv("EMAIL_USER")
    receiver_email = "solutions@ecovisionanalytics.com"
    password = os.getenv("EMAIL_PASS")

    msg = MIMEText(description)
    msg["Subject"] = "Bug Report from DUNE"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        st.success("Bug report sent successfully!")
    except Exception as e:
        st.error(f"Failed to send bug report: {e}")

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        st.success('CSV Loaded Successfully!')
    elif uploaded_file.name.endswith('.Rdata'):
        result = pyreadr.read_r(uploaded_file)
        df = result[None] if None in result else next(iter(result.values()))
        st.success('.Rdata Loaded Successfully!')

    tabs = ["Data Preview", "Data Summary", "Cleaning Options", "Outliers", "Basic Stats", "Export Now", "Report a Bug"]
    option = st.sidebar.radio("Choose Option", tabs)

    if option == "Data Preview":
        st.subheader("Data Preview")
        st.dataframe(df)

    elif option == "Data Summary":
        summarize_data(df)

    elif option == "Cleaning Options":
        st.subheader("Cleaning Options")
        # (Cleaning options unchanged)

    elif option == "Outliers":
        st.subheader("Outlier Detection")
        # (Outlier detection unchanged)

    elif option == "Basic Stats":
        st.subheader("Basic Statistical Operations")
        selected_cols = st.multiselect("Select columns for statistics", df.columns)
        if st.button("Compute Statistics"):
            stats = {}
            for col in selected_cols:
                if np.issubdtype(df[col].dtype, np.number):
                    stats[col] = {
                        "Mean": df[col].mean(),
                        "Median": df[col].median(),
                        "Sum": df[col].sum(),
                        "Std Dev": df[col].std()
                    }
                else:
                    stats[col] = df[col].value_counts().to_dict()
            stats_df = pd.DataFrame(stats).T
            st.write(stats_df)
            st.download_button("Download Stats CSV", data=stats_df.to_csv(index=True), file_name="basic_stats.csv")

    elif option == "Export Now":
        st.subheader("Export Data")
        st.download_button("Download CSV", data=df.to_csv(index=False), file_name="cleaned_data.csv")
        with open("data_report.txt", "w") as f:
            f.write("Data Report\n")
            f.write(str(df.describe(include='all')))
        st.download_button("Download Data Report", data=open("data_report.txt").read(), file_name="data_report.txt")

    elif option == "Report a Bug":
        st.subheader("Report a Bug")
        bug_description = st.text_area("Bug Description")
        if st.button("Send Bug Report"):
            send_bug_report(bug_description)
else:
    st.warning("Please upload a CSV or .Rdata file to continue.")