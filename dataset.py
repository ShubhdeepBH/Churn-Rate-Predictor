import pandas as pd
import numpy as np


num_records = 200

data = {
    "CustomerID": [f"CUST{i+1:03d}" for i in range(num_records)],
    "Tenure": np.random.randint(1, 72, num_records),  
    "MonthlyCharges": np.round(np.random.uniform(20, 120, num_records), 2),  
    "TotalCharges": np.round(np.random.uniform(100, 5000, num_records), 2),  
    "ContractType": np.random.choice([0, 1, 2], num_records),
    "PaymentMethod": np.random.choice(["Credit Card", "Bank Transfer", "PayPal", "Mailed Check"], num_records),
}


df = pd.DataFrame(data)


csv_filename = "customer_data_no_churn.csv"
df.to_csv(csv_filename, index=False)

print(f" CSV file '{csv_filename}' generated successfully! (No Churn column)")
