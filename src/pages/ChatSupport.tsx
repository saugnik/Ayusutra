import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useSubscription } from '../contexts/SubscriptionContext';
import { useNavigate } from 'react-router-dom';
import {
    Activity,
    Calendar,
    CheckCircle,
    Heart,
    Home,
    Loader,
    MessageCircle,
    Send,
    Settings,
    Sparkles,
    User,
    Users,
    Lock,
    Unlock,
    Bell,
    Trash2
} from 'lucide-react';
import Sidebar from '../components/Sidebar';
import api from '../services/api';
import toast, { Toaster } from 'react-hot-toast';
import NotificationDropdown, { Notification } from '../components/NotificationDropdown';

interface Practitioner {
    id: number;
    name: string;
    specialization?: string;
    online: boolean;
    last_seen?: string;
}

interface ChatMessage {
    id: number;
    sender_id: number;
    sender_type: string;
    recipient_id: number;
    recipient_type: string;
    content: string;
    read: boolean;
    created_at: string;
}

const ChatSupport = () => {
    const { user, logout } = useAuth();
    const { subscription, markConsultationUsed, upgradeToPremium, isLoading: subLoading } = useSubscription();
    const navigate = useNavigate();

    // State
    const [practitioners, setPractitioners] = useState<Practitioner[]>([]);
    const [selectedPractitioner, setSelectedPractitioner] = useState<Practitioner | null>(null);
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [messageInput, setMessageInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [chatMode, setChatMode] = useState<'practitioner' | 'ai'>('practitioner');

    // AI Chat state
    const [aiMessages, setAiMessages] = useState<any[]>([]);
    const [aiConversationId, setAiConversationId] = useState<string | null>(null);
    const [aiHistory, setAiHistory] = useState<any[]>([]);
    const [isNotificationOpen, setIsNotificationOpen] = useState(false);
    const [notificationsList, setNotificationsList] = useState<Notification[]>([
        { id: 'CN1', type: 'reminder', title: 'Message from Practitioner', message: 'Dr. Priya Sharma sent you a message about your diet plan.', time: '10 mins ago', read: false },
        { id: 'CN2', type: 'alert', title: 'Health Update', message: 'New activity detected in your metrics.', time: '3 hours ago', read: true },
    ]);

    // Alarm/Reminder State
    const [alarmsOpen, setAlarmsOpen] = useState(false);
    const [myReminders, setMyReminders] = useState<any[]>([]);

    useEffect(() => {
        if (alarmsOpen) {
            fetchReminders();
        }
    }, [alarmsOpen]);

    const fetchReminders = async () => {
        try {
            const res = await api.get('/reminders');
            setMyReminders(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    const executeDeleteReminder = async (id: number) => {
        try {
            await api.delete(`/reminders/${id}`);
            setMyReminders(prev => prev.filter(r => r.id !== id));
            toast.success('Reminder deleted successfully');
        } catch (err) {
            console.error("Failed to delete reminder", err);
            toast.error('Failed to delete reminder');
        }
    };

    const handleDeleteReminder = (id: number) => {
        toast((t) => (
            <div className="flex flex-col gap-2">
                <p className="font-medium text-gray-800 dark:text-white">Delete this alarm?</p>
                <div className="flex gap-2">
                    <button
                        onClick={() => {
                            toast.dismiss(t.id);
                            executeDeleteReminder(id);
                        }}
                        className="bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600 transition-colors"
                    >
                        Delete
                    </button>
                    <button
                        onClick={() => toast.dismiss(t.id)}
                        className="bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-3 py-1 rounded text-sm hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
                    >
                        Cancel
                    </button>
                </div>
            </div>
        ), {
            duration: 5000,
            icon: '⏰',
            className: 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-xl'
        });
    };

    const executeDeleteConversation = async (id: string) => {
        try {
            await api.delete(`/health/conversations/${id}`);
            setAiHistory(prev => prev.filter(c => c.conversation_id !== id));
            if (aiConversationId === id) {
                setAiConversationId(null);
                setAiMessages([]);
            }
            toast.success('Conversation deleted successfully');
        } catch (err) {
            console.error("Failed to delete conversation", err);
            toast.error('Failed to delete conversation');
        }
    };

    const handleDeleteConversation = (e: React.MouseEvent, id: string) => {
        e.stopPropagation(); // Prevent opening the chat

        toast((t) => (
            <div className="flex flex-col gap-2">
                <p className="font-medium text-gray-800 dark:text-white">Delete this conversation?</p>
                <div className="flex gap-2">
                    <button
                        onClick={() => {
                            toast.dismiss(t.id);
                            executeDeleteConversation(id);
                        }}
                        className="bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600 transition-colors"
                    >
                        Delete
                    </button>
                    <button
                        onClick={() => toast.dismiss(t.id)}
                        className="bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-3 py-1 rounded text-sm hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
                    >
                        Cancel
                    </button>
                </div>
            </div>
        ), {
            duration: 5000,
            icon: '🗑️',
            className: 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-xl'
        });
    };

    useEffect(() => {
        if (chatMode === 'ai') {
            fetchAIHistory();
        }
    }, [chatMode, aiConversationId]); // Refresh list when ID changes (new chat created)

    const fetchAIHistory = async () => {
        try {
            const response = await api.get('/health/conversations');
            setAiHistory(response.data);
        } catch (error) {
            console.error("Failed to fetch AI history", error);
        }
    };

    const loadConversation = async (id: string) => {
        try {
            setLoading(true);
            const response = await api.get(`/health/conversations/${id}`);
            setAiMessages(response.data.messages || []);
            setAiConversationId(id);
        } catch (error) {
            console.error("Failed to load conversation", error);
        } finally {
            setLoading(false);
        }
    };

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

    // Fetch practitioners on mount
    useEffect(() => {
        fetchPractitioners();
    }, []);

    // Poll for new messages when a practitioner is selected
    useEffect(() => {
        if (selectedPractitioner && chatMode === 'practitioner') {
            fetchMessages(selectedPractitioner.id);
            const interval = setInterval(() => {
                fetchMessages(selectedPractitioner.id);
            }, 5000); // Poll every 5 seconds

            return () => clearInterval(interval);
        }
    }, [selectedPractitioner, chatMode]);

    const fetchPractitioners = async () => {
        try {
            const response = await api.get('/chat/practitioners');
            setPractitioners(response.data);
        } catch (error) {
            console.error('Failed to fetch practitioners:', error);
        }
    };

    const fetchMessages = async (practitionerId: number) => {
        try {
            const response = await api.get(`/chat/messages?recipient_id=${practitionerId}`);
            setMessages(response.data);
        } catch (error) {
            console.error('Failed to fetch messages:', error);
        }
    };

    const handleSendMessage = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!messageInput.trim() || !selectedPractitioner) return;

        setLoading(true);

        try {
            await api.post('/chat/send', {
                recipient_id: selectedPractitioner.id,
                recipient_type: 'practitioner',
                content: messageInput
            });

            setMessageInput('');
            fetchMessages(selectedPractitioner.id);
        } catch (error) {
            console.error('Failed to send message:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleAIChat = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!messageInput.trim()) return;

        const userMessage = {
            role: 'user',
            content: messageInput,
            timestamp: new Date().toISOString()
        };

        setAiMessages(prev => [...prev, userMessage]);
        setMessageInput('');
        setLoading(true);

        try {
            const response = await api.post('/health/ask-ai', {
                question: messageInput,
                context: { conversation_id: aiConversationId }
            });

            const aiMessage = {
                role: 'assistant',
                content: response.data.answer,
                timestamp: new Date().toISOString()
            };

            setAiMessages(prev => [...prev, aiMessage]);
            setAiConversationId(response.data.conversation_id);
        } catch (error) {
            console.error('Failed to chat with AI:', error);
            const errorMessage = {
                role: 'assistant',
                content: 'Sorry, I encountered an error. Please try again.',
                timestamp: new Date().toISOString()
            };
            setAiMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
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

    const renderPractitionerList = () => (
        <div className="w-80 border-r border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Contacts</h2>
            </div>

            {/* Mode Toggle */}
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                <div className="flex space-x-2">
                    <button
                        onClick={() => setChatMode('practitioner')}
                        className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-colors ${chatMode === 'practitioner' ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
                    >
                        <Users className="h-4 w-4 inline mr-2" />
                        Practitioners
                    </button>
                    <button
                        onClick={() => setChatMode('ai')}
                        className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-colors ${chatMode === 'ai' ? 'bg-primary-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'}`}
                    >
                        <Sparkles className="h-4 w-4 inline mr-2" />
                        AI Assistant
                    </button>
                </div>
            </div>

            {/* Practitioner List */}
            {chatMode === 'practitioner' && (
                <div className="overflow-y-auto" style={{ height: 'calc(100vh - 200px)' }}>
                    {practitioners.length === 0 ? (
                        <p className="text-gray-500 text-center py-8 text-sm">No practitioners available</p>
                    ) : (
                        practitioners.map((prac) => (
                            <div
                                key={prac.id}
                                onClick={() => setSelectedPractitioner(prac)}
                                className={`p-4 border-b border-gray-100 dark:border-gray-700 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors ${selectedPractitioner?.id === prac.id ? 'bg-primary-50 dark:bg-primary-900/20' : ''}`}
                            >
                                <div className="flex items-center space-x-3">
                                    <div className="relative">
                                        <div className="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900/40 flex items-center justify-center">
                                            <User className="h-5 w-5 text-primary-600 dark:text-primary-400" />
                                        </div>
                                        {prac.online && (
                                            <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 border-2 border-white dark:border-gray-800 rounded-full"></div>
                                        )}
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <p className="text-sm font-medium text-gray-900 dark:text-white truncate">{prac.name}</p>
                                        {prac.specialization && (
                                            <p className="text-xs text-gray-500 dark:text-gray-400 truncate">{prac.specialization}</p>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            )}

            {/* AI Assistant History */}
            {chatMode === 'ai' && (
                <div className="overflow-y-auto" style={{ height: 'calc(100vh - 200px)' }}>
                    <div className="p-4 border-b border-gray-100 dark:border-gray-700">
                        <button
                            onClick={() => {
                                setAiConversationId(null);
                                setAiMessages([]);
                                setNotificationsList([]); // clear fake notifs if any
                            }}
                            className="w-full py-2 px-4 bg-primary-50 text-primary-600 rounded-lg text-sm font-medium hover:bg-primary-100 transition-colors"
                        >
                            + New Conversation
                        </button>
                    </div>
                    {aiHistory.length === 0 ? (
                        <p className="text-gray-500 text-center py-8 text-sm">No past conversations</p>
                    ) : (
                        aiHistory.map((chat) => (
                            <div
                                key={chat.conversation_id}
                                onClick={() => loadConversation(chat.conversation_id)}
                                className={`p-4 border-b border-gray-100 dark:border-gray-700 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors group flex justify-between items-center ${aiConversationId === chat.conversation_id ? 'bg-primary-50 dark:bg-primary-900/20' : ''}`}
                            >
                                <div className="flex items-center space-x-3 flex-1 min-w-0">
                                    <div className="w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-900/40 flex items-center justify-center flex-shrink-0">
                                        <Sparkles className="h-4 w-4 text-indigo-600 dark:text-indigo-400" />
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <p className="text-sm font-medium text-gray-900 dark:text-white truncate">{chat.title || "New Chat"}</p>
                                        <p className="text-xs text-gray-500 dark:text-gray-400 truncate">{new Date(chat.created_at).toLocaleDateString()}</p>
                                    </div>
                                </div>
                                <button
                                    onClick={(e) => handleDeleteConversation(e, chat.conversation_id)}
                                    className="text-gray-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity p-2"
                                    title="Delete Chat"
                                >
                                    <Trash2 size={16} />
                                </button>
                            </div>
                        ))
                    )}
                </div>
            )}
        </div>
    );

    const renderChatWindow = () => {
        if (chatMode === 'practitioner' && !selectedPractitioner) {
            return (
                <div className="flex-1 flex items-center justify-center bg-dashboard">
                    <div className="text-center">
                        <MessageCircle className="h-16 w-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
                        <p className="text-gray-500 dark:text-gray-400">Select a practitioner to start chatting</p>
                    </div>
                </div>
            );
        }

        const displayMessages = chatMode === 'practitioner' ? messages : aiMessages;



        // Feature Gating for Practitioner Chat
        if (chatMode === 'practitioner') {
            const isPremium = subscription?.plan_type === 'premium';
            const isFreeUsed = subscription?.free_consultation_used;

            if (!isPremium && isFreeUsed) {
                return (
                    <div className="flex-1 flex flex-col items-center justify-center p-8 text-center bg-gray-50 dark:bg-gray-900">
                        <div className="bg-purple-100 p-4 rounded-full mb-4">
                            <Lock className="h-12 w-12 text-purple-600" />
                        </div>
                        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Free Consultation Used</h2>
                        <p className="text-gray-600 dark:text-gray-400 mb-6 max-w-md">
                            You have used your one-time free doctor consultation. Upgrade to Premium for unlimited chat access with our practitioners.
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

            if (!isPremium && !isFreeUsed && messages.length === 0) {
                // First time user, hasn't started yet
                return (
                    <div className="flex-1 flex flex-col items-center justify-center p-8 text-center bg-white dark:bg-gray-900">
                        <div className="bg-green-100 p-4 rounded-full mb-4">
                            <Unlock className="h-12 w-12 text-green-600" />
                        </div>
                        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Start Your Free Consultation</h2>
                        <p className="text-gray-600 dark:text-gray-400 mb-6 max-w-md">
                            You have <b>1 free consultation</b> session available with Dr. {selectedPractitioner?.name || 'Practitioner'}.
                        </p>
                        <button
                            onClick={async () => {
                                await markConsultationUsed();
                                // Refresh logic might be needed or handled by context update
                            }}
                            className="btn-primary px-8 py-3 text-lg flex items-center"
                        >
                            Start Chat Now <Send className="ml-2 h-4 w-4" />
                        </button>
                    </div>
                );
            }
        }

        return (
            <div className="flex-1 flex flex-col bg-white dark:bg-gray-900">
                {/* Chat Header */}
                <div className="p-4 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
                    <div className="flex items-center space-x-3">
                        {chatMode === 'practitioner' ? (
                            <>
                                <div className="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900/40 flex items-center justify-center">
                                    <User className="h-5 w-5 text-primary-600 dark:text-primary-400" />
                                </div>
                                <div>
                                    <h2 className="text-lg font-semibold text-gray-900 dark:text-white">{selectedPractitioner?.name}</h2>
                                    {selectedPractitioner?.specialization && (
                                        <p className="text-sm text-gray-500 dark:text-gray-400">{selectedPractitioner.specialization}</p>
                                    )}
                                </div>
                            </>
                        ) : (
                            <>
                                <div className="w-10 h-10 bg-gradient-to-br from-primary-400 to-primary-600 rounded-full flex items-center justify-center">
                                    <Sparkles className="h-5 w-5 text-white" />
                                </div>
                                <div>
                                    <h2 className="text-lg font-semibold text-gray-900 dark:text-white">AI Health Assistant</h2>
                                    <p className="text-sm text-gray-500 dark:text-gray-400">Always available</p>
                                </div>
                            </>
                        )}
                    </div>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-6 space-y-4" style={{ height: 'calc(100vh - 240px)' }}>
                    {displayMessages.length === 0 ? (
                        <div className="text-center py-12">
                            <MessageCircle className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                            <p className="text-gray-500">No messages yet. Start the conversation!</p>
                        </div>
                    ) : (
                        displayMessages.map((msg: any, idx: number) => {
                            const isUser = chatMode === 'practitioner'
                                ? msg.sender_type === 'patient'
                                : msg.role === 'user';

                            return (
                                <div key={idx} className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
                                    <div className={`max-w-[70%] rounded-lg p-4 ${isUser ? 'bg-primary-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100'}`}>
                                        <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                                        <p className={`text-xs mt-2 ${isUser ? 'text-primary-100' : 'text-gray-500 dark:text-gray-400'}`}>
                                            {new Date(msg.created_at || msg.timestamp).toLocaleTimeString()}
                                        </p>
                                    </div>
                                </div>
                            );
                        })
                    )}
                    {loading && (
                        <div className="flex justify-start">
                            <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4">
                                <Loader className="h-5 w-5 animate-spin text-gray-500 dark:text-gray-400" />
                            </div>
                        </div>
                    )}
                </div>

                {/* Message Input */}
                <form
                    onSubmit={chatMode === 'practitioner' ? handleSendMessage : handleAIChat}
                    className="p-4 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800"
                >
                    <div className="flex space-x-2">
                        <input
                            type="text"
                            value={messageInput}
                            onChange={(e) => setMessageInput(e.target.value)}
                            placeholder="Type your message..."
                            className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                            disabled={loading}
                        />
                        <button
                            type="submit"
                            disabled={loading || !messageInput.trim()}
                            className="btn-primary px-6"
                        >
                            <Send className="h-5 w-5" />
                        </button>
                    </div>
                </form>
            </div>
        );
    };

    return (
        <div className="flex h-screen bg-dashboard">
            <Toaster
                position="top-right"
                toastOptions={{
                    className: 'dark:bg-gray-800 dark:text-white',
                    style: {
                        maxWidth: '500px',
                    },
                }}
            />
            {/* Alarms Modal */}
            {alarmsOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
                    <div className="bg-white rounded-xl p-6 w-96 max-h-[80vh] overflow-y-auto">
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="text-xl font-bold text-gray-800">My Alarms</h3>
                            <button onClick={() => setAlarmsOpen(false)} className="text-gray-500 hover:text-gray-700">✕</button>
                        </div>
                        {myReminders.length === 0 ? (
                            <p className="text-gray-500 text-center py-4">No active alarms.</p>
                        ) : (
                            <div className="space-y-3">
                                {myReminders.map(reminder => (
                                    <div key={reminder.id} className="bg-gray-50 p-3 rounded-lg flex justify-between items-start border border-gray-100">
                                        <div>
                                            <p className="font-semibold text-gray-800">{reminder.title}</p>
                                            <p className="text-sm text-gray-600">{reminder.time} ({reminder.frequency})</p>
                                        </div>
                                        <button
                                            onClick={() => handleDeleteReminder(reminder.id)}
                                            className="text-red-500 hover:text-red-700 bg-red-50 p-1 rounded"
                                        >
                                            <Trash2 size={16} />
                                        </button>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            )}

            <Sidebar items={sidebarItems} user={user} onLogout={handleLogout} />

            <div className="flex-1 flex flex-col overflow-hidden">
                {/* Header */}
                <div className="p-6 header-bg flex justify-between items-center">
                    <div>
                        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Chat Support</h1>
                        <p className="text-gray-600 dark:text-gray-400 mt-1">Connect with practitioners or chat with AI assistant</p>
                    </div>

                    <div className="flex items-center space-x-4 relative">
                        {/* Alarm Button */}
                        <button
                            onClick={() => setAlarmsOpen(true)}
                            className="bg-white border border-gray-300 text-gray-600 px-4 py-2 rounded-lg hover:bg-gray-50 flex items-center gap-2 transition-colors"
                        >
                            <Bell size={18} />
                            <span className="hidden md:inline">Alarms</span>
                        </button>

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

                {/* Chat Interface */}
                <div className="flex-1 flex overflow-hidden">
                    {renderPractitionerList()}
                    {renderChatWindow()}
                </div>
            </div>
        </div>
    );
};

export default ChatSupport;
