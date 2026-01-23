import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Activity,
    Calendar,
    TrendingUp,
    FileText,
    MessageCircle,
    Settings,
    Menu,
    X,
    Bell,
    AlertCircle,
    Info,
    CheckCircle,
    Trash2,
    MapPin
} from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import Sidebar, { SidebarItem } from '../components/Sidebar';

interface Notification {
    id: string;
    type: 'reminder' | 'alert' | 'info' | 'appointment';
    title: string;
    message: string;
    time: string;
    read: boolean;
}

const NotificationsPage = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [notifications, setNotifications] = useState<Notification[]>([
        { id: 'N001', type: 'reminder', title: 'Welcome to AyurSutra', message: 'We are glad to have you on your wellness journey.', time: '1 hour ago', read: false },
        { id: 'N002', type: 'appointment', title: 'Session Confirmed', message: 'Your Shirodhara session with Dr. Sharma is confirmed.', time: '2 hours ago', read: false },
        { id: 'N003', type: 'reminder', title: 'Drink Water', message: 'Time to hydrate! Drink a glass of warm water.', time: '3 hours ago', read: true },
        { id: 'N004', type: 'info', title: 'Health Tip', message: 'Morning meditation can help balance your Vata dosha.', time: '5 hours ago', read: true },
        { id: 'N005', type: 'alert', title: 'Appointment Reminder', message: 'Your appointment is tomorrow at 10:00 AM.', time: '1 day ago', read: false },
    ]);
    const [filter, setFilter] = useState<'all' | 'unread'>('all');

    const handleLogout = () => {
        logout();
        navigate('/auth');
    };

    const handleMarkAsRead = (id: string) => {
        setNotifications(prev => prev.map(n => n.id === id ? { ...n, read: true } : n));
    };

    const handleMarkAllAsRead = () => {
        setNotifications(prev => prev.map(n => ({ ...n, read: true })));
    };

    const handleDelete = (id: string) => {
        setNotifications(prev => prev.filter(n => n.id !== id));
    };

    const handleClearAll = () => {
        setNotifications([]);
    };

    const getIcon = (type: string) => {
        switch (type) {
            case 'reminder':
                return <Bell className="h-6 w-6 text-blue-500" />;
            case 'alert':
                return <AlertCircle className="h-6 w-6 text-red-500" />;
            case 'appointment':
                return <Calendar className="h-6 w-6 text-green-500" />;
            default:
                return <Info className="h-6 w-6 text-gray-500" />;
        }
    };

    const filteredNotifications = filter === 'all'
        ? notifications
        : notifications.filter(n => !n.read);

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
                    <div className="relative flex-1 flex flex-col max-w-xs w-full bg-white">
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
                        <div>
                            <h1 className="text-2xl font-semibold text-gray-900 dark:text-white">All Activity</h1>
                            <p className="text-sm text-gray-600 dark:text-gray-400">View and manage your notifications</p>
                        </div>
                    </div>
                </div>

                {/* Notifications content */}
                <main className="flex-1 overflow-y-auto p-6">
                    <div className="max-w-4xl mx-auto">
                        {/* Header with filters and actions */}
                        <div className="card mb-6">
                            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                                <div className="flex items-center gap-4">
                                    <button
                                        onClick={() => setFilter('all')}
                                        className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === 'all'
                                                ? 'bg-primary-600 text-white'
                                                : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
                                            }`}
                                    >
                                        All ({notifications.length})
                                    </button>
                                    <button
                                        onClick={() => setFilter('unread')}
                                        className={`px-4 py-2 rounded-lg font-medium transition-colors ${filter === 'unread'
                                                ? 'bg-primary-600 text-white'
                                                : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
                                            }`}
                                    >
                                        Unread ({notifications.filter(n => !n.read).length})
                                    </button>
                                </div>
                                <div className="flex items-center gap-2">
                                    <button
                                        onClick={handleMarkAllAsRead}
                                        className="px-4 py-2 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-lg font-medium hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                                    >
                                        Mark All Read
                                    </button>
                                    <button
                                        onClick={handleClearAll}
                                        className="px-4 py-2 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 rounded-lg font-medium hover:bg-red-200 dark:hover:bg-red-900/50 transition-colors"
                                    >
                                        Clear All
                                    </button>
                                </div>
                            </div>
                        </div>

                        {/* Notifications list */}
                        {filteredNotifications.length === 0 ? (
                            <div className="card text-center py-12">
                                <Bell className="h-16 w-16 mx-auto mb-4 text-gray-400 dark:text-gray-600" />
                                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                                    No notifications
                                </h3>
                                <p className="text-gray-600 dark:text-gray-400">
                                    {filter === 'unread' ? 'You have no unread notifications' : 'You have no notifications'}
                                </p>
                            </div>
                        ) : (
                            <div className="space-y-4">
                                {filteredNotifications.map((notification) => (
                                    <div
                                        key={notification.id}
                                        className={`card hover:shadow-lg transition-shadow ${!notification.read ? 'border-l-4 border-primary-500' : ''
                                            }`}
                                    >
                                        <div className="flex gap-4">
                                            {!notification.read && (
                                                <div className="flex-shrink-0 w-2 h-2 bg-primary-600 rounded-full mt-2" />
                                            )}

                                            <div className="flex-shrink-0 mt-1">
                                                {getIcon(notification.type)}
                                            </div>

                                            <div className="flex-1 min-w-0">
                                                <div className="flex items-start justify-between gap-4">
                                                    <div className="flex-1">
                                                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                                                            {notification.title}
                                                        </h3>
                                                        <p className="text-gray-600 dark:text-gray-300 mt-1">
                                                            {notification.message}
                                                        </p>
                                                        <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                                                            {notification.time}
                                                        </p>
                                                    </div>

                                                    <div className="flex items-center gap-2">
                                                        {!notification.read && (
                                                            <button
                                                                onClick={() => handleMarkAsRead(notification.id)}
                                                                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                                                                title="Mark as read"
                                                            >
                                                                <CheckCircle className="h-5 w-5 text-green-600 dark:text-green-400" />
                                                            </button>
                                                        )}
                                                        <button
                                                            onClick={() => handleDelete(notification.id)}
                                                            className="p-2 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors"
                                                            title="Delete notification"
                                                        >
                                                            <Trash2 className="h-5 w-5 text-red-600 dark:text-red-400" />
                                                        </button>
                                                    </div>
                                                </div>
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

export default NotificationsPage;
