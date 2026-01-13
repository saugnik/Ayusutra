import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LogOut } from 'lucide-react';

export interface SidebarItem {
    icon: any;
    label: string;
    path: string;
}

interface SidebarProps {
    items: SidebarItem[];
    user: any;
    onLogout: () => void;
}

const Sidebar = ({ items, user, onLogout }: SidebarProps) => {
    const location = useLocation();

    return (
        <div className="flex flex-col h-full bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800">
            {/* Logo */}
            <div className="flex items-center h-16 flex-shrink-0 px-6 bg-primary-600">
                <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center">
                    <span className="text-primary-600 font-bold text-lg">आ</span>
                </div>
                <span className="ml-3 text-xl font-bold text-white">AyurSutra</span>
            </div>

            {/* Patient Info */}
            <div className="p-6 border-b border-gray-200 dark:border-gray-800">
                <div className="flex items-center">
                    <div className="w-10 h-10 rounded-full overflow-hidden border-2 border-primary-200">
                        <img
                            src={`https://api.dicebear.com/7.x/notionists/svg?seed=${encodeURIComponent(user?.full_name || 'Guest')}&backgroundColor=e5e7eb`}
                            alt="User Avatar"
                            className="w-full h-full object-cover"
                        />
                    </div>
                    <div className="ml-3">
                        <p className="text-sm font-medium text-gray-900 dark:text-gray-100">{user?.full_name || 'Guest'}</p>
                        <p className="text-xs text-gray-500 dark:text-gray-400">{user?.role === 'patient' ? 'Patient' : 'User'}</p>
                    </div>
                </div>
            </div>

            {/* Navigation */}
            <nav className="mt-6 flex-1 px-6">
                <div className="space-y-2">
                    {items.map((item) => {
                        const isActive = location.pathname === item.path;

                        return (
                            <Link
                                key={item.path}
                                to={item.path}
                                className={`group flex items-center w-full px-4 py-2 text-sm font-medium rounded-lg transition-colors ${isActive
                                    ? 'bg-primary-100 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400'
                                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-gray-100'
                                    }`}
                            >
                                <item.icon className="mr-3 h-5 w-5" />
                                {item.label}
                            </Link>
                        );
                    })}
                </div>
            </nav>

            {/* Footer */}
            <div className="flex-shrink-0 p-6 border-t border-gray-200 dark:border-gray-800">
                <button
                    onClick={onLogout}
                    className="group flex items-center w-full px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-400 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
                >
                    <LogOut className="mr-3 h-5 w-5" />
                    Sign Out
                </button>
            </div>
        </div>
    );
};

export default Sidebar;
