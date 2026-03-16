import mlflow.pyfunc
import numpy as np

model = mlflow.pyfunc.load_model("mlruns")

sample = np.array([[5.1,3.5,1.4,0.2]])

prediction = model.predict(sample)

print("Prediction:",prediction)