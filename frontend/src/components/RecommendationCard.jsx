import React from "react";
import "./Card.css";

function RecommendationCard({ recommendation }) {
    if (!recommendation) return null;

    const riskLevel = recommendation.risk_level || "Unknown";
    const recommendations = recommendation.recommendations || [];

    const getRiskClass = (level) => {
        switch (level.toLowerCase()) {
            case "low":
                return "risk-low";
            case "moderate":
                return "risk-moderate";
            case "high":
                return "risk-high";
            case "very high":
                return "risk-very-high";
            default:
                return "risk-moderate";
        }
    };

    return (
        <div className="card recommendation-card">
            <div className="card-header">
                <span className="card-icon">🩺</span>
                <h3 className="card-title">Clinical Next Steps & Recommendations</h3>
            </div>

            <div className="recommendation-content">
                <div className="risk-level-container">
                    <span className="risk-label">Assessed Risk Level</span>
                    <div className={`risk-badge ${getRiskClass(riskLevel)}`}>
                        {riskLevel.toUpperCase()} RISK
                    </div>
                </div>

                <div className="recommendations-section">
                    <h4 className="rec-section-title">Actionable Recommendations:</h4>
                    <ul className="rec-list">
                        {recommendations.map((rec, index) => (
                            <li key={index} className="rec-item">
                                <span className="rec-check">✔</span>
                                <span className="rec-text">{rec}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default RecommendationCard;
