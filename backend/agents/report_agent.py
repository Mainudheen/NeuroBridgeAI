"""
=========================================================
NeuroBridge AI

Report Agent

Generates professional PDF report.

=========================================================
"""

from pathlib import Path
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)


class ReportAgent:

    def __init__(self):

        self.styles = getSampleStyleSheet()

    #########################################################

    def generate(
        self,
        patient,
        prediction,
        explanation,
        recommendation,
        llm_report,
        output_file
    ):

        output_file = Path(output_file)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        doc = SimpleDocTemplate(str(output_file))

        story = []

        #########################################################
        # Title
        #########################################################

        story.append(
            Paragraph(
                "<b>NeuroBridge AI</b>",
                self.styles["Title"]
            )
        )

        story.append(
            Paragraph(
                "Autism Prediction Report",
                self.styles["Heading1"]
            )
        )

        story.append(Spacer(1, 15))

        #########################################################
        # Generated Time
        #########################################################

        story.append(
            Paragraph(
                f"<b>Generated :</b> {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
                self.styles["Normal"]
            )
        )

        story.append(Spacer(1, 20))

        #########################################################
        # Patient Information
        #########################################################

        story.append(
            Paragraph(
                "<b>Patient Information</b>",
                self.styles["Heading2"]
            )
        )

        story.append(Spacer(1, 5))

        for key, value in patient.items():

            story.append(
                Paragraph(
                    f"<b>{key}</b> : {value}",
                    self.styles["Normal"]
                )
            )

        story.append(Spacer(1, 20))

        #########################################################
        # Prediction
        #########################################################

        story.append(
            Paragraph(
                "<b>Prediction Result</b>",
                self.styles["Heading2"]
            )
        )

        story.append(Spacer(1, 5))

        story.append(
            Paragraph(
                f"<b>Prediction :</b> {prediction['label']}",
                self.styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Confidence :</b> {prediction['confidence']} %",
                self.styles["Normal"]
            )
        )

        story.append(Spacer(1, 20))

        #########################################################
        # SHAP Explanation
        #########################################################

        story.append(
            Paragraph(
                "<b>Top Influencing Features</b>",
                self.styles["Heading2"]
            )
        )

        story.append(Spacer(1, 5))

        if explanation.get("status") == "success":

            for feature in explanation["top_features"]:

                story.append(
                    Paragraph(
                        f"• <b>{feature['Feature']}</b> : {round(feature['Importance'],4)}",
                        self.styles["Normal"]
                    )
                )

        else:

            story.append(
                Paragraph(
                    explanation.get(
                        "message",
                        "Explanation unavailable."
                    ),
                    self.styles["Normal"]
                )
            )

        story.append(Spacer(1, 20))

        #########################################################
        # Recommendations
        #########################################################

        story.append(
            Paragraph(
                "<b>Recommendations</b>",
                self.styles["Heading2"]
            )
        )

        story.append(Spacer(1, 5))

        story.append(
            Paragraph(
                f"<b>Risk Level :</b> {recommendation['risk_level']}",
                self.styles["Normal"]
            )
        )

        story.append(Spacer(1, 5))

        for rec in recommendation["recommendations"]:

            story.append(
                Paragraph(
                    "• " + rec,
                    self.styles["Normal"]
                )
            )

        story.append(Spacer(1, 20))

        #########################################################
        # Gemini AI Summary
        #########################################################

        story.append(
            Paragraph(
                "<b>AI Clinical Summary</b>",
                self.styles["Heading2"]
            )
        )

        story.append(Spacer(1, 5))

        if isinstance(llm_report, dict):

            report_text = llm_report.get(
                "summary",
                str(llm_report)
            )

        else:

            report_text = str(llm_report)

        story.append(
            Paragraph(
                report_text,
                self.styles["Normal"]
            )
        )

        story.append(Spacer(1, 25))

        #########################################################
        # Footer
        #########################################################

        story.append(
            Paragraph(
                "<b>Disclaimer</b>",
                self.styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                "This report is generated using NeuroBridge AI. "
                "It is intended only as a clinical decision support "
                "tool and should not replace professional medical diagnosis. "
                "Please consult a qualified healthcare professional for "
                "confirmation and further evaluation.",
                self.styles["Normal"]
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>Generated by NeuroBridge AI</b>",
                self.styles["Heading3"]
            )
        )

        #########################################################

        doc.build(story)

        return {
            "status": "success",
            "pdf_path": str(output_file)
        }


#########################################################
# Testing
#########################################################

if __name__ == "__main__":

    patient = {
        "Age": 6,
        "Gender": "Male",
        "Jundice": "Yes",
        "Autism Family History": "No"
    }

    prediction = {
        "label": "Autism Detected",
        "confidence": 79.15
    }

    explanation = {
        "status": "success",
        "top_features": [
            {
                "Feature": "A1_Score",
                "Importance": 0.81
            },
            {
                "Feature": "A6_Score",
                "Importance": 0.74
            },
            {
                "Feature": "Jundice",
                "Importance": 0.61
            }
        ]
    }

    recommendation = {
        "risk_level": "High",
        "recommendations": [
            "Consult an Autism Specialist.",
            "Schedule ADOS Assessment.",
            "Speech Therapy Evaluation.",
            "Occupational Therapy.",
            "Behavioural Therapy."
        ]
    }

    llm_report = """
The patient exhibits several behavioural indicators associated
with Autism Spectrum Disorder. The screening result indicates a
high likelihood of ASD. A comprehensive clinical assessment is
recommended to confirm the diagnosis and initiate early intervention.
"""

    agent = ReportAgent()

    result = agent.generate(
        patient,
        prediction,
        explanation,
        recommendation,
        llm_report,
        r"D:\Autism\backend\reports\autism_report.pdf"
    )

    print(result)