// Get marketing data from localStorage or use default data
const marketingData = (() => {
    const storedData = localStorage.getItem('marketingData');
    if (storedData) {
        const parsedData = JSON.parse(storedData);
        localStorage.removeItem('marketingData');
        
        console.log('Parsed Data:', parsedData);
        
        // The data is already in the correct structure from contentSuggestions
        return {
            user_id: "1",
            message: "Onboarding successful",
            status: "success",
            recommended_features: parsedData.features,
            marketing_channels: parsedData.marketing_channels,
            marketing_plan: parsedData.marketing_plan
        };
    }
    return {
        user_id: "1",
        message: "Onboarding successful",
        status: "success",
        recommended_features: [
            "marketing and content generation",
            "sales manager for hardware",
            "inventory management",
            "revenue management",
            "customer support",
            "engineering",
            "warehouse management",
            "accounting",
        ],
        marketing_channels: {
            recommended_channels: [
                {
                    channel: "LinkedIn",
                    priority: "high",
                    reason: "B2B focused, professional network for business connections and lead generation",
                },
                {
                    channel: "Email Marketing",
                    priority: "high",
                    reason: "Direct communication to businesses and wholesalers, effective for promotions and sales",
                },
                {
                    channel: "Content Marketing/Blog",
                    priority: "medium",
                    reason: "Thought leadership, SEO, and content sharing for industry engagement and education",
                },
                {
                    channel: "Trade Shows",
                    priority: "medium",
                    reason: "Direct interaction with potential clients, showcasing products and building relationships",
                },
                {
                    channel: "Direct Mail",
                    priority: "low",
                    reason: "Tangible promotional materials, effective follow-up to existing clients or leads",
                },
            ]
        },
        marketing_plan: {
            plan_overview: {
                duration_days: 90,
                start_date: "2023-04-01",
                primary_goals: [
                    "Increase sales by 20% within the 90-day period",
                    "Expand business connections with 50 new B2B contacts",
                    "Improve brand visibility within the target industry",
                ],
            },
            phases: [
                {
                    phase: "Awareness and Engagement",
                    duration_days: 30,
                    start_day: 1,
                    end_day: 30,
                    description:
                        "Focus on building brand awareness and engaging with potential clients through LinkedIn, Email Marketing, and Content Marketing/Blog.",
                    objectives: [
                        "Establish a consistent posting schedule on LinkedIn and Content Marketing/Blog",
                        "Send out weekly promotional emails to existing clients and leads",
                        "Connect with at least 10 new B2B contacts per week on LinkedIn",
                    ],
                },
                {
                    phase: "Lead Generation and Conversion",
                    duration_days: 30,
                    start_day: 31,
                    end_day: 60,
                    description:
                        "Transition from awareness to lead generation and conversion by utilizing targeted Email Marketing campaigns and attending Trade Shows.",
                    objectives: [
                        "Attend at least 1 trade show during this phase",
                        "Send out bi-weekly targeted email campaigns to potential clients",
                        "Follow up with leads from trade shows and previous email campaigns",
                    ],
                },
                {
                    phase: "Client Retention and Expansion",
                    duration_days: 30,
                    start_day: 61,
                    end_day: 90,
                    description:
                        "Focus on retaining existing clients and expanding business relationships through Email Marketing, Direct Mail, and LinkedIn.",
                    objectives: [
                        "Send out monthly newsletters to existing clients",
                        "Send out targeted promotional materials to potential clients via Direct Mail",
                        "Connect with at least 5 existing clients per week on LinkedIn and engage in conversations",
                    ],
                },
            ],
            channel_schedules: [
                {
                    channel: "LinkedIn",
                    priority: "high",
                    frequency: "daily",
                    best_posting_times: ["8:00 AM", "12:00 PM", "5:00 PM"],
                    content_types: ["Industry news", "Product showcases", "Thought leadership articles"],
                    weekly_schedule: {
                        Monday: ["Industry news"],
                        Wednesday: ["Product showcases"],
                        Friday: ["Thought leadership articles"],
                    },
                },
                {
                    channel: "Email Marketing",
                    priority: "high",
                    frequency: "weekly",
                    best_posting_times: ["Tuesday, 10:00 AM", "Thursday, 2:00 PM"],
                    content_types: ["Promotional offers", "Company updates", "Targeted product showcases"],
                    weekly_schedule: {
                        Tuesday: ["Promotional offers"],
                        Thursday: ["Company updates", "Targeted product showcases"],
                    },
                },
                {
                    channel: "Content Marketing/Blog",
                    priority: "medium",
                    frequency: "bi-weekly",
                    best_posting_times: ["Monday, 9:00 AM"],
                    content_types: ["How-to guides", "Industry insights", "Product tutorials"],
                    weekly_schedule: {
                        Monday: ["How-to guides", "Industry insights", "Product tutorials"],
                    },
                },
                {
                    channel: "Trade Shows",
                    priority: "medium",
                    frequency: "monthly",
                    best_posting_times: [],
                    content_types: ["Product demonstrations", "Networking opportunities", "Business relationship building"],
                    weekly_schedule: null,
                },
                {
                    channel: "Direct Mail",
                    priority: "low",
                    frequency: "monthly",
                    best_posting_times: [],
                    content_types: ["Promotional flyers", "Catalogs", "Follow-up letters"],
                    weekly_schedule: null,
                },
            ],
            resource_allocation: {
                budget_distribution: {
                    LinkedIn: 0.2,
                    "Email Marketing": 0.4,
                    "Content Marketing/Blog": 0.1,
                    "Trade Shows": 0.2,
                    "Direct Mail": 0.1,
                },
                team_requirements: {
                    "Social Media Manager": 1,
                    "Email Marketing Specialist": 1,
                    "Content Writer": 0.5,
                    "Event Coordinator": 0.5,
                    "Graphic Designer": 0.5,
                },
            },
            kpis: [
                {
                    metric: "Website traffic",
                    target: "20% increase",
                    measurement_frequency: "monthly",
                },
                {
                    metric: "Email open rate",
                    target: "25%",
                    measurement_frequency: "weekly",
                },
                {
                    metric: "Leads generated",
                    target: "100",
                    measurement_frequency: "monthly",
                },
                {
                    metric: "Sales conversion rate",
                    target: "25%",
                    measurement_frequency: "monthly",
                },
                {
                    metric: "Client retention rate",
                    target: "90%",
                    measurement_frequency: "monthly",
                },
            ],
            generated_at: "2025-02-14T16:14:07.257259",
            plan_version: "1.0",
        },
    };
})();

