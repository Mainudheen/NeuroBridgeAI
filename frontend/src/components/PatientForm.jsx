import React, { useState } from "react";
import api from "../services/api";
import "./PatientForm.css";

function PatientForm({ onPredictionStart, onPredictionSuccess, onPredictionError, loading }) {
    const questions = [
        { key: "A1_Score", title: "A1: Sights & Sounds", desc: "Does the person pay attention to small sounds or subtle visual details?" },
        { key: "A2_Score", title: "A2: Social Interaction", desc: "Does the person find it easy to socialise with peers?" },
        { key: "A3_Score", title: "A3: Imagination & Play", desc: "Does the person enjoy imaginative roleplay or fiction?" },
        { key: "A4_Score", title: "A4: Communication", desc: "Is it easy to read between the lines when someone is talking to them?" },
        { key: "A5_Score", title: "A5: Routine & Flexibility", desc: "Does the person get strongly upset by minor changes in routine?" },
        { key: "A6_Score", title: "A6: Focus & Fixation", desc: "Does the person fixate deeply on specific hobbies or details?" },
        { key: "A7_Score", title: "A7: Non-verbal Cues", desc: "Can the person easily work out what someone is thinking or feeling?" },
        { key: "A8_Score", title: "A8: Conversations", desc: "Does the person find back-and-forth conversation natural?" },
        { key: "A9_Score", title: "A9: Details vs Big Picture", desc: "Does the person notice patterns or details that others miss?" },
        { key: "A10_Score", title: "A10: Empathy & Intuition", desc: "Does the person intuitively understand body language and tone?" },
    ];

    const [formData, setFormData] = useState({
        A1_Score: 0,
        A2_Score: 1,
        A3_Score: 1,
        A4_Score: 0,
        A5_Score: 1,
        A6_Score: 0,
        A7_Score: 1,
        A8_Score: 1,
        A9_Score: 0,
        A10_Score: 1,
        age: 22,
        gender: 1,
        ethnicity: 3,
        jundice: 0,
        austim: 0,
        contry_of_res: 12,
        used_app_before: 1,
        age_desc: 0,
        relation: 5
    });

    const [validationError, setValidationError] = useState("");

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: parseInt(value, 10)
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setValidationError("");

        // Validation checks
        if (formData.age < 1 || formData.age > 120) {
            setValidationError("Age must be between 1 and 120.");
            return;
        }

        onPredictionStart();

        try {
            const payload = {
                A1_Score: Number(formData.A1_Score),
                A2_Score: Number(formData.A2_Score),
                A3_Score: Number(formData.A3_Score),
                A4_Score: Number(formData.A4_Score),
                A5_Score: Number(formData.A5_Score),
                A6_Score: Number(formData.A6_Score),
                A7_Score: Number(formData.A7_Score),
                A8_Score: Number(formData.A8_Score),
                A9_Score: Number(formData.A9_Score),
                A10_Score: Number(formData.A10_Score),
                age: Number(formData.age),
                gender: Number(formData.gender),
                ethnicity: Number(formData.ethnicity),
                jundice: Number(formData.jundice),
                austim: Number(formData.austim),
                contry_of_res: Number(formData.contry_of_res),
                used_app_before: Number(formData.used_app_before),
                age_desc: Number(formData.age_desc),
                relation: Number(formData.relation)
            };

            const response = await api.post("/predict", payload);
            if (response.data && response.data.status === "success") {
                onPredictionSuccess(response.data);
            } else if (response.data && response.data.validation && !response.data.validation.valid) {
                onPredictionError(`Validation Error: ${response.data.validation.errors.join(", ")}`);
            } else {
                onPredictionSuccess(response.data);
            }
        } catch (error) {
            console.error("Prediction Request Failed:", error);
            const msg = error.response?.data?.detail || "Backend Server Not Running or Connection Failed. Please verify FastAPI server.";
            onPredictionError(msg);
        }
    };

    return (
        <div className="form-card">
            <div className="form-header">
                <h2>Patient Screening Form</h2>
                <p>Enter patient demographic details and ASD screening questionnaire responses below.</p>
            </div>

            {validationError && (
                <div className="form-alert alert-error">
                    ⚠️ {validationError}
                </div>
            )}

            <form onSubmit={handleSubmit} className="patient-form">
                <div className="section-title">1. Patient Demographics & Medical History</div>
                <div className="form-grid">
                    <div className="form-group">
                        <label htmlFor="age">Age (Years)</label>
                        <input
                            id="age"
                            type="number"
                            name="age"
                            value={formData.age}
                            onChange={handleChange}
                            min="1"
                            max="120"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="gender">Gender</label>
                        <select id="gender" name="gender" value={formData.gender} onChange={handleChange}>
                            <option value={1}>Male</option>
                            <option value={0}>Female</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label htmlFor="ethnicity">Ethnicity Code</label>
                        <input
                            id="ethnicity"
                            type="number"
                            name="ethnicity"
                            value={formData.ethnicity}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="contry_of_res">Country of Residence Code</label>
                        <input
                            id="contry_of_res"
                            type="number"
                            name="contry_of_res"
                            value={formData.contry_of_res}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="jundice">Born with Jaundice?</label>
                        <select id="jundice" name="jundice" value={formData.jundice} onChange={handleChange}>
                            <option value={0}>No</option>
                            <option value={1}>Yes</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label htmlFor="austim">Family History of Autism?</label>
                        <select id="austim" name="austim" value={formData.austim} onChange={handleChange}>
                            <option value={0}>No</option>
                            <option value={1}>Yes</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label htmlFor="used_app_before">Used App Before?</label>
                        <select id="used_app_before" name="used_app_before" value={formData.used_app_before} onChange={handleChange}>
                            <option value={0}>No</option>
                            <option value={1}>Yes</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label htmlFor="relation">Relation / Evaluator Code</label>
                        <input
                            id="relation"
                            type="number"
                            name="relation"
                            value={formData.relation}
                            onChange={handleChange}
                            required
                        />
                    </div>
                </div>

                <div className="section-title" style={{ marginTop: "24px" }}>2. Behavioral Screening Questionnaire (AQ-10)</div>
                <div className="questionnaire-grid">
                    {questions.map((q) => (
                        <div key={q.key} className="question-card">
                            <div className="question-header">
                                <span className="question-title">{q.title}</span>
                                <select
                                    name={q.key}
                                    value={formData[q.key]}
                                    onChange={handleChange}
                                    className="score-select"
                                >
                                    <option value={0}>Score: 0</option>
                                    <option value={1}>Score: 1</option>
                                </select>
                            </div>
                            <p className="question-desc">{q.desc}</p>
                        </div>
                    ))}
                </div>

                <div className="form-actions">
                    <button type="submit" className="predict-btn" disabled={loading}>
                        {loading ? "Processing Prediction..." : "Predict Autism Risk"}
                    </button>
                </div>
            </form>
        </div>
    );
}

export default PatientForm;