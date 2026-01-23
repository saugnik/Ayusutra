import React, { useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Bell, X, Check, AlertCircle, Info, Calendar } from 'lucide-react';

export interface Notification {
    id: string;
    type: 'reminder' | 'alert' | 'info' | 'appointment';
    title: string;
    message: string;
    time: string;
    read: boolean;
}

interface NotificationDropdownProps {
    notifications: Notification[];
    isOpen: boolean;
    onClose: () => void;
    onMarkAsRead: (id: string) => void;
    onClearAll: () => void;
    onViewAll: () => void;
}

const NotificationDropdown: React.FC<NotificationDropdownProps> = ({
    notifications,
    isOpen,
    onClose,
    onMarkAsRead,
    onClearAll,
    onViewAll
}) => {
    const dropdownRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            const target = event.target as HTMLElement;
            // Don't close if clicking the "View All Activity" link
            if (target.closest('a[href="/notifications"]')) {
                return;
            }
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                onClose();
            }
        };

        if (isOpen) {
            document.addEventListener('mousedown', handleClickOutside);
        }

        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [isOpen, onClose]);

    if (!isOpen) return null;

    const getIcon = (type: string) => {
        switch (type) {
            case 'reminder':
                return <Bell className="h-5 w-5 text-blue-500" />;
            case 'alert':
                return <AlertCircle className="h-5 w-5 text-red-500" />;
            case 'appointment':
                return <Calendar className="h-5 w-5 text-green-500" />;
            default:
                return <Info className="h-5 w-5 text-gray-500" />;
        }
    };

    return (
        <div
            ref={dropdownRef}
            className="absolute right-0 top-full mt-2 w-96 max-w-[calc(100vw-2rem)] bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50 overflow-hidden"
        >
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    Notifications
                </h3>
                <div className="flex items-center gap-2">
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            e.preventDefault();
                            onClearAll();
                        }}
                        className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
                    >
                        Clear All
                    </button>
                    <button
                        onClick={onClose}
                        className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                    >
                        <X className="h-5 w-5" />
                    </button>
                </div>
            </div>

            {/* Notifications List */}
            <div className="max-h-96 overflow-y-auto">
                {notifications.length === 0 ? (
                    <div className="p-8 text-center text-gray-500 dark:text-gray-400">
                        <Bell className="h-12 w-12 mx-auto mb-2 opacity-50" />
                        <p>No new notifications</p>
                    </div>
                ) : (
                    <div className="divide-y divide-gray-200 dark:divide-gray-700">
                        {notifications.map((notification) => {
                            // Determine if this is a message notification and extract sender name
                            const isMessageNotification = notification.title.toLowerCase().includes('message') ||
                                notification.type === 'appointment';
                            const senderName = notification.title.includes('from')
                                ? notification.title.split('from')[1]?.trim()
                                : notification.title;

                            return (
                                <div
                                    key={notification.id}
                                    onClick={() => {
                                        onMarkAsRead(notification.id);
                                        // If it's a message notification, redirect to chat
                                        if (isMessageNotification) {
                                            window.location.href = '/chat-support';
                                        }
                                    }}
                                    className={`p-4 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors ${!notification.read ? 'bg-blue-50 dark:bg-blue-900/20' : ''
                                        }`}
                                >
                                    <div className="flex gap-3">
                                        {!notification.read && (
                                            <div className="flex-shrink-0 w-2 h-2 bg-blue-600 rounded-full mt-2" />
                                        )}

                                        <div className="flex-shrink-0 mt-1">
                                            {getIcon(notification.type)}
                                        </div>

                                        <div className="flex-1 min-w-0">
                                            <p className="text-sm font-medium text-gray-900 dark:text-white">
                                                {notification.title}
                                            </p>
                                            {/* Only show message preview for non-message notifications */}
                                            {!isMessageNotification && (
                                                <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                                                    {notification.message}
                                                </p>
                                            )}
                                            {isMessageNotification && (
                                                <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                                                    Click to view message
                                                </p>
                                            )}
                                            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                                {notification.time}
                                            </p>
                                        </div>

                                        {!notification.read && (
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    onMarkAsRead(notification.id);
                                                }}
                                                className="flex-shrink-0 h-6 w-6 rounded-full flex items-center justify-center hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                                                title="Mark as read"
                                            >
                                                <Check className="h-4 w-4 text-gray-600 dark:text-gray-300" />
                                            </button>
                                        )}
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                )}
            </div>

            {/* Footer */}
            <div className="p-3 border-t border-gray-200 dark:border-gray-700">
                <Link
                    to="/notifications"
                    onClick={(e) => {
                        e.stopPropagation();
                    }}
                    className="block w-full text-center text-sm text-blue-600 dark:text-blue-400 hover:underline font-medium py-2 cursor-pointer"
                >
                    View All Activity
                </Link>
            </div>
        </div>
    );
};

export default NotificationDropdown;