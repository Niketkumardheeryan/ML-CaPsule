/* ===== FALLING RUPEE SYMBOLS ===== */
(function () {
    const container = document.getElementById('rupeeFall');
    const count = 22;
    for (let i = 0; i < count; i++) {
        const el = document.createElement('span');
        el.className = 'rupee-symbol';
        el.textContent = '₹';
        el.style.left = Math.random() * 100 + 'vw';
        el.style.fontSize = (1.8 + Math.random() * 1.8) + 'rem';
        const dur = 8 + Math.random() * 12;
        const delay = Math.random() * 14;
        el.style.animation = `fall ${dur}s ${delay}s linear infinite`;
        container.appendChild(el);
    }
})();

/* ===== HELPERS ===== */
const EXAMPLE_QUERY = `I run a boutique fashion label in Mumbai, generating an average monthly net income of ₹4,20,000. My core personal cost of living, including apartment rent, utilities, transport, and household groceries, totals ₹1,20,000. I invest ₹85,000 monthly in premium design software, fabric sourcing platforms, and local fashion networking events. My discretionary spending on high-end trends, client dinners, and personal luxury shopping is around ₹70,000. I also fully sponsor my mother's medical treatments and insurance, which costs ₹60,000/month. My total monthly expenditure stands at ₹3,35,000, and I have zero debt. Is my current lifestyle and business spending sustainable given that fashion retail revenue is highly seasonal and fluctuates?`;

function fc(val) {
    return '₹' + Number(val).toLocaleString('en-IN', { maximumFractionDigits: 2 });
}

function pillClass(text) {
    const t = (text || '').toLowerCase();
    if (t.includes('yes') || t.includes('sufficient') || t.includes('enough') || t.includes('worth') && !t.includes('not')) return 'pill-green';
    if (t.includes('no') || t.includes('not')) return 'pill-red';
    return 'pill-blue';
}

