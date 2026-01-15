import React, { useState, useEffect } from 'react';
import { X, Printer, TrendingUp, Calendar, Users, Star } from 'lucide-react';
import { TreatmentAnalyticsResponse, MonthlySummaryResponse, FeedbackReportResponse } from '../types/api.types';
import practitionerService from '../services/practitioner.service';

// Reusable Modal Wrapper
const ReportModalWrapper = ({ isOpen, onClose, title, children, icon: Icon, onPrint }: any) => {
    if (!isOpen) return null;
    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-xl shadow-xl w-full max-w-4xl max-h-[90vh] flex flex-col overflow-hidden">
                <div className="flex justify-between items-center p-6 border-b border-gray-100">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-primary-50 rounded-lg">
                            <Icon className="h-6 w-6 text-primary-600" />
                        </div>
                        <div>
                            <h2 className="text-xl font-bold text-gray-900">{title}</h2>
                            <p className="text-sm text-gray-500">System generated report</p>
                        </div>
                    </div>
                    <button onClick={onClose} className="text-gray-400 hover:text-gray-600 transition-colors">
                        <X className="h-6 w-6" />
                    </button>
                </div>
                <div className="flex-1 overflow-y-auto p-6 bg-gray-50">
                    {children}
                </div>
                <div className="p-6 border-t border-gray-100 bg-white flex justify-end gap-3">
                    <button onClick={onClose} className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                        Close
                    </button>
                    {onPrint && (
                        <button onClick={onPrint} className="px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 flex items-center gap-2">
                            <Printer className="h-4 w-4" /> Print Report
                        </button>
                    )}
                </div>
            </div>
            <style>{`
                @media print {
                    body * { visibility: hidden; }
                    .print-content, .print-content * { visibility: visible; }
                    .print-content { position: absolute; left: 0; top: 0; width: 100%; }
                }
            `}</style>
        </div>
    );
};

