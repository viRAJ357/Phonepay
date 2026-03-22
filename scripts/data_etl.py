import os
import json
import pandas as pd
import sqlite3

def extract_data(base_path):
    all_data = {
        'aggregated_transaction': [],
        'aggregated_user': [],
        'aggregated_insurance': [],
        'map_transaction': [],
        'map_user': [],
        'map_insurance': [],
        'top_transaction': [],
        'top_user': [],
        'top_insurance': []
    }

    categories = ['aggregated', 'map', 'top']
    types = ['transaction', 'user', 'insurance']

    for cat in categories:
        for t in types:
            if cat == 'map':
                path = os.path.join(base_path, cat, t, 'hover', 'country', 'india', 'state')
            else:
                path = os.path.join(base_path, cat, t, 'country', 'india', 'state')
            
            if not os.path.exists(path):
                print(f"Path does not exist: {path}")
                continue
            
            table_name = f"{cat}_{t}"
            for state in os.listdir(path):
                state_path = os.path.join(path, state)
                for year in os.listdir(state_path):
                    year_path = os.path.join(state_path, year)
                    for file in os.listdir(year_path):
                        if file.endswith('.json'):
                            quarter = file.split('.')[0]
                            file_path = os.path.join(year_path, file)
                            try:
                                with open(file_path, 'r') as f:
                                    json_data = json.load(f)
                                
                                if not json_data.get('success'):
                                    continue
                                
                                data = json_data.get('data')
                                if not data:
                                    continue

                                # Aggregated
                                if cat == 'aggregated' and t == 'transaction':
                                    for row in data.get('transactionData', []):
                                        all_data[table_name].append({
                                            'State': state, 'Year': year, 'Quarter': int(quarter),
                                            'Transaction_Type': row['name'],
                                            'Transaction_Count': row['paymentInstruments'][0]['count'],
                                            'Transaction_Amount': row['paymentInstruments'][0]['amount']
                                        })
                                elif cat == 'aggregated' and t == 'user':
                                    users_by_brand = data.get('usersByDevice')
                                    if users_by_brand:
                                        for row in users_by_brand:
                                            all_data[table_name].append({
                                                'State': state, 'Year': year, 'Quarter': int(quarter),
                                                'Brand': row['brand'], 'Count': row['count'], 'Percentage': row['percentage']
                                            })
                                elif cat == 'aggregated' and t == 'insurance':
                                    for row in data.get('transactionData', []):
                                        all_data[table_name].append({
                                            'State': state, 'Year': year, 'Quarter': int(quarter),
                                            'Insurance_Type': row['name'],
                                            'Transaction_Count': row['paymentInstruments'][0]['count'],
                                            'Transaction_Amount': row['paymentInstruments'][0]['amount']
                                        })
                                
                                # Map
                                elif cat == 'map' and t == 'transaction':
                                    for row in data.get('hoverDataList', []):
                                        all_data[table_name].append({
                                            'State': state, 'Year': year, 'Quarter': int(quarter),
                                            'District': row['name'],
                                            'Transaction_Count': row['metric'][0]['count'],
                                            'Transaction_Amount': row['metric'][0]['amount']
                                        })
                                elif cat == 'map' and t == 'user':
                                    hover_data = data.get('hoverData')
                                    if hover_data:
                                        for district, info in hover_data.items():
                                            all_data[table_name].append({
                                                'State': state, 'Year': year, 'Quarter': int(quarter),
                                                'District': district,
                                                'RegisteredUsers': info['registeredUsers'],
                                                'AppOpens': info['appOpens']
                                            })
                                elif cat == 'map' and t == 'insurance':
                                    for row in data.get('hoverDataList', []):
                                        all_data[table_name].append({
                                            'State': state, 'Year': year, 'Quarter': int(quarter),
                                            'District': row['name'],
                                            'Transaction_Count': row['metric'][0]['count'],
                                            'Transaction_Amount': row['metric'][0]['amount']
                                        })
                                
                                # Top
                                elif cat == 'top' and t == 'transaction':
                                    for row in data.get('districts', []):
                                        all_data[table_name].append({
                                            'State': state, 'Year': year, 'Quarter': int(quarter),
                                            'District': row['entityName'],
                                            'Transaction_Count': row['metric']['count'],
                                            'Transaction_Amount': row['metric']['amount']
                                        })
                                elif cat == 'top' and t == 'user':
                                    for row in data.get('districts', []):
                                        all_data[table_name].append({
                                            'State': state, 'Year': year, 'Quarter': int(quarter),
                                            'District': row['name'],
                                            'RegisteredUsers': row['registeredUsers']
                                        })
                                elif cat == 'top' and t == 'insurance':
                                    for row in data.get('districts', []):
                                        all_data[table_name].append({
                                            'State': state, 'Year': year, 'Quarter': int(quarter),
                                            'District': row['entityName'],
                                            'Transaction_Count': row['metric']['count'],
                                            'Transaction_Amount': row['metric']['amount']
                                        })
                            except Exception as e:
                                print(f"Error processing {file_path}: {e}")
    return all_data

def save_to_sql(all_data, db_name='phonepe_pulse.db'):
    conn = sqlite3.connect(db_name)
    for table_name, data in all_data.items():
        if data:
            df = pd.DataFrame(data)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"Stored {len(df)} rows in {table_name}")
    conn.close()

if __name__ == "__main__":
    base_data_path = 'data/pulse/data'
    print("Extracting data...")
    all_data = extract_data(base_data_path)
    print("Saving to SQL...")
    save_to_sql(all_data)
    print("ETL process completed successfully!")
