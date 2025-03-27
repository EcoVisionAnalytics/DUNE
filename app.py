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
    ### DUNE: Data Unified Normalization Environment

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
        - Detect and optionally remove outliers in selected numeric columns (IQR method).

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

        with st.expander("Change Data Types"):
            col_dtype = st.selectbox("Select column to change type", df.columns)
            dtype = st.selectbox("Select new type", ["int", "float", "str"])
            if st.button("Apply Type Change"):
                try:
                    df[col_dtype] = df[col_dtype].astype(dtype)
                    st.success(f"{col_dtype} converted to {dtype}.")
                except Exception as e:
                    st.error(f"Type conversion failed: {e}")

        with st.expander("Rename Columns"):
            col_rename = st.selectbox("Select column to rename", df.columns)
            new_name = st.text_input("New column name")
            if st.button("Apply Rename") and new_name:
                df.rename(columns={col_rename: new_name}, inplace=True)
                st.success(f"Renamed {col_rename} to {new_name}.")

        with st.expander("Handle Missing Values"):
            na_col = st.selectbox("Column to handle NAs", df.columns)
            method = st.selectbox("NA handling method", ["Drop NA", "Mean", "Median", "Mode", "Custom Value"])
            custom_val = None
            if method == "Custom Value":
                custom_val = st.text_input("Custom value")

            if st.button("Apply NA Handling"):
                try:
                    if method == "Drop NA":
                        df.dropna(subset=[na_col], inplace=True)
                    elif method == "Mean":
                        df[na_col].fillna(df[na_col].mean(), inplace=True)
                    elif method == "Median":
                        df[na_col].fillna(df[na_col].median(), inplace=True)
                    elif method == "Mode":
                        df[na_col].fillna(df[na_col].mode()[0], inplace=True)
                    elif method == "Custom Value":
                        df[na_col].fillna(custom_val, inplace=True)
                    st.success(f"Missing values handled in {na_col}.")
                except Exception as e:
                    st.error(f"Error handling missing data: {e}")

        with st.expander("Scale Data"):
            num_cols = df.select_dtypes(include=np.number).columns.tolist()
            scale_col = st.selectbox("Select column to scale", num_cols)
            method = st.selectbox("Select scaling method", ["MinMax", "Standard", "Robust", "Normalization", "AbsMax"])

            if st.button("Apply Scaling"):
                try:
                    scaler = {
                        "MinMax": MinMaxScaler(),
                        "Standard": StandardScaler(),
                        "Robust": RobustScaler(),
                        "Normalization": Normalizer(),
                        "AbsMax": MaxAbsScaler()
                    }[method]
                    df[scale_col] = scaler.fit_transform(df[[scale_col]])
                    st.success(f"{scale_col} scaled with {method}.")
                except Exception as e:
                    st.error(f"Scaling failed: {e}")

        with st.expander("Remove Duplicates"):
            if st.button("Remove Duplicates"):
                df.drop_duplicates(inplace=True)
                st.success("Duplicates removed.")

    elif option == "Outliers":
        st.subheader("Outlier Detection")

        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if not numeric_cols:
            st.warning("No numeric columns found for outlier detection.")
        else:
            selected_col = st.selectbox("Select a numeric column", numeric_cols)
            detect = st.button("Detect Outliers")

            if detect:
                outliers = find_outliers(df, selected_col)
                if outliers.empty:
                    st.info("No outliers detected.")
                else:
                    st.write("Outliers found:")
                    st.dataframe(outliers)

                    if st.button("Remove Outliers Now"):
                        df.drop(outliers.index, inplace=True)
                        st.success(f"Outliers removed from {selected_col}.")

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