function renderMarkdown(text) {
    return text
        .replace(/### (.+)/g, '<h3>$1</h3>')
        .replace(/## (.+)/g, '<h2>$1</h2>')
        .replace(/# (.+)/g, '<h1>$1</h1>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        .replace(/^[\*\-] (.+)/gm, '<li>$1</li>')
        .replace(/(<li>.*<\/li>[\n]?)+/g, m => '<ul>' + m + '</ul>')
        .replace(/\n\n/g, '<br><br>');
}

/* In-memory store for guest/logged-in sessions */
let chatHistory = [];

/* ===== FIREBASE AUTH ACTIONS ===== */
window.signInGoogle = async function () {
    if (!window._fbAuth || !window._fbProvider) return;
    try {
        const { signInWithPopup } = await import('https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js');
        await signInWithPopup(window._fbAuth, window._fbProvider);
    } catch (e) {
        if (e.code && e.code !== 'auth/popup-closed-by-user' && e.code !== 'auth/cancelled-popup-request') {
            console.error('Sign-in error:', e);
        }
    }
};

window.signOutUser = async function () {
    if (!window._fbAuth) return;
    await window._fbSignOut(window._fbAuth);
    chatHistory = [];
    _recentChats = [];
    _savedBudgets = [];
    document.getElementById('dashMessages').innerHTML = '';
    document.getElementById('recentChatsList').innerHTML = '';
};

// Your existing window function updated to manage the 'active' state
window.toggleSidebar = function () {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
    }
};

// Global click listener to close the sidebar when clicking outside
document.addEventListener('click', function (event) {
    const sidebar = document.getElementById('sidebar');
    const menuButton = document.getElementById('menuButton');

    // Only run if the sidebar exists and currently has the 'active' class
    if (sidebar && sidebar.classList.contains('active')) {
        
        // If the click did NOT happen inside the sidebar AND NOT inside the menu button
        if (!sidebar.contains(event.target) && !menuButton.contains(event.target)) {
            sidebar.classList.remove('active');
        }
    }
});


/* ===== CHAT HELPERS ===== */
function appendMsg(containerId, role, content) {
    const box = document.getElementById(containerId);
    const wrap = document.createElement('div');
    wrap.className = 'msg ' + (role === 'user' ? 'user-msg' : 'finan-msg');

    let avatar;
    if (role === 'user' && window._currentUser && window._currentUser.photoURL) {
        avatar = document.createElement('img');
        avatar.src = window._currentUser.photoURL;
        avatar.alt = window._currentUser.displayName || 'You';
        avatar.className = 'msg-avatar avatar-img';
        avatar.referrerPolicy = 'no-referrer';
    } else {
        avatar = document.createElement('span');
        avatar.className = 'msg-avatar';
        avatar.textContent = role === 'user' ? '👤' : 'F₹';
    }

    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';

    if (typeof content === 'string') {
        //using .innerHTML is not a big issue here however it is best to user .setHTML most of the modern
        //browsers with remove harmful code like <script> clickon or <iframe> and others
        bubble.setHTML(content);
    } else {
        bubble.appendChild(content);
    }

    wrap.appendChild(avatar);
    wrap.appendChild(bubble);
    box.appendChild(wrap);
    box.scrollTop = box.scrollHeight;
    return bubble;
}

function showTyping(containerId) {
    const box = document.getElementById(containerId);
    const wrap = document.createElement('div');
    wrap.className = 'msg finan-msg';
    wrap.id = 'typingIndicator';

    const avatar = document.createElement('span');
    avatar.className = 'msg-avatar';
    avatar.textContent = 'F₹';

    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble typing-bubble';
    bubble.innerHTML = '<span></span><span></span><span></span>';

    wrap.appendChild(avatar);
    wrap.appendChild(bubble);
    box.appendChild(wrap);
    box.scrollTop = box.scrollHeight;
}

function removeTyping() {
    const el = document.getElementById('typingIndicator');
    if (el) el.remove();
}

/* ===== BUILD RESULT DOM ===== */
function buildResultNode(data, showSaveBtn) {
    const frag = document.createDocumentFragment();

    // Cards row
    const cards = document.createElement('div');
    cards.className = 'result-cards';

    // Extracted info card
    const c1 = document.createElement('div');
    c1.className = 'r-card';
    c1.innerHTML = `<h4>Extracted Info</h4><table>
        <tr><td>Income</td><td>${fc(data.extracted.monthly_income)}</td></tr>
        <tr><td>Cost of Living</td><td>${fc(data.extracted.cost_of_living)}</td></tr>
        <tr><td>Investments</td><td>${fc(data.extracted.investments)}</td></tr>
        <tr><td>Lifestyle</td><td>${fc(data.extracted.consumerist)}</td></tr>
        <tr><td>Emergency</td><td>${fc(data.extracted.crisis_shock)}</td></tr>
        <tr><td>Total Spend</td><td>${fc(data.extracted.total_expenditure)}</td></tr>
        <tr><td>Debt</td><td>${data.extracted.debt_status}</td></tr>
    </table>`;

    // Predictions card
    const c2 = document.createElement('div');
    c2.className = 'r-card';
    c2.innerHTML = `<h4>ML Predictions</h4>
        <table>
          <tr><td>Financial State</td><td><span class="badge-pill pill-blue">${data.predictions.financial_state}</span></td></tr>
          <tr><td>Income OK?</td><td><span class="badge-pill ${pillClass(data.predictions.income_sufficient)}">${data.predictions.income_sufficient}</span></td></tr>
          <tr><td>Spending OK?</td><td><span class="badge-pill ${pillClass(data.predictions.expenditure_worth_it)}">${data.predictions.expenditure_worth_it}</span></td></tr>
        </table>`;

    // Suggested budgets card
    const c3 = document.createElement('div');
    c3.className = 'r-card';
    c3.innerHTML = `<h4>Suggested Budgets</h4><table>
        <tr><td>Cost of Living</td><td>${fc(data.budgets.cost_of_living)}</td></tr>
        <tr><td>Investments</td><td>${fc(data.budgets.investments)}</td></tr>
        <tr><td>Lifestyle</td><td>${fc(data.budgets.consumerist)}</td></tr>
        <tr><td>Emergency</td><td>${fc(data.budgets.crisis_shock)}</td></tr>
    </table>`;

    cards.appendChild(c1);
    cards.appendChild(c2);
    cards.appendChild(c3);
    frag.appendChild(cards);

    // Save button for logged-in users
    if (showSaveBtn && window._currentUser) {
        const btn = document.createElement('button');
        btn.className = 'save-budget-btn';
        btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z"></path></svg>`;
        btn.onclick = () => saveBudget(data, btn);
        frag.appendChild(btn);
    }

    // Advice
    const adv = document.createElement('div');
    adv.className = 'advice-text';
    adv.innerHTML = renderMarkdown(data.advice);
    frag.appendChild(adv);

    return frag;
}

/* ===== CALL API ===== */
async function callAnalyze(query, messagesId, sendBtn) {
    sendBtn.disabled = true;
    showTyping(messagesId);

    try {
        const res = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        const data = await res.json();
        removeTyping();

        if (!res.ok || data.error) {
            appendMsg(messagesId, 'finan', `<span style="color:#ff6b6b">${data.error || 'An error occurred. Please try again.'}</span>`);
            return;
        }

        const node = buildResultNode(data, messagesId === 'dashMessages');
        const bubble = appendMsg(messagesId, 'finan', node);

        if (messagesId === 'dashMessages') {
            chatHistory.push({ role: 'finan', data });
            saveRecentChat(query, data);
        }

    } catch (e) {
        removeTyping();
        appendMsg(messagesId, 'finan', `<span style="color:#ff6b6b">Network error: ${e.message}</span>`);
    } finally {
        sendBtn.disabled = false;
    }
}

/* ===== FILL EXAMPLE PROMPT ===== */
window.fillExample = function () {
    const inp = document.getElementById('guestInput');
    inp.value = EXAMPLE_QUERY;
    inp.focus();
    inp.style.height = 'auto';
    inp.style.height = inp.scrollHeight + 'px';
};

/* ===== GUEST SEND ===== */
window.guestSend = async function () {
    const inp = document.getElementById('guestInput');
    const query = inp.value.trim();
    if (!query) return;
    inp.value = '';
    appendMsg('guestMessages', 'user', query);
    await callAnalyze(query, 'guestMessages', document.getElementById('guestSendBtn'));
};

document.getElementById('guestInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); window.guestSend(); }
});

/* ===== DASHBOARD SEND ===== */
window.dashSend = async function () {
    const inp = document.getElementById('dashInput');
    const query = inp.value.trim();
    if (!query) return;
    inp.value = '';
    closeBudgets();
    appendMsg('dashMessages', 'user', query);
    await callAnalyze(query, 'dashMessages', document.getElementById('dashSendBtn'));
};

document.getElementById('dashInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); window.dashSend(); }
});

