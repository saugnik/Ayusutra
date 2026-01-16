import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Calendar,
  Clock,
  Bell,
  Activity,
  TrendingUp,
  User as UserIcon,
  Settings,
  MessageCircle,
  Video,
  FileText,
  Menu,
  X,
  CheckCircle,
  MapPin
} from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import appointmentService from '../services/appointment.service';
import { AppointmentResponse } from '../types/api.types';
import BookAppointmentModal from '../components/BookAppointmentModal';
import toast from 'react-hot-toast';
import DailyWisdom from '../components/DailyWisdom';
import Sidebar, { SidebarItem } from '../components/Sidebar';
import NotificationDropdown, { Notification } from '../components/NotificationDropdown';
import HealthAgentChat from '../components/HealthAgentChat';

const PatientDashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [checkedItems, setCheckedItems] = useState<{ [key: string]: boolean }>({});
  const [appointments, setAppointments] = useState<AppointmentResponse[]>([]);
  const [isBookingModalOpen, setIsBookingModalOpen] = useState(false);
  const [isNotificationOpen, setIsNotificationOpen] = useState(false);
  const [notifications, setNotifications] = useState<Notification[]>([
    { id: 'N001', type: 'reminder', title: 'Welcome to AyurSutra', message: 'We are glad to have you on your wellness journey.', time: '1 hour ago', read: false },
    { id: 'N002', type: 'appointment', title: 'Session Confirmed', message: 'Your Shirodhara session with Dr. Sharma is confirmed.', time: '2 hours ago', read: false },
  ]);

  useEffect(() => {
    if (user) {
      loadAppointments();
    }
  }, [user]);

  const loadAppointments = async () => {
    try {
      const data = await appointmentService.getMyAppointments('scheduled');
      setAppointments(data);
    } catch (error) {
      console.error("Failed to load appointments", error);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/auth');
  };

  const nextSession = appointments.length > 0 ? appointments[0] : null;

  // Mock data for other sections
  const preCheckItems = [
    { id: 'pc1', text: 'Complete 12-hour fasting', completed: true, required: true },
    { id: 'pc2', text: 'Avoid oil consumption for 24 hours', completed: true, required: true },
    { id: 'pc3', text: 'Morning meditation (30 minutes)', completed: false, required: false },
    { id: 'pc4', text: 'Drink warm water upon waking', completed: false, required: true },
    { id: 'pc5', text: 'Arrive 30 minutes before session', completed: false, required: true }
  ];

  const handleMarkAsRead = (id: string) => {
    setNotifications(prev => prev.map(n => n.id === id ? { ...n, read: true } : n));
  };

  const handleClearAll = () => {
    setNotifications([]);
    setIsNotificationOpen(false);
  };

  const handleViewAllActivities = () => {
    setIsNotificationOpen(false);
    navigate('/progress'); // Redirect to Progress for now as it has history/activity
  };

  const handleCheckItem = (itemId: string) => {
    setCheckedItems(prev => ({
      ...prev,
      [itemId]: !prev[itemId]
    }));
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
      <BookAppointmentModal
        isOpen={isBookingModalOpen}
        onClose={() => setIsBookingModalOpen(false)}
        onSuccess={loadAppointments}
      />

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
            {/* Mobile sidebar content */}
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
              <h1 className="text-2xl font-semibold text-gray-900 dark:text-white">Namaste, {user?.full_name || 'AyurSeeker'}!</h1>
              <p className="text-sm text-gray-600 dark:text-gray-400">Your wellness journey continues</p>
            </div>
            <div className="flex items-center space-x-4 relative">
              <button
                onClick={() => setIsNotificationOpen(!isNotificationOpen)}
                className="p-2 text-gray-500 hover:text-gray-700 relative"
              >
                <Bell className="h-6 w-6" />
                {notifications.filter(n => !n.read).length > 0 && (
                  <span className="absolute -mt-1 ml-2 flex h-3 w-3 top-2 right-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
                  </span>
                )}
              </button>

              <NotificationDropdown
                notifications={notifications}
                isOpen={isNotificationOpen}
                onClose={() => setIsNotificationOpen(false)}
                onMarkAsRead={handleMarkAsRead}
                onClearAll={handleClearAll}
                onViewAll={handleViewAllActivities}
              />
            </div>
          </div>
        </div>

        {/* Dashboard content */}
        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto">
            {/* Next Session Card */}
            <div className="mb-8">
              <div className="card bg-gradient-to-r from-primary-500 to-primary-600 text-white">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h2 className="text-2xl font-bold mb-2">Next Session</h2>
                    {nextSession ? (
                      <div className="space-y-2">
                        <p className="text-xl font-medium">{nextSession.therapy_type}</p>
                        <p className="text-primary-100">
                          Doctor ID: {nextSession.practitioner_id} • 60 mins
                        </p>
                        <div className="flex items-center space-x-4 text-primary-100">
                          <div className="flex items-center">
                            <Calendar className="h-4 w-4 mr-1" />
                            <span>{new Date(nextSession.scheduled_datetime).toLocaleDateString()}</span>
                          </div>
                          <div className="flex items-center">
                            <Clock className="h-4 w-4 mr-1" />
                            <span>{new Date(nextSession.scheduled_datetime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                          </div>
                        </div>
                      </div>
                    ) : (
                      <div className="space-y-2">
                        <p className="text-xl font-medium">No upcoming sessions</p>
                        <p className="text-primary-100">Book your first consultation to get started.</p>
                      </div>
                    )}
                  </div>
                  <div className="flex flex-col space-y-2">
                    {!nextSession && (
                      <button
                        onClick={() => setIsBookingModalOpen(true)}
                        className="bg-white text-primary-600 px-6 py-2 rounded-lg font-medium hover:bg-primary-50"
                      >
                        Book Now
                      </button>
                    )}
                    {nextSession && (
                      <button className="bg-white text-primary-600 px-6 py-2 rounded-lg font-medium hover:bg-primary-50">
                        <Video className="h-4 w-4 inline mr-2" />
                        Join Session
                      </button>
                    )}
                  </div>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Daily Wisdom & Checklist */}
              <div className="lg:col-span-2 space-y-6">

                {/* Daily Wisdom Widget */}
                <DailyWisdom />

                {/* Checklist */}
                <div className="card">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Pre-procedure Checklist</h3>
                    <span className="text-sm text-gray-500 dark:text-gray-400">For your wellbeing</span>
                  </div>
                  <div className="space-y-4">
                    {preCheckItems.map((item) => (
                      <div key={item.id} className="flex items-start space-x-3">
                        <button
                          onClick={() => handleCheckItem(item.id)}
                          className={`flex-shrink-0 mt-0.5 w-5 h-5 rounded border-2 flex items-center justify-center ${item.completed || checkedItems[item.id]
                            ? 'bg-green-500 border-green-500'
                            : 'border-gray-300 hover:border-primary-500'
                            }`}
                        >
                          {(item.completed || checkedItems[item.id]) && (
                            <CheckCircle className="h-3 w-3 text-white" />
                          )}
                        </button>
                        <div className="flex-1">
                          <p className={`text-sm ${item.completed || checkedItems[item.id]
                            ? 'text-gray-400 dark:text-gray-500 line-through'
                            : 'text-gray-900 dark:text-gray-200'
                            }`}>
                            {item.text}
                            {item.required && (
                              <span className="text-red-500 ml-1">*</span>
                            )}
                          </p>
                          {item.required && !(item.completed || checkedItems[item.id]) && (
                            <p className="text-xs text-red-500 mt-1">Required</p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Progress & Actions */}
              <div className="space-y-6">

                <div className="card">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Quick Actions</h3>
                  <div className="space-y-3">
                    <button
                      onClick={() => setIsBookingModalOpen(true)}
                      className="w-full btn-primary text-left flex items-center"
                    >
                      <Calendar className="h-4 w-4 mr-3" />
                      Book New Session
                    </button>
                    <button className="w-full bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 px-4 py-3 rounded-lg font-medium hover:bg-gray-200 dark:hover:bg-gray-700 text-left flex items-center">
                      <MessageCircle className="h-4 w-4 mr-3" />
                      Contact Practitioner
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Upcoming Sessions List */}
            <div className="grid grid-cols-1 gap-6 mt-8">
              <div className="card">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Your Appointments</h3>
                </div>
                {appointments.length === 0 ? (
                  <p className="text-gray-500 text-center py-4">No appointments scheduled.</p>
                ) : (
                  <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2">
                    {appointments.map((session) => (
                      <div key={session.id} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-900/50 rounded-lg border border-gray-100 dark:border-gray-800">
                        <div>
                          <p className="font-medium text-gray-900 dark:text-white">{session.therapy_type}</p>
                          <p className="text-sm text-gray-600 dark:text-gray-400">Practitioner ID: {session.practitioner_id}</p>
                          <div className="flex items-center space-x-4 text-xs text-gray-500 dark:text-gray-400 mt-1">
                            <span>{new Date(session.scheduled_datetime).toLocaleDateString()}</span>
                            <span>{new Date(session.scheduled_datetime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                          </div>
                        </div>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${session.status === 'confirmed' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' :
                          session.status === 'scheduled' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400' :
                            'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300'
                          }`}>
                          {session.status.toUpperCase()}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </main>
      </div>
      <HealthAgentChat />
    </div>
  );
};

export default PatientDashboard;
