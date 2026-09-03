import { useState } from "react";
import "./App.css";

const API_URL = "https://cybershield-ai-yhzr.onrender.com";

function ShieldIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      className="shield-icon"
      aria-hidden="true"
    >
      <path
        d="M12 3L20 6V11C20 16.2 16.6 20 12 21C7.4 20 4 16.2 4 11V6L12 3Z"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
      />
      <path
        d="M9 12L11 14L15 10"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function RiskIcon() {
  return (
    <svg viewBox="0 0 24 24" className="small-icon">
      <path
        d="M12 3L21 20H3L12 3Z"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.6"
      />
      <path
        d="M12 9V14"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
      />
      <circle cx="12" cy="17" r="0.8" fill="currentColor" />
    </svg>
  );
}

function BrainIcon() {
  return (
    <svg viewBox="0 0 24 24" className="small-icon">
      <path
        d="M9 4.5C7.3 3.1 4.8 4.1 5 6.4C2.8 6.7 2 9.4 3.7 10.8C2.1 12.4 3.2 15.1 5.4 15C5.1 17.5 7.8 19 9.5 17.5C10.1 20 13.9 20 14.5 17.5C16.2 19 18.9 17.5 18.6 15C20.8 15.1 21.9 12.4 20.3 10.8C22 9.4 21.2 6.7 19 6.4C19.2 4.1 16.7 3.1 15 4.5C13.9 2.5 10.1 2.5 9 4.5Z"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.4"
      />
      <path
        d="M9 8.5C10.5 9.5 10.5 14.5 9 15.5M15 8.5C13.5 9.5 13.5 14.5 15 15.5M9.5 12H14.5"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.3"
        strokeLinecap="round"
      />
    </svg>
  );
}

function LinkIcon() {
  return (
    <svg viewBox="0 0 24 24" className="small-icon">
      <path
        d="M10 13.5L14 9.5M8.5 16.5L7 18C5.3 19.7 2.5 19.7 1.5 18C0.3 16.5 0.7 14.3 2 13L5 10M15.5 7.5L17 6C18.7 4.3 21.5 4.3 22.5 6C23.7 7.5 23.3 9.7 22 11L19 14"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
      />
    </svg>
  );
}

