import pandas as pd
import numpy as np


np.random.seed(42)


num_samples = 1000


columns = ['CustomerID', 'SubscriptionType', 'MonthlyFee', 'TotalListenHours', 
           'NumDevices', 'HasAutoRenew', 'LastPaymentMissed', 
           'AvgListenTimePerDay']


df = pd.DataFrame({
    'CustomerID': range(2001, 2001 + num_samples),
    'SubscriptionType': np.random.choice(['Free', 'Premium'], num_samples),
    'MonthlyFee': np.random.choice([0, 9.99], num_samples),  
    'TotalListenHours': np.random.randint(10, 1000, size=num_samples),
    'NumDevices': np.random.randint(1, 6, size=num_samples),
    'HasAutoRenew': np.random.choice([0, 1], num_samples),
    'LastPaymentMissed': np.random.choice([0, 1], num_samples),
    'AvgListenTimePerDay': np.round(np.random.uniform(0.5, 10.0, size=num_samples), 2),
})


print(df.head())


df.to_csv('spotify_no_churn.csv', index=False)


print("Dataset saved as 'spotify_no_churn.csv'.")
