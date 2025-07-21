import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { signupAdmin } from "../api/adminApi"; // adjust path based on your structure

const AdminSignup = () => {
    const [formData, setFormData] = useState({
        name: "",
        dob: "",
        personal_email: "",
        alt_email: "",
        years_exp: "",
        username: "",
        password: "",
        photo: null,
    });

    const [message, setMessage] = useState("");
    const [messageType, setMessageType] = useState(""); // "success" | "error"
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value, files } = e.target;
        if (name === "photo") {
            setFormData({ ...formData, [name]: files[0] });
        } else {
            setFormData({ ...formData, [name]: value });
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const result = await signupAdmin(formData);

        if (result.ok) {
            setMessage("Signup successful! Redirecting to login...");
            setMessageType("success");
            setTimeout(() => navigate("/admin/login"), 1500);
        } else {
            setMessage(result.data.error || "Signup failed. Please check your details.");
            setMessageType("error");
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="bg-white p-6 rounded-lg shadow-md w-80 text-center">
                <h2 className="text-purple-700 text-xl font-semibold mb-3">Admin Signup</h2>

                {message && (
                    <div
                        className={`text-sm font-semibold mb-2 ${
                            messageType === "success" ? "text-green-600" : "text-red-600"
                        }`}
                    >
                        {message}
                    </div>
                )}

                <form onSubmit={handleSubmit} encType="multipart/form-data">
                    <input
                        type="text"
                        name="name"
                        placeholder="Name"
                        required
                        value={formData.name}
                        onChange={handleChange}
                        className="w-full p-3 border rounded mb-2 focus:outline-none focus:border-purple-600"
                    />
                    <input
                        type="date"
                        name="dob"
                        required
                        value={formData.dob}
                        onChange={handleChange}
                        className="w-full p-3 border rounded mb-2 focus:outline-none focus:border-purple-600"
                    />
                    <input
                        type="email"
                        name="personal_email"
                        placeholder="Personal Email"
                        required
                        value={formData.personal_email}
                        onChange={handleChange}
                        className="w-full p-3 border rounded mb-2 focus:outline-none focus:border-purple-600"
                    />
                    <input
                        type="email"
                        name="alt_email"
                        placeholder="Alternative Email"
                        required
                        value={formData.alt_email}
                        onChange={handleChange}
                        className="w-full p-3 border rounded mb-2 focus:outline-none focus:border-purple-600"
                    />
                    <input
                        type="number"
                        name="years_exp"
                        placeholder="Years of Experience"
                        required
                        value={formData.years_exp}
                        onChange={handleChange}
                        className="w-full p-3 border rounded mb-2 focus:outline-none focus:border-purple-600"
                    />
                    <input
                        type="text"
                        name="username"
                        placeholder="Username"
                        required
                        value={formData.username}
                        onChange={handleChange}
                        className="w-full p-3 border rounded mb-2 focus:outline-none focus:border-purple-600"
                    />
                    <input
                        type="password"
                        name="password"
                        placeholder="Password"
                        required
                        value={formData.password}
                        onChange={handleChange}
                        className="w-full p-3 border rounded mb-2 focus:outline-none focus:border-purple-600"
                    />
                    <input
                        type="file"
                        name="photo"
                        accept="image/*"
                        required
                        onChange={handleChange}
                        className="w-full p-3 border rounded mb-2"
                    />
                    <button
                        type="submit"
                        className="w-full bg-purple-700 text-white font-bold py-2 rounded hover:bg-purple-800 transition"
                    >
                        Sign Up
                    </button>
                </form>

                <Link
                    to="/admin/login"
                    className="text-purple-700 text-sm mt-3 inline-block hover:underline"
                >
                    ⬅ Back to Admin Login
                </Link>
            </div>
        </div>
    );
};

export default AdminSignup;
