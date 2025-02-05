import pandas as pd
import numpy as np


def generate_netflix_data():
    data = {
        'CustomerID': np.arange(2001, 2201),
        'SubscriptionType': np.random.choice(['Basic', 'Standard', 'Premium'], 200),
        'MonthlyFee': np.random.choice([8.99, 13.99, 17.99], 200),
        'TotalWatchHours': np.random.randint(50, 700, 200),
        'NumDevices': np.random.randint(1, 6, 200),
        'HasAutoRenew': np.random.choice([0, 1], 200),
        'LastPaymentMissed': np.random.choice([0, 1], 200),
        'AvgWatchTimePerDay': np.random.uniform(0.5, 6.5, 200),
        'CancelledBefore': np.random.choice([0, 1], 200) 
    }
    df = pd.DataFrame(data)
    df.rename(columns={'CancelledBefore': 'Churn'}, inplace=True)  
    
    
    df.to_csv('netflix_data.csv', index=False)
    print("Dataset saved as 'netflix_data2.csv'")


generate_netflix_data()
