
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useAuth } from './AuthContext';
import axios from 'axios';
import toast from 'react-hot-toast';

// Types
export type PlanType = 'trial' | 'premium';
export type SubscriptionStatus = 'active' | 'expired' | 'cancelled';

export interface Subscription {
    id: number;
    user_id: number;
    plan_type: PlanType;
    status: SubscriptionStatus;
    end_date: string | null;
    free_consultation_used: boolean;
}

interface SubscriptionContextType {
    subscription: Subscription | null;
    isLoading: boolean;
    activateTrial: () => Promise<void>;
    upgradeToPremium: () => Promise<void>;
    checkStatus: () => Promise<void>;
    markConsultationUsed: () => Promise<void>;
}

const SubscriptionContext = createContext<SubscriptionContextType | undefined>(undefined);

export const SubscriptionProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const { user, isAuthenticated } = useAuth();
    const [subscription, setSubscription] = useState<Subscription | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    const API_URL = 'http://localhost:8001';

    const getAuthHeader = () => {
        const token = localStorage.getItem('access_token');
        return { headers: { Authorization: `Bearer ${token}` } };
    };

    const checkStatus = async () => {
        if (!isAuthenticated) return;

        try {
            // setIsLoading(true); // Don't block UI on every check
            const response = await axios.get(`${API_URL}/subscription/status`, getAuthHeader());
            setSubscription(response.data);
        } catch (error) {
            console.error('Failed to fetch subscription status', error);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (isAuthenticated) {
            checkStatus();
        } else {
            setSubscription(null);
        }
    }, [isAuthenticated]);

    const activateTrial = async () => {
        setIsLoading(true);
        try {
            const response = await axios.post(`${API_URL}/subscription/activate-trial`, {}, getAuthHeader());
            setSubscription(response.data);
            toast.success("Free Trial Activated! Enjoy 7 days of AI access.");
        } catch (error: any) {
            toast.error(error.response?.data?.detail || "Failed to activate trial");
        } finally {
            setIsLoading(false);
        }
    };

    const upgradeToPremium = async () => {
        setIsLoading(true);
        try {
            // Mock payment delay
            await new Promise(resolve => setTimeout(resolve, 1500));
            const response = await axios.post(`${API_URL}/subscription/upgrade`, { plan_type: "premium" }, getAuthHeader());
            setSubscription(response.data);
            toast.success("Upgraded to Premium! Unlimited access unlocked.");
        } catch (error: any) {
            toast.error("Failed to upgrade");
        } finally {
            setIsLoading(false);
        }
    };

    const markConsultationUsed = async () => {
        try {
            const response = await axios.post(`${API_URL}/subscription/use-consultation`, {}, getAuthHeader());
            setSubscription(response.data);
        } catch (error) {
            console.error("Failed to mark consultation used");
        }
    };

    return (
        <SubscriptionContext.Provider value={{
            subscription,
            isLoading,
            activateTrial,
            upgradeToPremium,
            checkStatus,
            markConsultationUsed
        }}>
            {children}
        </SubscriptionContext.Provider>
    );
};

export const useSubscription = () => {
    const context = useContext(SubscriptionContext);
    if (!context) {
        throw new Error('useSubscription must be used within a SubscriptionProvider');
    }
    return context;
};
