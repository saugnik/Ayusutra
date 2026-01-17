import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageSquare, X, Send, CheckCircle, Clock, UserPlus, Droplets, Activity } from 'lucide-react';
import { agentService, AgentAction, ChatResponse } from '../services/agent.service';
import { toast } from 'react-hot-toast';

interface Message {
    id: number;
    type: 'user' | 'agent';
    text: string;
    actions?: AgentAction[];
}

const HealthAgentChat: React.FC = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState<Message[]>([
        { id: 0, type: 'agent', text: 'Namaste! I am your personal Health Agent. I can help you plan your diet, schedule workouts, or find a doctor. How can I assist you today?' }
    ]);
    const [isLoading, setIsLoading] = useState(false);
    const [confirmedActions, setConfirmedActions] = useState<Set<string>>(new Set());
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMsg: Message = { id: Date.now(), type: 'user', text: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await agentService.chat(userMsg.text);

            const agentMsg: Message = {
                id: Date.now() + 1,
                type: 'agent',
                text: response.reply,
                actions: response.actions
            };

            setMessages(prev => [...prev, agentMsg]);
        } catch (error) {
            console.error('Agent Error:', error);
            toast.error("Failed to reach Health Agent");
        } finally {
            setIsLoading(false);
        }
    };

    const handleConfirmAction = async (action: AgentAction, messageId: number) => {
        const actionKey = `${messageId}-${action.type}-${action.label}`;

        try {
            await agentService.confirmActions([action]);
            toast.success(action.type === 'create_reminder' ? 'Reminder Set Successfully!' : 'Action Confirmed');

            // Mark this action as confirmed
            setConfirmedActions(prev => new Set(prev).add(actionKey));
        } catch (error) {
            toast.error("Failed to execute action");
        }
    };

    const renderActionCard = (action: AgentAction, msgId: number) => {
        const actionKey = `${msgId}-${action.type}-${action.label}`;
        const isConfirmed = confirmedActions.has(actionKey);

        let Icon = Activity;
        let color = "text-blue-500 bg-blue-100";

        if (action.type === 'create_reminder') {
            if (action.label.toLowerCase().includes('water')) {
                Icon = Droplets;
                color = "text-blue-500 bg-blue-100";
            } else {
                Icon = Clock;
                color = "text-orange-500 bg-orange-100";
            }
        } else if (action.type === 'find_practitioner') {
            Icon = UserPlus;
            color = "text-purple-500 bg-purple-100";
        }

        return (
            <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`mt-3 p-3 rounded-xl border shadow-sm ${isConfirmed ? 'bg-gray-50 border-gray-200' : 'bg-white border-gray-100'}`}
            >
                <div className="flex items-start gap-3">
                    <div className={`p-2 rounded-lg ${isConfirmed ? 'bg-green-100 text-green-600' : color}`}>
                        {isConfirmed ? <CheckCircle size={18} /> : <Icon size={18} />}
                    </div>
                    <div className="flex-1">
                        <h4 className={`text-sm font-semibold ${isConfirmed ? 'text-gray-500' : 'text-gray-800'}`}>
                            {action.label}
                        </h4>
                        <p className={`text-xs mt-1 ${isConfirmed ? 'text-gray-400' : 'text-gray-500'}`}>
                            {action.data.message || "Would you like to proceed with this action?"}
                        </p>
                        {action.data.time && (
                            <div className={`mt-1 text-xs font-mono inline-block px-2 py-0.5 rounded ${isConfirmed ? 'bg-gray-100 text-gray-500' : 'bg-gray-50 text-gray-600'}`}>
                                ⏰ {action.data.time} ({action.data.frequency})
                            </div>
                        )}

                        {isConfirmed ? (
                            <div className="mt-3 flex items-center gap-2 text-green-600 text-sm font-medium">
                                <CheckCircle size={14} />
                                Confirmed!
                            </div>
                        ) : (
                            <button
                                onClick={() => handleConfirmAction(action, msgId)}
                                className="mt-3 w-full flex items-center justify-center gap-2 bg-gradient-to-r from-emerald-500 to-teal-600 text-white py-1.5 rounded-lg text-sm font-medium hover:from-emerald-600 hover:to-teal-700 transition-colors"
                            >
                                <CheckCircle size={14} />
                                Confirm & Set
                            </button>
                        )}
                    </div>
                </div>
            </motion.div>
        );
    };

    return (
        <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9, y: 20 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.9, y: 20 }}
                        className="mb-4 w-96 max-h-[600px] bg-white rounded-2xl shadow-2xl border border-gray-100 overflow-hidden flex flex-col"
                    >
                        {/* Header */}
                        <div className="bg-gradient-to-r from-emerald-600 to-teal-600 p-4 flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <div className="bg-white/20 p-2 rounded-full">
                                    <Activity className="text-white" size={20} />
                                </div>
                                <div>
                                    <h3 className="text-white font-bold">AyurSutra Agent</h3>
                                    <p className="text-emerald-100 text-xs">Always here to help</p>
                                </div>
                            </div>
                            <button
                                onClick={() => setIsOpen(false)}
                                className="text-white/80 hover:text-white transition-colors"
                            >
                                <X size={20} />
                            </button>
                        </div>

                        {/* Messages */}
                        <div className="flex-1 overflow-y-auto p-4 bg-gray-50 min-h-[300px] max-h-[400px]">
                            {messages.map((msg) => (
                                <div
                                    key={msg.id}
                                    className={`mb-4 flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
                                >
                                    <div className={`max-w-[85%] rounded-2xl p-3 ${msg.type === 'user'
                                        ? 'bg-emerald-600 text-white rounded-tr-none'
                                        : 'bg-white text-gray-800 shadow-sm rounded-tl-none border border-gray-100'
                                        }`}>
                                        <p className="text-sm leading-relaxed whitespace-pre-line">{msg.text}</p>

                                        {msg.actions && msg.actions.length > 0 && (
                                            <div className="mt-2 space-y-2">
                                                {msg.actions.map((action, idx) => (
                                                    <div key={idx}>{renderActionCard(action, msg.id)}</div>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))}
                            {isLoading && (
                                <div className="flex justify-start mb-4">
                                    <div className="bg-white rounded-2xl p-3 rounded-tl-none border border-gray-100 shadow-sm">
                                        <div className="flex gap-1">
                                            <motion.div animate={{ y: [0, -5, 0] }} transition={{ repeat: Infinity, duration: 0.6 }} className="w-2 h-2 bg-gray-400 rounded-full" />
                                            <motion.div animate={{ y: [0, -5, 0] }} transition={{ repeat: Infinity, duration: 0.6, delay: 0.1 }} className="w-2 h-2 bg-gray-400 rounded-full" />
                                            <motion.div animate={{ y: [0, -5, 0] }} transition={{ repeat: Infinity, duration: 0.6, delay: 0.2 }} className="w-2 h-2 bg-gray-400 rounded-full" />
                                        </div>
                                    </div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>

                        {/* Input */}
                        <div className="p-3 bg-white border-t border-gray-100">
                            <form
                                onSubmit={(e) => { e.preventDefault(); handleSend(); }}
                                className="flex gap-2"
                            >
                                <input
                                    type="text"
                                    value={input}
                                    onChange={(e) => setInput(e.target.value)}
                                    placeholder="Ask about diet, workout, or doctors..."
                                    className="flex-1 bg-gray-50 border border-gray-200 rounded-full px-4 py-2 text-sm focus:outline-none focus:border-emerald-500 transition-colors"
                                />
                                <button
                                    type="submit"
                                    disabled={!input.trim() || isLoading}
                                    className="bg-emerald-600 text-white p-2 rounded-full hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                                >
                                    <Send size={18} />
                                </button>
                            </form>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setIsOpen(!isOpen)}
                className="bg-emerald-600 text-white p-4 rounded-full shadow-lg hover:bg-emerald-700 transition-colors flex items-center gap-2 group"
            >
                {isOpen ? <X size={24} /> : <MessageSquare size={24} />}
                {!isOpen && <span className="max-w-0 overflow-hidden group-hover:max-w-xs transition-all duration-300 ease-out whitespace-nowrap font-medium">Chat Assistant</span>}
            </motion.button>
        </div>
    );
};

export default HealthAgentChat;
