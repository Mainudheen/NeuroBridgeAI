import React from "react";
import "./Card.css";

function AIReport({ llmReport }) {
    if (!llmReport) return null;

    // Helper to format raw markdown or plain text with headings nicely
    const formatReport = (reportText) => {
        if (typeof reportText !== "string") return JSON.stringify(reportText);

        const lines = reportText.split("\n");
        return lines.map((line, index) => {
            const trimmed = line.trim();
            if (!trimmed) return <div key={index} className="report-spacer" />;

            if (trimmed.startsWith("### ") || trimmed.startsWith("1. ") || trimmed.startsWith("2. ") || trimmed.startsWith("3. ") || trimmed.startsWith("4. ") || trimmed.startsWith("5. ") || trimmed.startsWith("6. ") || trimmed.endsWith(":")) {
                return (
                    <h4 key={index} className="report-section-heading">
                        {trimmed.replace(/^#+\s*/, '')}
                    </h4>
                );
            } else if (trimmed.startsWith("- ") || trimmed.startsWith("* ")) {
                return (
                    <li key={index} className="report-bullet-item">
                        {trimmed.substring(2)}
                    </li>
                );
            } else {
                return (
                    <p key={index} className="report-paragraph">
                        {trimmed}
                    </p>
                );
            }
        });
    };

    return (
        <div className="card report-card">
            <div className="card-header">
                <span className="card-icon">🤖</span>
                <div>
                    <h3 className="card-title">AI Clinical Summary (Gemini Powered)</h3>
                    <p className="card-subtitle">Automated multi-agent synthesis of screening indicators and clinical context</p>
                </div>
            </div>

            <div className="report-scroll-container">
                <div className="report-text-body">
                    {formatReport(llmReport)}
                </div>
            </div>
        </div>
    );
}

export default AIReport;
