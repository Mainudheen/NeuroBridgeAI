from pydantic import BaseModel


class PatientData(BaseModel):

    A1_Score: int
    A2_Score: int
    A3_Score: int
    A4_Score: int
    A5_Score: int
    A6_Score: int
    A7_Score: int
    A8_Score: int
    A9_Score: int
    A10_Score: int

    age: int
    gender: int
    ethnicity: int

    jundice: int
    austim: int

    contry_of_res: int

    used_app_before: int

    age_desc: int

    relation: int