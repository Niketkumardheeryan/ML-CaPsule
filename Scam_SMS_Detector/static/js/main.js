/**
 * Scam SMS Detector - Frontend JavaScript Handler
 */

document.addEventListener('DOMContentLoaded', () => {
    const smsForm = document.getElementById('sms-form');
    const messageInput = document.getElementById('message-input');
    const charCount = document.getElementById('char-count');
    const clearBtn = document.getElementById('clear-btn');
    const analyzeBtn = document.getElementById('analyze-btn');
    const btnContent = analyzeBtn.querySelector('.btn-content');
    const btnSpinner = analyzeBtn.querySelector('.btn-spinner');

    const resultsPlaceholder = document.getElementById('results-placeholder');
    const resultsCard = document.getElementById('results-card');

    const riskBadge = document.getElementById('risk-badge');
    const confidenceScore = document.getElementById('confidence-score');
    const progressCircle = document.getElementById('progress-circle');
    const verdictTitle = document.getElementById('verdict-title');
    const verdictDesc = document.getElementById('verdict-desc');
    const triggerList = document.getElementById('trigger-list');

    const sampleChips = document.querySelectorAll('.chip');

    // SVG Ring Constants
    const radius = progressCircle.r.baseVal.value;
    const circumference = 2 * Math.PI * radius;
    progressCircle.style.strokeDasharray = `${circumference} ${circumference}`;
    progressCircle.style.strokeDashoffset = circumference;

    function setGaugeProgress(percent, isScam) {
        const offset = circumference - (percent / 100) * circumference;
        progressCircle.style.strokeDashoffset = offset;
        
        if (isScam) {
            if (percent > 75) {
                progressCircle.style.stroke = '#ef4444'; // Red
            } else {
                progressCircle.style.stroke = '#f59e0b'; // Amber
            }
        } else {
            progressCircle.style.stroke = '#10b981'; // Green
        }
    }

    // Update Character Count
    messageInput.addEventListener('input', () => {
        const len = messageInput.value.length;
        charCount.textContent = `${len} character${len === 1 ? '' : 's'}`;
    });

    // Clear Button
    clearBtn.addEventListener('click', () => {
        messageInput.value = '';
        charCount.textContent = '0 characters';
        messageInput.focus();
    });

    // Sample Chips Click
    sampleChips.forEach(chip => {
        chip.addEventListener('click', () => {
            const sampleText = chip.getAttribute('data-text');
            messageInput.value = sampleText;
            charCount.textContent = `${sampleText.length} characters`;
            messageInput.focus();
        });
    });

    // Form Submission
    smsForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = messageInput.value.trim();

        if (!text) return;

        // UI Loading State
        btnContent.classList.add('hidden');
        btnSpinner.classList.remove('hidden');
        analyzeBtn.disabled = true;

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();

            if (response.ok && data.status === 'success') {
                renderResults(data);
            } else {
                alert(data.message || 'An error occurred while inspecting the message.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to connect to the SMS Detector server. Make sure Flask app is running.');
        } finally {
            // Reset Loading State
            btnContent.classList.remove('hidden');
            btnSpinner.classList.add('hidden');
            analyzeBtn.disabled = false;
        }
    });

    function renderResults(data) {
        resultsPlaceholder.classList.add('hidden');
        resultsCard.classList.remove('hidden');

        const { is_scam, confidence_score, risk_level, risk_badge, triggers } = data;

        // Risk Badge & Color Class
        riskBadge.textContent = risk_level;
        riskBadge.className = 'risk-badge';
        if (risk_badge === 'critical') {
            riskBadge.classList.add('badge-critical');
        } else if (risk_badge === 'warning' || risk_badge === 'caution') {
            riskBadge.classList.add('badge-warning');
        } else {
            riskBadge.classList.add('badge-safe');
        }

        // Confidence & Gauge
        confidenceScore.textContent = `${confidence_score}%`;
        setGaugeProgress(confidence_score, is_scam);

        // Verdict Text
        if (is_scam) {
            verdictTitle.textContent = '🚨 Warning: High Scam Risk Message';
            verdictTitle.style.color = '#ef4444';
            verdictDesc.textContent = 'Our Machine Learning security model detected strong indicators of phishing, monetary deception, or urgent account baiting.';
        } else {
            verdictTitle.textContent = '✅ Message Verified Safe';
            verdictTitle.style.color = '#10b981';
            verdictDesc.textContent = 'Our model analyzed text structure and vocabulary and found no high-risk fraud or scam indicators.';
        }

        // Triggers Breakdown
        triggerList.innerHTML = '';
        if (triggers && triggers.length > 0) {
            triggers.forEach(t => {
                const item = document.createElement('div');
                item.className = 'trigger-item';
                item.innerHTML = `
                    <i class="fa-solid fa-triangle-exclamation trigger-icon"></i>
                    <div class="trigger-info">
                        <h5>${t.type}</h5>
                        <p>${t.desc}</p>
                    </div>
                `;
                triggerList.appendChild(item);
            });
        } else {
            triggerList.innerHTML = `
                <div class="no-triggers">
                    <i class="fa-solid fa-shield-check"></i> No suspicious keywords, urgent flags, or phishing links detected.
                </div>
            `;
        }
    }
});
