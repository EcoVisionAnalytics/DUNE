🌵 DUNE: Data Unified Normalization Environment

"Highly organized research is guaranteed to produce nothing new."— Frank Herbert, Dune

🧹 Welcome to DUNE!

DUNE (Data Unified Normalization Environment) is your all-in-one toolkit designed to simplify and streamline the process of cleaning, transforming, and analyzing your data. Built with scientists, ecologists, and researchers in mind, DUNE allows you to quickly and efficiently prepare your datasets for insightful analyses.

Created and maintained by EcoVision Analytics, we strive to deliver open-source, cutting-edge analytical tools to the ecological and scientific communities. Our mission is to elevate data-driven decision-making and bring next-level analytical capability directly to your research.

🚀 Key Features

📂 Upload & Go

Easily ingest .csv and .Rdata files.

Automatic rejection of unsupported file formats to ensure data integrity.

🔎 Explore Your Data

Instant data preview and dynamic sorting.

Comprehensive summaries including descriptive statistics and data type overviews.

🛠️ Powerful Data Cleaning

Convert data types, rename columns, and manage missing values with ease.

Impute or remove missing data using intuitive methods (mean, median, mode, or custom).

Scale numeric columns effortlessly: Absolute Maximum, Min-Max, Normalization, Standardization, and Robust Scaling.

Quickly identify and remove duplicate records.

📊 Advanced Statistical Insights

Detect and manage outliers effectively.

Compute fundamental statistics on numeric data including mean, median, sum, and standard deviation.

Count and analyze occurrences within categorical or textual data effortlessly.

💾 Export & Report

Export cleaned datasets as .csv files.

Automatically generate comprehensive data summary reports to document your cleaning process.

🐞 Bug Reporting Made Easy

Encountered an issue? Quickly report bugs directly from within the app, ensuring rapid resolution and continuous improvement.

📖 Getting Started

Running DUNE Locally:

Clone this repository:

git clone https://github.com/your-username/DUNE-App.git

Navigate into the directory:

cd DUNE-App

Install dependencies:

pip install -r requirements.txt

Run the app locally:

streamlit run app.py

🌿 About EcoVision Analytics

At EcoVision Analytics, we're dedicated to empowering scientists and ecologists with open-source tools designed for impactful research. Our focus is on enabling deeper insights, smarter decisions, and better stewardship of our natural world through advanced analytics.

Learn more about our mission and tools.

📬 Questions & Support

Report bugs or request features directly through DUNE.

Contact us: solutions@ecovisionanalytics.com

Let's transform data into actionable knowledge, together!

🌎🌱📈

✅ Latest Fixes

Outlier Detection:

Buttons now trigger detection and removal correctly.

Results are shown in a table with proper user confirmation.

Cleaning Options:

All operations (rename, change type, impute, scale, remove duplicates) are separated into expandable sections.

Improved error handling and feedback display.

These improvements ensure smoother workflows and better visibility of your transformations!