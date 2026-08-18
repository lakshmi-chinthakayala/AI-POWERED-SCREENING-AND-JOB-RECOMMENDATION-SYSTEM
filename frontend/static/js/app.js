/**
 * Main Application Frontend Logic and UI State Manager
 */

let currentResumeId = 1; // Default loaded sample resume ID
let selectedFile = null;
let skillsChartInstance = null;
let jobMatchesChartInstance = null;

// Initialize App
document.addEventListener("DOMContentLoaded", () => {
    setupDragAndDrop();
    setupFileInput();
    executeJobSearch(); // Preload jobs list
});

// View Navigation Router
function showView(viewId) {
    const views = ["landing", "upload", "analysis", "recommendations", "jobs", "dashboard"];
    views.forEach(v => {
        const el = document.getElementById(`view-${v}`);
        const navBtn = document.getElementById(`nav-${v}`);
        if (el) {
            if (v === viewId) {
                el.classList.remove("hidden");
                el.classList.add("animate-fade-in");
            } else {
                el.classList.add("hidden");
            }
        }
        if (navBtn) {
            if (v === viewId) navBtn.classList.add("active");
            else navBtn.classList.remove("active");
        }
    });

    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Trigger dynamic data fetch for specific views
    if (viewId === 'analysis' && currentResumeId) {
        loadResumeAnalysisView(currentResumeId);
    } else if (viewId === 'recommendations' && currentResumeId) {
        loadRecommendationsView(currentResumeId);
    } else if (viewId === 'dashboard' && currentResumeId) {
        loadDashboardView(currentResumeId);
    }
}

// Drag & Drop Setup
function setupDragAndDrop() {
    const dropZone = document.getElementById("drop-zone");
    if (!dropZone) return;

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('border-indigo-500', 'bg-slate-800/50'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('border-indigo-500', 'bg-slate-800/50'), false);
    });

    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelected(files[0]);
        }
    });
}

function setupFileInput() {
    const input = document.getElementById("resume-file-input");
    if (input) {
        input.addEventListener("change", (e) => {
            if (e.target.files.length > 0) {
                handleFileSelected(e.target.files[0]);
            }
        });
    }
}

function handleFileSelected(file) {
    const validExts = ['.pdf', '.docx'];
    const fileName = file.name.toLowerCase();
    const isValid = validExts.some(ext => fileName.endsWith(ext));

    if (!isValid) {
        alert("Please select a valid PDF (.pdf) or Word (.docx) file.");
        return;
    }

    selectedFile = file;
    document.getElementById("file-name").innerText = file.name;
    document.getElementById("file-size").innerText = `${(file.size / (1024 * 1024)).toFixed(2)} MB`;
    
    document.getElementById("file-info").classList.remove("hidden");
    document.getElementById("upload-action").classList.remove("hidden");
}

function removeSelectedFile() {
    selectedFile = null;
    document.getElementById("resume-file-input").value = "";
    document.getElementById("file-info").classList.add("hidden");
    document.getElementById("upload-action").classList.add("hidden");
}