/* ===== NEW CHAT ===== */
window.startNewChat = function () {
    document.getElementById('dashMessages').innerHTML = `
        <div class="msg finan-msg">
            <span class="msg-avatar">F₹</span>
            <div class="msg-bubble">
                Starting a new chat! Tell me about your financial situation and I'll provide personalised advice for the Indian economic landscape.
            </div>
        </div>`;
    chatHistory = [];
    closeBudgets();
    if (window.innerWidth <= 768) document.getElementById('sidebar').classList.remove('open');
};

/* ===== FIRESTORE HELPERS ===== */
let _recentChats = [];
let _savedBudgets = [];

function chatsRef() {
    if (!window._currentUser || !window._db) return null;
    return window._fsCollection(window._db, 'users', window._currentUser.uid, 'chats');
}
function budgetsRef() {
    if (!window._currentUser || !window._db) return null;
    return window._fsCollection(window._db, 'users', window._currentUser.uid, 'budgets');
}

async function saveRecentChat(query, responseData) {
    const ref = chatsRef(); if (!ref) return;
    const snippet = query.substring(0, 55) + (query.length > 55 ? '…' : '');
    const storedResponse = responseData ? {
        extracted: responseData.extracted,
        predictions: responseData.predictions,
        budgets: responseData.budgets,
        advice: (responseData.advice || '').substring(0, 4000)
    } : null;
    try {
        await window._fsAddDoc(ref, { text: snippet, full: query, ts: Date.now(), response: storedResponse });
        await loadRecentChats();
    } catch (e) { console.error('saveRecentChat:', e); }
}

