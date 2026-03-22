import pandas as pd
import sqlite3
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def train_and_save_model(db_path='phonepe_pulse.db', model_dir='models'):
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    print("Connecting to database...")
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT State, Year, Quarter, Transaction_Type, Transaction_Amount FROM aggregated_transaction", conn)
    conn.close()

    print("Preprocessing data...")
    # Convert types
    df['Year'] = df['Year'].astype(int)
    df['Quarter'] = df['Quarter'].astype(int)

    # Encode categorical variables
    le_state = LabelEncoder()
    le_type = LabelEncoder()
    df['State_Encoded'] = le_state.fit_transform(df['State'])
    df['Type_Encoded'] = le_type.fit_transform(df['Transaction_Type'])

    # Features and Target
    X = df[['State_Encoded', 'Year', 'Quarter', 'Type_Encoded']]
    y = df['Transaction_Amount']

    print("Training model...")
    # Using a subset or full data depends on size, but RF handles this well
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    print(f"Model Score (R2): {model.score(X_test, y_test):.4f}")

    print("Saving model and encoders...")
    joblib.dump(model, os.path.join(model_dir, 'rf_model.joblib'))
    joblib.dump(le_state, os.path.join(model_dir, 'le_state.joblib'))
    joblib.dump(le_type, os.path.join(model_dir, 'le_type.joblib'))
    
    # Save the categories for the UI
    categories = {
        'states': sorted(df['State'].unique().tolist()),
        'types': sorted(df['Transaction_Type'].unique().tolist())
    }
    joblib.dump(categories, os.path.join(model_dir, 'metadata.joblib'))

    print("Training complete! Model and encoders saved in 'models/'")

if __name__ == "__main__":
    train_and_save_model()