document.addEventListener("DOMContentLoaded", () => {
    console.log('Full Marketing Data:', marketingData);
    console.log('Features:', marketingData.recommended_features);
    console.log('Channels:', marketingData.marketing_channels);
    console.log('Marketing Plan:', marketingData.marketing_plan);
    
    renderUserInfo();
    renderFeatures();
    renderMarketingChannels();
    renderMarketingPlan();
    renderKPIs();
    initializeAnimations();
});

function renderUserInfo() {
    const userDetails = document.getElementById("user-details");
    userDetails.innerHTML = `
        <div class="card fade-in">
            <p><strong>User ID:</strong> 1</p>
            <p><strong>Status:</strong> <span class="success">Active</span></p>
        </div>
    `;
}

function renderFeatures() {
    const featureList = document.getElementById("feature-list");
    const features = marketingData.recommended_features;
    
    if (!features || !Array.isArray(features)) {
        console.error('Features data is missing or invalid:', features);
        return;
    }
    
    const featuresHTML = features
        .map((feature, index) => `
            <li class="feature-item fade-in" style="animation-delay: ${index * 0.1}s">
                <span class="feature-text">${feature}</span>
            </li>
        `).join('');
    
    featureList.innerHTML = featuresHTML;
}

function renderMarketingChannels() {
    const channelGrid = document.getElementById("channel-grid");
    const channels = marketingData.marketing_channels?.recommended_channels;
    
    if (!channels || !Array.isArray(channels)) {
        console.error('Channels data is missing or invalid:', channels);
        return;
    }
    
    const channelsHTML = channels
        .map((channel, index) => `
            <div class="channel-card fade-in" style="animation-delay: ${index * 0.1}s">
                <h3 class="channel-name">${channel.channel}</h3>
                <div class="priority-badge ${channel.priority}">${channel.priority}</div>
                <p class="channel-reason">${channel.reason}</p>
            </div>
        `).join('');
    
    channelGrid.innerHTML = channelsHTML;
}