window.loadRecentChats = async function () {
    const ref = chatsRef(); if (!ref) return;
    const list = document.getElementById('recentChatsList');
    list.innerHTML = '<div style="font-size:0.78rem;color:var(--text-dim);padding:0.4rem 0.8rem;">Loading…</div>';
    try {
        const q = window._fsQuery(ref, window._fsOrderBy('ts', 'desc'));
        const snap = await window._fsGetDocs(q);
        _recentChats = snap.docs.map(d => ({ id: d.id, ...d.data() }));
    } catch (e) { console.error('loadRecentChats:', e); _recentChats = []; }

    if (_recentChats.length === 0) {
        list.innerHTML = '<div style="font-size:0.78rem;color:var(--text-dim);padding:0.4rem 0.8rem;">No recent chats</div>';
        return;
    }
    list.innerHTML = _recentChats.map((c, i) => `
        <div class="chat-history-item" onclick="loadChat(${i})">
            <span style="flex-shrink:0">💬</span>
            <span class="chat-item-label">${c.text}</span>
            <button class="chat-item-del" onclick="deleteRecentChat(${i}, event)" title="Delete">✕</button>
        </div>`).join('');
};

window.deleteRecentChat = async function (i, e) {
    e.stopPropagation();
    const chat = _recentChats[i];
    if (!chat || !window._db || !window._currentUser) return;
    try {
        await window._fsDeleteDoc(window._fsDoc(window._db, 'users', window._currentUser.uid, 'chats', chat.id));
        await loadRecentChats();
    } catch (e) { console.error('deleteRecentChat:', e); }
};

window.clearAllChats = async function () {
    if (!confirm('Delete all recent chats? This cannot be undone.')) return;
    const ref = chatsRef(); if (!ref) return;
    try {
        const snap = await window._fsGetDocs(ref);
        const batch = window._fsWriteBatch(window._db);
        snap.docs.forEach(d => batch.delete(d.ref));
        await batch.commit();
        await loadRecentChats();
    } catch (e) { console.error('clearAllChats:', e); }
};

window.loadChat = async function (i) {
    const chat = _recentChats[i]; if (!chat) return;
    closeBudgets();
    if (window.innerWidth <= 768) document.getElementById('sidebar').classList.remove('open');

    const msgs = document.getElementById('dashMessages');
    msgs.innerHTML = '';
    const query = chat.full || chat.text;
    appendMsg('dashMessages', 'user', query);

    if (chat.response) {
        const node = buildResultNode(chat.response, true);
        appendMsg('dashMessages', 'finan', node);
    } else {
        await callAnalyze(query, 'dashMessages', document.getElementById('dashSendBtn'));
    }
};

/* ===== SAVE BUDGET ===== */
window.saveBudget = async function (data, btn) {
    const ref = budgetsRef(); if (!ref) return;
    try {
        await window._fsAddDoc(ref, {
            date: new Date().toLocaleDateString('en-IN'),
            income: data.extracted.monthly_income,
            state: data.predictions.financial_state,
            col: data.budgets.cost_of_living,
            inv: data.budgets.investments,
            con: data.budgets.consumerist,
            crisis: data.budgets.crisis_shock,
            ts: Date.now()
        });
        btn.textContent = '✓ Saved!';
        btn.disabled = true;
        setTimeout(() => {
            btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z"></path></svg>`;
            btn.disabled = false;
        }, 2000);
    } catch (e) { console.error('saveBudget:', e); }
};

