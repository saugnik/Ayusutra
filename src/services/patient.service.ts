/**
 * Patient Service
 * API calls for patient-specific functionality
 */

import apiClient from './api';
import { DashboardStats, Appointment } from '../types/api.types';

class PatientService {
    /**
     * Get patient dashboard statistics
     */
    async getDashboardStats(): Promise<DashboardStats> {
        const response = await apiClient.get<DashboardStats>('/patient/dashboard');
        return response.data;
    }

    /**
     * Get patient appointments
     */
    async getAppointments(status?: string): Promise<Appointment[]> {
        const params = status ? { status } : {};
        const response = await apiClient.get<Appointment[]>('/appointments', { params });
        return response.data;
    }
}

export default new PatientService();
