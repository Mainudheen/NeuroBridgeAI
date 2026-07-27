from utils.preprocessing import DataPreprocessor

processor = DataPreprocessor()

processor.process(

    input_path=r"D:\AUTISM\datasets\questionaire\autism.csv",

    output_path=r"D:\AUTISM\datasets\questionaire\autism_clean.csv",

    encoder_path=r"D:\AUTISM\backend\models\label_encoders.pkl"

)