function renderMarketingPlan() {
    renderPlanOverview();
    renderPlanPhases();
    renderChannelSchedules();
    renderResourceAllocation();
}

function renderPlanOverview() {
    const planOverview = document.getElementById("plan-overview");
    if (!marketingData.marketing_plan?.plan_overview) return;
    
    const overview = marketingData.marketing_plan.plan_overview;
    planOverview.innerHTML = `
        <div class="overview-card fade-in">
            <h3>Plan Duration: ${overview.duration_days} days</h3>
            <p><strong>Start Date:</strong> ${overview.start_date}</p>
            <div class="goals-section">
                <h4>Primary Goals:</h4>
                <ul>
                    ${overview.primary_goals.map(goal => `
                        <li>${goal}</li>
                    `).join('')}
                </ul>
            </div>
        </div>
    `;
}

function renderPlanPhases() {
    const planPhases = document.getElementById("plan-phases");
    if (!marketingData.marketing_plan?.phases) return;
    
    const phasesHTML = marketingData.marketing_plan.phases
        .map((phase, index) => `
            <div class="phase-card fade-in" style="animation-delay: ${index * 0.1}s">
                <div class="phase-header">
                    <h3>${phase.phase}</h3>
                    <span class="phase-duration">Days ${phase.start_day}-${phase.end_day}</span>
                </div>
                <p class="phase-description">${phase.description}</p>
                <div class="objectives">
                    <h4>Objectives:</h4>
                    <ul>
                        ${phase.objectives.map(objective => `
                            <li>${objective}</li>
                        `).join('')}
                    </ul>
                </div>
            </div>
        `).join('');
    
    planPhases.innerHTML = phasesHTML;
}

function renderChannelSchedules() {
    const schedules = document.getElementById("channel-schedules");
    if (!marketingData.marketing_plan?.channel_schedules) return;
    
    const schedulesHTML = marketingData.marketing_plan.channel_schedules
        .map((schedule, index) => `
            <div class="schedule-card fade-in" style="animation-delay: ${index * 0.1}s">
                <h3>${schedule.channel}</h3>
                <div class="schedule-details">
                    <p><strong>Priority:</strong> ${schedule.priority}</p>
                    <p><strong>Frequency:</strong> ${schedule.frequency}</p>
                    ${schedule.best_posting_times.length ? `
                        <div class="posting-times">
                            <h4>Best Posting Times:</h4>
                            <ul>
                                ${schedule.best_posting_times.map(time => `
                                    <li>${time}</li>
                                `).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    <div class="content-types">
                        <h4>Content Types:</h4>
                        <ul>
                            ${schedule.content_types.map(type => `
                                <li>${type}</li>
                            `).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        `).join('');
    
    schedules.innerHTML = schedulesHTML;
}

function renderResourceAllocation() {
    const allocation = document.getElementById("resource-allocation");
    if (!marketingData.marketing_plan?.resource_allocation) return;
    
    const resources = marketingData.marketing_plan.resource_allocation;
    allocation.innerHTML = `
        <div class="resource-card fade-in">
            <div class="budget-section">
                <h3>Budget Distribution</h3>
                <ul>
                    ${Object.entries(resources.budget_distribution).map(([channel, budget]) => `
                        <li><strong>${channel}:</strong> ${budget}</li>
                    `).join('')}
                </ul>
            </div>
            <div class="team-section">
                <h3>Team Requirements</h3>
                <ul>
                    ${Object.entries(resources.team_requirements).map(([role, count]) => `
                        <li><strong>${role}:</strong> ${count}</li>
                    `).join('')}
                </ul>
            </div>
        </div>
    `;
}

function renderKPIs() {
    const kpiGrid = document.getElementById("kpi-grid");
    if (!marketingData.marketing_plan?.kpis) return;
    
    const kpisHTML = marketingData.marketing_plan.kpis
        .map((kpi, index) => `
            <div class="kpi-card fade-in" style="animation-delay: ${index * 0.1}s">
                <h3>${kpi.metric}</h3>
                <p class="kpi-target">Target: ${kpi.target}</p>
                <p class="kpi-frequency">Measured: ${kpi.measurement_frequency}</p>
            </div>
        `).join('');
    
    kpiGrid.innerHTML = kpisHTML;
}