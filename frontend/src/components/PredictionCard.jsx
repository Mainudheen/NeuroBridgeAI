import React from "react";
import "./Card.css";

function PredictionCard({ prediction }) {
    if (!prediction) return null;

    const isAutism = prediction.prediction === 1;
    const confidence = prediction.confidence || 0;
    const probability = (confidence / 100).toFixed(4);

    return (
        <div className={`card prediction-card ${isAutism ? "card-autism" : "card-no-autism"}`}>
            <div className="card-header">
                <span className="card-icon">{isAutism ? "🚨" : "✅"}</span>
                <h3 className="card-title">ML Model Prediction</h3>
            </div>

            <div className="prediction-content">
                <div className="prediction-badge-container">
                    <span className="prediction-label-text">Result</span>
                    <div className={`prediction-badge ${isAutism ? "badge-detected" : "badge-clear"}`}>
                        {prediction.label || (isAutism ? "Autism Detected" : "No Autism")}
                    </div>
                </div>

                <div className="prediction-metrics">
                    <div className="metric-box">
                        <span className="metric-label">Model Confidence</span>
                        <span className="metric-value">{confidence}%</span>
                        <div className="progress-bar-bg">
                            <div
                                className={`progress-bar-fill ${isAutism ? "fill-autism" : "fill-clear"}`}
                                style={{ width: `${Math.min(confidence, 100)}%` }}
                            ></div>
                        </div>
                    </div>

                    <div className="metric-box">
                        <span className="metric-label">Probability Score</span>
                        <span className="metric-value">{probability}</span>
                        <span className="metric-sub">Classification threshold: 0.50</span>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default PredictionCard;
