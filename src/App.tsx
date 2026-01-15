import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import WelcomeIntro from './components/WelcomeIntro';
import LandingPage from './pages/LandingPage';
import SimpleAuthPage from './pages/SimpleAuthPage';
import PatientDashboard from './pages/PatientDashboard';
import MySessions from './pages/MySessions';
import Progress from './pages/Progress';
import PractitionerDashboard from './pages/PractitionerDashboard';
import Scheduler from './pages/Scheduler';
import TherapyRoom from './pages/TherapyRoom';
import AdminConsole from './pages/AdminConsole';
import Settings from './pages/Settings';
import HealthSupport from './pages/HealthSupport';
import ChatSupport from './pages/ChatSupport';
import DebugAuth from './components/DebugAuth';
import ClinicMap from './pages/ClinicMap';
import AIAssistant from './components/AIAssistant';
import './App.css';

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <div className="min-h-screen bg-dashboard">
            <Routes>
              <Route path="/" element={<WelcomeIntro />} />
              <Route path="/home" element={<LandingPage />} />
              <Route path="/auth" element={<SimpleAuthPage />} />
              <Route path="/patient" element={<PatientDashboard />} />
              <Route path="/my-sessions" element={<MySessions />} />
              <Route path="/progress" element={<Progress />} />
              <Route path="/practitioner" element={<PractitionerDashboard />} />
              <Route path="/scheduler" element={<Scheduler />} />
              <Route path="/therapy-room/:sessionId" element={<TherapyRoom />} />
              <Route path="/admin" element={<AdminConsole />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="/health-support" element={<HealthSupport />} />
              <Route path="/chat-support" element={<ChatSupport />} />
              <Route path="/map" element={<ClinicMap />} />
              <Route path="/debug" element={<DebugAuth />} />

              {/* Redirects for legacy or missing routes */}
              <Route path="/dashboard" element={<Navigate to="/patient" replace />} />
              <Route path="/appointments" element={<Navigate to="/my-sessions" replace />} />
            </Routes>
            <AIAssistant />
          </div>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