function App() {
  const [scanType, setScanType] = useState("url");
  const [input, setInput] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // =====================================================
  // SCAN
  // =====================================================

  const handleScan = async () => {
    if (!input.trim()) {
      setError(
        scanType === "url"
          ? "Please enter a URL to scan."
          : "Please enter a message to analyze."
      );
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      // Select backend endpoint
      const endpoint =
        scanType === "url"
          ? `${API_URL}/scan/url`
          : `${API_URL}/scan/message`;

      // Prepare request body
      const body =
        scanType === "url"
          ? { url: input.trim() }
          : { message: input.trim() };

      console.log("=================================");
      console.log("CyberShield Scan");
      console.log("Endpoint:", endpoint);
      console.log("Request:", body);
      console.log("=================================");

      // Send request
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      // Read response as text first
      const responseText = await response.text();

      console.log("Backend Status:", response.status);
      console.log("Backend Response:", responseText);

      // Backend returned an error
      if (!response.ok) {
        throw new Error(
          `Server returned ${response.status}: ${responseText}`
        );
      }

      // Convert response to JSON
      const data = JSON.parse(responseText);

      console.log("CyberShield Result:", data);

      // Store result
      setResult(data);

    } catch (err) {
      console.error("CyberShield Error:", err);

      setError(
        err.message ||
          "Unable to connect to CyberShield backend."
      );

    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // CLEAR RESULT
  // =====================================================

  const clearResult = () => {
    setInput("");
    setResult(null);
    setError("");
  };

  // =====================================================
  // EXTRACT BACKEND DATA
  // =====================================================

  const fusion = result?.risk_fusion;
  const explanation = result?.explanation;
  const ml = result?.ml_analysis;
  const rule = result?.rule_analysis;

  // =====================================================
  // RISK SCORE
  // =====================================================

  const riskScore = Number(
    fusion?.final_risk_score ??
      rule?.risk_score ??
      0
  );

  const riskClass =
    riskScore >= 75
      ? "high"
      : riskScore >= 45
      ? "suspicious"
      : "low";

  // =====================================================
  // ML PROBABILITIES
  // =====================================================

  const phishingProbability = Number(
    ml?.phishing_probability ?? 0
  );

  const legitimateProbability = Number(
    ml?.legitimate_probability ?? 0
  );

  // =====================================================
  // CONTRIBUTIONS
  // =====================================================

  const mlContribution = Number(
    explanation?.contribution?.ml_contribution ?? 0
  );

  const ruleContribution = Number(
    explanation?.contribution?.rule_contribution ?? 0
  );

  // =====================================================
  // EVIDENCE
  // =====================================================

  const evidence = explanation?.evidence || [];

  // =====================================================
  // SEVERITY CLASS
  // =====================================================

  const getSeverityClass = (severity) => {
    return String(severity || "low").toLowerCase();
  };

  // =====================================================
  // SIGNAL ICON
  // =====================================================

  const getSignalIcon = (signal) => {
    const value = String(signal || "").toLowerCase();

    if (value.includes("url")) return "LINK";
    if (value.includes("credential")) return "AUTH";
    if (value.includes("financial")) return "MONEY";
    if (value.includes("threat")) return "THREAT";
    if (value.includes("urgency")) return "TIME";
    if (value.includes("action")) return "ACTION";

    return "SIGNAL";
  };

  return (
    <div className="app">

      {/* =====================================================
          NAVBAR
      ===================================================== */}

      <header className="navbar">

        <div className="brand">

          <div className="brand-icon">
            <ShieldIcon />
          </div>

          <div>
            <div className="brand-name">
              CyberShield<span> AI</span>
            </div>

            <div className="brand-subtitle">
              INTELLIGENT THREAT DETECTION
            </div>
          </div>

        </div>

        <div className="system-status">
          <span className="status-dot"></span>
          SYSTEM ONLINE
        </div>

      </header>


      {/* =====================================================
          MAIN
      ===================================================== */}

      <main className="main-container">


        {/* =====================================================
            HERO
        ===================================================== */}

        <section className="hero-section">

          <div className="hero-badge">
            <span className="badge-dot"></span>
            AI-POWERED SECURITY
          </div>

          <h1>
            Detect threats.
            <br />
            <span>Understand the risk.</span>
          </h1>

          <p>
            CyberShield combines machine learning, rule-based
            analysis, risk fusion and explainable AI to identify
            phishing and social engineering threats.
          </p>

        </section>


        {/* =====================================================
            SCANNER
        ===================================================== */}

        <section className="scanner-card">

          <div className="scanner-header">

            <div>

              <div className="eyebrow">
                THREAT ANALYSIS
              </div>

              <h2>
                Threat Scanner
              </h2>

              <p>
                Analyze a URL or message for malicious and
                suspicious behavior.
              </p>

            </div>

            <div className="scanner-status">
              <span></span>
              READY
            </div>

          </div>


          {/* =================================================
              TABS
          ================================================= */}

          <div className="scanner-tabs">

            <button
              className={
                scanType === "url"
                  ? "tab active"
                  : "tab"
              }
              onClick={() => {
                setScanType("url");
                setResult(null);
                setError("");
                setInput("");
              }}
            >
              <span>↗</span>
              URL Scanner
            </button>


            <button
              className={
                scanType === "message"
                  ? "tab active"
                  : "tab"
              }
              onClick={() => {
                setScanType("message");
                setResult(null);
                setError("");
                setInput("");
              }}
            >
              <span>✉</span>
              Message Scanner
            </button>

          </div>


          {/* =================================================
              INPUT
          ================================================= */}

          <div className="input-area">

            {scanType === "url" ? (

              <input
                type="text"
                placeholder="https://example.com/login"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    handleScan();
                  }
                }}
              />

            ) : (

              <textarea
                placeholder="Paste a suspicious message here..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
              />

            )}


            <button
              className="scan-button"
              onClick={handleScan}
              disabled={loading}
            >

              {loading ? (
                <>
                  <span className="spinner"></span>
                  ANALYZING
                </>
              ) : (
                <>
                  SCAN NOW
                  <span>→</span>
                </>
              )}

            </button>

          </div>


          {/* =================================================
              ERROR
          ================================================= */}

          {error && (
            <div className="error-box">

              <span>!</span>

              <div>
                {error}
              </div>

            </div>
          )}

        </section>


        {/* =====================================================
            RESULTS
        ===================================================== */}

        {result && (

          <section className="results-section">


            {/* =================================================
                RESULTS HEADER
            ================================================= */}

            <div className="results-heading">

              <div>

                <span className="section-label">
                  ANALYSIS COMPLETE
                </span>

                <h2>
                  Security Assessment
                </h2>

              </div>

              <button
                className="new-scan-button"
                onClick={clearResult}
              >
                + New Scan
              </button>

            </div>


            {/* =================================================
                RISK OVERVIEW
            ================================================= */}

            <div className="risk-grid">


              {/* RISK CARD */}

              <div className={`risk-card ${riskClass}`}>

                <div className="card-top">

                  <div className="card-label">
                    FINAL RISK SCORE
                  </div>

                  <div
                    className={`risk-status ${riskClass}`}
                  >
                    {fusion?.classification ||
                      rule?.classification ||
                      "UNKNOWN"}
                  </div>

                </div>


                <div className="risk-score">
                  {riskScore.toFixed(2)}
                  <span>/100</span>
                </div>


                <div className="risk-progress">

                  <div
                    style={{
                      width: `${Math.min(
                        riskScore,
                        100
                      )}%`,
                    }}
                  />

                </div>


                <div className="risk-scale">
                  <span>LOW</span>
                  <span>SUSPICIOUS</span>
                  <span>HIGH</span>
                </div>

              </div>


              {/* ML CARD */}

              <div className="metric-card">

                <div className="metric-header">

                  <span>
                    ML ANALYSIS
                  </span>

                  <span className="metric-icon">
                    <BrainIcon />
                  </span>

                </div>

                <div className="metric-value">
                  {(phishingProbability * 100).toFixed(1)}%
                </div>

                <div className="metric-title">
                  Phishing Probability
                </div>

                <div className="mini-progress">

                  <div
                    style={{
                      width: `${Math.min(
                        phishingProbability * 100,
                        100
                      )}%`,
                    }}
                  />

                </div>

                <div className="metric-description">
                  {ml?.classification || "No analysis"}
                </div>

              </div>


              {/* RULE CARD */}

              <div className="metric-card">

                <div className="metric-header">

                  <span>
                    RULE ANALYSIS
                  </span>

                  <span className="metric-icon">
                    <RiskIcon />
                  </span>

                </div>

                <div className="metric-value">
                  {rule?.risk_score ?? "—"}
                </div>

                <div className="metric-title">
                  Rule Risk Score
                </div>

                <div className="mini-progress">

                  <div
                    style={{
                      width: `${Math.min(
                        Number(rule?.risk_score ?? 0),
                        100
                      )}%`,
                    }}
                  />

                </div>

                <div className="metric-description">
                  {rule?.classification || "No analysis"}
                </div>

              </div>

            </div>


            {/* =================================================
                MESSAGE INTELLIGENCE
            ================================================= */}

            {scanType === "message" && input && (

              <div className="intelligence-card">

                <div className="intelligence-header">

                  <div>

                    <span className="section-label">
                      MESSAGE INTELLIGENCE
                    </span>

                    <h2>
                      Threat signal map
                    </h2>

                    <p>
                      Key indicators identified by the
                      CyberShield analysis pipeline.
                    </p>

                  </div>

                  <div className="intelligence-badge">
                    LIVE ANALYSIS
                  </div>

                </div>


                <div className="signal-map">

                  {evidence.length > 0 ? (

                    evidence.map((item, index) => (

                      <div
                        className={`signal-chip-card ${getSeverityClass(
                          item.severity
                        )}`}
                        key={index}
                      >

                        <div className="signal-chip-top">

                          <span className="signal-index">
                            {String(index + 1).padStart(
                              2,
                              "0"
                            )}
                          </span>

                          <span
                            className={`signal-severity ${getSeverityClass(
                              item.severity
                            )}`}
                          >
                            {item.severity}
                          </span>

                        </div>


                        <div className="signal-icon-box">
                          {getSignalIcon(item.signal)}
                        </div>


                        <strong>
                          {item.signal}
                        </strong>


                        <p>
                          {item.explanation}
                        </p>


                        {item.detected &&
                          item.detected.length > 0 && (

                            <div className="detected-tags">

                              {item.detected.map(
                                (word, wordIndex) => (

                                  <span key={wordIndex}>
                                    {word}
                                  </span>

                                )
                              )}

                            </div>

                          )}

                      </div>

                    ))

                  ) : (

                    <div className="no-signals">
                      No major threat signals detected.
                    </div>

                  )}

                </div>

              </div>

            )}


            {/* =================================================
                XAI
            ================================================= */}

            {explanation && (

              <div className="xai-card">


                {/* XAI HEADER */}

                <div className="xai-header">

                  <div>

                    <span className="section-label">
                      EXPLAINABLE AI
                    </span>

                    <h2>
                      Why did CyberShield reach this result?
                    </h2>

                    <p className="xai-subtitle">
                      Transparent reasoning from the
                      detection pipeline.
                    </p>

                  </div>

                  <div className="xai-badge">
                    <span>◈</span>
                    XAI ACTIVE
                  </div>

                </div>


                {/* =================================================
                    SUMMARY
                ================================================= */}

                <div className="xai-summary">

                  <div className="summary-mark">
                    "
                  </div>

                  <div>

                    <div className="summary-label">
                      ASSESSMENT SUMMARY
                    </div>

                    <p>
                      {explanation.summary}
                    </p>

                  </div>

                </div>


                {/* =================================================
                    THREAT CHAIN
                ================================================= */}

                <div className="threat-chain">

                  <div className="subsection-title">
                    THREAT DECISION CHAIN
                  </div>

                  <div className="chain-container">


                    <div className="chain-node">

                      <span>01</span>

                      INPUT

                      <small>
                        Message received
                      </small>

                    </div>


                    <div className="chain-arrow">
                      →
                    </div>


                    <div className="chain-node">

                      <span>02</span>

                      SIGNALS

                      <small>
                        Threat indicators
                      </small>

                    </div>


                    <div className="chain-arrow">
                      →
                    </div>


                    <div className="chain-node">

                      <span>03</span>

                      ML MODEL

                      <small>
                        DistilBERT analysis
                      </small>

                    </div>


                    <div className="chain-arrow">
                      →
                    </div>


                    <div className="chain-node">

                      <span>04</span>

                      RISK FUSION

                      <small>
                        Combined assessment
                      </small>

                    </div>


                    <div className="chain-arrow">
                      →
                    </div>


                    <div className="chain-node final">

                      <span>05</span>

                      DECISION

                      <small>
                        {fusion?.classification ||
                          "UNKNOWN"}
                      </small>

                    </div>


                  </div>

                </div>


                {/* =================================================
                    SIGNAL ANALYSIS
                ================================================= */}

                <div className="signal-box">

                  <div className="signal-heading">

                    <div>

                      <div className="subsection-title">
                        SIGNAL ANALYSIS
                      </div>

                      <p>
                        {explanation.signal_analysis ||
                          "The analytical engines evaluated the available threat signals."}
                      </p>

                    </div>

                    <div className="agreement-badge">
                      {fusion?.signal_agreement ||
                        "UNKNOWN"}
                    </div>

                  </div>


                  {/* CONTRIBUTION */}

                  <div className="contribution-title">
                    Risk contribution
                  </div>


                  <div className="contribution-bars">


                    {/* ML */}

                    <div className="contribution-row">

                      <div className="contribution-info">

                        <span>
                          Machine Learning
                        </span>

                        <strong>
                          {mlContribution.toFixed(2)}
                        </strong>

                      </div>


                      <div className="contribution-track">

                        <div
                          className="ml-bar"
                          style={{
                            width: `${Math.min(
                              mlContribution,
                              100
                            )}%`,
                          }}
                        />

                      </div>

                    </div>


                    {/* RULE */}

                    <div className="contribution-row">

                      <div className="contribution-info">

                        <span>
                          Rule Engine
                        </span>

                        <strong>
                          {ruleContribution.toFixed(2)}
                        </strong>

                      </div>


                      <div className="contribution-track">

                        <div
                          className="rule-bar"
                          style={{
                            width: `${Math.min(
                              ruleContribution,
                              100
                            )}%`,
                          }}
                        />

                      </div>

                    </div>


                  </div>

                </div>


                {/* =================================================
                    EVIDENCE
                ================================================= */}

                {evidence.length > 0 && (

                  <div className="evidence-section">

                    <div className="subsection-title">
                      DETECTED EVIDENCE
                    </div>


                    <div className="evidence-list">

                      {evidence.map(
                        (item, index) => (

                          <div
                            className="evidence-item"
                            key={index}
                          >

                            <div
                              className={`severity ${getSeverityClass(
                                item.severity
                              )}`}
                            >
                              {item.severity}
                            </div>


                            <div className="evidence-number">
                              {String(index + 1).padStart(
                                2,
                                "0"
                              )}
                            </div>


                            <div className="evidence-content">

                              <div className="evidence-title-row">

                                <strong>
                                  {item.signal}
                                </strong>

                                <span className="evidence-type">
                                  {getSignalIcon(item.signal)}
                                </span>

                              </div>


                              <p>
                                {item.explanation}
                              </p>


                              {item.detected &&
                                item.detected.length > 0 && (

                                  <div className="detected-tags">

                                    {item.detected.map(
                                      (word, wordIndex) => (

                                        <span key={wordIndex}>
                                          {word}
                                        </span>

                                      )
                                    )}

                                  </div>

                                )}

                            </div>

                          </div>

                        )
                      )}

                    </div>

                  </div>

                )}


                {/* =================================================
                    ML EXPLANATION
                ================================================= */}

                {explanation.ml_explanation?.length > 0 && (

                  <div className="explanation-block">

                    <div className="subsection-title">
                      MACHINE LEARNING EXPLANATION
                    </div>


                    {explanation.ml_explanation.map(
                      (text, index) => (

                        <p key={index}>

                          <span className="bullet">
                            •
                          </span>

                          {text}

                        </p>

                      )
                    )}


                    <div className="probability-grid">

                      <div>

                        <span>
                          PHISHING
                        </span>

                        <strong>
                          {(phishingProbability * 100).toFixed(
                            2
                          )}
                          %
                        </strong>

                      </div>


                      <div>

                        <span>
                          LEGITIMATE
                        </span>

                        <strong>
                          {(legitimateProbability * 100).toFixed(
                            2
                          )}
                          %
                        </strong>

                      </div>

                    </div>

                  </div>

                )}


                {/* =================================================
                    RULE EXPLANATION
                ================================================= */}

                {explanation.rule_explanation?.length > 0 && (

                  <div className="explanation-block">

                    <div className="subsection-title">
                      RULE-BASED EXPLANATION
                    </div>


                    {explanation.rule_explanation.map(
                      (text, index) => (

                        <p key={index}>

                          <span className="bullet">
                            •
                          </span>

                          {text}

                        </p>

                      )
                    )}

                  </div>

                )}


                {/* =================================================
                    RECOMMENDATION
                ================================================= */}

                <div className="recommendation">

                  <div className="recommendation-icon">
                    !
                  </div>

                  <div>

                    <div className="recommendation-label">
                      SECURITY RECOMMENDATION
                    </div>

                    <p>
                      {explanation.recommendation ||
                        "Verify suspicious requests through an official channel."}
                    </p>

                  </div>

                </div>

              </div>

            )}


            {/* =================================================
                TECHNICAL DETAILS
            ================================================= */}

            <details className="technical-details">

              <summary>

                <span>
                  Technical Analysis
                </span>

                <span>
                  VIEW RAW DATA ↓
                </span>

              </summary>

              <pre>
                {JSON.stringify(result, null, 2)}
              </pre>

            </details>


          </section>

        )}


        {/* =====================================================
            FOOTER
        ===================================================== */}

        <footer>

          <div className="footer-brand">

            <ShieldIcon />

            <span>
              CyberShield AI
            </span>

          </div>

          <span>
            AI-powered phishing & social engineering detection
          </span>

        </footer>


      </main>

    </div>
  );
}

export default App;