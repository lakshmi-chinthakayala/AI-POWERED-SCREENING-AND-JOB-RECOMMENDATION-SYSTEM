/**
 * REST API Client for AI Resume Screening & Recommendation Backend
 */

const API_BASE = "";

async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: "Server error occurred" }));
            throw new Error(errorData.detail || `Request failed with status ${response.status}`);
        }
        return await response.json();
    } catch (err) {
        console.error(`[API Error] ${endpoint}:`, err);
        throw err;
    }
}

const API = {
    // Upload Resume File
    uploadResume: async (file) => {
        const formData = new FormData();
        formData.append("file", file);
        return await apiRequest("/api/resume/upload", {
            method: "POST",
            body: formData
        });
    },

    // Fetch Resume Analysis Details
    getResumeAnalysis: async (resumeId) => {
        return await apiRequest(`/api/resume/${resumeId}/analysis`);
    },

    // Fetch Job Recommendations & Skill Gap Analysis
    getJobRecommendations: async (resumeId) => {
        return await apiRequest(`/api/recommendations/${resumeId}`);
    },

    // Search and Filter Jobs
    searchJobs: async (params = {}) => {
        const queryStr = new URLSearchParams(params).toString();
        return await apiRequest(`/api/jobs/search?${queryStr}`);
    },

    // Fetch Dashboard Statistics
    getDashboardStats: async (resumeId) => {
        return await apiRequest(`/api/dashboard/stats/${resumeId}`);
    }
};