// Upload & Analyze Resume
async function uploadAndAnalyzeResume() {
    if (!selectedFile) return;

    try {
        const btn = document.querySelector("#upload-action button");
        btn.disabled = true;
        btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Processing NLP Extraction...`;

        const res = await API.uploadResume(selectedFile);
        currentResumeId = res.resume_id;

        btn.disabled = false;
        btn.innerHTML = `<i class="fa-solid fa-bolt"></i> Analyze Resume Now`;

        showView("analysis");
    } catch (err) {
        alert(`Error analyzing resume: ${err.message}`);
        const btn = document.querySelector("#upload-action button");
        btn.disabled = false;
        btn.innerHTML = `<i class="fa-solid fa-bolt"></i> Analyze Resume Now`;
    }
}

// Quick Demo Load Sample Resume
async function loadSampleResumeDemo(filename) {
    try {
        // Fetch recommendations directly for demo resumes (seeded IDs 1 to 10)
        let sampleId = 1;
        if (filename.includes("ml_engineer")) sampleId = 2;
        else if (filename.includes("data_scientist")) sampleId = 3;
        else if (filename.includes("python_dev")) sampleId = 4;

        currentResumeId = sampleId;
        showView("analysis");
    } catch (err) {
        alert(`Demo load failed: ${err.message}`);
    }
}

// Renders Resume Analysis View
async function loadResumeAnalysisView(resumeId) {
    try {
        const data = await API.getResumeAnalysis(resumeId);
        
        document.getElementById("an-candidate-name").innerText = data.candidate_info.name || "Candidate Profile";
        document.getElementById("an-filename").innerText = `Source file: ${data.filename}`;
        document.getElementById("an-score-value").innerText = Math.round(data.resume_score);

        // Animate Circle Path
        const circle = document.getElementById("score-circle-path");
        const dashVal = `${Math.round(data.resume_score)}, 100`;
        circle.setAttribute("stroke-dasharray", dashVal);

        document.getElementById("an-email").innerText = data.candidate_info.email;
        document.getElementById("an-phone").innerText = data.candidate_info.phone;
        document.getElementById("an-location").innerText = data.candidate_info.location;
        document.getElementById("an-github").innerText = data.candidate_info.github.replace("https://", "");
        document.getElementById("an-github").href = data.candidate_info.github;

        // Score breakdown
        const sb = data.score_breakdown || {};
        document.getElementById("sb-skills").innerText = `${sb.skills?.score || 90}%`;
        document.getElementById("sb-exp").innerText = `${sb.experience?.score || 85}%`;
        document.getElementById("sb-projects").innerText = `${sb.projects?.score || 85}%`;
        document.getElementById("sb-edu").innerText = `${sb.education?.score || 95}%`;
        document.getElementById("sb-certs").innerText = `${sb.certifications?.score || 75}%`;
        document.getElementById("sb-comp").innerText = `${sb.completeness?.score || 100}%`;

        // Recommendations
        const recList = document.getElementById("an-recommendations-list");
        recList.innerHTML = (data.recommendations || [])
            .map(r => `<li class="flex items-start gap-2"><i class="fa-solid fa-check text-indigo-400 mt-1 text-xs"></i><span>${r}</span></li>`)
            .join("");

        // Render Categorized Skills
        document.getElementById("an-skill-count").innerText = data.skill_count;
        const skillsContainer = document.getElementById("an-skills-container");
        skillsContainer.innerHTML = "";

        const skillsByCat = data.skills_by_category || {};
        Object.keys(skillsByCat).forEach(cat => {
            const skills = skillsByCat[cat];
            if (skills.length > 0) {
                const card = document.createElement("div");
                card.className = "bg-slate-800/60 p-4 rounded-xl border border-slate-700 space-y-2";
                card.innerHTML = `
                    <h4 class="text-xs font-bold uppercase tracking-wider text-indigo-300">${cat}</h4>
                    <div class="flex flex-wrap gap-1.5 pt-1">
                        ${skills.map(s => `<span class="px-2.5 py-1 bg-indigo-500/10 text-indigo-200 border border-indigo-500/20 text-xs rounded-md font-medium">${s}</span>`).join("")}
                    </div>
                `;
                skillsContainer.appendChild(card);
            }
        });

        // Education
        const eduList = document.getElementById("an-education-list");
        eduList.innerHTML = (data.education || []).map(e => `
            <div class="p-3 bg-slate-800/50 rounded-xl border border-slate-700/60">
                <p class="font-semibold text-white text-sm">${e.degree}</p>
                <p class="text-xs text-slate-400">${e.institution} • Grad: ${e.graduation_year}</p>
                <p class="text-xs text-indigo-300 mt-1 font-medium">${e.specialization}</p>
            </div>
        `).join("");

        // Certifications
        const certList = document.getElementById("an-certifications-list");
        certList.innerHTML = (data.certifications || []).map(c => `
            <span class="px-3 py-1.5 bg-violet-500/10 text-violet-300 border border-violet-500/30 text-xs font-medium rounded-lg">
                <i class="fa-solid fa-award mr-1"></i> ${c}
            </span>
        `).join("");

        // Projects
        const projList = document.getElementById("an-projects-list");
        projList.innerHTML = (data.projects || []).map(p => `
            <div class="p-3 bg-slate-800/50 rounded-xl border border-slate-700/60 space-y-1">
                <p class="font-semibold text-white text-sm">${p.name}</p>
                <p class="text-xs text-indigo-300 font-medium">Tech: ${p.technologies}</p>
                <p class="text-xs text-slate-400">${p.description}</p>
            </div>
        `).join("");

        // Experience
        const expList = document.getElementById("an-experience-list");
        expList.innerHTML = (data.experience || []).map(ex => `
            <div class="p-3 bg-slate-800/50 rounded-xl border border-slate-700/60 space-y-1">
                <div class="flex justify-between items-center">
                    <p class="font-semibold text-white text-sm">${ex.role}</p>
                    <span class="text-xs text-slate-400">${ex.duration}</span>
                </div>
                <p class="text-xs text-slate-300">${ex.company}</p>
                <p class="text-xs text-slate-400">${ex.responsibilities}</p>
            </div>
        `).join("");

    } catch (err) {
        console.error("Error loading resume analysis view:", err);
    }
}

// Renders Job Recommendations & Skill Gap View
async function loadRecommendationsView(resumeId) {
    try {
        const data = await API.getJobRecommendations(resumeId);
        document.getElementById("rec-top-role").innerText = data.top_recommended_role;

        const container = document.getElementById("recommendations-container");
        container.innerHTML = "";

        data.recommendations.forEach((job, idx) => {
            const card = document.createElement("div");
            card.className = "bg-slate-900 p-6 rounded-2xl border border-slate-800 space-y-4 hover:border-slate-700 transition";
            
            const matchColor = job.match_percentage >= 80 ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30' :
                               job.match_percentage >= 65 ? 'text-indigo-400 bg-indigo-500/10 border-indigo-500/30' :
                               'text-amber-400 bg-amber-500/10 border-amber-500/30';

            card.innerHTML = `
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
                    <div>
                        <div class="flex items-center gap-3">
                            <span class="w-7 h-7 rounded-full bg-slate-800 text-xs font-bold text-slate-300 flex items-center justify-center">#${idx + 1}</span>
                            <h3 class="text-xl font-bold text-white">${job.job_title}</h3>
                        </div>
                        <p class="text-xs text-slate-400 mt-1">${job.company} • ${job.location} • ${job.employment_type} • ${job.salary}</p>
                    </div>
                    
                    <div class="flex items-center gap-3">
                        <div class="px-4 py-1.5 rounded-xl border font-bold text-base ${matchColor}">
                            ${job.match_percentage}% Match
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                    <!-- Matching Skills -->
                    <div class="bg-slate-800/40 p-4 rounded-xl border border-slate-800 space-y-2">
                        <h4 class="font-bold text-emerald-400 flex items-center gap-1.5">
                            <i class="fa-solid fa-circle-check"></i> Matching Skills (${job.matching_skills.length})
                        </h4>
                        <div class="flex flex-wrap gap-1.5">
                            ${job.matching_skills.map(s => `<span class="px-2.5 py-1 bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 rounded-md">${s}</span>`).join("")}
                        </div>
                    </div>

                    <!-- Missing Skills -->
                    <div class="bg-slate-800/40 p-4 rounded-xl border border-slate-800 space-y-2">
                        <h4 class="font-bold text-amber-400 flex items-center gap-1.5">
                            <i class="fa-solid fa-circle-exclamation"></i> Missing Skills (${job.missing_skills.length})
                        </h4>
                        <div class="flex flex-wrap gap-1.5">
                            ${job.missing_skills.map(s => `<span class="px-2.5 py-1 bg-amber-500/10 text-amber-300 border border-amber-500/20 rounded-md">${s}</span>`).join("")}
                        </div>
                    </div>
                </div>

                <!-- Skill Gap Learning Advice -->
                ${job.skill_gap_recommendations.length > 0 ? `
                    <div class="bg-slate-800/60 p-4 rounded-xl border border-slate-700/60 space-y-2">
                        <h4 class="text-xs font-bold text-indigo-300 uppercase tracking-wider">Skill Gap Learning Recommendations</h4>
                        <div class="space-y-1.5 text-xs text-slate-300">
                            ${job.skill_gap_recommendations.map(r => `
                                <p><span class="font-bold text-white">${r.skill}:</span> ${r.recommendation}</p>
                            `).join("")}
                        </div>
                    </div>
                ` : ''}
            `;
            container.appendChild(card);
        });

    } catch (err) {
        console.error("Error loading recommendations view:", err);
    }
}

// Executes Job Search & Filter Query
async function executeJobSearch() {
    try {
        const q = document.getElementById("filter-q")?.value || "";
        const location = document.getElementById("filter-location")?.value || "All";
        const type = document.getElementById("filter-type")?.value || "All";

        const res = await API.searchJobs({ q, location, employment_type: type });
        const grid = document.getElementById("jobs-grid-container");
        if (!grid) return;

        grid.innerHTML = "";
        res.jobs.forEach(job => {
            const card = document.createElement("div");
            card.className = "bg-slate-900 p-5 rounded-2xl border border-slate-800 space-y-3 hover:border-slate-700 transition";
            card.innerHTML = `
                <div class="flex justify-between items-start">
                    <div>
                        <h3 class="text-lg font-bold text-white">${job.title}</h3>
                        <p class="text-xs text-slate-400">${job.company} • ${job.location}</p>
                    </div>
                    <span class="px-2.5 py-1 bg-slate-800 text-slate-300 rounded-lg text-xs font-medium border border-slate-700">${job.employment_type}</span>
                </div>

                <p class="text-xs text-slate-300 line-clamp-2">${job.description}</p>

                <div class="flex flex-wrap gap-1.5 pt-1">
                    ${job.required_skills.slice(0, 5).map(s => `<span class="px-2 py-0.5 bg-indigo-500/10 text-indigo-300 text-[11px] rounded border border-indigo-500/20">${s}</span>`).join("")}
                </div>

                <div class="flex justify-between items-center pt-2 border-t border-slate-800 text-xs">
                    <span class="font-semibold text-slate-200">${job.salary}</span>
                    <a href="${job.application_url}" target="_blank" class="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-lg transition">Apply Now</a>
                </div>
            `;
            grid.appendChild(card);
        });

    } catch (err) {
        console.error("Error searching jobs:", err);
    }
}

// Renders Interactive Analytics Dashboard View
async function loadDashboardView(resumeId) {
    try {
        const stats = await API.getDashboardStats(resumeId);

        document.getElementById("dash-score").innerText = Math.round(stats.resume_score);
        document.getElementById("dash-skills").innerText = stats.skills_count;
        document.getElementById("dash-projects").innerText = stats.projects_count;
        document.getElementById("dash-certs").innerText = stats.certifications_count;
        document.getElementById("dash-exp").innerText = stats.years_of_experience;
        document.getElementById("dash-top-match").innerText = `${stats.top_match_percentage}%`;

        // Render Chart 1: Skills Category Distribution
        const ctxSkills = document.getElementById("chart-skills-dist").getContext("2d");
        if (skillsChartInstance) skillsChartInstance.destroy();

        const skillLabels = Object.keys(stats.skills_distribution);
        const skillValues = Object.values(stats.skills_distribution);

        skillsChartInstance = new Chart(ctxSkills, {
            type: 'doughnut',
            data: {
                labels: skillLabels,
                datasets: [{
                    data: skillValues,
                    backgroundColor: ['#6366f1', '#8b5cf6', '#ec4899', '#10b981', '#f59e0b', '#06b6d4', '#3b82f6']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'right', labels: { color: '#94a3b8', font: { size: 11 } } }
                }
            }
        });

        // Render Chart 2: Top Job Match Bar Chart
        const ctxMatches = document.getElementById("chart-job-matches").getContext("2d");
        if (jobMatchesChartInstance) jobMatchesChartInstance.destroy();

        const jobTitles = stats.top_matching_jobs.map(j => j.job_title);
        const matchPercentages = stats.top_matching_jobs.map(j => j.match_percentage);

        jobMatchesChartInstance = new Chart(ctxMatches, {
            type: 'bar',
            data: {
                labels: jobTitles,
                datasets: [{
                    label: 'Match Score (%)',
                    data: matchPercentages,
                    backgroundColor: '#6366f1',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { display: false } },
                    y: { min: 0, max: 100, ticks: { color: '#94a3b8' }, grid: { color: '#334155' } }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });

    } catch (err) {
        console.error("Error loading dashboard view:", err);
    }
}
