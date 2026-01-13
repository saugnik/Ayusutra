import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send, Sparkles, Loader } from 'lucide-react';
import aiService, { AIResponse } from '../services/ai.service';
import ReactMarkdown from 'react-markdown';

interface Message {
    id: string;
    sender: 'user' | 'ai';
    text: string;
    timestamp: Date;
    confidence?: string;
    evidence?: string[];
}

const AIAssistant: React.FC = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([
        {
            id: 'welcome',
            sender: 'ai',
            text: "Namaste! I am **AyurGenius**, your Ayurvedic wellness assistant. \n\nI can answer questions about your therapy, specific doshas, or general Ayurvedic practices. How can I help you today?",
            timestamp: new Date()
        }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isOpen]);

    const handleSend = async () => {
        if (!inputValue.trim() || isLoading) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            sender: 'user',
            text: inputValue,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);

        try {
            const response = await aiService.askQuestion(userMessage.text);

            const aiMessage: Message = {
                id: (Date.now() + 1).toString(),
                sender: 'ai',
                text: response.answer.text,
                timestamp: new Date(),
                confidence: response.answer.confidence,
                evidence: response.answer.evidence
            };

            setMessages(prev => [...prev, aiMessage]);
        } catch (error) {
            const errorMessage: Message = {
                id: (Date.now() + 1).toString(),
                sender: 'ai',
                text: "I apologize, but I'm having trouble connecting to my knowledge base right now. Please try again later.",
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="fixed bottom-6 right-6 z-50 font-sans">
            {/* Chat Window */}
            {isOpen && (
                <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-96 h-[32rem] flex flex-col mb-4 overflow-hidden border border-gray-200 dark:border-gray-700 animate-fade-in-up">
                    {/* Header */}
                    <div className="bg-gradient-to-r from-primary-600 to-primary-700 p-4 flex items-center justify-between text-white">
                        <div className="flex items-center space-x-2">
                            <div className="bg-white/20 p-2 rounded-lg">
                                <Sparkles className="h-5 w-5 text-yellow-300" />
                            </div>
                            <div>
                                <h3 className="font-bold text-lg">AyurGenius</h3>
                                <p className="text-xs text-primary-100 flex items-center">
                                    <span className="w-2 h-2 bg-green-400 rounded-full mr-1 animate-pulse"></span>
                                    Online
                                </p>
                            </div>
                        </div>
                        <button
                            onClick={() => setIsOpen(false)}
                            className="p-1 hover:bg-white/20 rounded-full transition-colors"
                        >
                            <X className="h-5 w-5" />
                        </button>
                    </div>

                    {/* Messages Area */}
                    <div className="flex-1 overflow-y-auto p-4 bg-gray-50 dark:bg-gray-900 space-y-4">
                        {messages.map((msg) => (
                            <div
                                key={msg.id}
                                className={`flex w-full ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                <div
                                    className={`max-w-[85%] rounded-2xl p-3 ${msg.sender === 'user'
                                        ? 'bg-primary-600 text-white rounded-br-none'
                                        : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-800 dark:text-gray-200 rounded-bl-none shadow-sm'
                                        }`}
                                >
                                    {msg.sender === 'ai' && (
                                        <div className="flex items-center space-x-1 mb-1 opacity-75">
                                            <Sparkles className="h-3 w-3 text-primary-500" />
                                            <span className="text-xs font-semibold text-primary-600 dark:text-primary-400">AyurGenius</span>
                                        </div>
                                    )}
                                    <div className={`text-sm prose prose-sm max-w-none ${msg.sender === 'user' ? 'prose-invert text-white' : ''}`}>
                                        <ReactMarkdown>{msg.text}</ReactMarkdown>
                                    </div>

                                    {/* Evidence / Confidence Footer for AI */}
                                    {msg.sender === 'ai' && msg.evidence && msg.evidence.length > 0 && (
                                        <div className="mt-2 pt-2 border-t border-gray-100 dark:border-gray-700">
                                            <p className="text-xs text-gray-400 dark:text-gray-500 flex items-center">
                                                Based on: {msg.evidence.slice(0, 2).map((e: string) => e.split(' ').slice(0, 4).join(' ')).join(', ')}...
                                            </p>
                                        </div>
                                    )}

                                    <p className={`text-[10px] mt-1 text-right ${msg.sender === 'user' ? 'text-primary-200' : 'text-gray-400 dark:text-gray-500'}`}>
                                        {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                    </p>
                                </div>
                            </div>
                        ))}
                        {isLoading && (
                            <div className="flex justify-start">
                                <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl rounded-bl-none p-4 shadow-sm flex items-center space-x-2">
                                    <div className="flex space-x-1">
                                        <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                        <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                        <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                                    </div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input Area */}
                    <div className="p-4 bg-white dark:bg-gray-800 border-t border-gray-100 dark:border-gray-700">
                        <div className="flex items-center space-x-2 bg-gray-50 dark:bg-gray-900 rounded-full border border-gray-200 dark:border-gray-700 px-4 py-2 focus-within:ring-2 focus-within:ring-primary-500 focus-within:border-transparent transition-all">
                            <input
                                type="text"
                                value={inputValue}
                                onChange={(e) => setInputValue(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Ask anything about Ayurveda..."
                                className="flex-1 bg-transparent border-none focus:ring-0 text-sm py-1 placeholder-gray-400 dark:placeholder-gray-500 text-gray-700 dark:text-gray-200"
                                disabled={isLoading}
                            />
                            <button
                                onClick={handleSend}
                                disabled={!inputValue.trim() || isLoading}
                                className={`p-2 rounded-full transition-all ${inputValue.trim() && !isLoading
                                    ? 'bg-primary-600 text-white hover:bg-primary-700 shadow-md'
                                    : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                                    }`}
                            >
                                {isLoading ? <Loader className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                            </button>
                        </div>
                        <p className="text-center text-[10px] text-gray-400 mt-2">
                            AI can make mistakes. Please consult your practitioner.
                        </p>
                    </div>
                </div>
            )}

            {/* Floating Toggle Button */}
            {!isOpen && (
                <button
                    onClick={() => setIsOpen(true)}
                    className="group flex items-center justify-center w-14 h-14 bg-gradient-to-r from-primary-600 to-primary-700 text-white rounded-full shadow-lg hover:shadow-xl hover:scale-110 transition-all duration-300 relative border-2 border-white"
                >
                    <Sparkles className="h-6 w-6 animate-pulse" />
                    <span className="absolute -top-1 -right-1 h-3 w-3 bg-red-500 rounded-full border-2 border-white"></span>

                    {/* Tooltip */}
                    <div className="absolute right-full mr-4 bg-gray-900 text-white text-xs px-3 py-1.5 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
                        Ask AyurGenius AI
                    </div>
                </button>
            )}
        </div>
    );
};

export default AIAssistant;
