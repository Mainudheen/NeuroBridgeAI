import React from "react";
import "./Card.css";

function ExplanationCard({ explanation }) {
    if (!explanation) return null;

    const topPositive = explanation.top_positive || [];
    const topNegative = explanation.top_negative || [];
    const topFeatures = explanation.top_features || [];

    return (
        <div className="card explanation-card">
            <div className="card-header">
                <span className="card-icon">📊</span>
                <div>
                    <h3 className="card-title">SHAP Feature Importance Explanation</h3>
                    <p className="card-subtitle">Explainable AI details showing which features influenced the model's decision</p>
                </div>
            </div>

            <div className="explanation-grid">
                {/* Positive Contributors */}
                <div className="shap-box positive-box">
                    <h4 className="shap-box-title">
                        <span className="bullet-dot dot-positive"></span>
                        Top Positive Factors (Increasing Autism Risk)
                    </h4>
                    {topPositive.length > 0 ? (
                        <ul className="shap-list">
                            {topPositive.map((item, idx) => (
                                <li key={idx} className="shap-item">
                                    <span className="feature-name">{item.feature || item.Feature}</span>
                                    <span className="shap-score positive-score">+{typeof item.value === 'number' ? item.value.toFixed(2) : (item.SHAP_Value || item.Importance || 0)}</span>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p className="no-data-text">No significant positive feature factors.</p>
                    )}
                </div>

                {/* Negative Contributors */}
                <div className="shap-box negative-box">
                    <h4 className="shap-box-title">
                        <span className="bullet-dot dot-negative"></span>
                        Top Negative Factors (Decreasing Autism Risk)
                    </h4>
                    {topNegative.length > 0 ? (
                        <ul className="shap-list">
                            {topNegative.map((item, idx) => (
                                <li key={idx} className="shap-item">
                                    <span className="feature-name">{item.feature || item.Feature}</span>
                                    <span className="shap-score negative-score">{typeof item.value === 'number' ? item.value.toFixed(2) : (item.SHAP_Value || item.Importance || 0)}</span>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p className="no-data-text">No significant negative feature factors.</p>
                    )}
                </div>
            </div>

            {/* Overall Top Features Table */}
            {topFeatures.length > 0 && (
                <div className="top-features-container">
                    <h4 className="sub-header">Overall Top Influencing Features</h4>
                    <div className="features-pill-grid">
                        {topFeatures.slice(0, 6).map((feat, i) => (
                            <div key={i} className="feature-pill">
                                <span className="pill-name">{feat.Feature}</span>
                                <span className="pill-val">Importance: {feat.Importance ? feat.Importance.toFixed(2) : 'N/A'}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default ExplanationCard;
