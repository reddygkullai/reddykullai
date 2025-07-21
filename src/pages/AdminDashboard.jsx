import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
    fetchAdminDashboardData,
    logoutAdmin,
    getStudentsByStaff
} from "../api/adminApi"; // ensure this path matches your structure

const AdminDashboard = () => {
    const [adminName, setAdminName] = useState("Admin");
    const [staffList, setStaffList] = useState([]);
    const [studentList, setStudentList] = useState([]);
    const navigate = useNavigate();

    // Fetch admin dashboard data on mount
    useEffect(() => {
        const loadDashboard = async () => {
            const result = await fetchAdminDashboardData();
            if (result.ok) {
                setAdminName(result.data.admin_name);
                setStaffList(result.data.staff_list);
                setStudentList(result.data.student_list);
            } else {
                navigate("/admin/login");
            }
        };
        loadDashboard();
    }, [navigate]);

    const handleLogout = async () => {
        await logoutAdmin();
        navigate("/admin/login");
    };

    const handleStaffClick = async (staffId) => {
        const result = await getStudentsByStaff(staffId);
        if (result.ok) {
            setStudentList(result.data);
            document
                .getElementById("student-details-section")
                .scrollIntoView({ behavior: "smooth" });
        } else {
            setStudentList([]);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100">
            <header className="bg-purple-700 text-white flex justify-between items-center p-4">
                <h2 className="text-lg font-semibold">Welcome, {adminName}</h2>
                <button
                    onClick={handleLogout}
                    className="bg-white text-purple-700 px-4 py-2 rounded font-bold hover:bg-purple-50"
                >
                    Logout
                </button>
            </header>

            <div className="p-5">
                <h3 className="text-purple-700 text-lg font-semibold mb-3">Staff Details</h3>
                <div className="overflow-x-auto">
                    <table className="min-w-full bg-white border border-gray-300 mb-6">
                        <thead>
                            <tr className="bg-purple-50">
                                <th className="border px-3 py-2">Name</th>
                                <th className="border px-3 py-2">Department</th>
                                <th className="border px-3 py-2">Experience</th>
                                <th className="border px-3 py-2">Mobile</th>
                                <th className="border px-3 py-2">Email</th>
                                <th className="border px-3 py-2">Username</th>
                            </tr>
                        </thead>
                        <tbody>
                            {staffList.map((staff) => (
                                <tr key={staff[0]} className="hover:bg-purple-50">
                                    <td className="border px-3 py-2">
                                        <button
                                            onClick={() => handleStaffClick(staff[0])}
                                            className="text-purple-700 font-semibold hover:underline"
                                        >
                                            {staff[1]}
                                        </button>
                                    </td>
                                    <td className="border px-3 py-2">{staff[3]}</td>
                                    <td className="border px-3 py-2">{staff[4]}</td>
                                    <td className="border px-3 py-2">{staff[5]}</td>
                                    <td className="border px-3 py-2">{staff[6]}</td>
                                    <td className="border px-3 py-2">{staff[7]}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div id="student-details-section">
                    <h3 className="text-purple-700 text-lg font-semibold mb-3">Student Details</h3>
                    {studentList.length === 0 ? (
                        <p className="text-gray-600">No students to display.</p>
                    ) : (
                        <div className="flex flex-wrap gap-4">
                            {studentList.map((student) => (
                                <div
                                    key={student[0]}
                                    className="bg-white border border-gray-300 rounded-lg shadow p-4 w-full sm:w-[48%] md:w-[30%]"
                                >
                                    <h4 className="text-purple-700 font-semibold text-lg mb-2">
                                        {student[1]}
                                    </h4>
                                    <p className="text-sm">
                                        <strong>Department:</strong> {student[3]}
                                    </p>
                                    <p className="text-sm">
                                        <strong>Hallticket:</strong> {student[4]}
                                    </p>
                                    <p className="text-sm">
                                        <strong>Mobile:</strong> {student[5]}
                                    </p>
                                    <p className="text-sm">
                                        <strong>Email:</strong> {student[6]}
                                    </p>
                                    <p className="text-sm">
                                        <strong>Username:</strong> {student[7]}
                                    </p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default AdminDashboard;
