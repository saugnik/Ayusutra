/**
 * Practitioner Service
 * API calls for practitioner-specific functionality
 */

import apiClient from './api';
import { DashboardStats, Appointment, PatientListItem, Notification } from '../types/api.types';

class PractitionerService {
    /**
     * Get list of patients for current practitioner
     */
    async getMyPatients(): Promise<PatientListItem[]> {
        const response = await apiClient.get<PatientListItem[]>('/practitioner/patients');
        return response.data;
    }

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

    /**
     * Get notifications for current practitioner
     */
    async getNotifications(): Promise<Notification[]> {
        const response = await apiClient.get<Notification[]>('/notifications');
        return response.data;
    }

    /**
     * Mark a notification as read
     */
    async markNotificationAsRead(id: number | string): Promise<void> {
        await apiClient.patch(`/notifications/${id}/read`);
    }
}

export default new PractitionerService();
