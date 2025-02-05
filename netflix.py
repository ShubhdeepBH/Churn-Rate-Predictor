import pandas as pd
import numpy as np


np.random.seed(42)


num_users = 1000


customer_ids = np.arange(2001, 2001 + num_users)

subscription_types = ['Basic', 'Standard', 'Premium']
subscription_probs = [0.4, 0.4, 0.2]  

subscription_type = np.random.choice(subscription_types, size=num_users, p=subscription_probs)


monthly_fee = np.where(subscription_type == 'Basic', np.random.choice([8.99, 13.99, 17.99], size=num_users),
                       np.where(subscription_type == 'Standard', np.random.choice([8.99, 13.99, 17.99], size=num_users),
                                np.random.choice([8.99, 13.99, 17.99], size=num_users)))


total_watch_hours = np.random.randint(50, 700, size=num_users)


num_devices = np.random.randint(1, 6, size=num_users)


has_auto_renew = np.random.randint(0, 2, size=num_users)


last_payment_missed = np.random.randint(0, 2, size=num_users)


avg_watch_time_per_day = np.round(np.random.uniform(0.5, 6.5, size=num_users), 6)


churn = np.where((total_watch_hours < 100) | (last_payment_missed == 1), 1, 0)


# Create DataFrame
data = pd.DataFrame({
    'CustomerID': customer_ids,
    'SubscriptionType': subscription_type,
    'MonthlyFee': monthly_fee,
    'TotalWatchHours': total_watch_hours,
    'NumDevices': num_devices,
    'HasAutoRenew': has_auto_renew,
    'LastPaymentMissed': last_payment_missed,
    'AvgWatchTimePerDay': avg_watch_time_per_day,
    
})

# Save to CSV
data.to_csv('customer_data_1000.csv', index=False)

print("Dataset generated and saved as 'customer_data_1000.csv'")