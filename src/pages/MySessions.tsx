import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Calendar,
    Clock,
    Video,
    Activity,
    TrendingUp,
    Settings,
    MessageCircle,
    FileText,
    Menu,
    X,
    MapPin,
    CheckCircle,
    XCircle
} from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import appointmentService from '../services/appointment.service';
import { AppointmentResponse } from '../types/api.types';
import Sidebar, { SidebarItem } from '../components/Sidebar';

const MySessions = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [activeTab, setActiveTab] = useState<'upcoming' | 'past'>('upcoming');
    const [appointments, setAppointments] = useState<AppointmentResponse[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadAppointments();
    }, [activeTab]);

    const loadAppointments = async () => {
        setLoading(true);
        try {
            // For real implementation, we would filter by status or date in the backend
            // Currently getMyAppointments accepts a status, but we might want all to filter client side
            // or make two calls. For now, let's fetch 'scheduled' for upcoming and others for past if possible.
            // Since the API is simple, let's just fetch 'scheduled' for UPCOMING and assuming 'completed' for PAST.

            const status = activeTab === 'upcoming' ? 'scheduled' : 'completed';
            const data = await appointmentService.getMyAppointments(status);
            setAppointments(data);
        } catch (error) {
            console.error("Failed to load appointments", error);
        } finally {
            setLoading(false);
        }
    };

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
                        <h1 className="text-xl font-semibold text-gray-900 dark:text-white">My Sessions</h1>
                    </div>
                </div>

                {/* Page Content */}
                <main className="flex-1 overflow-y-auto p-6">
                    <div className="max-w-4xl mx-auto">

                        {/* Tabs */}
                        <div className="flex space-x-1 bg-white dark:bg-gray-800 p-1 rounded-xl shadow-sm mb-6 w-fit">
                            <button
                                onClick={() => setActiveTab('upcoming')}
                                className={`px-6 py-2.5 text-sm font-medium rounded-lg transition-all ${activeTab === 'upcoming'
                                    ? 'bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300 shadow-sm'
                                    : 'text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700'
                                    }`}
                            >
                                Upcoming
                            </button>
                            <button
                                onClick={() => setActiveTab('past')}
                                className={`px-6 py-2.5 text-sm font-medium rounded-lg transition-all ${activeTab === 'past'
                                    ? 'bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300 shadow-sm'
                                    : 'text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700'
                                    }`}
                            >
                                Past History
                            </button>
                        </div>

                        {/* List */}
                        {loading ? (
                            <div className="flex justify-center py-12">
                                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
                            </div>
                        ) : appointments.length === 0 ? (
                            <div className="text-center py-12 card border-dashed border-gray-300 dark:border-gray-700">
                                <Calendar className="mx-auto h-12 w-12 text-gray-400 dark:text-gray-600" />
                                <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">No sessions found</h3>
                                <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                                    You don't have any {activeTab} appointments.
                                </p>
                                {activeTab === 'upcoming' && (
                                    <div className="mt-6">
                                        <button
                                            onClick={() => navigate('/patient')}
                                            className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                                        >
                                            Book a Session
                                        </button>
                                    </div>
                                )}
                            </div>
                        ) : (
                            <div className="space-y-4">
                                {appointments.map((session) => (
                                    <div key={session.id} className="card hover:shadow-md transition-shadow p-6">
                                        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">

                                            {/* Info */}
                                            <div className="flex items-start space-x-4">
                                                <div className={`p-3 rounded-xl ${session.status === 'confirmed' || session.status === 'scheduled' ? 'bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400' :
                                                    session.status === 'completed' ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400' :
                                                        'bg-gray-50 dark:bg-gray-800 text-gray-500 dark:text-gray-400'
                                                    }`}>
                                                    <Video className="h-6 w-6" />
                                                </div>
                                                <div>
                                                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{session.therapy_type}</h3>
                                                    <div className="flex flex-wrap items-center gap-4 mt-1 text-sm text-gray-500 dark:text-gray-400">
                                                        <div className="flex items-center">
                                                            <UserIcon className="h-4 w-4 mr-1.5" />
                                                            <span>Dr. {session.practitioner_id}</span>
                                                        </div>
                                                        <div className="flex items-center">
                                                            <Calendar className="h-4 w-4 mr-1.5" />
                                                            <span>{new Date(session.scheduled_datetime).toLocaleDateString()}</span>
                                                        </div>
                                                        <div className="flex items-center">
                                                            <Clock className="h-4 w-4 mr-1.5" />
                                                            <span>{new Date(session.scheduled_datetime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>

                                            {/* Action */}
                                            <div className="flex items-center gap-3">
                                                <span className={`px-3 py-1 rounded-full text-xs font-medium uppercase tracking-wide ${session.status === 'confirmed' || session.status === 'scheduled' ? 'bg-green-100 dark:bg-green-900/40 text-green-800 dark:text-green-400' :
                                                    session.status === 'completed' ? 'bg-blue-100 dark:bg-blue-900/40 text-blue-800 dark:text-blue-400' :
                                                        'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300'
                                                    }`}>
                                                    {session.status}
                                                </span>

                                                {activeTab === 'upcoming' && (
                                                    <button className="flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm font-medium shadow-sm hover:shadow-md">
                                                        <Video className="h-4 w-4 mr-2" />
                                                        Join
                                                    </button>
                                                )}
                                                {activeTab === 'past' && (
                                                    <button className="flex items-center px-4 py-2 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors text-sm font-medium">
                                                        <FileText className="h-4 w-4 mr-2" />
                                                        View Notes
                                                    </button>
                                                )}
                                            </div>

                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}

                    </div>
                </main>
            </div>
        </div>
    );
};

// Helper for icon
function UserIcon(props: any) {
    return (
        <svg
            {...props}
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
        </svg>
    )
}

export default MySessions;
