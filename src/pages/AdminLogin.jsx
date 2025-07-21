import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { loginAdmin } from "../api/adminApi"; // ensure your api file path matches

const AdminLogin = () => {
    const [adminUsername, setAdminUsername] = useState("");
    const [adminPassword, setAdminPassword] = useState("");
    const [message, setMessage] = useState("");
    const [messageType, setMessageType] = useState(""); // "flash" | "error"
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const result = await loginAdmin({
            username: adminUsername,
            password: adminPassword
        });

        if (result.ok) {
            setMessage("Login successful!");
            setMessageType("flash");
            setTimeout(() => navigate("/admin/dashboard"), 1000);
        } else {
            setMessage(result.data.error || "Login failed. Check your credentials.");
            setMessageType("error");
        }
    };

    return (
        <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-purple-100 to-purple-200">
            <div className="bg-white p-8 rounded-xl shadow-md w-80 text-center">
                <div className="text-4xl mb-3">🛡️</div>
                <h2 className="text-purple-700 font-bold text-xl mb-2">Admin Login</h2>
                {message && (
                    <p className={`mb-2 font-semibold ${messageType === "flash" ? "text-green-600" : "text-red-600"}`}>
                        {message}
                    </p>
                )}
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        placeholder="Username"
                        value={adminUsername}
                        onChange={(e) => setAdminUsername(e.target.value)}
                        required
                        className="w-full p-3 border border-gray-300 rounded-md mb-3 focus:outline-none focus:border-purple-600"
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={adminPassword}
                        onChange={(e) => setAdminPassword(e.target.value)}
                        required
                        className="w-full p-3 border border-gray-300 rounded-md mb-3 focus:outline-none focus:border-purple-600"
                    />
                    <button
                        type="submit"
                        className="w-full bg-purple-700 text-white py-3 rounded-md font-bold hover:bg-purple-800 transition duration-200"
                    >
                        🔐 Login
                    </button>
                </form>
                <div className="mt-4 space-y-2">
                    <Link to="/admin/signup" className="text-purple-700 hover:text-purple-900 text-sm block">
                        📝 Sign Up
                    </Link>
                    <Link to="/admin/forgot-password" className="text-purple-700 hover:text-purple-900 text-sm block">
                        🔑 Forgot Password?
                    </Link>
                    <Link to="/" className="text-purple-700 hover:text-purple-900 text-sm block">
                        ⬅ Exit to Home
                    </Link>
                </div>
            </div>
            <footer className="fixed bottom-0 w-full text-center py-3 bg-purple-800 text-white text-xs">
                © 2025 BET e-Portal. All rights reserved.
            </footer>
        </div>
    );
};

export default AdminLogin;
