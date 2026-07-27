import React from "react";
import api from "../services/api";
import "./Card.css";

function DownloadReport({ pdfPath }) {
    const handleDownload = () => {
        const apiBaseUrl = api.defaults.baseURL || import.meta.env.VITE_API_URL || "";
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
