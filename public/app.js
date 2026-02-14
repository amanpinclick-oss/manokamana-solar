/**
 * Manokamana Solar Agentic Engine - Frontend Controller
 * Responsible for fetching data from the local engine folders (reports/ and content/blogs/)
 */

document.addEventListener('DOMContentLoaded', () => {
    initApp();
    loadDashboardStats();
    loadLeadTable();
    loadBlogInsights();

    // Auto-refresh dashboard every 30 seconds
    if (window.location.pathname.includes('dashboard.html')) {
        setInterval(() => {
            loadDashboardStats();
            loadLeadTable();
        }, 30000);
    }
});

function initApp() {
    // Header Scroll Effect
    const header = document.querySelector('header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // ROI Form Handling
    const roiForm = document.getElementById('roi-form');
    if (roiForm) {
        roiForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = roiForm.querySelector('button');
            const originalText = btn.innerText;

            btn.innerText = 'INITIALIZING AGENTIC ANALYSIS...';
            btn.disabled = true;

            // Simulate lead capture process
            setTimeout(() => {
                btn.innerText = 'ANALYSIS COMPLETE. CHECK YOUR EMAIL.';
                btn.style.background = 'var(--success)';
                roiForm.reset();

                setTimeout(() => {
                    btn.innerText = originalText;
                    btn.disabled = false;
                    btn.style.background = '';
                }, 5000);
            }, 2000);
        });
    }
}

async function loadDashboardStats() {
    try {
        const response = await fetch('../reports/system_summary.json');
        if (!response.ok) return;
        const data = await response.json();

        document.getElementById('stat-total-leads').innerText = data.total_leads || 0;

        // Accessing tier_counts based on actual JSON structure
        const tierA = data.tier_counts ? data.tier_counts.A : 0;
        document.getElementById('stat-tier-a').innerText = tierA || 0;

        document.getElementById('stat-phase').innerText = data.published_assets_count > 0 ? 'PHASE 2: OPTIMIZING' : 'PHASE 1: INITIALIZING';

        const health = data.current_risk_health === 'Healthy' ? 100 : 85;
        const healthElement = document.getElementById('stat-health');
        if (healthElement) healthElement.innerText = `${health}%`;

        const lastUpdated = document.getElementById('last-updated');
        if (lastUpdated) {
            lastUpdated.innerText = `LAST SYNC: ${new Date().toLocaleTimeString()}`;
        }
    } catch (e) {
        console.log("Stats not available yet.");
    }
}

async function loadLeadTable() {
    try {
        const response = await fetch('../reports/leads_detailed.csv');
        if (!response.ok) return;
        const csvText = await response.text();
        const rows = csvText.split('\n').filter(r => r.trim()).slice(1); // Skip header and empty rows

        const tbody = document.getElementById('lead-table-body');
        if (!tbody) return;

        tbody.innerHTML = '';
        if (rows.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="padding: 40px; text-align: center; color: var(--text-secondary);">No leads captured in current cycle.</td></tr>';
            return;
        }

        rows.forEach(row => {
            const columns = row.split(',');
            if (columns.length < 3) return;

            const [timestamp, score, capex] = columns;
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td style="padding: 24px;">${timestamp}</td>
                <td style="padding: 24px;"><span style="color: ${score === 'A' ? 'var(--accent)' : '#fff'}; font-weight: 700;">${score}</span></td>
                <td style="padding: 24px;">₹${parseFloat(capex).toLocaleString('en-IN')}</td>
                <td style="padding: 24px;">
                    <span style="padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; background: ${score === 'A' ? 'rgba(255, 180, 0, 0.1)' : 'rgba(255,255,255,0.05)'}; color: ${score === 'A' ? 'var(--accent)' : 'var(--text-secondary)'};">
                        ${score === 'A' ? 'PRIORITY ROUTING' : 'NURTURING'}
                    </span>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.log("Lead data not available yet.");
    }
}

async function loadBlogInsights() {
    const container = document.getElementById('blog-container');
    if (!container) return;

    try {
        const blogs = ['solar-roi-for-industrial-clients'];
        container.innerHTML = '';

        for (const slug of blogs) {
            const response = await fetch(`../content/blogs/${slug}.md`);
            if (!response.ok) continue;
            const text = await response.text();

            // Simplified extraction for the simulation
            const titleMatch = text.match(/# (.*)/);
            const contentMatch = text.split('\n').slice(5, 10).join(' '); // Skip frontmatter

            const card = document.createElement('div');
            card.className = 'glass blog-card fade-in';
            card.innerHTML = `
                <div class="date">High Authority Report</div>
                <h2>${titleMatch ? titleMatch[1] : 'Autonomous Insight'}</h2>
                <p style="margin-top: 16px; color: var(--text-secondary);">
                    ${contentMatch ? contentMatch.substring(0, 250) + '...' : 'Analysis in progress...'}
                </p>
                <div style="margin-top: 24px;">
                    <a href="blog.html?slug=${slug}" style="color: var(--accent); text-decoration: none; font-weight: 600; font-size: 0.9rem;">Read Full Analysis →</a>
                </div>
            `;
            container.appendChild(card);
        }
    } catch (e) {
        console.log("Blogs not available yet.");
    }
}
