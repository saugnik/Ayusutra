import React, { useState, useEffect } from 'react';
import { Sun, RefreshCw, Sparkles } from 'lucide-react';
import aiService from '../services/ai.service';

const DailyWisdom = () => {
    const [tip, setTip] = useState<string>('');
    const [loading, setLoading] = useState(true);

    const fetchTip = async (force: boolean = false) => {
        setLoading(true);

        // Check local storage first (cache for 24h)
        const today = new Date().toDateString();
        const cached = localStorage.getItem('daily_wisdom');

        if (!force && cached) {
            const parsed = JSON.parse(cached);
            if (parsed.date === today) {
                setTip(parsed.text);
                setLoading(false);
                return;
            }
        }

        try {
            const response = await aiService.askQuestion(
                "Give me one short, inspiring Ayurvedic daily health tip (max 2 sentences) for general well-being. Do not use markdown."
            );

            const newTip = response.answer.text;
            setTip(newTip);

            localStorage.setItem('daily_wisdom', JSON.stringify({
                date: today,
                text: newTip
            }));
        } catch (error) {
            setTip("Drink warm water throughout the day to maintain digestive fire (Agni) and remove toxins.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTip();
    }, []);

    return (
        <div className="card bg-gradient-to-br from-orange-50 to-white dark:from-orange-950/20 dark:to-gray-800 border-orange-100 dark:border-orange-900/30 relative overflow-hidden">
            {/* Decorative Background */}
            <div className="absolute top-0 right-0 -mr-4 -mt-4 opacity-10">
                <Sun className="h-24 w-24 text-orange-500" />
            </div>

            <div className="relative z-10">
                <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-2">
                        <Sparkles className="h-5 w-5 text-orange-500" />
                        <h3 className="font-bold text-gray-800 dark:text-gray-100">Daily Wisdom</h3>
                    </div>
                    <button
                        onClick={() => fetchTip(true)}
                        disabled={loading}
                        className={`p-1.5 rounded-full hover:bg-orange-100 text-orange-400 transition-all ${loading ? 'animate-spin' : ''}`}
                        title="Get new tip"
                    >
                        <RefreshCw className="h-4 w-4" />
                    </button>
                </div>

                <div className="min-h-[60px] flex items-center">
                    {loading ? (
                        <div className="space-y-2 w-full">
                            <div className="h-4 bg-orange-100 rounded w-3/4 animate-pulse"></div>
                            <div className="h-4 bg-orange-100 rounded w-1/2 animate-pulse"></div>
                        </div>
                    ) : (
                        <p className="text-gray-700 dark:text-gray-200 italic text-lg leading-relaxed font-serif">
                            "{tip}"
                        </p>
                    )}
                </div>

                <div className="mt-4 flex items-center text-xs text-orange-400 font-medium uppercase tracking-wide">
                    <span className="w-8 h-px bg-orange-200 mr-2"></span>
                    Ayurvedic Sutra
                </div>
            </div>
        </div>
    );
};

export default DailyWisdom;
