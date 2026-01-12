import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import WelcomeIntro from './components/WelcomeIntro';
import LandingPage from './pages/LandingPage';
import SimpleAuthPage from './pages/SimpleAuthPage';
import PatientDashboard from './pages/PatientDashboard';
import PractitionerDashboard from './pages/PractitionerDashboard';
import Scheduler from './pages/Scheduler';
import TherapyRoom from './pages/TherapyRoom';
import AdminConsole from './pages/AdminConsole';
import Settings from './pages/Settings';
import DebugAuth from './components/DebugAuth';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            <Route path="/" element={<WelcomeIntro />} />
            <Route path="/home" element={<LandingPage />} />
            <Route path="/auth" element={<SimpleAuthPage />} />
            <Route path="/patient" element={<PatientDashboard />} />
            <Route path="/practitioner" element={<PractitionerDashboard />} />
            <Route path="/scheduler" element={<Scheduler />} />
            <Route path="/therapy-room/:sessionId" element={<TherapyRoom />} />
            <Route path="/admin" element={<AdminConsole />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/debug" element={<DebugAuth />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
