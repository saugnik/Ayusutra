import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useTheme } from '../contexts/ThemeContext';
import { useNavigate } from 'react-router-dom';
import {
  User,
  Mail,
  Phone,
  Shield,
  Bell,
  Save,
  CheckCircle,
  AlertCircle,
  Lock,
  Moon,
  Sun,
  Camera,
  Download,
  Trash2,
  AlertTriangle,
  Menu,
  X,
  Home,
  Calendar,
  Activity,
  MessageCircle,
  Settings as SettingsIcon
} from 'lucide-react';
import api from '../services/api';
import Sidebar from '../components/Sidebar';
import NotificationDropdown, { Notification } from '../components/NotificationDropdown';

interface UserProfile {
  full_name: string;
  email: string;
  phone: string;
  role: string;
  profile_picture?: string;
}

const Settings = () => {
  const { user, login, logout } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('general');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);
  const { theme, toggleTheme } = useTheme();
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [profilePicturePreview, setProfilePicturePreview] = useState<string | null>(null);
  const [isNotificationOpen, setIsNotificationOpen] = useState(false);
  const [notificationsList, setNotificationsList] = useState<Notification[]>([
    { id: 'SN1', type: 'info', title: 'Profile Updated', message: 'Your profile information was successfully updated.', time: '1 hour ago', read: true },
    { id: 'SN2', type: 'alert', title: 'Security Alert', message: 'A new login was detected from a new device.', time: '2 hours ago', read: false },
  ]);

  // Form States
  const [profile, setProfile] = useState<UserProfile>({
    full_name: '',
    email: '',
    phone: '',
    role: ''
  });

  const [passwords, setPasswords] = useState({
    current: '',
    new: '',
    confirm: ''
  });

  // Notifications Mock State
  const [notifications, setNotifications] = useState({
    email: true,
    sms: false,
    appointments: true,
    marketing: false
  });

  useEffect(() => {
    const fetchUserData = async () => {
      if (user) {
        try {
          const response = await api.get('/users/me');
          setProfile({
            full_name: response.data.full_name,
            email: response.data.email,
            phone: response.data.phone || '',
            role: response.data.role
          });
        } catch (error) {
          console.error('Failed to fetch user data:', error);
          // Fallback to basic user data
          setProfile({
            full_name: user.full_name,
            email: '',
            phone: '',
            role: user.role
          });
        }
      }
    };
    fetchUserData();
  }, [user]);

  const handleProfileUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      const response = await api.put('/users/me', {
        full_name: profile.full_name,
        email: profile.email,
        phone: profile.phone,
        profile_picture: profile.profile_picture
      });

      setMessage({ type: 'success', text: 'Profile updated successfully!' });
    } catch (error) {
      console.error(error);
      setMessage({ type: 'error', text: 'Failed to update profile.' });
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (passwords.new !== passwords.confirm) {
      setMessage({ type: 'error', text: 'New passwords do not match.' });
      return;
    }

    setLoading(true);
    setMessage(null);

    try {
      await api.put('/users/me', {
        password: passwords.new
      });
      setMessage({ type: 'success', text: 'Password updated successfully!' });
      setPasswords({ current: '', new: '', confirm: '' });
    } catch (error) {
      console.error(error);
      setMessage({ type: 'error', text: 'Failed to update password.' });
    } finally {
      setLoading(false);
    }
  };

  const handleProfilePictureChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64String = reader.result as string;
        setProfilePicturePreview(base64String);
        setProfile({ ...profile, profile_picture: base64String });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleMarkAsRead = (id: string) => {
    setNotificationsList(prev => prev.map(n => n.id === id ? { ...n, read: true } : n));
  };

  const handleClearAll = () => {
    setNotificationsList([]);
    setIsNotificationOpen(false);
  };

  const handleViewAllActivities = () => {
    setIsNotificationOpen(false);
    if (user?.role === 'practitioner') {
      navigate('/practitioner');
    } else if (user?.role === 'admin') {
      navigate('/admin');
    } else {
      navigate('/progress');
    }
  };

  const handleThemeToggle = () => {
    toggleTheme();
    setMessage({ type: 'success', text: `Theme changed to ${theme === 'light' ? 'dark' : 'light'} mode!` });
  };

  const handleExportData = async () => {
    try {
      const response = await api.get('/users/me');
      const dataStr = JSON.stringify(response.data, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `ayursutra-data-${new Date().toISOString()}.json`;
      link.click();
      setMessage({ type: 'success', text: 'Data exported successfully!' });
    } catch (error) {
      console.error(error);
      setMessage({ type: 'error', text: 'Failed to export data.' });
    }
  };

  const handleDeleteAccount = async () => {
    setLoading(true);
    try {
      // In a real implementation, you'd have a DELETE /users/me endpoint
      // await apiClient.delete('/users/me');
      setMessage({ type: 'success', text: 'Account deletion requested. Logging out...' });
      setTimeout(() => {
        logout();
        navigate('/auth');
      }, 2000);
    } catch (error) {
      console.error(error);
      setMessage({ type: 'error', text: 'Failed to delete account.' });
    } finally {
      setLoading(false);
      setShowDeleteModal(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/auth');
  };

  const renderTabs = () => (
    <div className="flex border-b border-gray-200 dark:border-gray-700 mb-6 overflow-x-auto scrollbar-hide">
      {[
        { id: 'general', icon: User, label: 'General' },
        { id: 'security', icon: Shield, label: 'Security' },
        { id: 'notifications', icon: Bell, label: 'Notifications' },
        { id: 'appearance', icon: theme === 'light' ? Sun : Moon, label: 'Appearance' },
        { id: 'privacy', icon: Lock, label: 'Privacy' },
      ].map((tab) => (
        <button
          key={tab.id}
          onClick={() => setActiveTab(tab.id)}
          className={`flex items-center space-x-2 py-4 px-6 font-medium text-sm border-b-2 transition-all whitespace-nowrap ${activeTab === tab.id
            ? 'border-primary-600 text-primary-600 dark:text-primary-400 dark:border-primary-400'
            : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'
            }`}
        >
          <tab.icon className="h-4 w-4" />
          <span>{tab.label}</span>
        </button>
      ))}
    </div>
  );

  const renderGeneral = () => (
    <form onSubmit={handleProfileUpdate} className="space-y-6 max-w-2xl">
      {/* Profile Picture Section */}
      <div className="flex items-center space-x-6">
        <div className="relative">
          <div className="w-24 h-24 rounded-full overflow-hidden bg-gray-200 dark:bg-gray-700 flex items-center justify-center border-2 border-primary-100 dark:border-primary-900/30 shadow-sm">
            {profilePicturePreview || profile.profile_picture ? (
              <img
                src={profilePicturePreview || profile.profile_picture}
                alt="Profile"
                className="w-full h-full object-cover"
              />
            ) : (
              <User className="h-12 w-12 text-gray-400 dark:text-gray-500" />
            )}
          </div>
          <label className="absolute bottom-0 right-0 bg-primary-600 rounded-full p-2 cursor-pointer hover:bg-primary-700 transition-colors shadow-lg border-2 border-white dark:border-gray-800">
            <Camera className="h-4 w-4 text-white" />
            <input
              type="file"
              accept="image/*"
              onChange={handleProfilePictureChange}
              className="hidden"
            />
          </label>
        </div>
        <div>
          <h3 className="text-sm font-semibold text-gray-900 dark:text-white">Profile Photo</h3>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Accepts JPG, PNG or GIF (Max 2MB)</p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Full Name</label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <User className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              value={profile.full_name}
              onChange={(e) => setProfile({ ...profile, full_name: e.target.value })}
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-900 text-gray-900 dark:text-white sm:text-sm transition-all shadow-sm"
              placeholder="Your full name"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email Address</label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Mail className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="email"
              value={profile.email}
              onChange={(e) => setProfile({ ...profile, email: e.target.value })}
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-900 text-gray-900 dark:text-white sm:text-sm transition-all shadow-sm"
              placeholder="Email address"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Phone Number</label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Phone className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="tel"
              value={profile.phone}
              onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-900 text-gray-900 dark:text-white sm:text-sm transition-all shadow-sm"
              placeholder="Your phone number"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Account Role</label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Shield className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              value={profile.role.toUpperCase()}
              disabled
              className="block w-full pl-10 pr-3 py-2 border border-gray-200 dark:border-gray-800 rounded-lg bg-gray-50 dark:bg-gray-800/50 text-gray-500 dark:text-gray-400 sm:text-sm cursor-not-allowed"
            />
          </div>
        </div>
      </div>

      <div className="flex justify-end pt-4 border-t border-gray-100 dark:border-gray-800">
        <button
          type="submit"
          disabled={loading}
          className="btn-primary flex items-center space-x-2 px-6 py-2.5 rounded-lg shadow-md hover:shadow-lg transition-all"
        >
          {loading ? (
            <CheckCircle className="h-4 w-4 animate-spin" />
          ) : (
            <Save className="h-4 w-4" />
          )}
          <span>{loading ? 'Saving Changes...' : 'Save Changes'}</span>
        </button>
      </div>
    </form>
  );

  const renderSecurity = () => (
    <form onSubmit={handlePasswordUpdate} className="space-y-6 max-w-2xl">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Security Settings</h3>
        <p className="text-sm text-gray-500 dark:text-gray-400">Update your password to keep your account secure.</p>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">New Password</label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Lock className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="password"
              value={passwords.new}
              onChange={(e) => setPasswords({ ...passwords, new: e.target.value })}
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-900 text-gray-900 dark:text-white sm:text-sm transition-all shadow-sm"
              placeholder="Minimum 8 characters"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Confirm New Password</label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Lock className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="password"
              value={passwords.confirm}
              onChange={(e) => setPasswords({ ...passwords, confirm: e.target.value })}
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-900 text-gray-900 dark:text-white sm:text-sm transition-all shadow-sm"
              placeholder="Repeat new password"
            />
          </div>
        </div>
      </div>

      <div className="flex justify-end pt-4 border-t border-gray-100 dark:border-gray-800">
        <button
          type="submit"
          disabled={loading}
          className="btn-primary flex items-center space-x-2 px-6 py-2.5 rounded-lg shadow-md hover:shadow-lg transition-all"
        >
          {loading ? (
            <CheckCircle className="h-4 w-4 animate-spin" />
          ) : (
            <Shield className="h-4 w-4" />
          )}
          <span>{loading ? 'Updating...' : 'Update Password'}</span>
        </button>
      </div>
    </form>
  );

  const renderNotifications = () => (
    <div className="space-y-6 max-w-2xl">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Notification Preferences</h3>
        <p className="text-sm text-gray-500 dark:text-gray-400">Choose how you want to be notified about your health and sessions.</p>
      </div>

      <div className="space-y-4">
        {[
          { id: 'email', title: 'Email Notifications', desc: 'Appointments, summaries and healthy tips.' },
          { id: 'sms', title: 'SMS Notifications', desc: 'Direct alerts and urgent reminders.' },
          { id: 'appointments', title: 'Appointment Reminders', desc: 'Stay updated on your upcoming therapy.' },
          { id: 'marketing', title: 'Ayurvedic Insights', desc: 'Personalized wellness recommendations.' },
        ].map((item) => (
          <div key={item.id} className="flex items-center justify-between py-4 border-b border-gray-100 dark:border-gray-800 last:border-0">
            <div>
              <h4 className="text-sm font-semibold text-gray-900 dark:text-gray-100">{item.title}</h4>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{item.desc}</p>
            </div>
            <button
              onClick={() => setNotifications({ ...notifications, [item.id]: !notifications[item.id as keyof typeof notifications] })}
              className={`relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none ${notifications[item.id as keyof typeof notifications] ? 'bg-primary-600' : 'bg-gray-200 dark:bg-gray-700'}`}
            >
              <span className={`pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200 ${notifications[item.id as keyof typeof notifications] ? 'translate-x-5' : 'translate-x-0'}`} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );

  const renderAppearance = () => (
    <div className="space-y-6 max-w-2xl">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Appearance Settings</h3>
        <p className="text-sm text-gray-500 dark:text-gray-400">Personalize your AyurSutra experience.</p>
      </div>

      <div className="flex items-center justify-between py-6 border-b border-gray-100 dark:border-gray-800">
        <div className="flex items-center space-x-4">
          <div className={`p-3 rounded-xl ${theme === 'light' ? 'bg-yellow-100' : 'bg-indigo-900/40'}`}>
            {theme === 'light' ? (
              <Sun className="h-6 w-6 text-yellow-600" />
            ) : (
              <Moon className="h-6 w-6 text-indigo-400" />
            )}
          </div>
          <div>
            <h4 className="text-sm font-semibold text-gray-900 dark:text-white">Interface Theme</h4>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              Currently using <span className="font-semibold text-primary-600 dark:text-primary-400">{theme.charAt(0).toUpperCase() + theme.slice(1)} Mode</span>
            </p>
          </div>
        </div>
        <button
          onClick={handleThemeToggle}
          className="flex items-center space-x-2 px-6 py-2 border-2 border-primary-100 dark:border-primary-900/30 text-primary-700 dark:text-primary-400 font-medium rounded-lg hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-all"
        >
          {theme === 'light' ? <Moon className="h-4 w-4" /> : <Sun className="h-4 w-4" />}
          <span>Switch Mode</span>
        </button>
      </div>
    </div>
  );

  const renderPrivacy = () => (
    <div className="space-y-6 max-w-2xl">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Privacy & Data Management</h3>
        <p className="text-sm text-gray-500 dark:text-gray-400">Control your information and account status.</p>
      </div>

      {/* Export Data */}
      <div className="border border-gray-200 dark:border-gray-700 rounded-xl p-6 bg-white dark:bg-gray-800/50 shadow-sm">
        <div className="flex flex-col sm:flex-row items-start justify-between gap-4">
          <div className="flex items-start space-x-4">
            <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-xl">
              <Download className="h-6 w-6 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <h4 className="text-sm font-semibold text-gray-900 dark:text-white">Export My Data</h4>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 max-w-md">
                Get a comprehensive copy of your profile, history, and health logs.
              </p>
            </div>
          </div>
          <button
            onClick={handleExportData}
            className="w-full sm:w-auto px-6 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 font-medium rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-all flex items-center justify-center space-x-2"
          >
            <Download className="h-4 w-4" />
            <span>Export (JSON)</span>
          </button>
        </div>
      </div>

      {/* Delete Account */}
      <div className="border border-red-100 dark:border-red-900/30 rounded-xl p-6 bg-red-50 dark:bg-red-900/10 shadow-sm transition-all hover:bg-red-100/50 dark:hover:bg-red-900/20">
        <div className="flex flex-col sm:flex-row items-start justify-between gap-4">
          <div className="flex items-start space-x-4">
            <div className="p-3 bg-red-100 dark:bg-red-900/40 rounded-xl">
              <Trash2 className="h-6 w-6 text-red-600 dark:text-red-400" />
            </div>
            <div>
              <h4 className="text-sm font-semibold text-gray-900 dark:text-white">Delete Account</h4>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 max-w-md">
                Permanently close your account and wipe all data. This cannot be undone.
              </p>
            </div>
          </div>
          <button
            onClick={() => setShowDeleteModal(true)}
            className="w-full sm:w-auto px-6 py-2 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 transition-all shadow-md hover:shadow-lg flex items-center justify-center space-x-2"
          >
            <Trash2 className="h-4 w-4" />
            <span>Delete Permanently</span>
          </button>
        </div>
      </div>
    </div>
  );

  // Sidebar navigation items
  const sidebarItems = [
    { icon: Home, label: 'Dashboard', path: '/patient' },
    { icon: Calendar, label: 'My Sessions', path: '/my-sessions' },
    { icon: Activity, label: 'My Progress', path: '/progress' },
    { icon: MessageCircle, label: 'Health Support', path: '/health-support' },
    { icon: SettingsIcon, label: 'Settings', path: '/settings' }
  ];

  return (
    <div className="flex h-screen bg-dashboard">
      {/* Sidebar */}
      <div className="hidden md:block w-64 flex-shrink-0">
        <Sidebar items={sidebarItems} user={user} onLogout={handleLogout} />
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <main className="flex-1 overflow-y-auto focus:outline-none scroll-smooth">
          <div className="py-8 px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto">
              <div className="flex items-center justify-between mb-8">
                <div>
                  <h1 className="text-3xl font-extrabold text-gray-900 dark:text-white tracking-tight">Settings</h1>
                  <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">Manage your account preferences and security settings.</p>
                </div>

                <div className="flex items-center space-x-4 relative">
                  <button
                    onClick={() => setIsNotificationOpen(!isNotificationOpen)}
                    className="p-2 text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 relative bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700"
                  >
                    <Bell className="h-6 w-6" />
                    {notificationsList.filter(n => !n.read).length > 0 && (
                      <span className="absolute -top-1 -right-1 flex h-4 w-4">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-4 w-4 bg-red-500 text-[10px] text-white flex items-center justify-center font-bold">
                          {notificationsList.filter(n => !n.read).length}
                        </span>
                      </span>
                    )}
                  </button>

                  <NotificationDropdown
                    notifications={notificationsList}
                    isOpen={isNotificationOpen}
                    onClose={() => setIsNotificationOpen(false)}
                    onMarkAsRead={handleMarkAsRead}
                    onClearAll={handleClearAll}
                    onViewAll={handleViewAllActivities}
                  />
                </div>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl dark:shadow-2xl-strong border border-gray-100 dark:border-gray-700/50 overflow-hidden transition-all">
                <div className="p-6">
                  {message && (
                    <div className={`mb-8 p-4 rounded-xl flex items-center animate-fade-in ${message.type === 'success' ? 'bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-300 border border-green-100 dark:border-green-800' : 'bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-300 border border-red-100 dark:border-red-800'}`}>
                      {message.type === 'success' ? (
                        <CheckCircle className="h-5 w-5 mr-3 flex-shrink-0" />
                      ) : (
                        <AlertCircle className="h-5 w-5 mr-3 flex-shrink-0" />
                      )}
                      <span className="text-sm font-medium">{message.text}</span>
                    </div>
                  )}

                  {renderTabs()}

                  <div className="mt-8 transition-all duration-300">
                    {activeTab === 'general' && renderGeneral()}
                    {activeTab === 'security' && renderSecurity()}
                    {activeTab === 'notifications' && renderNotifications()}
                    {activeTab === 'appearance' && renderAppearance()}
                    {activeTab === 'privacy' && renderPrivacy()}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>

        {/* Delete Account Confirmation Modal */}
        {showDeleteModal && (
          <div className="fixed inset-0 bg-gray-950/80 backdrop-blur-sm flex items-center justify-center z-[100] p-4 transition-all animate-in fade-in duration-300">
            <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-2xl w-full max-w-md overflow-hidden transform transition-all border border-gray-100 dark:border-gray-800 animate-in zoom-in-95 duration-300">
              <div className="p-6">
                <div className="flex items-center space-x-4 mb-6">
                  <div className="p-3 bg-red-100 dark:bg-red-900/30 rounded-2xl">
                    <AlertTriangle className="h-8 w-8 text-red-600 dark:text-red-400" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white">Delete Account?</h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400">This action is irreversible.</p>
                  </div>
                </div>

                <div className="space-y-4 mb-8">
                  <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
                    You are about to permanently remove your AyurSutra account. This includes:
                  </p>
                  <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-2">
                    {['Health history & Progress', 'Appointments & Logs', 'Personalized Dosha data'].map((item, i) => (
                      <li key={i} className="flex items-center">
                        <span className="w-1.5 h-1.5 bg-red-500 rounded-full mr-2" />
                        {item}
                      </li>
                    ))}
                  </ul>
                  <p className="text-xs font-bold text-red-600 dark:text-red-400 uppercase tracking-widest pt-2">
                    Action cannot be undone
                  </p>
                </div>

                <div className="flex flex-col sm:flex-row gap-3">
                  <button
                    onClick={() => setShowDeleteModal(false)}
                    className="flex-1 px-6 py-2.5 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white font-semibold rounded-xl hover:bg-gray-100 dark:hover:bg-gray-700 transition-all border border-gray-200 dark:border-gray-700"
                  >
                    Keep Account
                  </button>
                  <button
                    onClick={handleDeleteAccount}
                    disabled={loading}
                    className="flex-1 px-6 py-2.5 bg-red-600 text-white font-semibold rounded-xl hover:bg-red-700 transition-all shadow-lg hover:shadow-red-500/20 disabled:opacity-50"
                  >
                    {loading ? 'Deleting...' : 'Confirm Delete'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Settings;
