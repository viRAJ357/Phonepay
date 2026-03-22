# PhonePe Pulse Data Visualization and Analysis deploy link https://viraj357-phonepay-app-jokpqy.streamlit.app/

## Project Overview
This project is a comprehensive data visualization and exploration tool for PhonePe Pulse data (2018 - 2024). It provides an interactive dashboard to explore transaction trends, user demographics, insurance penetration, and future growth predictions across India.

## Core Features
- **ETL Pipeline**: Automated script (`scripts/data_etl.py`) to fetch and transform raw JSON data into a structured SQLite database.
- **Interactive Maps**: Choropleth maps visualizing transaction hotspots across Indian states.
- **Insurance Insights**: Dedicated analysis of digital insurance purchasing patterns.
- **Top 10 Rankings**: Leaderboards for states and districts based on transaction volume and user growth.
- **ML Forecasting**: A Random Forest model to predict future quarterly transaction amounts for specific states and categories.

## Project Structure
- `app.py`: Main Streamlit application.
- `scripts/`:
  - `data_etl.py`: Data extraction and transformation script.
  - `train_model.py`: ML training script for growth forecasting.
- `models/`: Saved Random Forest model and label encoders.
- `notebooks/`: EDA and ML submission notebooks.
- `data/`: Raw data from the PhonePe Pulse repository.
- `phonepe_pulse.db`: Consolidated SQLite database.

## Installation & Usage
1. **Clone the repository**.
2. **Install dependencies**:
   ```bash
   pip install pandas sqlite3 streamlit plotly joblib scikit-learn
   ```
3. **Run ETL (Optional)**:
   ```bash
   python scripts/data_etl.py
   ```
4. **Train Model (Optional)**:
   ```bash
   python scripts/train_model.py
   ```
5. **Launch Dashboard**:
   ```bash
   streamlit run app.py
   ```

## Technologies Used
- **Python**: Core logic and data processing.
- **SQLite**: Reliable local data storage.
- **Streamlit**: Modern, interactive web framework.
- **Plotly**: Premium data visualizations and maps.
- **Scikit-learn**: Machine learning and predictive modeling.

Developed by Nikhil Kumar | LabMentix Data Science Internship
