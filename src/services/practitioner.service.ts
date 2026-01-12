/**
 * Practitioner Service
 * API calls for practitioner-specific functionality
 */

import apiClient from './api';
import { DashboardStats, Appointment } from '../types/api.types';

class PractitionerService {
    /**
     * Get practitioner dashboard statistics
     */
    async getDashboardStats(): Promise<DashboardStats> {
        const response = await apiClient.get<DashboardStats>('/practitioner/dashboard');
        return response.data;
    }

    /**
     * Get practitioner appointments
     */
    async getAppointments(status?: string): Promise<Appointment[]> {
        const params = status ? { status } : {};
        const response = await apiClient.get<Appointment[]>('/appointments', { params });
        return response.data;
    }

    /**
     * Get treatment analytics
     */
    async getAnalytics(days: number = 30): Promise<any> {
        const response = await apiClient.get('/reports/treatments', { params: { days } });
        return response.data;
    }
}

export default new PractitionerService();
