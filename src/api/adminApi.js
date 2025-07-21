// src/api/adminApi.js

// Adjust to your backend URL (e.g., http://localhost:5000/api or /api if using proxy)
const BASE_URL = "/api";

/**
 * POST: Admin Login
 * @param {Object} credentials { username, password }
 */
export const loginAdmin = async (credentials) => {
    try {
        const response = await fetch(`${BASE_URL}/admin_login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include", // required for Flask session cookies
            body: JSON.stringify(credentials),
        });
        const data = await response.json();
        return { ok: response.ok, data };
    } catch (error) {
        return { ok: false, data: { error: "Server error." } };
    }
};

/**
 * POST: Admin Signup
 * @param {FormData} formData - includes name, dob, emails, experience, username, password, photo
 */
export const signupAdmin = async (formData) => {
    try {
        const response = await fetch(`${BASE_URL}/admin_signup`, {
            method: "POST",
            credentials: "include",
            body: formData,
        });
        const data = await response.json();
        return { ok: response.ok, data };
    } catch (error) {
        return { ok: false, data: { error: "Server error." } };
    }
};

/**
 * POST: Admin Forgot Password
 * @param {string} email
 */
export const forgotAdminPassword = async (email) => {
    try {
        const response = await fetch(`${BASE_URL}/admin_forgot_password`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ admin_email: email }),
        });
        const data = await response.json();
        return { ok: response.ok, data };
    } catch (error) {
        return { ok: false, data: { error: "Server error." } };
    }
};

/**
 * GET: Admin Logout
 */
export const logoutAdmin = async () => {
    try {
        const response = await fetch(`${BASE_URL}/logout`, {
            method: "GET",
            credentials: "include",
        });
        return response.ok;
    } catch (error) {
        return false;
    }
};

/**
 * GET: Fetch Admin Dashboard Data
 * returns { admin_name, staff_list, student_list }
 */
export const fetchAdminDashboardData = async () => {
    try {
        const response = await fetch(`${BASE_URL}/get_admin_dashboard_data`, {
            method: "GET",
            credentials: "include",
        });
        const data = await response.json();
        return { ok: response.ok, data };
    } catch (error) {
        return { ok: false, data: { error: "Server error." } };
    }
};

/**
 * GET: Fetch Students Assigned to a Staff
 * @param {string|number} staffId
 */
export const getStudentsByStaff = async (staffId) => {
    try {
        const response = await fetch(`${BASE_URL}/get_students_by_staff/${staffId}`, {
            method: "GET",
            credentials: "include",
        });
        const data = await response.json();
        return { ok: response.ok, data };
    } catch (error) {
        return { ok: false, data: { error: "Server error." } };
    }
};
