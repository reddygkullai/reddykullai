import React from "react";
import { Link } from "react-router-dom";

const HomePage = () => {
    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-purple-50 to-purple-100">
            <div className="bg-white p-8 rounded-xl shadow-lg text-center max-w-md w-11/12">
                <h1 className="text-2xl font-bold text-purple-700 mb-4">
                    Welcome to BET e-Portal
                </h1>
                <p className="text-gray-700 mb-6">
                    Please select your role to continue:
                </p>

                <div className="flex flex-col gap-4">
                    <Link
                        to="/admin/login"
                        className="bg-purple-700 text-white font-semibold py-2 rounded hover:bg-purple-800 transition"
                    >
                        👩‍💼 Admin Login
                    </Link>
                    <Link
                        to="/staff/login"
                        className="bg-purple-700 text-white font-semibold py-2 rounded hover:bg-purple-800 transition"
                    >
                        👨‍🏫 Staff Login
                    </Link>
                    <Link
                        to="/student/login"
                        className="bg-purple-700 text-white font-semibold py-2 rounded hover:bg-purple-800 transition"
                    >
                        🎓 Student Login
                    </Link>
                </div>
            </div>

            <footer className="mt-8 text-sm text-gray-600 text-center">
                © 2025 BET e-Portal. All rights reserved.
            </footer>
        </div>
    );
};

export default HomePage;