export const TreatmentAnalyticsModal = ({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) => {
    const [data, setData] = useState<TreatmentAnalyticsResponse | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (isOpen) {
            setLoading(true);
            practitionerService.getTreatmentAnalytics().then(setData).finally(() => setLoading(false));
        }
    }, [isOpen]);

    return (
        <ReportModalWrapper isOpen={isOpen} onClose={onClose} title="Treatment Analytics" icon={TrendingUp} onPrint={() => window.print()}>
            {loading ? <div className="text-center py-8">Loading analytics...</div> : data && (
                <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 print-content">
                    <div className="mb-8 text-center border-b pb-6">
                        <h1 className="text-2xl font-bold text-primary-800">Treatment Performance Report</h1>
                        <p className="text-gray-500">Generated on {new Date().toLocaleDateString()}</p>
                    </div>

                    <div className="grid grid-cols-2 gap-4 mb-8">
                        <div className="p-4 bg-green-50 rounded-lg">
                            <p className="text-sm text-green-700">Success Rate</p>
                            <p className="text-3xl font-bold text-green-900">{data.success_rate_overall}%</p>
                        </div>
                        <div className="p-4 bg-blue-50 rounded-lg">
                            <p className="text-sm text-blue-700">Total Treatments</p>
                            <p className="text-3xl font-bold text-blue-900">{data.total_treatments}</p>
                        </div>
                    </div>

                    <h3 className="font-semibold text-gray-900 mb-4">Treatment Breakdown</h3>
                    <table className="w-full text-sm text-left mb-8">
                        <thead className="bg-gray-50">
                            <tr><th className="p-3">Type</th><th className="p-3">Count</th><th className="p-3">Success %</th></tr>
                        </thead>
                        <tbody>
                            {data.type_distribution.map((t, i) => (
                                <tr key={i} className="border-b">
                                    <td className="p-3 font-medium">{t.type}</td>
                                    <td className="p-3">{t.count}</td>
                                    <td className="p-3">{t.success_rate}%</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </ReportModalWrapper>
    );
};

export const MonthlySummaryModal = ({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) => {
    const [data, setData] = useState<MonthlySummaryResponse | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (isOpen) {
            setLoading(true);
            practitionerService.getMonthlySummary().then(setData).finally(() => setLoading(false));
        }
    }, [isOpen]);

    return (
        <ReportModalWrapper isOpen={isOpen} onClose={onClose} title="Monthly Summary" icon={Calendar} onPrint={() => window.print()}>
            {loading ? <div className="text-center py-8">Loading summary...</div> : data && (
                <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 print-content">
                    <div className="mb-8 text-center border-b pb-6">
                        <h1 className="text-2xl font-bold text-primary-800">{data.month} Activity Report</h1>
                        <p className="text-gray-500">{new Date().getFullYear()}</p>
                    </div>

                    <div className="grid grid-cols-3 gap-4 mb-8">
                        <div className="text-center p-4 border rounded-lg">
                            <p className="text-gray-500 text-sm">Revenue</p>
                            <p className="text-2xl font-bold text-gray-900">${data.total_revenue}</p>
                        </div>
                        <div className="text-center p-4 border rounded-lg">
                            <p className="text-gray-500 text-sm">Appointments</p>
                            <p className="text-2xl font-bold text-gray-900">{data.total_appointments}</p>
                        </div>
                        <div className="text-center p-4 border rounded-lg">
                            <p className="text-gray-500 text-sm">New Patients</p>
                            <p className="text-2xl font-bold text-gray-900">{data.new_patients}</p>
                        </div>
                    </div>

                    <div className="mb-6">
                        <h3 className="font-semibold text-gray-900 mb-2">Popular Therapies</h3>
                        <div className="flex gap-2">
                            {data.popular_therapies.map(t => (
                                <span key={t} className="px-3 py-1 bg-primary-100 text-primary-800 rounded-full text-sm">{t}</span>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </ReportModalWrapper>
    );
};

export const FeedbackReportModal = ({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) => {
    const [data, setData] = useState<FeedbackReportResponse | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (isOpen) {
            setLoading(true);
            practitionerService.getFeedbackReport().then(setData).finally(() => setLoading(false));
        }
    }, [isOpen]);

    return (
        <ReportModalWrapper isOpen={isOpen} onClose={onClose} title="Patient Feedback" icon={Users} onPrint={() => window.print()}>
            {loading ? <div className="text-center py-8">Loading feedback...</div> : data && (
                <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 print-content">
                    <div className="mb-8 text-center border-b pb-6">
                        <h1 className="text-2xl font-bold text-primary-800">Patient Feedback Summary</h1>
                    </div>

                    <div className="flex items-center justify-center mb-8 gap-4">
                        <div className="text-center">
                            <p className="text-5xl font-bold text-yellow-500 flex items-center justify-center gap-2">
                                {data.summary.average_rating} <Star className="h-8 w-8 fill-current" />
                            </p>
                            <p className="text-gray-500 mt-2">Based on {data.summary.total_reviews} reviews</p>
                        </div>
                    </div>

                    <h3 className="font-semibold text-gray-900 mb-4">Recent Comments</h3>
                    <div className="space-y-4">
                        {data.summary.recent_feedback.map(f => (
                            <div key={f.id} className="p-4 bg-gray-50 rounded-lg">
                                <div className="flex justify-between mb-2">
                                    <div className="flex text-yellow-400">
                                        {[...Array(5)].map((_, i) => (
                                            <Star key={i} className={`h-4 w-4 ${i < f.rating ? 'fill-current' : 'text-gray-300'}`} />
                                        ))}
                                    </div>
                                    <span className="text-xs text-gray-500">{new Date(f.created_at).toLocaleDateString()}</span>
                                </div>
                                <p className="text-gray-700 italic">"{f.comments || 'No comment provided'}"</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </ReportModalWrapper>
    );
};
