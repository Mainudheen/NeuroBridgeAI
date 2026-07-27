import joblib
from utils.train import AutismTrainer

trainer = AutismTrainer()

trainer.run(
    dataset_path=r"D:\AUTISM\datasets\questionaire\autism_clean.csv",
    model_path=r"D:\AUTISM\backend\models\autism_model.pkl",
    results_path=r"D:\AUTISM\backend\models\model_results.csv"
)