import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE  

class ChurnPredictor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy='median')
        self.model = None
        self.target_col = 'Churn'
        self.feature_columns = None

    def _preprocess_data(self, df, training=True):
        """Universal preprocessing pipeline"""
        df = df.replace([np.inf, -np.inf], np.nan)
        numeric_cols = df.select_dtypes(include=np.number).columns
        df[numeric_cols] = self.imputer.fit_transform(df[numeric_cols])

        if self.target_col in df.columns:
            df[self.target_col] = df[self.target_col].apply(lambda x: 1 if x > 0 else 0)
            if len(df[self.target_col].unique()) != 2:
                raise ValueError("Churn column must be binary (0/1 or Yes/No)")

        categorical_cols = df.select_dtypes(exclude=np.number).columns
        if self.target_col in categorical_cols:
            categorical_cols = categorical_cols.drop(self.target_col)
        df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

        if training:
            self.feature_columns = df.drop(columns=[self.target_col]).columns.tolist()
        elif self.feature_columns:
            df = df.reindex(columns=self.feature_columns, fill_value=0)

        df[numeric_cols] = self.scaler.fit_transform(df[numeric_cols])
        return df

    def _train_model(self, X_train, y_train):
        """Train a new model with balanced data"""
        smote = SMOTE(random_state=42)
        X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

        self.model = RandomForestClassifier(random_state=42)
        self.model.fit(X_train_resampled, y_train_resampled)

        joblib.dump(self.model, 'churn_model.pkl')
        joblib.dump(self.scaler, 'churn_scaler.pkl')
        joblib.dump(self.feature_columns, 'feature_columns.pkl')

    def analyze_dataset(self, file_path):
        """
        Main function: Determines whether to train or predict.
        Returns a dictionary with the following keys:
          - message: Status message.
          - churn_rate: Calculated churn rate (as a float, not formatted).
          - churn_users_count: Number of users likely to churn.
          - churn_user_ids: List of user IDs for those predicted to churn.
        """
        try:
            # Read data from CSV or Excel
            df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
            processed_df = self._preprocess_data(df, training=self.target_col in df.columns)

            if self.target_col in processed_df.columns:
                # Training branch
                X = processed_df.drop(columns=[self.target_col])
                y = processed_df[self.target_col]

                if not y.isin([0, 1]).all():
                    y = y.apply(lambda x: 1 if x > 0 else 0)

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                self._train_model(X_train, y_train)

                churn_rate = y.mean() * 100
                churn_count = int(y.sum())

                if 'CustomerID' in df.columns:
                    churn_user_ids = df.loc[y == 1, 'CustomerID'].tolist()
                else:
                    churn_user_ids = df.index[y == 1].tolist()

                print(f"\nTraining Complete! Churn Rate: {churn_rate:.2f}%")
                return {
                    'message': 'Training complete! Model trained and churn analysis computed.',
                    'churn_rate': churn_rate,
                    'churn_users_count': churn_count,
                    'churn_user_ids': churn_user_ids
                }
            else:
                # Prediction branch
                self.model = joblib.load('churn_model.pkl')
                self.scaler = joblib.load('churn_scaler.pkl')
                self.feature_columns = joblib.load('feature_columns.pkl')

                processed_df = processed_df.reindex(columns=self.feature_columns, fill_value=0)
                predictions = self.model.predict(processed_df)
                churn_rate = predictions.mean() * 100
                churn_count = int(predictions.sum())

                # Find the original indices of rows predicted to churn
                churn_users = processed_df[predictions == 1]

                if 'CustomerID' in df.columns:
                    churn_user_ids = df.loc[churn_users.index, 'CustomerID'].tolist()
                else:
                    churn_user_ids = churn_users.index.tolist()

                print(f"\n🔍 Predicted Churn Rate: {churn_rate:.2f}%")
                print(f"\nNumber of users likely to churn: {churn_count}")
                print(f"Users likely to churn (Customer IDs): {churn_user_ids}")

                return {
                    'message': 'Prediction complete! Churn analysis computed.',
                    'churn_rate': churn_rate,
                    'churn_users_count': churn_count,
                    'churn_user_ids': churn_user_ids
                }

        except FileNotFoundError:
            error_message = "No trained model found. Train the model first with a dataset that contains 'Churn'."
            print(error_message)
            return {'message': error_message}
        except Exception as e:
            print(f"\nError: {str(e)}")
            return {'message': str(e)}

if __name__ == "__main__":
    predictor = ChurnPredictor()
    predictor.analyze_dataset("customer_data_1000.csv")
