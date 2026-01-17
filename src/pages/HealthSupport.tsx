import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useSubscription } from '../contexts/SubscriptionContext';
import { useNavigate } from 'react-router-dom';
import {
    Activity,
    AlertCircle,
    Calendar,
    CheckCircle,
    Heart,
    Home,
    Loader,
    MessageCircle,
    Plus,
    Send,
    Settings,
    Sparkles,
    TrendingUp,
    User,
    Lock
} from 'lucide-react';
import Sidebar from '../components/Sidebar';
import api from '../services/api';
import NotificationDropdown, { Notification } from '../components/NotificationDropdown';
import { Bell } from 'lucide-react';

interface Symptom {
    id: number;
    symptom_name: string;
    severity: string;
    notes?: string;
    duration_days?: number;
    created_at: string;
}

interface Recommendation {
    category: string;
    suggestion: string;
    reason: string;
    priority: string;
}

interface ChatMessage {
    role: 'user' | 'assistant';
    content: string;
    timestamp: string;
}

const HealthSupport = () => {
    const { user, logout } = useAuth();
    const { subscription, upgradeToPremium, isLoading: subLoading, activateTrial } = useSubscription();
    const navigate = useNavigate();

    // State
    const [activeTab, setActiveTab] = useState<'symptoms' | 'ai-chat' | 'recommendations'>('symptoms');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

    // Symptom logging state
    const [symptomForm, setSymptomForm] = useState({
        symptom_name: '',
        severity: 'moderate',
        notes: '',
        duration_days: 1
    });
    const [symptoms, setSymptoms] = useState<Symptom[]>([]);

    // AI chat state
    const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
    const [chatInput, setChatInput] = useState('');
    const [conversationId, setConversationId] = useState<string | null>(null);

    // Recommendations state
    const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
    const [doshaAnalysis, setDoshaAnalysis] = useState<any>(null);
    const [isNotificationOpen, setIsNotificationOpen] = useState(false);
    const [notificationsList, setNotificationsList] = useState<Notification[]>([
        { id: 'HN1', type: 'appointment', title: 'Consultation Tomorrow', message: 'Reminder: Your session with Dr. Priya is tomorrow at 10 AM.', time: '2 hours ago', read: false },
        { id: 'HN2', type: 'info', title: 'Health Tip', message: 'Check out your new Ayurvedic recommendations!', time: '1 day ago', read: true },
    ]);

    // Sidebar items
    const sidebarItems = [
        { icon: Home, label: 'Dashboard', path: '/dashboard' },
        { icon: Calendar, label: 'Appointments', path: '/appointments' },
        { icon: Activity, label: 'My Progress', path: '/progress' },
        { icon: Heart, label: 'Health Support', path: '/health-support' },
        { icon: MessageCircle, label: 'Chat Support', path: '/chat-support' },
        { icon: Settings, label: 'Settings', path: '/settings' }
    ];

    const handleLogout = () => {
        logout();
        navigate('/auth');
    };

    // Fetch data on mount
    useEffect(() => {
        fetchSymptoms();
        fetchRecommendations();
    }, []);

    const fetchSymptoms = async () => {
        try {
            const response = await api.get('/health/symptoms?limit=10');
            setSymptoms(response.data);
        } catch (error) {
            console.error('Failed to fetch symptoms:', error);
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

    const fetchRecommendations = async () => {
        try {
            const response = await api.get('/health/recommendations');
            setRecommendations(response.data.recommendations);
            setDoshaAnalysis(response.data.dosha_analysis);
        } catch (error) {
            console.error('Failed to fetch recommendations:', error);
        }
    };

    const handleSymptomSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setMessage(null);

        try {
            await api.post('/health/symptoms', symptomForm);
            setMessage({ type: 'success', text: 'Symptom logged successfully!' });
            setSymptomForm({
                symptom_name: '',
                severity: 'moderate',
                notes: '',
                duration_days: 1
            });
            fetchSymptoms();
            fetchRecommendations(); // Refresh recommendations
        } catch (error) {
            console.error(error);
            setMessage({ type: 'error', text: 'Failed to log symptom.' });
        } finally {
            setLoading(false);
        }
    };

    const handleAIChat = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!chatInput.trim()) return;

        const userMessage: ChatMessage = {
            role: 'user',
            content: chatInput,
            timestamp: new Date().toISOString()
        };

        setChatMessages(prev => [...prev, userMessage]);
        setChatInput('');
        setLoading(true);

        try {
            const response = await api.post('/health/ask-ai', {
                question: chatInput,
                context: {}
            });

            const aiMessage: ChatMessage = {
                role: 'assistant',
                content: response.data.answer,
                timestamp: new Date().toISOString()
            };

            setChatMessages(prev => [...prev, aiMessage]);
            setConversationId(response.data.conversation_id);
        } catch (error) {
            console.error(error);
            const errorMessage: ChatMessage = {
                role: 'assistant',
                content: 'Sorry, I encountered an error. Please try again.',
                timestamp: new Date().toISOString()
            };
            setChatMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    const getSeverityColor = (severity: string) => {
        switch (severity.toLowerCase()) {
            case 'low': return 'bg-green-100 text-green-800';
            case 'moderate': return 'bg-yellow-100 text-yellow-800';
            case 'high': return 'bg-orange-100 text-orange-800';
            case 'severe': return 'bg-red-100 text-red-800';
            default: return 'bg-gray-100 text-gray-800';
        }
    };

    const getPriorityIcon = (priority: string) => {
        return priority === 'high' ? <AlertCircle className="h-4 w-4 text-red-500" /> : <CheckCircle className="h-4 w-4 text-green-500" />;
    };

    const renderSymptomTab = () => (
        <div className="space-y-6">
            {/* Symptom Logging Form */}
            <div className="card bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                    <Plus className="h-5 w-5 mr-2 text-primary-600" />
                    Log New Symptom
                </h2>

                <form onSubmit={handleSymptomSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Symptom Name</label>
                        <input
                            type="text"
                            value={symptomForm.symptom_name}
                            onChange={(e) => setSymptomForm({ ...symptomForm, symptom_name: e.target.value })}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                            placeholder="e.g., Headache, Fatigue, Nausea"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Severity</label>
                        <select
                            value={symptomForm.severity}
                            onChange={(e) => setSymptomForm({ ...symptomForm, severity: e.target.value })}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                        >
                            <option value="low">Low</option>
                            <option value="moderate">Moderate</option>
                            <option value="high">High</option>
                            <option value="severe">Severe</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Duration (days)</label>
                        <input
                            type="number"
                            min="1"
                            value={symptomForm.duration_days}
                            onChange={(e) => setSymptomForm({ ...symptomForm, duration_days: parseInt(e.target.value) })}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Additional Notes</label>
                        <textarea
                            value={symptomForm.notes}
                            onChange={(e) => setSymptomForm({ ...symptomForm, notes: e.target.value })}
                            rows={3}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                            placeholder="Describe your symptom in detail..."
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full btn-primary flex items-center justify-center"
                    >
                        {loading ? <Loader className="h-5 w-5 animate-spin" /> : <Plus className="h-5 w-5 mr-2" />}
                        {loading ? 'Logging...' : 'Log Symptom'}
                    </button>
                </form>
            </div>

            {/* Recent Symptoms */}
            <div className="card bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Recent Symptoms</h2>

                {symptoms.length === 0 ? (
                    <p className="text-gray-500 text-center py-8">No symptoms logged yet</p>
                ) : (
                    <div className="space-y-3">
                        {symptoms.map((symptom) => (
                            <div key={symptom.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                                <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                        <h3 className="font-medium text-gray-900 dark:text-white">{symptom.symptom_name}</h3>
                                        {symptom.notes && (
                                            <p className="text-sm text-gray-600 mt-1">{symptom.notes}</p>
                                        )}
                                        <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                                            <span>{new Date(symptom.created_at).toLocaleDateString()}</span>
                                            {symptom.duration_days && <span>{symptom.duration_days} days</span>}
                                        </div>
                                    </div>
                                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${getSeverityColor(symptom.severity)}`}>
                                        {symptom.severity}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );



    const renderAIChatTab = () => {
        // Feature Gating Logic
        const isTrialExpired = subscription?.status === 'expired' && subscription?.plan_type === 'trial';

        if (isTrialExpired) {
            return (
                <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm h-[600px] flex flex-col items-center justify-center p-8 text-center">
                    <div className="bg-purple-100 p-4 rounded-full mb-4">
                        <Lock className="h-10 w-10 text-purple-600" />
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Free Trial Expired</h2>
                    <p className="text-gray-600 dark:text-gray-400 mb-6 max-w-md">
                        Your 7-day free trial of AI Health Assistant has ended. Upgrade to Premium to continue receiving personalized Ayurvedic insights.
                    </p>
                    <button
                        onClick={upgradeToPremium}
                        className="btn-primary px-8 py-3 text-lg shadow-lg hover:shadow-xl transform transition-all hover:-translate-y-1"
                    >
                        {subLoading ? 'Processing...' : 'Upgrade to Premium - ₹499/mo'}
                    </button>
                </div>
            );
        }

        return (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm h-[600px] flex flex-col">
                <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                    <h2 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center">
                        <Sparkles className="h-5 w-5 mr-2 text-primary-600" />
                        AI Health Assistant
                    </h2>
                    <p className="text-sm text-gray-600 mt-1">Ask questions about Ayurveda, wellness, and your health</p>
                </div>

                {/* Chat Messages */}
                <div className="flex-1 overflow-y-auto p-6 space-y-4">
                    {chatMessages.length === 0 ? (
                        <div className="text-center py-12">
                            <Sparkles className="h-12 w-12 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
                            <p className="text-gray-500 underline-offset-4">Start a conversation with the AI health assistant</p>
                            <p className="text-sm text-gray-400 mt-2">Ask about symptoms, remedies, or Ayurvedic practices</p>
                        </div>
                    ) : (
                        chatMessages.map((msg, idx) => (
                            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[80%] rounded-lg p-4 ${msg.role === 'user' ? 'bg-primary-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100'}`}>
                                    <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                                    <p className={`text-xs mt-2 ${msg.role === 'user' ? 'text-primary-100' : 'text-gray-500'}`}>
                                        {new Date(msg.timestamp).toLocaleTimeString()}
                                    </p>
                                </div>
                            </div>
                        ))
                    )}
                    {loading && (
                        <div className="flex justify-start">
                            <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4">
                                <Loader className="h-5 w-5 animate-spin text-gray-500 dark:text-gray-400" />
                            </div>
                        </div>
                    )}
                </div>

                {/* Chat Input */}
                <form onSubmit={handleAIChat} className="p-6 border-t border-gray-200 dark:border-gray-700">
                    <div className="flex space-x-2">
                        <input
                            type="text"
                            value={chatInput}
                            onChange={(e) => setChatInput(e.target.value)}
                            placeholder="Ask a health question..."
                            className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                            disabled={loading}
                        />
                        <button
                            type="submit"
                            disabled={loading || !chatInput.trim()}
                            className="btn-primary px-6"
                        >
                            <Send className="h-5 w-5" />
                        </button>
                    </div>
                </form>
            </div>
        );
    };

    const renderRecommendationsTab = () => (
        <div className="space-y-6">
            {/* Dosha Analysis */}
            {doshaAnalysis && (
                <div className="card bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
                    <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                        <TrendingUp className="h-5 w-5 mr-2 text-primary-600" />
                        Dosha Balance
                    </h2>
                    <div className="grid grid-cols-3 gap-4">
                        <div className="text-center">
                            <div className="text-3xl font-bold text-blue-600">{doshaAnalysis.vata}%</div>
                            <div className="text-sm text-gray-600 mt-1">Vata</div>
                            <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                                <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${doshaAnalysis.vata}%` }}></div>
                            </div>
                        </div>
                        <div className="text-center">
                            <div className="text-3xl font-bold text-red-600">{doshaAnalysis.pitta}%</div>
                            <div className="text-sm text-gray-600 mt-1">Pitta</div>
                            <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                                <div className="bg-red-600 h-2 rounded-full" style={{ width: `${doshaAnalysis.pitta}%` }}></div>
                            </div>
                        </div>
                        <div className="text-center">
                            <div className="text-3xl font-bold text-green-600">{doshaAnalysis.kapha}%</div>
                            <div className="text-sm text-gray-600 mt-1">Kapha</div>
                            <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                                <div className="bg-green-600 h-2 rounded-full" style={{ width: `${doshaAnalysis.kapha}%` }}></div>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Recommendations */}
            <div className="card bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Personalized Recommendations</h2>

                {recommendations.length === 0 ? (
                    <p className="text-gray-500 text-center py-8">No recommendations available yet</p>
                ) : (
                    <div className="space-y-4">
                        {recommendations.map((rec, idx) => (
                            <div key={idx} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:border-primary-300 dark:hover:border-primary-500 transition-colors">
                                <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                        <div className="flex items-center space-x-2 mb-2">
                                            {getPriorityIcon(rec.priority)}
                                            <span className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">{rec.category}</span>
                                        </div>
                                        <h3 className="font-medium text-gray-900 dark:text-white mb-1">{rec.suggestion}</h3>
                                        <p className="text-sm text-gray-600 dark:text-gray-400">{rec.reason}</p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );

    return (
        <div className="flex h-screen bg-dashboard">
            <Sidebar items={sidebarItems} user={user} onLogout={handleLogout} />

            <div className="flex-1 overflow-auto">
                <div className="p-8">
                    <div className="max-w-5xl mx-auto">
                        {/* Header */}
                        <div className="mb-6 flex justify-between items-center">
                            <div>
                                <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Health Support</h1>
                                <p className="text-gray-600 dark:text-gray-400 mt-2">Track symptoms, get AI-powered health insights, and receive personalized recommendations</p>
                            </div>

                            <div className="flex items-center space-x-4 relative">
                                <button
                                    onClick={() => setIsNotificationOpen(!isNotificationOpen)}
                                    className="p-2 text-gray-400 hover:text-gray-500 relative"
                                >
                                    <Bell className="h-6 w-6" />
                                    {notificationsList.filter(n => !n.read).length > 0 && (
                                        <span className="absolute top-1 right-1 flex h-3 w-3">
                                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                                            <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
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

                        {/* Message Alert */}
                        {message && (
                            <div className={`mb-6 p-4 rounded-lg flex items-center ${message.type === 'success' ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
                                {message.type === 'success' ? <CheckCircle className="h-5 w-5 mr-2" /> : <AlertCircle className="h-5 w-5 mr-2" />}
                                <span>{message.text}</span>
                            </div>
                        )}

                        {/* Tabs */}
                        <div className="flex border-b border-gray-200 dark:border-gray-700 mb-6 font-medium">
                            <button
                                onClick={() => setActiveTab('symptoms')}
                                className={`py-4 px-6 font-medium text-sm border-b-2 transition-colors ${activeTab === 'symptoms' ? 'border-primary-600 text-primary-600 dark:text-primary-400' : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'}`}
                            >
                                Log Symptoms
                            </button>
                            <button
                                onClick={() => setActiveTab('ai-chat')}
                                className={`py-4 px-6 font-medium text-sm border-b-2 transition-colors ${activeTab === 'ai-chat' ? 'border-primary-600 text-primary-600 dark:text-primary-400' : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'}`}
                            >
                                AI Assistant
                            </button>
                            <button
                                onClick={() => setActiveTab('recommendations')}
                                className={`py-4 px-6 font-medium text-sm border-b-2 transition-colors ${activeTab === 'recommendations' ? 'border-primary-600 text-primary-600 dark:text-primary-400' : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'}`}
                            >
                                Recommendations
                            </button>
                        </div>

                        {/* Tab Content */}
                        {activeTab === 'symptoms' && renderSymptomTab()}
                        {activeTab === 'ai-chat' && renderAIChatTab()}
                        {activeTab === 'recommendations' && renderRecommendationsTab()}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default HealthSupport;
