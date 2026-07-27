import React from "react";
import "./Spinner.css";

function LoadingSpinner() {
    return (
        <div className="spinner-container">
            <div className="spinner"></div>
            <h3 className="spinner-title">Analyzing Screening Data...</h3>
            <p className="spinner-sub">Executing LangGraph AI Multi-Agent Workflow (Validation → Prediction → SHAP Explanation → Recommendation → Gemini AI Report)</p>
        </div>
    );
}

export default LoadingSpinner;
