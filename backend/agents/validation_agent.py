"""
=========================================================
NeuroBridge AI

Validation Agent

Checks whether the patient input is valid before prediction.
=========================================================
"""


class ValidationAgent:

    def __init__(self):

        self.errors = []

    ##################################################

    def validate(self, patient):

        self.errors = []

        ##################################################
        # Age
        ##################################################

        age = patient.get("age")

        if age is None:

            self.errors.append("Age is missing.")

        elif age < 1 or age > 120:

            self.errors.append(
                "Age should be between 1 and 120."
            )

        ##################################################
        # Questionnaire Scores
        ##################################################

        for i in range(1, 11):

            key = f"A{i}_Score"

            value = patient.get(key)

            if value is None:

                self.errors.append(
                    f"{key} is missing."
                )

            elif value not in [0, 1]:

                self.errors.append(
                    f"{key} should be either 0 or 1."
                )

        ##################################################
        # Binary Features
        ##################################################

        binary_columns = [

            "gender",

            "jundice",

            "austim",

            "used_app_before"

        ]

        for column in binary_columns:

            value = patient.get(column)

            if value is None:

                self.errors.append(
                    f"{column} is missing."
                )

            elif value not in [0, 1]:

                self.errors.append(
                    f"{column} should be either 0 or 1."
                )

        ##################################################

        return {

            "valid": len(self.errors) == 0,

            "errors": self.errors

        }


###########################################################

if __name__ == "__main__":

    patient = {

        "age": 18,

        "A1_Score": 1,
        "A2_Score": 0,
        "A3_Score": 1,
        "A4_Score": 1,
        "A5_Score": 0,
        "A6_Score": 1,
        "A7_Score": 0,
        "A8_Score": 1,
        "A9_Score": 0,
        "A10_Score": 1,

        "gender": 1,

        "jundice": 0,

        "austim": 0,

        "used_app_before": 1

    }

    agent = ValidationAgent()

    result = agent.validate(patient)

    print(result)