import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Activity,
    Calendar,
    TrendingUp,
    FileText,
    MapPin,
    MessageCircle,
    Settings,
    Menu,
    X,
    Droplets,
    Zap,
    Moon,
    Wind,
    Flame,
    MousePointer2
} from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import Sidebar, { SidebarItem } from '../components/Sidebar';
import { healthService } from '../services/health.service';
import { HealthLog } from '../types/api.types';

const Progress = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [activeTab, setActiveTab] = useState<'overview' | 'log'>('overview');
    const [loading, setLoading] = useState(true);
    const [healthLog, setHealthLog] = useState<HealthLog | null>(null);

    useEffect(() => {
        const fetchHealthData = async () => {
            try {
                // Only fetch if user is a patient, or handle error gracefully
                const logs = await healthService.getMyLogs();
                if (logs && logs.length > 0) {
                    setHealthLog(logs[0]); // Use the latest log
                }
            } catch (error) {
                console.error("Failed to fetch health logs", error);
                // Optional: Show toast or ignore
            } finally {
                setLoading(false);
            }
        };
        fetchHealthData();
    }, []);

    const handleLogout = () => {
        logout();
        navigate('/auth');
    };

    const sidebarItems: SidebarItem[] = [
        { icon: Activity, label: 'Dashboard', path: '/patient' },
        { icon: Calendar, label: 'My Sessions', path: '/my-sessions' },
        { icon: TrendingUp, label: 'Progress', path: '/progress' },
        { icon: FileText, label: 'Health Records', path: '/health-support' },
        { icon: MapPin, label: 'Find Clinics', path: '/map' },
        { icon: MessageCircle, label: 'Chat Support', path: '/chat-support' },
        { icon: Settings, label: 'Settings', path: '/settings' }
    ];

    // Derived Data
    const metrics = [
        {
            label: 'Sleep Score',
            value: healthLog?.sleep_score?.toString() || '0',
            unit: '/100',
            icon: Moon,
            change: healthLog ? 'Latest' : '',
            color: 'text-indigo-600',
            bg: 'bg-indigo-100'
        },
        {
            label: 'Stress Level',
            value: healthLog?.stress_level || '--',
            unit: '',
            icon: Zap,
            change: healthLog ? 'Latest' : '',
            color: 'text-amber-600',
            bg: 'bg-amber-100'
        },
        {
            label: 'Hydration',
            value: healthLog?.hydration?.toString() || '0',
            unit: 'L',
            icon: Droplets,
            change: 'Target 2.5L',
            color: 'text-blue-600',
            bg: 'bg-blue-100'
        },
    ];

    const doshaData = [
        { type: 'Vata', value: healthLog?.dosha_vata || 0, color: 'bg-blue-400' },
        { type: 'Pitta', value: healthLog?.dosha_pitta || 0, color: 'bg-red-400' },
        { type: 'Kapha', value: healthLog?.dosha_kapha || 0, color: 'bg-green-400' },
    ];

    if (loading) {
        return <div className="min-h-screen flex items-center justify-center bg-dashboard text-gray-900 dark:text-gray-100">Loading health data...</div>;
    }

    return (
        <div className="bg-dashboard flex text-gray-900 dark:text-gray-100">
            {/* Mobile sidebar overlay */}
            {isSidebarOpen && (
                <div className="fixed inset-0 z-50 lg:hidden">
                    <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setIsSidebarOpen(false)}></div>
                    <div className="relative flex-1 flex flex-col max-w-xs w-full bg-white dark:bg-gray-900">
                        <div className="absolute top-0 right-0 -mr-12 pt-2">
                            <button
                                className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
                                onClick={() => setIsSidebarOpen(false)}
                            >
                                <X className="h-6 w-6 text-white" />
                            </button>
                        </div>
                        <Sidebar items={sidebarItems} user={user} onLogout={handleLogout} />
                    </div>
                </div>
            )}

            {/* Desktop sidebar */}
            <div className="hidden lg:flex lg:flex-col lg:flex-shrink-0 w-64">
                <Sidebar items={sidebarItems} user={user} onLogout={handleLogout} />
            </div>

            {/* Main content */}
            <div className="flex flex-col flex-1">
                {/* Top navigation */}
                <div className="relative z-10 flex-shrink-0 flex h-16 header-bg shadow-sm">
                    <button
                        className="px-4 border-r border-gray-200 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500 lg:hidden"
                        onClick={() => setIsSidebarOpen(true)}
                    >
                        <Menu className="h-6 w-6" />
                    </button>
                    <div className="flex-1 px-4 flex justify-between items-center">
                        <h1 className="text-xl font-semibold text-gray-900 dark:text-white">Your Wellness Progress</h1>
                    </div>
                </div>

                {/* Page Content */}
                <main className="flex-1 overflow-y-auto p-6">
                    <div className="max-w-5xl mx-auto">

                        {/* Health Overview Cards */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                            {metrics.map((metric, idx) => (
                                <div key={idx} className="card flex items-center p-6">
                                    <div className={`p-4 rounded-xl ${metric.bg} dark:bg-opacity-20 ${metric.color} dark:text-opacity-90 mr-5`}>
                                        <metric.icon className="h-8 w-8" />
                                    </div>
                                    <div>
                                        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">{metric.label}</p>
                                        <div className="flex items-baseline mt-1">
                                            <span className="text-2xl font-bold text-gray-900 dark:text-white">{metric.value}</span>
                                            <span className="ml-1 text-sm text-gray-500 dark:text-gray-400">{metric.unit}</span>
                                        </div>
                                        <span className={`text-xs font-medium ${metric.change.includes('+') ? 'text-green-600 dark:text-green-400' : 'text-gray-500 dark:text-gray-400'}`}>
                                            {metric.change}
                                        </span>
                                    </div>
                                </div>
                            ))}
                        </div>

                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

                            {/* Dosha Balance Visualization */}
                            <div className="card">
                                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Current Dosha Balance</h3>
                                <div className="space-y-6">
                                    {doshaData.map((d) => (
                                        <div key={d.type}>
                                            <div className="flex justify-between mb-2">
                                                <div className="flex items-center">
                                                    {d.type === 'Vata' && <Wind className="h-4 w-4 text-blue-500 mr-2" />}
                                                    {d.type === 'Pitta' && <Flame className="h-4 w-4 text-red-500 mr-2" />}
                                                    {d.type === 'Kapha' && <Droplets className="h-4 w-4 text-green-500 mr-2" />}
                                                    <span className="font-medium text-gray-700 dark:text-gray-300">{d.type}</span>
                                                </div>
                                                <span className="text-sm text-gray-500 dark:text-gray-400">{d.value}%</span>
                                            </div>
                                            <div className="h-3 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                                                <div
                                                    className={`h-full rounded-full transition-all duration-1000 ${d.color}`}
                                                    style={{ width: `${d.value}%` }}
                                                />
                                            </div>
                                        </div>
                                    ))}
                                </div>
                                {healthLog?.recommendations ? (
                                    <div className="mt-8 p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-100 dark:border-gray-700">
                                        <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-1">Practitioner's Recommendation</h4>
                                        <p className="text-sm text-gray-600 dark:text-gray-400">
                                            "{healthLog.recommendations}"
                                        </p>
                                    </div>
                                ) : (
                                    <div className="mt-8 p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-100 dark:border-gray-700 text-center">
                                        <p className="text-sm text-gray-500 dark:text-gray-400">No recommendations available yet.</p>
                                    </div>
                                )}
                            </div>

                            {/* Notes / Log Section (Replace Symptoms with Notes) */}
                            <div className="card">
                                <div className="flex items-center justify-between mb-6">
                                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Clinical Notes</h3>
                                </div>

                                {healthLog?.notes ? (
                                    <div className="prose prose-sm text-gray-600 dark:text-gray-400">
                                        <p>{healthLog.notes}</p>
                                        <p className="text-xs text-gray-400 dark:text-gray-500 mt-4">Last Updated: {new Date(healthLog.created_at).toLocaleDateString()}</p>
                                    </div>
                                ) : (
                                    <div className="flex flex-col items-center justify-center h-48 text-gray-400 dark:text-gray-600">
                                        <FileText className="h-12 w-12 mb-2 opacity-50" />
                                        <p>No clinical notes recorded.</p>
                                    </div>
                                )}
                            </div>
                        </div>

                    </div>
                </main>
            </div>
        </div>
    );
};

export default Progress;
