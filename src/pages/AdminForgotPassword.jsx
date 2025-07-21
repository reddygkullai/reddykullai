import React, { useState } from "react";
import { Link } from "react-router-dom";
import { forgotAdminPassword } from "../api/adminApi"; // adjust path as per your structure

const AdminForgotPassword = () => {
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");
    const [messageType, setMessageType] = useState(""); // "success" | "error"

    const handleSubmit = async (e) => {
        e.preventDefault();

        const result = await forgotAdminPassword(email);

        if (result.ok) {
            setMessage("Reset link sent successfully. Check your email.");
            setMessageType("success");
            setEmail("");
        } else {
            setMessage(result.data.error || "Failed to send reset link.");
            setMessageType("error");
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="bg-white p-6 rounded-lg shadow-md w-80 text-center">
                <h2 className="text-purple-700 text-lg font-semibold mb-3">
                    Admin Forgot Password
                </h2>

                {message && (
                    <p
                        className={`mb-2 font-semibold ${
                            messageType === "success" ? "text-green-600" : "text-red-600"
                        }`}
                    >
                        {message}
                    </p>
                )}

                <form onSubmit={handleSubmit}>
                    <input
                        type="email"
                        name="admin_email"
                        placeholder="Enter your email"
                        required
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="w-full p-3 border border-gray-300 rounded mb-3 focus:outline-none focus:border-purple-600"
                    />
                    <button
                        type="submit"
                        className="w-full bg-purple-700 text-white font-bold py-2 rounded hover:bg-purple-800 transition"
                    >
                        Send Reset Link
                    </button>
                </form>

                <Link
                    to="/admin/login"
                    className="text-purple-700 text-sm mt-3 inline-block hover:underline"
                >
                    ⬅ Back to Login
                </Link>
            </div>
        </div>
    );
};

export default AdminForgotPassword;
