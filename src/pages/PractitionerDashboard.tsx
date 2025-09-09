import React, { useState } from 'react';
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
  LogOut
} from 'lucide-react';

const PractitionerDashboard = () => {
  const [selectedTab, setSelectedTab] = useState('overview');
  const [selectedPatient, setSelectedPatient] = useState(null);

  // Mock data
  const todayStats = {
    totalPatients: 24,
    todayAppointments: 8,
    activeTherapies: 12,
    pendingReports: 3
  };

  const todayAppointments = [
    {
      id: 1,
      patient: 'Rajesh Kumar',
      time: '9:00 AM',
      therapy: 'Abhyanga',
      status: 'upcoming',
      duration: '90 min'
    },
    {
      id: 2,
      patient: 'Priya Sharma',
      time: '11:00 AM',
      therapy: 'Virechana',
      status: 'in-progress',
      duration: '120 min'
    },
    {
      id: 3,
      patient: 'Amit Singh',
      time: '2:00 PM',
      therapy: 'Nasya',
      status: 'upcoming',
      duration: '60 min'
    },
    {
      id: 4,
      patient: 'Sunita Devi',
      time: '4:00 PM',
      therapy: 'Shirodhara',
      status: 'upcoming',
      duration: '75 min'
    }
  ];

  const allPatients = [
    {
      id: 1,
      name: 'Rajesh Kumar',
      age: 45,
      gender: 'Male',
      phone: '+91 98765 43210',
      email: 'rajesh.k@email.com',
      currentTherapy: 'Panchakarma',
      stage: 'Purvakarma',
      nextAppointment: '2024-01-15',
      status: 'active',
      prakriti: 'Vata-Pitta'
    },
    {
      id: 2,
      name: 'Priya Sharma',
      age: 38,
      gender: 'Female',
      phone: '+91 87654 32109',
      email: 'priya.s@email.com',
      currentTherapy: 'Virechana',
      stage: 'Pradhanakarma',
      nextAppointment: '2024-01-16',
      status: 'active',
      prakriti: 'Pitta-Kapha'
    },
    {
      id: 3,
      name: 'Amit Singh',
      age: 52,
      gender: 'Male',
      phone: '+91 76543 21098',
      email: 'amit.s@email.com',
      currentTherapy: 'Nasya',
      stage: 'Paschatkarma',
      nextAppointment: '2024-01-17',
      status: 'completed',
      prakriti: 'Vata-Kapha'
    }
  ];

  const recentAlerts = [
    {
      id: 1,
      type: 'warning',
      message: 'Patient Rajesh Kumar missed yesterday\'s appointment',
      time: '2 hours ago'
    },
    {
      id: 2,
      type: 'info',
      message: 'New patient registration: Sunita Devi',
      time: '4 hours ago'
    },
    {
      id: 3,
      type: 'success',
      message: 'Priya Sharma completed Virechana therapy successfully',
      time: '1 day ago'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'upcoming': return 'text-blue-600 bg-blue-100';
      case 'in-progress': return 'text-green-600 bg-green-100';
      case 'completed': return 'text-gray-600 bg-gray-100';
      case 'active': return 'text-primary-600 bg-primary-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

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
              <p className="text-2xl font-bold text-gray-900">{todayStats.totalPatients}</p>
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
              <p className="text-2xl font-bold text-gray-900">{todayStats.todayAppointments}</p>
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
              <p className="text-2xl font-bold text-gray-900">{todayStats.activeTherapies}</p>
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
              <p className="text-2xl font-bold text-gray-900">{todayStats.pendingReports}</p>
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
            {todayAppointments.map((appointment) => (
              <div key={appointment.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
                <div className="flex items-center space-x-4">
                  <div className="text-center">
                    <p className="text-sm font-medium text-gray-900">{appointment.time}</p>
                    <p className="text-xs text-gray-500">{appointment.duration}</p>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{appointment.patient}</p>
                    <p className="text-sm text-gray-600">{appointment.therapy}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(appointment.status)}`}>
                    {appointment.status.replace('-', ' ')}
                  </span>
                  <button className="p-2 hover:bg-gray-100 rounded-lg">
                    <MoreVertical className="h-4 w-4 text-gray-600" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Alerts */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Recent Alerts</h3>
          <div className="space-y-4">
            {recentAlerts.map((alert) => (
              <div key={alert.id} className="flex items-start space-x-3">
                <div className={`p-2 rounded-lg ${
                  alert.type === 'warning' ? 'bg-yellow-100' :
                  alert.type === 'info' ? 'bg-blue-100' : 'bg-green-100'
                }`}>
                  {alert.type === 'warning' ? (
                    <AlertCircle className="h-4 w-4 text-yellow-600" />
                  ) : alert.type === 'info' ? (
                    <Bell className="h-4 w-4 text-blue-600" />
                  ) : (
                    <CheckCircle className="h-4 w-4 text-green-600" />
                  )}
                </div>
                <div className="flex-1">
                  <p className="text-sm text-gray-900">{alert.message}</p>
                  <p className="text-xs text-gray-500 mt-1">{alert.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const renderPatients = () => (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Patient Management</h2>
        <div className="flex space-x-3">
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
              {allPatients.map((patient) => (
                <tr key={patient.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-4 px-4">
                    <div>
                      <p className="font-medium text-gray-900">{patient.name}</p>
                      <p className="text-sm text-gray-600">{patient.age}yr, {patient.gender} • {patient.prakriti}</p>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <p className="font-medium text-gray-900">{patient.currentTherapy}</p>
                  </td>
                  <td className="py-4 px-4">
                    <span className="px-3 py-1 bg-primary-100 text-primary-800 rounded-full text-sm">
                      {patient.stage}
                    </span>
                  </td>
                  <td className="py-4 px-4">
                    <p className="text-gray-900">{patient.nextAppointment}</p>
                  </td>
                  <td className="py-4 px-4">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(patient.status)}`}>
                      {patient.status}
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

  const renderReports = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Reports & Analytics</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="card text-center">
          <TrendingUp className="h-12 w-12 text-primary-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Treatment Success Rate</h3>
          <p className="text-3xl font-bold text-primary-600 mb-2">94.5%</p>
          <p className="text-sm text-gray-600">Last 30 days</p>
        </div>
        
        <div className="card text-center">
          <Users className="h-12 w-12 text-green-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Patient Satisfaction</h3>
          <p className="text-3xl font-bold text-green-600 mb-2">4.8/5</p>
          <p className="text-sm text-gray-600">Average rating</p>
        </div>
        
        <div className="card text-center">
          <Calendar className="h-12 w-12 text-blue-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Monthly Treatments</h3>
          <p className="text-3xl font-bold text-blue-600 mb-2">156</p>
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
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-xl">आ</span>
                </div>
                <span className="ml-3 text-xl font-bold text-gray-900">AyurSutra</span>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <button className="p-2 hover:bg-gray-100 rounded-lg relative">
                <Bell className="h-5 w-5 text-gray-600" />
                <span className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white rounded-full text-xs flex items-center justify-center">3</span>
              </button>
              
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                  <User className="h-5 w-5 text-primary-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-900">Dr. Priya Sharma</p>
                  <p className="text-xs text-gray-600">Practitioner</p>
                </div>
              </div>
              
              <button className="p-2 hover:bg-gray-100 rounded-lg">
                <Settings className="h-5 w-5 text-gray-600" />
              </button>
              
              <button className="p-2 hover:bg-gray-100 rounded-lg">
                <LogOut className="h-5 w-5 text-gray-600" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', name: 'Overview', icon: TrendingUp },
              { id: 'patients', name: 'Patients', icon: Users },
              { id: 'reports', name: 'Reports', icon: FileText }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setSelectedTab(tab.id)}
                className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm ${
                  selectedTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
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
      </main>
    </div>
  );
};

export default PractitionerDashboard;
