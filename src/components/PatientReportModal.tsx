import React, { useState } from 'react';
import { X, FileText, Printer, Download, User, Activity, Calendar } from 'lucide-react';
import { PatientListItem, PatientReportResponse } from '../types/api.types';
import practitionerService from '../services/practitioner.service';
import { useAuth } from '../hooks/useAuth';

interface PatientReportModalProps {
    isOpen: boolean;
    onClose: () => void;
    patients: PatientListItem[];
    initialPatientId?: number | null;
}

const PatientReportModal: React.FC<PatientReportModalProps> = ({ isOpen, onClose, patients, initialPatientId }) => {
    const [selectedPatientId, setSelectedPatientId] = useState<number | ''>('');

    React.useEffect(() => {
        if (isOpen && initialPatientId) {
            setSelectedPatientId(initialPatientId);
        } else if (!isOpen) {
            // Reset when closed if desired, or keep last state. 
            // Better to reset if we want fresh state next time, but typically handled by parent passing new initialId.
            // If passing null, we might want to reset? 
            // Let's just set it if initialPatientId is provided.
        }
    }, [isOpen, initialPatientId]);
    const [isLoading, setIsLoading] = useState(false);
    const [reportData, setReportData] = useState<PatientReportResponse | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleGenerate = async () => {
        if (!selectedPatientId) return;

        setIsLoading(true);
        setError(null);
        try {
            const data = await practitionerService.getPatientReport(Number(selectedPatientId));
            setReportData(data);
        } catch (err: any) {
            console.error("Failed to generate report:", err);
            setError(err.response?.data?.detail || "Failed to generate report. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    const handlePrint = () => {
        window.print();
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-xl w-full max-w-4xl max-h-[90vh] flex flex-col overflow-hidden">
                {/* Header */}
                <div className="flex justify-between items-center p-6 border-b border-gray-100 dark:border-gray-700">
                    <div>
                        <h2 className="text-xl font-bold text-gray-900 dark:text-white">Patient Progress Report</h2>
                        <p className="text-sm text-gray-500 dark:text-gray-400">Generate and print detailed patient reports</p>
                    </div>
                    <button onClick={onClose} className="text-gray-400 hover:text-gray-600 transition-colors">
                        <X className="h-6 w-6" />
                    </button>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto p-6 bg-gray-50 dark:bg-gray-900/50">
                    {/* Controls */}
                    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-100 dark:border-gray-700 mb-6 flex flex-col md:flex-row gap-4 items-end no-print">
                        <div className="flex-1 w-full">
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Select Patient</label>
                            <select
                                className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                                value={selectedPatientId}
                                onChange={(e) => setSelectedPatientId(Number(e.target.value))}
                            >
                                <option value="">-- Choose a patient --</option>
                                {patients.map(p => (
                                    <option key={p.id} value={p.id}>{p.name} (Age: {p.age || 'N/A'})</option>
                                ))}
                            </select>
                        </div>
                        <button
                            onClick={handleGenerate}
                            disabled={!selectedPatientId || isLoading}
                            className="w-full md:w-auto px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                        >
                            {isLoading ? 'Generating...' : <><FileText className="h-4 w-4" /> Generate Report</>}
                        </button>
                    </div>

                    {error && (
                        <div className="bg-red-50 text-red-600 p-4 rounded-lg mb-6 border border-red-100">
                            {error}
                        </div>
                    )}

                    {/* Report Preview */}
                    {reportData && (
                        <div className="bg-white dark:bg-gray-800 p-8 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 print-content" id="printable-report">
                            {/* Report Header */}
                            <div className="border-b border-gray-200 dark:border-gray-700 pb-6 mb-6 flex justify-between items-start">
                                <div>
                                    <h1 className="text-2xl font-bold text-primary-800 dark:text-primary-400">AyurSutra Wellness Report</h1>
                                    <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">Generated on {new Date(reportData.generated_at).toLocaleDateString()}</p>
                                </div>
                                <div className="text-right">
                                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{reportData.patient_name}</h3>
                                    <div className="text-sm text-gray-600 dark:text-gray-300 space-y-1">
                                        <p>Age: {reportData.patient_age || 'N/A'} • Gender: {reportData.patient_gender || 'N/A'}</p>
                                        <p>Prakriti: <span className="font-medium text-primary-600 dark:text-primary-400">{reportData.prakriti_type}</span></p>
                                    </div>
                                </div>
                            </div>

                            {/* Health Snapshot */}
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                                <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg text-center">
                                    <p className="text-sm text-blue-600 dark:text-blue-400 mb-1">Avg Sleep</p>
                                    <p className="text-xl font-bold text-blue-900 dark:text-blue-300">{reportData.health_stats.average_sleep ?? '-'} hrs</p>
                                </div>
                                <div className="bg-teal-50 dark:bg-teal-900/20 p-4 rounded-lg text-center">
                                    <p className="text-sm text-teal-600 dark:text-teal-400 mb-1">Avg Hydration</p>
                                    <p className="text-xl font-bold text-teal-900 dark:text-teal-300">{reportData.health_stats.average_hydration ?? '-'} L</p>
                                </div>
                                <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg text-center">
                                    <p className="text-sm text-purple-600 dark:text-purple-400 mb-1">Dominant Dosha</p>
                                    <p className="text-xl font-bold text-purple-900 dark:text-purple-300">{reportData.health_stats.dominant_dosha}</p>
                                </div>
                                <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg text-center">
                                    <p className="text-sm text-green-600 dark:text-green-400 mb-1">Stress Trend</p>
                                    <p className="text-xl font-bold text-green-900 dark:text-green-300">{reportData.health_stats.stress_trend}</p>
                                </div>
                            </div>

                            {/* Recent Appointments */}
                            <div className="mb-8">
                                <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 flex items-center gap-2">
                                    <Calendar className="h-5 w-5 text-gray-500" /> Recent Appointments
                                </h3>
                                {reportData.recent_appointments.length > 0 ? (
                                    <div className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
                                        <table className="w-full text-sm text-left">
                                            <thead className="bg-gray-50 dark:bg-gray-900/50 text-gray-600 dark:text-gray-400 font-medium">
                                                <tr>
                                                    <th className="p-3">Date</th>
                                                    <th className="p-3">Therapy</th>
                                                    <th className="p-3">Status</th>
                                                    <th className="p-3">Notes</th>
                                                </tr>
                                            </thead>
                                            <tbody className="divide-y divide-gray-100 dark:divide-gray-700 text-gray-900 dark:text-gray-200">
                                                {reportData.recent_appointments.map(appt => (
                                                    <tr key={appt.id}>
                                                        <td className="p-3">{new Date(appt.scheduled_datetime).toLocaleDateString()}</td>
                                                        <td className="p-3 font-medium text-gray-900 dark:text-white">{appt.therapy_type}</td>
                                                        <td className="p-3 capitalize">{appt.status.replace('_', ' ')}</td>
                                                        <td className="p-3 text-gray-500 dark:text-gray-400 italic">{appt.notes || '-'}</td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                ) : (
                                    <p className="text-gray-500 italic text-sm">No recent appointments found.</p>
                                )}
                            </div>

                            {/* Doctor's Notes */}
                            <div className="bg-yellow-50 dark:bg-yellow-900/20 p-6 rounded-lg border border-yellow-100 dark:border-yellow-900/30">
                                <h3 className="text-lg font-semibold text-yellow-800 dark:text-yellow-400 mb-2">Doctor's Notes & Observations</h3>
                                <p className="text-yellow-900 dark:text-yellow-300 whitespace-pre-wrap">{reportData.doctor_notes || "No notes available for this period."}</p>
                            </div>
                        </div>
                    )}
                </div>

                {/* Footer Actions */}
                <div className="p-6 border-t border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-800 flex justify-end gap-3">
                    <button onClick={onClose} className="px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
                        Close
                    </button>
                    {reportData && (
                        <button
                            onClick={handlePrint}
                            className="px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 flex items-center gap-2"
                        >
                            <Printer className="h-4 w-4" /> Print Report
                        </button>
                    )}
                </div>
            </div>

            {/* Print Styles */}
            <style>{`
                @media print {
                    body * {
                        visibility: hidden;
                    }
                    .print-content, .print-content * {
                        visibility: visible;
                    }
                    .print-content {
                        position: absolute;
                        left: 0;
                        top: 0;
                        width: 100%;
                    }
                    .no-print {
                        display: none !important;
                    }
                }
            `}</style>
        </div>
    );
};

export default PatientReportModal;
