import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import {
  Users,
  UserCheck,
  Building2,
  TrendingUp,
  DollarSign,
  Calendar,
  Shield,
  Settings,
  Bell,
  Search,
  Filter,
  Plus,
  Edit,
  Trash2,
  Eye,
  MoreVertical,
  User,
  LogOut,
  AlertTriangle,
  CheckCircle,
  Clock,
  BarChart3,
  PieChart,
  Activity,
  FileText,
  Download
} from 'lucide-react';
import NotificationDropdown, { Notification } from '../components/NotificationDropdown';

const AdminConsole = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [selectedTab, setSelectedTab] = useState('dashboard');
  const [selectedTimeRange, setSelectedTimeRange] = useState('30d');
  const [isNotificationOpen, setIsNotificationOpen] = useState(false);
  const [notifications, setNotifications] = useState<Notification[]>([
    { id: 'AN1', type: 'alert', title: 'System Security Alert', message: 'Multiple failed login attempts from IP 192.168.1.1', time: '10 mins ago', read: false },
    { id: 'AN2', type: 'info', title: 'Backup Successful', message: 'Daily system backup completed successfully.', time: '1 hour ago', read: false },
    { id: 'AN3', type: 'reminder', title: 'License Renewal', message: 'Enterprise license for "Holistic Health" expires in 15 days.', time: '2 hours ago', read: true },
  ]);

  // Mock data
  const systemStats = {
    totalUsers: 1247,
    activePractitioners: 89,
    totalClinics: 45,
    monthlyRevenue: 125000,
    activePatients: 1158,
    completedTreatments: 2847
  };

  const recentActivities = [
    {
      id: 1,
      type: 'user_registration',
      message: 'New practitioner Dr. Amit Sharma registered',
      time: '2 hours ago',
      status: 'success'
    },
    {
      id: 2,
      type: 'system_alert',
      message: 'Server maintenance scheduled for tomorrow',
      time: '4 hours ago',
      status: 'warning'
    },
    {
      id: 3,
      type: 'payment',
      message: 'Payment of ₹25,000 received from Vedic Wellness Center',
      time: '6 hours ago',
      status: 'success'
    },
    {
      id: 4,
      type: 'support_ticket',
      message: 'Support ticket #1234 - Technical issue resolved',
      time: '1 day ago',
      status: 'info'
    }
  ];

  const practitioners = [
    {
      id: 1,
      name: 'Dr. Priya Sharma',
      email: 'priya.sharma@email.com',
      clinic: 'Vedic Wellness Center',
      patients: 34,
      joinedDate: '2023-06-15',
      status: 'active',
      revenue: 45000
    },
    {
      id: 2,
      name: 'Dr. Rajesh Kumar',
      email: 'rajesh.kumar@email.com',
      clinic: 'Ayush Healing Center',
      patients: 28,
      joinedDate: '2023-08-20',
      status: 'active',
      revenue: 38000
    },
    {
      id: 3,
      name: 'Dr. Meera Patel',
      email: 'meera.patel@email.com',
      clinic: 'Holistic Health Clinic',
      patients: 42,
      joinedDate: '2023-04-10',
      status: 'inactive',
      revenue: 52000
    }
  ];

  const clinics = [
    {
      id: 1,
      name: 'Vedic Wellness Center',
      location: 'Mumbai, Maharashtra',
      practitioners: 5,
      patients: 156,
      subscription: 'Premium',
      status: 'active',
      monthlyRevenue: 75000
    },
    {
      id: 2,
      name: 'Ayush Healing Center',
      location: 'Delhi, NCR',
      practitioners: 3,
      patients: 89,
      subscription: 'Standard',
      status: 'active',
      monthlyRevenue: 45000
    },
    {
      id: 3,
      name: 'Holistic Health Clinic',
      location: 'Bangalore, Karnataka',
      practitioners: 4,
      patients: 112,
      subscription: 'Premium',
      status: 'pending',
      monthlyRevenue: 60000
    }
  ];

  const handleLogout = () => {
    logout();
    navigate('/auth');
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
    setSelectedTab('logs');
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100';
      case 'inactive': return 'text-red-600 bg-red-100';
      case 'pending': return 'text-yellow-600 bg-yellow-100';
      case 'success': return 'text-green-600 bg-green-100';
      case 'warning': return 'text-yellow-600 bg-yellow-100';
      case 'info': return 'text-blue-600 bg-blue-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'user_registration': return <UserCheck className="h-4 w-4" />;
      case 'system_alert': return <AlertTriangle className="h-4 w-4" />;
      case 'payment': return <DollarSign className="h-4 w-4" />;
      case 'support_ticket': return <FileText className="h-4 w-4" />;
      default: return <Bell className="h-4 w-4" />;
    }
  };

  const renderDashboard = () => (
    <div className="space-y-6">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-blue-100 rounded-lg">
              <Users className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Users</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{systemStats.totalUsers.toLocaleString()}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-green-100 rounded-lg">
              <UserCheck className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Active Practitioners</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{systemStats.activePractitioners}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-purple-100 rounded-lg">
              <Building2 className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Clinics</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{systemStats.totalClinics}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-primary-100 rounded-lg">
              <Activity className="h-6 w-6 text-primary-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Active Patients</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{systemStats.activePatients.toLocaleString()}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-orange-100 rounded-lg">
              <CheckCircle className="h-6 w-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Completed Treatments</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{systemStats.completedTreatments.toLocaleString()}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-emerald-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-emerald-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Monthly Revenue</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">₹{(systemStats.monthlyRevenue / 1000)}K</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Revenue Chart */}
        <div className="lg:col-span-2 card">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Revenue Analytics</h3>
            <select
              value={selectedTimeRange}
              onChange={(e) => setSelectedTimeRange(e.target.value)}
              className="input-field text-sm w-auto"
            >
              <option value="7d">Last 7 days</option>
              <option value="30d">Last 30 days</option>
              <option value="90d">Last 90 days</option>
            </select>
          </div>

          <div className="h-64 flex items-center justify-center bg-gray-50 dark:bg-gray-800 rounded-lg">
            <div className="text-center">
              <BarChart3 className="h-16 w-16 text-gray-400 dark:text-gray-600 mx-auto mb-4" />
              <p className="text-gray-600 dark:text-gray-400">Revenue chart would be displayed here</p>
              <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">Integration with charting library needed</p>
            </div>
          </div>
        </div>

        {/* Recent Activities */}
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Recent Activities</h3>
            <button
              onClick={handleViewAllActivities}
              className="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 font-medium"
            >
              View All
            </button>
          </div>
          <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2">
            {recentActivities.map((activity) => (
              <div key={activity.id} className="flex items-start space-x-3 p-3 bg-gray-50 dark:bg-gray-900/50 rounded-lg border border-gray-100 dark:border-gray-800">
                <div className={`p-2 rounded-lg ${getStatusColor(activity.status)} text-white`}>
                  {getActivityIcon(activity.type)}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-900 dark:text-gray-200">{activity.message}</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{activity.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const renderPractitioners = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Practitioner Management</h2>
        <div className="flex space-x-3">
          <div className="relative">
            <Search className="h-5 w-5 text-gray-400 absolute left-3 top-3" />
            <input
              type="text"
              placeholder="Search practitioners..."
              className="input-field pl-10"
            />
          </div>
          <button className="btn-outline px-4 py-2">
            <Filter className="h-4 w-4 mr-2" /> Filter
          </button>
          <button className="btn-primary px-4 py-2">
            <Plus className="h-4 w-4 mr-2" /> Add Practitioner
          </button>
        </div>
      </div>

      <div className="card">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-700">
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Practitioner</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Clinic</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Patients</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Revenue</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Status</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Joined</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Actions</th>
              </tr>
            </thead>
            <tbody>
              {practitioners.map((practitioner) => (
                <tr key={practitioner.id} className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50">
                  <td className="py-4 px-4">
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white">{practitioner.name}</p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">{practitioner.email}</p>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <p className="text-gray-900 dark:text-gray-300">{practitioner.clinic}</p>
                  </td>
                  <td className="py-4 px-4">
                    <p className="font-medium text-gray-900 dark:text-white">{practitioner.patients}</p>
                  </td>
                  <td className="py-4 px-4">
                    <p className="font-medium text-gray-900 dark:text-white">₹{practitioner.revenue.toLocaleString()}</p>
                  </td>
                  <td className="py-4 px-4">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(practitioner.status)}`}>
                      {practitioner.status}
                    </span>
                  </td>
                  <td className="py-4 px-4">
                    <p className="text-gray-900 dark:text-gray-300">{new Date(practitioner.joinedDate).toLocaleDateString()}</p>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex space-x-2">
                      <button className="p-2 hover:bg-gray-100 rounded-lg">
                        <Eye className="h-4 w-4 text-gray-600" />
                      </button>
                      <button className="p-2 hover:bg-gray-100 rounded-lg">
                        <Edit className="h-4 w-4 text-gray-600" />
                      </button>
                      <button className="p-2 hover:bg-gray-100 rounded-lg">
                        <MoreVertical className="h-4 w-4 text-gray-600" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderClinics = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Clinic Management</h2>
        <div className="flex space-x-3">
          <div className="relative">
            <Search className="h-5 w-5 text-gray-400 absolute left-3 top-3" />
            <input
              type="text"
              placeholder="Search clinics..."
              className="input-field pl-10"
            />
          </div>
          <button className="btn-outline px-4 py-2">
            <Download className="h-4 w-4 mr-2" /> Export
          </button>
          <button className="btn-primary px-4 py-2">
            <Plus className="h-4 w-4 mr-2" /> Add Clinic
          </button>
        </div>
      </div>

      <div className="card">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-700">
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Clinic Name</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Location</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Practitioners</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Patients</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Subscription</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Revenue</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Status</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Actions</th>
              </tr>
            </thead>
            <tbody>
              {clinics.map((clinic) => (
                <tr key={clinic.id} className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50">
                  <td className="py-4 px-4">
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white">{clinic.name}</p>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <p className="text-gray-900 dark:text-gray-300">{clinic.location}</p>
                  </td>
                  <td className="py-4 px-4">
                    <p className="font-medium text-gray-900 dark:text-white">{clinic.practitioners}</p>
                  </td>
                  <td className="py-4 px-4">
                    <p className="font-medium text-gray-900 dark:text-white">{clinic.patients}</p>
                  </td>
                  <td className="py-4 px-4">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${clinic.subscription === 'Premium' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'
                      }`}>
                      {clinic.subscription}
                    </span>
                  </td>
                  <td className="py-4 px-4">
                    <p className="font-medium text-gray-900 dark:text-white">₹{clinic.monthlyRevenue.toLocaleString()}</p>
                  </td>
                  <td className="py-4 px-4">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(clinic.status)}`}>
                      {clinic.status}
                    </span>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex space-x-2">
                      <button className="p-2 hover:bg-gray-100 rounded-lg">
                        <Eye className="h-4 w-4 text-gray-600" />
                      </button>
                      <button className="p-2 hover:bg-gray-100 rounded-lg">
                        <Edit className="h-4 w-4 text-gray-600" />
                      </button>
                      <button className="p-2 hover:bg-gray-100 rounded-lg">
                        <MoreVertical className="h-4 w-4 text-gray-600" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderSettings = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white">System Settings</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">System Configuration</h3>
          <div className="space-y-4">
            <div className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-gray-900 dark:text-white">Email Notifications</h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400">System-wide email notification settings</p>
                </div>
                <button className="btn-outline px-4 py-2">Configure</button>
              </div>
            </div>

            <div className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-gray-900 dark:text-white">Security Settings</h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Password policies and security configurations</p>
                </div>
                <button className="btn-outline px-4 py-2">Manage</button>
              </div>
            </div>

            <div className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-gray-900 dark:text-white">Backup & Recovery</h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Data backup and recovery settings</p>
                </div>
                <button className="btn-outline px-4 py-2">Setup</button>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Integration Settings</h3>
          <div className="space-y-4">
            <div className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-gray-900 dark:text-white">Payment Gateway</h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Configure payment processing settings</p>
                </div>
                <span className="px-3 py-1 bg-green-100 dark:bg-green-900/40 text-green-800 dark:text-green-400 rounded-full text-sm">Active</span>
              </div>
            </div>

            <div className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-gray-900 dark:text-white">SMS Service</h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400">SMS notification service configuration</p>
                </div>
                <span className="px-3 py-1 bg-green-100 dark:bg-green-900/40 text-green-800 dark:text-green-400 rounded-full text-sm">Active</span>
              </div>
            </div>

            <div className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-gray-900 dark:text-white">Analytics</h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Third-party analytics integration</p>
                </div>
                <span className="px-3 py-1 bg-yellow-100 dark:bg-yellow-900/40 text-yellow-800 dark:text-yellow-400 rounded-full text-sm">Pending</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderLogs = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">System Logs & Activities</h2>
        <div className="flex space-x-3">
          <button className="btn-outline px-4 py-2">
            <Download className="h-4 w-4 mr-2" /> Export Logs
          </button>
          <button className="btn-primary px-4 py-2">
            <Filter className="h-4 w-4 mr-2" /> Filter
          </button>
        </div>
      </div>

      <div className="card">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-700">
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Time</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Type</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Activity</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 dark:divide-gray-800">
              {[...recentActivities, ...recentActivities].map((activity, idx) => (
                <tr key={`${activity.id}-${idx}`} className="hover:bg-gray-50 dark:hover:bg-gray-800/50">
                  <td className="py-4 px-4 text-sm text-gray-600 dark:text-gray-400">{activity.time}</td>
                  <td className="py-4 px-4 text-sm font-medium text-gray-900 dark:text-white uppercase tracking-wider">{activity.type.replace('_', ' ')}</td>
                  <td className="py-4 px-4 text-sm text-gray-900 dark:text-gray-300">{activity.message}</td>
                  <td className="py-4 px-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(activity.status)}`}>
                      {activity.status.toUpperCase()}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
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
              <Link to="/admin" className="flex-shrink-0 flex items-center">
                <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-xl">आ</span>
                </div>
                <span className="ml-3 text-xl font-bold text-gray-900 dark:text-white">AyurSutra Admin</span>
              </Link>
            </div>

            <div className="flex items-center space-x-4 relative">
              <button
                onClick={() => setIsNotificationOpen(!isNotificationOpen)}
                className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg relative"
              >
                <Bell className="h-5 w-5 text-gray-600 dark:text-gray-400" />
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

              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-primary-100 dark:bg-primary-900/40 rounded-full flex items-center justify-center">
                  <Shield className="h-5 w-5 text-primary-600 dark:text-primary-400" />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-900 dark:text-white">System Admin</p>
                  <p className="text-xs text-gray-600 dark:text-gray-400">Administrator</p>
                </div>
              </div>

              <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg">
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
              { id: 'dashboard', name: 'Dashboard', icon: TrendingUp },
              { id: 'practitioners', name: 'Practitioners', icon: UserCheck },
              { id: 'clinics', name: 'Clinics', icon: Building2 },
              { id: 'logs', name: 'Logs', icon: FileText },
              { id: 'settings', name: 'Settings', icon: Settings }
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
        {selectedTab === 'dashboard' && renderDashboard()}
        {selectedTab === 'practitioners' && renderPractitioners()}
        {selectedTab === 'clinics' && renderClinics()}
        {selectedTab === 'logs' && renderLogs()}
        {selectedTab === 'settings' && renderSettings()}
      </main>
    </div>
  );
};

export default AdminConsole;
