import pandas as pd
from textblob import TextBlob
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import sklearn.metrics as m
from sklearn.preprocessing import OneHotEncoder
import nltk

data = pd.read_excel('12.2022-Complaint Data.xlsx')
case_num, description, sentiment_score, polarity_score, type, subtype, rating, dates = [], [], [], [], [], [], [], []
complaint_type_ , MSE_LR, MSE_XGB, R2_LR, R2_XGB = [], [], [], [], []
x = 0
while x < len(data):
    description_x = str(data.iat[x,data.columns.get_loc('Description of the Problem/Request')]).strip()
    type_x = str(data.iat[x,data.columns.get_loc('Concern Type')]).strip()
    subtype_x = str(data.iat[x,data.columns.get_loc('Concern Sub-Type')]).strip()
    case_num_x = str(data.iat[x,data.columns.get_loc('Case Number')]).strip()
    sentiment_score_x = TextBlob(description_x).sentiment.subjectivity    
    polarity_score_x = TextBlob(description_x).sentiment.polarity    
    sentiment_category = [1 if sentiment_score_x > 0                      
                          else -1 if sentiment_score_x < 0                        
                          else 0]
    case_num.append(case_num_x)
    description.append(description_x)
    sentiment_score.append(sentiment_score_x)
    polarity_score.append(polarity_score_x)
    rating.append(sentiment_category)
    type.append(type_x)
    subtype.append(subtype_x)
    dates.append(data.iat[x,data.columns.get_loc('Opened Date')])
    x = x + 1
# pre process data for training model
day_of_week = [datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S').weekday() for date in dates]
results = {  'Case Number': case_num  
            ,'Day of Week' : day_of_week  
            ,'Type': type          
            ,'Sub-Type': subtype          
            ,'Description': description          
            ,'Sentiment': sentiment_score          
            ,'Polarity': polarity_score          
            ,'Rating Score': rating
            }

pre_results_df = pd.DataFrame(results)
encoder = OneHotEncoder(handle_unknown='ignore')
x_encoded = encoder.fit_transform(pre_results_df['Type'].values.reshape(-1,1))
x_encoded_df = pd.DataFrame(x_encoded.toarray(), columns=encoder.get_feature_names_out(['Type']))
encoded_df = pd.concat([pre_results_df, x_encoded_df], axis=1)
encoded_df = encoded_df.drop(['Type'], axis=1)
x_encoded = encoder.fit_transform(encoded_df['Day of Week'].values.reshape(-1,1))
x_encoded_df = pd.DataFrame(x_encoded.toarray(), columns=encoder.get_feature_names_out(['Day of Week']))
encoded_df = pd.concat([encoded_df, x_encoded_df], axis=1)
encoded_df = encoded_df.drop(['Day of Week'], axis=1)
complaint_types = encoded_df.columns.tolist()

# create training and testing models for each complaint type
x = 6
while x < len(complaint_types):
    complaint_type_.append(complaint_types[x])
    # split complaint data into training / test sets    
    features = [complaint_types[x], 'Sentiment' ]
    target = "Polarity"
    x_train, x_test, y_train, y_test = train_test_split(encoded_df[features], encoded_df[target], test_size=0.3, random_state=0)

    # train the prediction models    
    regressor = LinearRegression()
    x_regressor = XGBRegressor(random_state=42)
    y_train = y_train.values.reshape(-1,1)
    regressor.fit(x_train, y_train)
    x_regressor.fit(x_train,y_train)

    # make prediction using test data    
    M_pred = regressor.predict(x_test)
    X_pred = x_regressor.predict(x_test)

    # evaluate model performance    
    mse = m.mean_squared_error(y_test, M_pred)
    R2_ = m.r2_score(y_test,M_pred)
    MSE_LR.append(mse)
    R2_LR.append(R2_)
    mse_ = m.mean_squared_error(y_test,X_pred)
    MSE_XGB.append(mse_)
    R2__ = m.r2_score(y_test,X_pred)
    R2_XGB.append(R2__)
    x = x + 1

trained_results = { 'Complaint Type' : complaint_type_
                  ,'MSE LR' : MSE_LR
                  ,'R2 LR': R2_LR
                  ,'MSE X' : MSE_XGB
                  ,'R2 X' : R2_XGB                  
                  }

trained_results_df = pd.DataFrame(trained_results)
