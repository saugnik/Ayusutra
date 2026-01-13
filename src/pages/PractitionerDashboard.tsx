import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Calendar,
  Users,
  Clock,
  TrendingUp,
  Bell,
  Settings,
  FileText,
  Activity,
  CheckCircle,
  AlertCircle,
  User,
  Phone,
  Mail,
  MapPin,
  Plus,
  Search,
  Filter,
  Eye,
  Edit,
  MoreVertical,
  LogOut,
  Download
} from 'lucide-react';
import PractitionerUpdateModal from '../components/PractitionerUpdateModal';
import practitionerService from '../services/practitioner.service';
import { useAuth } from '../hooks/useAuth';
import { Appointment, DashboardStats, PatientListItem } from '../types/api.types';
import NotificationDropdown, { Notification } from '../components/NotificationDropdown';

const PractitionerDashboard = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [selectedTab, setSelectedTab] = useState('overview');
  const [selectedPatient, setSelectedPatient] = useState<{ id: number, name: string } | null>(null);
  const [isUpdateModalOpen, setIsUpdateModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [isNotificationOpen, setIsNotificationOpen] = useState(false);
  const [notifications, setNotifications] = useState<Notification[]>([
    { id: 'PN1', type: 'alert', title: 'New Patient Registration', message: 'Rahul Kumar has registered for consultations.', time: '10 mins ago', read: false },
    { id: 'PN2', type: 'appointment', title: 'Upcoming Session', message: 'You have a Shirodhara session in 15 minutes.', time: '15 mins ago', read: false },
    { id: 'PN3', type: 'info', title: 'Report Due', message: 'Monthly analysis report for June is ready to view.', time: '1 hour ago', read: true },
  ]);

  // Real Data State
  const [stats, setStats] = useState<DashboardStats>({
    total_patients: 0,
    today_appointments: 0,
    active_treatments: 0,
    pending_reports: 0
  });
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [patients, setPatients] = useState<PatientListItem[]>([]);

  // Analytics State
  const [analytics, setAnalytics] = useState<any>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [dashboardStats, myPatients, allAppointments, analyticsData] = await Promise.all([
          practitionerService.getDashboardStats(),
          practitionerService.getMyPatients(),
          practitionerService.getAppointments(),
          practitionerService.getAnalytics()
        ]);

        setStats(dashboardStats);
        setPatients(myPatients);
        setAnalytics(analyticsData);

        // Filter appointments for today
        const today = new Date().toDateString();
        const todays = allAppointments.filter(app =>
          new Date(app.scheduled_datetime).toDateString() === today
        ).sort((a, b) => new Date(a.scheduled_datetime).getTime() - new Date(b.scheduled_datetime).getTime());

        setAppointments(todays);
      } catch (error) {
        console.error("Failed to fetch dashboard data", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Helpers
  const handleLogout = () => {
    logout();
    navigate('/auth');
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'scheduled': return 'text-blue-600 bg-blue-100'; // Maps to 'upcoming' visually
      case 'upcoming': return 'text-blue-600 bg-blue-100';
      case 'in_progress': return 'text-green-600 bg-green-100';
      case 'in-progress': return 'text-green-600 bg-green-100';
      case 'completed': return 'text-gray-600 bg-gray-100';
      case 'active': return 'text-primary-600 bg-primary-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const handleOpenUpdateModal = (patient: any) => {
    setSelectedPatient({ id: patient.id, name: patient.name });
    setIsUpdateModalOpen(true);
  };

  const handleMarkAsRead = (id: string) => {
    setNotifications(prev => prev.map(n => n.id === id ? { ...n, read: true } : n));
  };

  const handleClearAll = () => {
    setNotifications([]);
    setIsNotificationOpen(false);
  };

  const handleViewAllActivities = () => {
    setIsNotificationOpen(false);
    setSelectedTab('activities');
  };

  // Mock Alerts (Leave as mock for now or clear)
  const recentAlerts: any[] = [];

  const renderOverview = () => (
    <div className="space-y-6">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-blue-100 rounded-lg">
              <Users className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Patients</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total_patients || 0}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-green-100 rounded-lg">
              <Calendar className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Today's Appointments</p>
              <p className="text-2xl font-bold text-gray-900">{stats.today_appointments || 0}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-primary-100 rounded-lg">
              <Activity className="h-6 w-6 text-primary-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Active Therapies</p>
              <p className="text-2xl font-bold text-gray-900">{stats.active_treatments || 0}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-orange-100 rounded-lg">
              <FileText className="h-6 w-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Pending Reports</p>
              <p className="text-2xl font-bold text-gray-900">{stats.pending_reports || 0}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Today's Schedule */}
        <div className="lg:col-span-2 card">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Today's Schedule</h3>
            <button className="btn-primary text-sm px-4 py-2">
              <Plus className="h-4 w-4 mr-1" /> Add Appointment
            </button>
          </div>

          <div className="space-y-4">
            {appointments.length === 0 ? (
              <p className="text-gray-500 text-center py-4">No appointments scheduled for today.</p>
            ) : (
              appointments.map((appointment) => (
                <div key={appointment.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
                  <div className="flex items-center space-x-4">
                    <div className="text-center">
                      <p className="text-sm font-medium text-gray-900">
                        {new Date(appointment.scheduled_datetime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </p>
                      <p className="text-xs text-gray-500">{appointment.duration_minutes} min</p>
                    </div>
                    <div>
                      {/* Assuming we might not have patient name populated in Appointment list yet without join, checking API response */}
                      {/* The AppointmentResponse doesn't technically have patient name, but in a real app we'd fetch it or include it. 
                            For now, since appointment creation might be bare bones, I'll fallback or use ID if name missing. 
                            Wait, AppointmentResponse has patient_id. I can look up the patient name from `patients` list.
                        */}
                      <p className="font-medium text-gray-900">
                        {patients.find(p => p.id === appointment.patient_id)?.name || `Patient #${appointment.patient_id}`}
                      </p>
                      <p className="text-sm text-gray-600">{appointment.therapy_type}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(appointment.status)}`}>
                      {appointment.status.replace('_', ' ')}
                    </span>
                    <button className="p-2 hover:bg-gray-100 rounded-lg">
                      <MoreVertical className="h-4 w-4 text-gray-600" />
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Recent Alerts */}
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Recent Alerts</h3>
            <button
              onClick={handleViewAllActivities}
              className="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 font-medium"
            >
              View All
            </button>
          </div>
          <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2">
            {recentAlerts.length === 0 ? (
              <div className="text-center py-8">
                <Bell className="h-12 w-12 text-gray-200 dark:text-gray-700 mx-auto mb-3" />
                <p className="text-gray-500 dark:text-gray-400">No recent alerts.</p>
              </div>
            ) : (
              recentAlerts.map((alert: any) => (
                <div key={alert.id} className="flex items-start space-x-3 p-3 bg-gray-50 dark:bg-gray-900/50 rounded-lg border border-gray-100 dark:border-gray-800">
                  <div className={`p-2 rounded-lg ${alert.status === 'urgent' ? 'bg-red-100 text-red-600' : 'bg-blue-100 text-blue-600'}`}>
                    <AlertCircle className="h-4 w-4" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 dark:text-gray-100">{alert.title}</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{alert.message}</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );

  const renderPatients = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Patient Management</h2>
        {/* ... buttons ... */}
        <div className="flex space-x-3">
          {/* Search/Filter UI preserved */}
          <div className="relative">
            <Search className="h-5 w-5 text-gray-400 absolute left-3 top-3" />
            <input
              type="text"
              placeholder="Search patients..."
              className="input-field pl-10"
            />
          </div>
          <button className="btn-outline px-4 py-2">
            <Filter className="h-4 w-4 mr-2" /> Filter
          </button>
          <button className="btn-primary px-4 py-2">
            <Plus className="h-4 w-4 mr-2" /> New Patient
          </button>
        </div>
      </div>

      <div className="card">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-medium text-gray-900">Patient</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">Current Therapy</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">Stage</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">Next Appointment</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">Status</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">Actions</th>
              </tr>
            </thead>
            <tbody>
              {patients.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-gray-500">No patients found. Create one to get started.</td>
                </tr>
              ) : (
                patients.map((patient) => (
                  <tr key={patient.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-4 px-4">
                      <div>
                        <p className="font-medium text-gray-900">{patient.name}</p>
                        <p className="text-sm text-gray-600">{patient.age ? `${patient.age}yr, ` : ''}{patient.gender} • {patient.prakriti}</p>
                      </div>
                    </td>
                    <td className="py-4 px-4">
                      <p className="font-medium text-gray-900">{patient.current_therapy}</p>
                    </td>
                    <td className="py-4 px-4">
                      <span className="px-3 py-1 bg-primary-100 text-primary-800 rounded-full text-sm">
                        {patient.stage}
                      </span>
                    </td>
                    <td className="py-4 px-4">
                      <p className="text-gray-900">
                        {patient.next_appointment ? new Date(patient.next_appointment).toLocaleDateString() : 'None'}
                      </p>
                    </td>
                    <td className="py-4 px-4">
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(patient.status)}`}>
                        {patient.status}
                      </span>
                    </td>
                    <td className="py-4 px-4">
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleOpenUpdateModal(patient)}
                          className="p-2 hover:bg-green-100 text-green-600 rounded-lg flex items-center"
                          title="Update Health Status"
                        >
                          <Activity className="h-4 w-4" />
                        </button>
                        <button className="p-2 hover:bg-gray-100 rounded-lg">
                          <Eye className="h-4 w-4 text-gray-600" />
                        </button>
                        <button className="p-2 hover:bg-gray-100 rounded-lg">
                          <Edit className="h-4 w-4 text-gray-600" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderActivities = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Activity History</h2>
        <div className="flex space-x-3">
          <button className="btn-outline px-4 py-2">
            <Download className="h-4 w-4 mr-2" /> Export History
          </button>
        </div>
      </div>

      <div className="card">
        <div className="divide-y divide-gray-100 dark:divide-gray-800">
          {[...notifications, ...notifications].map((item, idx) => (
            <div key={`${item.id}-${idx}`} className="py-6 flex items-start space-x-4">
              <div className={`p-2 rounded-lg ${item.type === 'alert' ? 'bg-red-100 text-red-600' :
                item.type === 'appointment' ? 'bg-green-100 text-green-600' :
                  item.type === 'reminder' ? 'bg-blue-100 text-blue-600' :
                    'bg-gray-100 text-gray-600'
                }`}>
                {item.type === 'alert' ? <AlertCircle className="h-5 w-5" /> :
                  item.type === 'appointment' ? <Calendar className="h-5 w-5" /> :
                    <Bell className="h-5 w-5" />}
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <h4 className="text-lg font-semibold text-gray-900 dark:text-white">{item.title}</h4>
                  <span className="text-sm text-gray-500 dark:text-gray-400">{item.time}</span>
                </div>
                <p className="text-gray-600 dark:text-gray-400 leading-relaxed">{item.message}</p>
                <div className="mt-3 flex items-center space-x-4">
                  <span className={`px-2 py-0.5 rounded text-xs font-medium uppercase tracking-wider ${item.read ? 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400' : 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-400'
                    }`}>
                    {item.read ? 'Read' : 'New'}
                  </span>
                  <button className="text-sm text-primary-600 dark:text-primary-400 hover:underline">Mark as flagship</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderReports = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Reports & Analytics</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Using real analytics from state */}
        <div className="card text-center">
          <TrendingUp className="h-12 w-12 text-primary-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Treatment Success Rate</h3>
          <p className="text-3xl font-bold text-primary-600 mb-2">{analytics?.success_rate || 0}%</p>
          <p className="text-sm text-gray-600">Last 30 days</p>
        </div>

        <div className="card text-center">
          <Users className="h-12 w-12 text-green-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Patient Satisfaction</h3>
          <p className="text-3xl font-bold text-green-600 mb-2">{analytics?.patient_satisfaction || 0}/5</p>
          <p className="text-sm text-gray-600">Average rating</p>
        </div>

        <div className="card text-center">
          <Calendar className="h-12 w-12 text-blue-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Monthly Treatments</h3>
          <p className="text-3xl font-bold text-blue-600 mb-2">
            {analytics?.monthly_trends && analytics.monthly_trends.length > 0
              ? analytics.monthly_trends[0].sessions
              : 0}
          </p>
          <p className="text-sm text-gray-600">This month</p>
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Generate Reports</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow text-left">
            <FileText className="h-6 w-6 text-primary-600 mb-2" />
            <h4 className="font-medium text-gray-900">Patient Progress Report</h4>
            <p className="text-sm text-gray-600">Detailed progress for individual patients</p>
          </button>

          <button className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow text-left">
            <TrendingUp className="h-6 w-6 text-green-600 mb-2" />
            <h4 className="font-medium text-gray-900">Treatment Analytics</h4>
            <p className="text-sm text-gray-600">Success rates and outcomes analysis</p>
          </button>

          <button className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow text-left">
            <Calendar className="h-6 w-6 text-blue-600 mb-2" />
            <h4 className="font-medium text-gray-900">Monthly Summary</h4>
            <p className="text-sm text-gray-600">Complete monthly activity report</p>
          </button>

          <button className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow text-left">
            <Users className="h-6 w-6 text-purple-600 mb-2" />
            <h4 className="font-medium text-gray-900">Patient Feedback</h4>
            <p className="text-sm text-gray-600">Compiled feedback and ratings</p>
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <div className="bg-dashboard">
      {/* Header */}
      <header className="shadow-sm header-bg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-xl">आ</span>
                </div>
                <span className="ml-3 text-xl font-bold text-gray-900 dark:text-white">AyurSutra</span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-4 relative">
                <button
                  onClick={() => setIsNotificationOpen(!isNotificationOpen)}
                  className="p-2 hover:bg-gray-100 rounded-lg relative"
                >
                  <Bell className="h-5 w-5 text-gray-600" />
                  {notifications.filter(n => !n.read).length > 0 && (
                    <span className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white rounded-full text-xs flex items-center justify-center">
                      {notifications.filter(n => !n.read).length}
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

              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 rounded-full overflow-hidden border-2 border-primary-200 dark:border-primary-800">
                  <img
                    src={`https://api.dicebear.com/7.x/notionists/svg?seed=${encodeURIComponent('Dr. Priya Sharma')}&backgroundColor=e5e7eb`}
                    alt="User Avatar"
                    className="w-full h-full object-cover"
                  />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-900 dark:text-white">Dr. Priya Sharma</p>
                  <p className="text-xs text-gray-600 dark:text-gray-400">Practitioner</p>
                </div>
              </div>

              <button className="p-2 hover:bg-gray-100 rounded-lg">
                <Settings className="h-5 w-5 text-gray-600 dark:text-gray-400" />
              </button>

              <button
                onClick={handleLogout}
                className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg"
                title="Sign Out"
              >
                <LogOut className="h-5 w-5 text-gray-600 dark:text-gray-400" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="header-bg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', name: 'Overview', icon: TrendingUp },
              { id: 'patients', name: 'Patients', icon: Users },
              { id: 'reports', name: 'Reports', icon: FileText },
              { id: 'activities', name: 'Activities', icon: Bell }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setSelectedTab(tab.id)}
                className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-all ${selectedTab === tab.id
                  ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:border-gray-300 dark:hover:border-gray-600'
                  }`}
              >
                <tab.icon className="h-5 w-5" />
                <span>{tab.name}</span>
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {selectedTab === 'overview' && renderOverview()}
        {selectedTab === 'patients' && renderPatients()}
        {selectedTab === 'reports' && renderReports()}
        {selectedTab === 'activities' && renderActivities()}
      </main>

      {/* Update Modal */}
      {selectedPatient && (
        <PractitionerUpdateModal
          isOpen={isUpdateModalOpen}
          onClose={() => setIsUpdateModalOpen(false)}
          patientId={selectedPatient.id}
          patientName={selectedPatient.name}
        />
      )}
    </div>
  );
};

export default PractitionerDashboard;
