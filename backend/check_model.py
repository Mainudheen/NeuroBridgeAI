import joblib

model = joblib.load(r"D:\Autism\backend\models\autism_model.pkl")

print(type(model))

if hasattr(model, "named_steps"):
    print("\nPipeline Steps:")
    print(model.named_steps)

    print("\nStep Names:")
    print(list(model.named_steps.keys()))
else:
    print("Not a pipeline")