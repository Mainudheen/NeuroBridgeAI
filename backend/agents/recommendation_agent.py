"""
=========================================================
NeuroBridge AI

Recommendation Agent

Provides personalized recommendations based on
prediction confidence.

=========================================================
"""


class RecommendationAgent:

    def __init__(self):
        pass

    #########################################################

    def recommend(self, prediction_result):

        prediction = prediction_result["prediction"]

        confidence = prediction_result["confidence"]

        if prediction == 0:

            return {

                "risk_level": "Low",

                "recommendations": [

                    "No strong indication of Autism Spectrum Disorder.",

                    "Continue monitoring developmental milestones.",

                    "Maintain regular health checkups.",

                    "Encourage social interaction and communication.",

                    "Consult a pediatrician if new symptoms appear."

                ]

            }

        #########################################################

        elif confidence < 70:

            return {

                "risk_level": "Moderate",

                "recommendations": [

                    "Schedule a clinical autism assessment.",

                    "Observe behavioural changes over time.",

                    "Consult a developmental pediatrician.",

                    "Begin early behavioural screening."

                ]

            }

        #########################################################

        elif confidence < 90:

            return {

                "risk_level": "High",

                "recommendations": [

                    "Consult an Autism Specialist.",

                    "Begin Speech Therapy evaluation.",

                    "Consider Occupational Therapy.",

                    "Conduct ADOS assessment.",

                    "Provide family counselling."

                ]

            }

        #########################################################

        else:

            return {

                "risk_level": "Very High",

                "recommendations": [

                    "Immediate comprehensive clinical evaluation.",

                    "Start Early Intervention Program.",

                    "Speech Therapy.",

                    "Behaviour Therapy (ABA if clinically appropriate).",

                    "Occupational Therapy.",

                    "Psychological Assessment.",

                    "Parent Training Program."

                ]

            }


#############################################################

if __name__ == "__main__":

    prediction = {

        "prediction": 1,

        "confidence": 96.8

    }

    agent = RecommendationAgent()

    result = agent.recommend(prediction)

    print(result)