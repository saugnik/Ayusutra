import React, { useEffect, useState } from 'react';
import { X, Calendar, Activity, FileText, Clock } from 'lucide-react';

interface HistoryModalProps {
    userId: number | null;
    isOpen: boolean;
    onClose: () => void;
}

const HistoryModal: React.FC<HistoryModalProps> = ({ userId, isOpen, onClose }) => {
    const [history, setHistory] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (userId && isOpen) {
            fetchHistory(userId);
        } else {
            setHistory(null);
        }
    }, [userId, isOpen]);

    const fetchHistory = async (id: number) => {
        setLoading(true);
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:8001/admin/users/${id}/history`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            if (response.ok) {
                const data = await response.json();
                setHistory(data);
            }
        } catch (error) {
            console.error("Error fetching history:", error);
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">
                <div className="p-6 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                        User History {history?.user ? `- ${history.user.full_name}` : ''}
                    </h2>
                    <button onClick={onClose} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
                        <X className="h-5 w-5 text-gray-500" />
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto p-6 space-y-8">
                    {loading ? (
                        <div className="flex justify-center p-8">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
                        </div>
                    ) : history ? (
                        <>
                            {/* User Details Card */}
                            <div className="bg-gray-50 dark:bg-gray-900/50 p-4 rounded-lg">
                                <h3 className="text-sm font-semibold text-gray-500 uppercase mb-3">Profile Details</h3>
                                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                    <div>
                                        <label className="text-xs text-gray-500">Email</label>
                                        <p className="text-sm font-medium text-gray-900 dark:text-white">{history.user.email}</p>
                                    </div>
                                    <div>
                                        <label className="text-xs text-gray-500">Phone</label>
                                        <p className="text-sm font-medium text-gray-900 dark:text-white">{history.user.phone || 'N/A'}</p>
                                    </div>
                                    <div>
                                        <label className="text-xs text-gray-500">Role</label>
                                        <p className="text-sm font-medium text-gray-900 dark:text-white capitalize">{history.user.role}</p>
                                    </div>
                                    <div>
                                        <label className="text-xs text-gray-500">Joined</label>
                                        <p className="text-sm font-medium text-gray-900 dark:text-white">{new Date(history.user.created_at).toLocaleDateString()}</p>
                                    </div>
                                </div>
                            </div>

                            {/* Appointments */}
                            <div>
                                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                                    <Calendar className="h-5 w-5 mr-2 text-primary-600" /> Appointment History
                                </h3>
                                {history.appointments && history.appointments.length > 0 ? (
                                    <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
                                        <table className="w-full text-sm">
                                            <thead className="bg-gray-50 dark:bg-gray-900">
                                                <tr>
                                                    <th className="px-4 py-2 text-left">Date</th>
                                                    <th className="px-4 py-2 text-left">Therapy</th>
                                                    <th className="px-4 py-2 text-left">Status</th>
                                                    <th className="px-4 py-2 text-left">Notes</th>
                                                </tr>
                                            </thead>
                                            <tbody className="divide-y divide-gray-100 dark:divide-gray-800">
                                                {history.appointments.map((appt: any) => (
                                                    <tr key={appt.id}>
                                                        <td className="px-4 py-2">{new Date(appt.scheduled_datetime).toLocaleDateString()}</td>
                                                        <td className="px-4 py-2">{appt.therapy_type}</td>
                                                        <td className="px-4 py-2">
                                                            <span className={`px-2 py-1 rounded-xs text-xs ${appt.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                                                                }`}>
                                                                {appt.status}
                                                            </span>
                                                        </td>
                                                        <td className="px-4 py-2 text-gray-500">{appt.notes || '-'}</td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                ) : (
                                    <p className="text-sm text-gray-500 italic">No appointments found.</p>
                                )}
                            </div>

                            {/* Audit Logs */}
                            <div>
                                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                                    <Activity className="h-5 w-5 mr-2 text-orange-600" /> Activity Log
                                </h3>
                                <div className="space-y-3">
                                    {history.audit_logs && history.audit_logs.map((log: any) => (
                                        <div key={log.id} className="flex items-start space-x-3 text-sm border-b border-gray-100 dark:border-gray-800 pb-3 last:border-0">
                                            <Clock className="h-4 w-4 text-gray-400 mt-0.5" />
                                            <div>
                                                <p className="text-gray-900 dark:text-white font-medium">{log.action}</p>
                                                <p className="text-gray-500 text-xs">{new Date(log.created_at).toLocaleString()}</p>
                                                {log.details && (
                                                    <pre className="text-xs text-gray-500 mt-1 bg-gray-50 dark:bg-gray-900 p-1 rounded">
                                                        {JSON.stringify(log.details, null, 2)}
                                                    </pre>
                                                )}
                                            </div>
                                        </div>
                                    ))}
                                    {(!history.audit_logs || history.audit_logs.length === 0) && (
                                        <p className="text-sm text-gray-500 italic">No activity logs found.</p>
                                    )}
                                </div>
                            </div>
                        </>
                    ) : (
                        <div className="text-center text-gray-500">User not found.</div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default HistoryModal;