/* ===== SHOW BUDGETS PANEL ===== */
async function renderBudgetTable() {
    const ref = budgetsRef();
    const wrap = document.getElementById('budgetTableWrap');
    wrap.innerHTML = '<p class="no-budgets">Loading…</p>';
    if (!ref) {
        wrap.innerHTML = '<p class="no-budgets">Sign in to view saved budgets.</p>';
        return;
    }
    try {
        const q = window._fsQuery(ref, window._fsOrderBy('ts', 'desc'));
        const snap = await window._fsGetDocs(q);
        _savedBudgets = snap.docs.map(d => ({ id: d.id, ...d.data() }));
    } catch (e) { console.error('renderBudgetTable:', e); _savedBudgets = []; }

    if (_savedBudgets.length === 0) {
        wrap.innerHTML = '<p class="no-budgets">No saved budgets yet. Ask Finan for advice and save your suggested budget.</p>';
        return;
    }
    wrap.innerHTML = `<table class="budget-table">
        <thead><tr>
            <th>Date</th><th>Monthly Income</th><th>Financial State</th>
            <th>Cost of Living</th><th>Investments</th><th>Lifestyle</th><th>Emergency</th><th></th>
        </tr></thead>
        <tbody>${_savedBudgets.map((b, i) => `<tr>
            <td>${b.date}</td>
            <td class="amt">${fc(b.income)}</td>
            <td>${b.state}</td>
            <td class="amt">${fc(b.col)}</td>
            <td class="amt">${fc(b.inv)}</td>
            <td class="amt">${fc(b.con)}</td>
            <td class="amt">${fc(b.crisis)}</td>
            <td><button class="budget-del-btn" onclick="deleteBudget(${i})" title="Delete this entry">✕</button></td>
        </tr>`).join('')}</tbody>
    </table>`;
}

window.showBudgets = async function () {
    document.getElementById('budgetPanel').classList.remove('hidden');
    await renderBudgetTable();
    if (window.innerWidth <= 768) document.getElementById('sidebar').classList.remove('open');
};

window.deleteBudget = async function (i) {
    const b = _savedBudgets[i];
    if (!b || !window._db || !window._currentUser) return;
    try {
        await window._fsDeleteDoc(window._fsDoc(window._db, 'users', window._currentUser.uid, 'budgets', b.id));
        await renderBudgetTable();
    } catch (e) { console.error('deleteBudget:', e); }
};

window.clearAllBudgets = async function () {
    if (!confirm('Delete all saved budgets? This cannot be undone.')) return;
    const ref = budgetsRef(); if (!ref) return;
    try {
        const snap = await window._fsGetDocs(ref);
        const batch = window._fsWriteBatch(window._db);
        snap.docs.forEach(d => batch.delete(d.ref));
        await batch.commit();
        await renderBudgetTable();
    } catch (e) { console.error('clearAllBudgets:', e); }
};

window.exportBudgetsCSV = function () {
    if (_savedBudgets.length === 0) return alert('No budgets to export.');
    const header = 'Date,Monthly Income,Financial State,Cost of Living,Investments,Lifestyle,Emergency\n';
    const rows = _savedBudgets.map(b =>
        `${b.date},${b.income},${b.state},${b.col},${b.inv},${b.con},${b.crisis}`
    ).join('\n');
    const blob = new Blob([header + rows], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'finan_budgets.csv'; a.click();
    URL.revokeObjectURL(url);
};

window.closeBudgets = function () {
    document.getElementById('budgetPanel').classList.add('hidden');
};