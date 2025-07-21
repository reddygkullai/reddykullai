import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Import your pages
import HomePage from "./pages/HomePage";
import AdminLogin from "./pages/admin/AdminLogin";
import AdminSignup from "./pages/admin/AdminSignup";
import AdminDashboard from "./pages/admin/AdminDashboard";
import AdminForgotPassword from "./pages/admin/AdminForgotPassword";

// Placeholder imports for Staff and Student (you can create these later)
import StaffLogin from "./pages/staff/StaffLogin";
import StaffDashboard from "./pages/staff/StaffDashboard";
import StudentLogin from "./pages/student/StudentLogin";
import StudentDashboard from "./pages/student/StudentDashboard";

const App = () => {
    return (
        <Router>
            <Routes>
                {/* Home */}
                <Route path="/" element={<HomePage />} />

                {/* Admin Routes */}
                <Route path="/admin/login" element={<AdminLogin />} />
                <Route path="/admin/signup" element={<AdminSignup />} />
                <Route path="/admin/dashboard" element={<AdminDashboard />} />
                <Route path="/admin/forgot-password" element={<AdminForgotPassword />} />

                {/* Staff Routes */}
                <Route path="/staff/login" element={<StaffLogin />} />
                <Route path="/staff/dashboard" element={<StaffDashboard />} />

                {/* Student Routes */}
                <Route path="/student/login" element={<StudentLogin />} />
                <Route path="/student/dashboard" element={<StudentDashboard />} />

                {/* Optional: 404 Page */}
                <Route
                    path="*"
                    element={
                        <div className="min-h-screen flex items-center justify-center bg-gray-100">
                            <div className="text-center">
                                <h1 className="text-3xl font-bold text-purple-700 mb-2">404 - Page Not Found</h1>
                                <a href="/" className="text-purple-700 hover:underline">
                                    ⬅ Return to Home
                                </a>
                            </div>
                        </div>
                    }
                />
            </Routes>
        </Router>
    );
};

export default App;
