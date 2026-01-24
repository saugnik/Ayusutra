import React, { useState, useEffect } from 'react';
import { Sun, RefreshCw, Sparkles } from 'lucide-react';

// Array of Ayurvedic wisdom quotes
const AYURVEDIC_WISDOM = [
    "Start your day with warm water and lemon to kindle your digestive fire (Agni) and cleanse your system.",
    "Practice oil pulling with sesame or coconut oil each morning to promote oral health and remove toxins.",
    "Eat your largest meal at midday when your digestive fire is strongest, and keep dinner light.",
    "Massage warm oil into your skin before bathing (Abhyanga) to nourish tissues and calm the nervous system.",
    "Go to bed before 10 PM to align with nature's rhythms and ensure restorative sleep.",
    "Drink warm water throughout the day to maintain digestive fire and remove toxins from your body.",
    "Practice mindful eating: sit down, chew thoroughly, and avoid distractions during meals.",
    "Include all six tastes (sweet, sour, salty, bitter, pungent, astringent) in your daily diet for balance.",
    "Wake up during Brahma Muhurta (before sunrise) for enhanced mental clarity and spiritual connection.",
    "Use spices like turmeric, ginger, and cumin in your cooking to support digestion and reduce inflammation.",
    "Practice Pranayama (breathing exercises) daily to balance your doshas and calm your mind.",
    "Eat seasonal and local foods to stay in harmony with nature's cycles.",
    "Avoid ice-cold drinks and foods as they dampen your digestive fire.",
    "Take a short walk after meals to aid digestion and prevent sluggishness.",
    "Practice tongue scraping each morning to remove toxins accumulated overnight.",
    "Meditate daily to calm the mind, reduce stress, and enhance overall well-being.",
    "Use ghee (clarified butter) in moderation to nourish tissues and support healthy digestion.",
    "Avoid eating when emotionally upset, as it can disturb digestion and create toxins.",
    "Sleep on your left side to support digestion and promote better sleep quality.",
    "Practice gratitude before meals to enhance digestion and appreciation for nourishment.",
    "Drink herbal teas like ginger, tulsi, or fennel to support various bodily functions.",
    "Maintain a regular daily routine (Dinacharya) to keep your doshas in balance.",
    "Use natural, chemical-free products for skincare and personal hygiene.",
    "Practice yoga asanas suited to your constitution for physical and mental balance.",
    "Avoid overeating; leave one-third of your stomach empty to aid digestion.",
    "Use copper vessels for storing water overnight to benefit from its antimicrobial properties.",
    "Take time for self-care and rest; it's essential for maintaining health and vitality.",
    "Connect with nature daily through walks, gardening, or simply being outdoors.",
    "Use Triphala powder before bed to support gentle detoxification and regular elimination.",
    "Practice self-massage with warm oil to ground Vata, cool Pitta, or stimulate Kapha."
];

const DailyWisdom = () => {
    const [tip, setTip] = useState<string>('');
    const [loading, setLoading] = useState(true);

    const fetchTip = (force: boolean = false) => {
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

        // Get wisdom based on day of year for consistent daily rotation
        const dayOfYear = Math.floor((Date.now() - new Date(new Date().getFullYear(), 0, 0).getTime()) / 86400000);
        const wisdomIndex = dayOfYear % AYURVEDIC_WISDOM.length;
        const newTip = AYURVEDIC_WISDOM[wisdomIndex];

        setTip(newTip);

        localStorage.setItem('daily_wisdom', JSON.stringify({
            date: today,
            text: newTip
        }));

        setLoading(false);
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
