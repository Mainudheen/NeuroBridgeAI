import React from "react";
import "./Card.css";

function DownloadReport({ pdfPath }) {
    const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

    const handleDownload = () => {
        // Trigger download directly from backend server endpoint
        const downloadUrl = `${apiBaseUrl}/download-report`;
        window.open(downloadUrl, "_blank");
    };

    return (
        <div className="card download-card">
            <div className="download-content">
                <div className="download-info">
                    <span className="download-icon">📄</span>
                    <div>
                        <h3 className="download-title">Download Formal PDF Report</h3>
                        <p className="download-sub">Includes patient records, prediction results, SHAP feature rankings, clinical recommendations, and Gemini summary.</p>
                    </div>
                </div>
                <button onClick={handleDownload} className="download-btn">
                    📥 Download PDF Report
                </button>
            </div>
        </div>
    );
}

export default DownloadReport;
