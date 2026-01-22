import { useState, useEffect } from 'react';
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
  Download,
  Database,
  History
} from 'lucide-react';
import NotificationDropdown, { Notification } from '../components/NotificationDropdown';
import HistoryModal from '../components/admin/HistoryModal';

const AdminConsole = () => {
  const { logout, login } = useAuth(); // Assuming login function is available in useAuth for impersonation token handling
  const navigate = useNavigate();
  const [selectedTab, setSelectedTab] = useState('dashboard');
  const [selectedTimeRange, setSelectedTimeRange] = useState('30d');
  const [isNotificationOpen, setIsNotificationOpen] = useState(false);
  const [notifications, setNotifications] = useState<Notification[]>([]);

  // Real Data State
  const [dashboardStats, setDashboardStats] = useState<any>(null);
  const [users, setUsers] = useState<any[]>([]);
  const [logs, setLogs] = useState<any[]>([]);
  const [clinics, setClinics] = useState<any[]>([]); // Real clinics data
  const [settings, setSettings] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [userFilter, setUserFilter] = useState<string>('all');
  const [statusFilter, setStatusFilter] = useState<string>('all');

  // Modal State
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const [selectedUserId, setSelectedUserId] = useState<number | null>(null);

  // Fetch Dashboard Data
  useEffect(() => {
    if (selectedTab === 'dashboard') {
      fetchDashboard();
    } else if (selectedTab === 'users' || selectedTab === 'practitioners') {
      fetchUsers();
    } else if (selectedTab === 'clinics') {
      fetchClinics(); // Fetch real clinics
    } else if (selectedTab === 'logs') {
      fetchLogs();
    } else if (selectedTab === 'settings') {
      fetchSettings();
    }
  }, [selectedTab]);

  const fetchDashboard = async () => {
    try {
      const token = localStorage.getItem('token') || localStorage.getItem('access_token');
      console.log('[DEBUG] Fetching dashboard with token:', token ? 'Token exists' : 'No token');
      const response = await fetch('http://localhost:8002/admin/dashboard', {
        headers: { Authorization: `Bearer ${token}` }
      });
      console.log('[DEBUG] Dashboard response status:', response.status);
      if (response.ok) {
        const data = await response.json();
        console.log('[DEBUG] Dashboard data received:', data);
        setDashboardStats(data);
        console.log('[DEBUG] Dashboard stats set successfully');
      } else {
        console.error('[DEBUG] Dashboard fetch failed:', response.status, await response.text());
      }
    } catch (error) {
      console.error("Error fetching dashboard:", error);
    }
  };

  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem('token') || localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8002/admin/users?limit=100', {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setUsers(data);
      }
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  };

  const fetchLogs = async () => {
    try {
      const token = localStorage.getItem('token') || localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8002/admin/audit-logs', {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setLogs(data);
      }
    } catch (error) {
      console.error("Error fetching logs:", error);
    }
  };

  const fetchClinics = async () => {
    try {
      const token = localStorage.getItem('token') || localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8002/admin/clinics', {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setClinics(data);
      }
    } catch (error) {
      console.error("Error fetching clinics:", error);
    }
  };

  const fetchSettings = async () => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token') || localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8002/admin/settings', {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setSettings(data);
      } else {
        setError(`Failed to load settings: ${response.statusText}`);
        if (response.status === 401 || response.status === 403) {
          // Optionally redirect to login or show specific auth error
          setError("Session expired or unauthorized. Please login again.");
        }
      }
    } catch (error) {
      console.error("Error fetching settings:", error);
      setError("Network error. Please check backend connection.");
    } finally {
      setLoading(false);
    }
  };

  const updateSetting = async (key: string, newValue: any) => {
    try {
      const token = localStorage.getItem('token') || localStorage.getItem('access_token');
      const response = await fetch(`http://localhost:8002/admin/settings?key=${key}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ value: newValue })
      });
      if (response.ok) {
        alert("Setting updated");
        fetchSettings();
      }
    } catch (error) {
      console.error("Error updating setting:", error);
    }
  };

  const handleViewHistory = (userId: number) => {
    setSelectedUserId(userId);
    setIsHistoryOpen(true);
  };

  const handleImpersonate = async (userId: number) => {
    if (!window.confirm("Are you sure you want to login as this user?")) return;

    try {
      const token = localStorage.getItem('token') || localStorage.getItem('access_token');
      const response = await fetch(`http://localhost:8002/admin/impersonate/${userId}`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        // Use the new token to login
        // We might need to manually set token and reload or use context
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('user', JSON.stringify({
          id: data.user_id,
          role: data.role,
          full_name: data.full_name
        }));
        // Navigate to appropriate dashboard
        if (data.role === 'patient') navigate('/patient-dashboard');
        else if (data.role === 'practitioner') navigate('/practitioner-dashboard');
        else window.location.reload();
      } else {
        alert("Impersonation failed");
      }
    } catch (error) {
      console.error("Impersonation error:", error);
      alert("Error during impersonation");
    }
  };

  const handleDeactivate = async (userId: number) => {
    if (!window.confirm("Are you sure you want to deactivate this user?")) return;
    try {
      const token = localStorage.getItem('token') || localStorage.getItem('access_token');
      const response = await fetch(`http://localhost:8002/admin/users/${userId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        alert("User deactivated");
        fetchUsers();
      } else {
        alert("Failed to deactivate");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };



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

  // Mock data for initial render or fallback (could be removed if confident)
  // const practitioners = ... (Removed)
  // const clinics = ... (Removed)

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
        <div className="card cursor-pointer hover:shadow-lg transition-shadow" onClick={() => { setSelectedTab('users'); setUserFilter('all'); setStatusFilter('all'); }}>
          <div className="flex items-center">
            <div className="p-3 bg-blue-100 rounded-lg">
              <Users className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Users</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{dashboardStats?.total_users?.toLocaleString() || 0}</p>
            </div>
          </div>
        </div>

        <div className="card cursor-pointer hover:shadow-lg transition-shadow" onClick={() => { setSelectedTab('users'); setUserFilter('practitioner'); setStatusFilter('active'); }}>
          <div className="flex items-center">
            <div className="p-3 bg-green-100 rounded-lg">
              <UserCheck className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Active Practitioners</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{dashboardStats?.total_practitioners || 0}</p>
            </div>
          </div>
        </div>

        <div className="card cursor-pointer hover:shadow-lg transition-shadow" onClick={() => setSelectedTab('clinics')}>
          <div className="flex items-center">
            <div className="p-3 bg-purple-100 rounded-lg">
              <Building2 className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Clinics</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{dashboardStats?.total_clinics || 0}</p>
            </div>
          </div>
        </div>

        <div className="card cursor-pointer hover:shadow-lg transition-shadow" onClick={() => { setSelectedTab('users'); setUserFilter('patient'); setStatusFilter('active'); }}>
          <div className="flex items-center">
            <div className="p-3 bg-primary-100 rounded-lg">
              <Activity className="h-6 w-6 text-primary-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Active Patients</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{dashboardStats?.total_patients?.toLocaleString() || 0}</p>
            </div>
          </div>
        </div>

        <div className="card cursor-pointer hover:shadow-lg transition-shadow" onClick={() => setSelectedTab('logs')}>
          <div className="flex items-center">
            <div className="p-3 bg-orange-100 rounded-lg">
              <CheckCircle className="h-6 w-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Completed Treatments</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{dashboardStats?.total_appointments?.toLocaleString() || 0}</p>
            </div>
          </div>
        </div>

        <div className="card cursor-pointer hover:shadow-lg transition-shadow" onClick={() => setSelectedTab('dashboard')}>
          <div className="flex items-center">
            <div className="p-3 bg-emerald-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-emerald-600" />
            </div>
            <div className="ml-4">
              <p className="text-2xl font-bold text-gray-900 dark:text-white">₹{(dashboardStats?.total_appointments * 1500 / 1000) || 0}K</p>
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

  const renderUsers = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">User Management</h2>
        <div className="flex space-x-3">
          <div className="relative">
            <Search className="h-5 w-5 text-gray-400 absolute left-3 top-3" />
            <input
              type="text"
              placeholder="Search users..."
              className="input-field pl-10"
            />
          </div>
          <div className="flex items-center space-x-2 bg-white dark:bg-gray-800 rounded-lg p-1 border border-gray-200 dark:border-gray-700">
            <button
              onClick={() => setStatusFilter('all')}
              className={`px-3 py-1 text-sm rounded-md transition-colors ${statusFilter === 'all' ? 'bg-gray-100 text-gray-900 font-medium' : 'text-gray-500 hover:text-gray-700'}`}
            >
              All
            </button>
            <button
              onClick={() => setStatusFilter('active')}
              className={`px-3 py-1 text-sm rounded-md transition-colors ${statusFilter === 'active' ? 'bg-green-50 text-green-700 font-medium' : 'text-gray-500 hover:text-gray-700'}`}
            >
              Online Now
            </button>
          </div>
          <button className="btn-primary px-4 py-2">
            <Plus className="h-4 w-4 mr-2" /> Add User
          </button>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex space-x-4 border-b border-gray-200 dark:border-gray-700">
        {[
          { id: 'all', label: 'All Users' },
          { id: 'practitioner', label: 'Practitioners' },
          { id: 'patient', label: 'Patients' },
          { id: 'admin', label: 'Admins' }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setUserFilter(tab.id)}
            className={`py-2 px-4 border-b-2 font-medium text-sm transition-all ${userFilter === tab.id
              ? 'border-primary-500 text-primary-600 dark:text-primary-400'
              : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="card">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-700">
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">User</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Role</th>
                {userFilter === 'practitioner' && <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Clinic</th>}
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Status</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Joined</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Actions</th>
              </tr>
            </thead>
            <tbody>
              {users
                .filter(u => userFilter === 'all' || u.role.toLowerCase() === userFilter.toLowerCase())
                .filter(u => {
                  if (statusFilter === 'all') return true;
                  if (statusFilter === 'active') {
                    // Check if user logged in within last 15 minutes (currently online)
                    if (!u.last_login) return false;
                    const lastLogin = new Date(u.last_login);
                    const now = new Date();
                    const diffMinutes = (now.getTime() - lastLogin.getTime()) / (1000 * 60);
                    return diffMinutes <= 15; // Online if logged in within last 15 minutes
                  }
                  return true;
                })
                .map((user) => (
                  <tr key={user.id} className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50">
                    <td className="py-4 px-4">
                      <div>
                        <p className="font-medium text-gray-900 dark:text-white">{user.full_name}</p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">{user.email}</p>
                      </div>
                    </td>
                    <td className="py-4 px-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium uppercase
                          ${user.role.toLowerCase() === 'admin' ? 'bg-purple-100 text-purple-600' :
                          user.role.toLowerCase() === 'practitioner' ? 'bg-blue-100 text-blue-600' : 'bg-green-100 text-green-600'}
                      `}>
                        {user.role}
                      </span>
                    </td>
                    {userFilter === 'practitioner' && (
                      <td className="py-4 px-4">
                        <p className="text-gray-900 dark:text-gray-300">
                          {user.practitioner_profile?.clinic_name || '-'}
                        </p>
                      </td>
                    )}
                    <td className="py-4 px-4">
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${user.is_active ? 'text-green-600 bg-green-100' : 'text-red-600 bg-red-100'}`}>
                        {user.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="py-4 px-4">
                      <p className="text-gray-900 dark:text-gray-300">{new Date(user.created_at).toLocaleDateString()}</p>
                    </td>
                    <td className="py-4 px-4">
                      <div className="flex space-x-2">
                        <button className="p-2 hover:bg-gray-100 rounded-lg" title="Login As" onClick={() => handleImpersonate(user.id)}>
                          <LogOut className="h-4 w-4 text-blue-600" />
                        </button>
                        <button className="p-2 hover:bg-gray-100 rounded-lg" title="View History" onClick={() => handleViewHistory(user.id)}>
                          <History className="h-4 w-4 text-gray-600" />
                        </button>
                        <button className="p-2 hover:bg-gray-100 rounded-lg" onClick={() => handleDeactivate(user.id)}>
                          <Trash2 className="h-4 w-4 text-red-600" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              {users.filter(u => {
                const roleMatch = userFilter === 'all' || u.role.toLowerCase() === userFilter.toLowerCase();
                if (!roleMatch) return false;
                if (statusFilter === 'all') return true;
                if (statusFilter === 'active') {
                  if (!u.last_login) return false;
                  const lastLogin = new Date(u.last_login);
                  const now = new Date();
                  const diffMinutes = (now.getTime() - lastLogin.getTime()) / (1000 * 60);
                  return diffMinutes <= 15;
                }
                return true;
              }).length === 0 && (
                  <tr>
                    <td colSpan={6} className="text-center py-8 text-gray-500">No users found.</td>
                  </tr>
                )}
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
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Revenue</th>
                <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Status</th>
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
                    <p className="font-medium text-gray-900 dark:text-white">₹{clinic.monthly_revenue.toLocaleString()}</p>
                  </td>
                  <td className="py-4 px-4">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(clinic.status)}`}>
                      {clinic.status}
                    </span>
                  </td>
                </tr>
              ))}
              {clinics.length === 0 && (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-gray-500">No clinics data available.</td>
                </tr>
              )}
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
        {error && (
          <div className="col-span-1 lg:col-span-2 p-4 bg-red-50 text-red-600 rounded-lg border border-red-200">
            {error}
          </div>
        )}

        {settings.map((setting) => (
          <div key={setting.key} className="card overflow-hidden">
            <div className="bg-gray-50 dark:bg-gray-800/50 px-6 py-4 border-b border-gray-100 dark:border-gray-700">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white capitalize flex items-center">
                {setting.category === 'notifications' && <Bell className="w-5 h-5 mr-2 text-primary-500" />}
                {setting.category === 'security' && <Shield className="w-5 h-5 mr-2 text-primary-500" />}
                {setting.category === 'backup' && <Database className="w-5 h-5 mr-2 text-primary-500" />}
                {setting.category} Settings
              </h3>
            </div>

            <div className="p-6 space-y-6">
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="font-medium text-gray-900 dark:text-white text-lg mb-1">
                    {setting.key.split('_').map((w: string) => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                  </h4>
                  <p className="text-sm text-gray-500 dark:text-gray-400 max-w-md">
                    {setting.description}
                  </p>
                </div>
                {/* Main Toggle if 'enabled' exists */}
                {typeof setting.value.enabled === 'boolean' && (
                  <button
                    onClick={() => updateSetting(setting.key, { ...setting.value, enabled: !setting.value.enabled })}
                    className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none ${setting.value.enabled ? 'bg-primary-600' : 'bg-gray-200 dark:bg-gray-700'
                      }`}
                  >
                    <span
                      className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${setting.value.enabled ? 'translate-x-5' : 'translate-x-0'
                        }`}
                    />
                  </button>
                )}
              </div>

              {/* Render other fields */}
              <div className="space-y-4 pt-4 border-t border-gray-100 dark:border-gray-700">
                {Object.entries(setting.value).map(([key, value]) => {
                  if (key === 'enabled') return null; // Already handled above

                  return (
                    <div key={key} className="grid grid-cols-1 sm:grid-cols-3 gap-4 items-center">
                      <label className="text-sm font-medium text-gray-700 dark:text-gray-300 capitalize sm:col-span-1">
                        {key.replace(/_/g, ' ')}
                      </label>
                      <div className="sm:col-span-2">
                        {typeof value === 'boolean' ? (
                          <button
                            onClick={() => updateSetting(setting.key, { ...setting.value, [key]: !value })}
                            className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none ${value ? 'bg-primary-600' : 'bg-gray-200 dark:bg-gray-700'
                              }`}
                          >
                            <span
                              className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${value ? 'translate-x-5' : 'translate-x-0'
                                }`}
                            />
                          </button>
                        ) : (
                          <input
                            type={typeof value === 'number' ? 'number' : 'text'}
                            value={value as string | number}
                            onChange={(e) => {
                              const val = typeof value === 'number' ? parseFloat(e.target.value) : e.target.value;
                              updateSetting(setting.key, { ...setting.value, [key]: val });
                            }}
                            className="input-field w-full text-sm py-1.5"
                          />
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        ))}
        {!loading && settings.length === 0 && !error && (
          <p className="text-center col-span-2 text-gray-500">No settings found.</p>
        )}
        {loading && (
          <div className="col-span-2 flex justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            <span className="ml-2 text-gray-500">Loading settings...</span>
          </div>
        )}
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
              {logs.map((activity, idx) => (
                <tr key={`${activity.id}-${idx}`} className="hover:bg-gray-50 dark:hover:bg-gray-800/50">
                  <td className="py-4 px-4 text-sm text-gray-600 dark:text-gray-400">{new Date(activity.created_at).toLocaleString()}</td>
                  <td className="py-4 px-4 text-sm font-medium text-gray-900 dark:text-white uppercase tracking-wider">{activity.action.replace('_', ' ')}</td>
                  <td className="py-4 px-4 text-sm text-gray-900 dark:text-gray-300">{JSON.stringify(activity.details)}</td>
                  <td className="py-4 px-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium text-gray-600 bg-gray-100`}>
                      LOG
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

              <button
                onClick={() => setSelectedTab('settings')}
                className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg"
              >
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
              { id: 'users', name: 'User Management', icon: Users },
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
        {selectedTab === 'users' && renderUsers()}
        {selectedTab === 'clinics' && renderClinics()}
        {selectedTab === 'logs' && renderLogs()}
        {selectedTab === 'settings' && renderSettings()}
      </main>
      {/* Modal */}
      <HistoryModal
        userId={selectedUserId}
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
      />
    </div>
  );
};

export default AdminConsole;
