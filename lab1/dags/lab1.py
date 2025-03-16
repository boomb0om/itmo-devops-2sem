import datetime
import pandas as pd
import numpy as np
import pendulum
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator


def create_dataset():
    X, y = make_regression(n_samples=100, n_features=1, noise=0.1, random_state=42)
    df = pd.DataFrame(data=X, columns=['feature'])
    df['target'] = y
    print("Dataset created")
    df.to_csv('/tmp/regression_data.csv', index=False)


def train_model():
    df = pd.read_csv('/tmp/regression_data.csv')
    X = df[['feature']]
    y = df['target']
    
    model = LinearRegression()
    model.fit(X, y)
    print("Model trained")
    print("Model MSE:", metrics.mean_squared_error(y, model.predict(X)))
    print("Model R2:", metrics.r2_score(y, model.predict(X)))

dag = DAG(
    'regression_training',
    #schedule_interval='@daily',
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False
)

create_data = PythonOperator(
    task_id='create_dataset',
    python_callable=create_dataset,
    dag=dag
)

train_regression = PythonOperator(
    task_id='train_model',
    python_callable=train_model, 
    dag=dag
)

create_data >> train_regression
