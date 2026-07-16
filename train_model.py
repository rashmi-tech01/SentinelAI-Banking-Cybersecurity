import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle


# Sample Banking Transaction Data

data = {
    "amount":[500,2000,95000,70000,300,120000,4500,80000],
    "device":[0,0,1,1,0,1,0,1],
    "vpn":[0,0,1,1,0,1,0,1],
    "login_attempts":[0,1,5,6,0,8,1,7],
    "fraud":[0,0,1,1,0,1,0,1]
}


df = pd.DataFrame(data)



X = df.drop("fraud",axis=1)

y = df["fraud"]



X_train,X_test,y_train,y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)



model = RandomForestClassifier()

model.fit(X_train,y_train)



accuracy = model.score(X_test,y_test)

print("Model Accuracy:",accuracy)



# Save Model

with open("model/fraud_model.pkl","wb") as file:

    pickle.dump(model,file)


print("Model Saved Successfully")