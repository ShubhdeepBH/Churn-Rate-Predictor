import pandas as pd
import numpy as np


np.random.seed(42)


num_samples = 1000


columns = ['CustomerID', 'SubscriptionType', 'OrderFrequency', 'TotalSpend', 
           'NumOrders', 'DeliveryPreference', 'AvgOrderValue', 'CustomerRating']


df = pd.DataFrame({
    'CustomerID': range(2001, 2001 + num_samples),
    'SubscriptionType': np.random.choice(['Basic', 'Premium'], num_samples),  
    'OrderFrequency': np.random.choice(['Daily', 'Weekly', 'Monthly'], num_samples),  
    'TotalSpend': np.random.randint(50, 5000, size=num_samples),
    'NumOrders': np.random.randint(1, 200, size=num_samples),  
    'DeliveryPreference': np.random.choice(['Home Delivery', 'Pick-up'], num_samples),  
    'AvgOrderValue': np.round(np.random.uniform(10, 150, size=num_samples), 2),  
    'CustomerRating': np.round(np.random.uniform(1, 5, size=num_samples), 2),  
    
})


 
print(df.head())


df.to_csv('food_delivery_service_data222.csv', index=False)


print("Dataset saved as 'food_delivery_service_data.csv222'.")
