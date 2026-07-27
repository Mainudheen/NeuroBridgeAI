import React from "react";
import "./Navbar.css";

function Navbar() {
    return (
        <header className="navbar">
            <div className="navbar-container">
                <div className="navbar-brand">
                    <span className="brand-icon">🧬</span>
                    <div>
                        <h1 className="logo-title">NeuroBridge AI</h1>
                        <p className="logo-subtitle">Autism Prediction & Clinical Decision Support System</p>
                    </div>
                </div>
                <div className="navbar-status">
                    <span className="status-dot"></span>
                    <span className="status-text">AI Agents Active</span>
                </div>
            </div>
        </header>
    );
}

export default Navbar;