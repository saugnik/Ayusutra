import api from './api';
import { HealthLog, HealthLogCreate } from '../types/api.types';

export const healthService = {
    createLog: async (data: HealthLogCreate): Promise<HealthLog> => {
        const response = await api.post<HealthLog>('/api/health-logs', data);
        return response.data;
    },

    getMyLogs: async (): Promise<HealthLog[]> => {
        const response = await api.get<HealthLog[]>('/api/health-logs/me');
        return response.data;
    },

    // Helper to interpret Dosha values
    getDoshaLevel: (value: number) => {
        if (value < 30) return 'Low';
        if (value < 70) return 'Balanced';
        return 'Aggravated';
    }
};
