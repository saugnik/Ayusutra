/**
 * Appointment Service
 * API calls for appointment management
 */

import apiClient from './api';
import { Appointment, AppointmentCreate } from '../types/api.types';

class AppointmentService {
    /**
     * Create a new appointment
     */
    async createAppointment(appointmentData: AppointmentCreate): Promise<Appointment> {
        const response = await apiClient.post<Appointment>('/appointments', appointmentData);
        return response.data;
    }

    /**
     * Get all appointments for current user
     */
    async getAppointments(status?: string, limit: number = 50): Promise<Appointment[]> {
        const params: any = { limit };
        if (status) params.status = status;

        const response = await apiClient.get<Appointment[]>('/appointments', { params });
        return response.data;
    }

    /**
     * Update appointment
     */
    async updateAppointment(id: number, updates: Partial<Appointment>): Promise<Appointment> {
        const response = await apiClient.put<Appointment>(`/appointments/${id}`, updates);
        return response.data;
    }

    /**
     * Cancel appointment
     */
    async cancelAppointment(id: number): Promise<Appointment> {
        return this.updateAppointment(id, { status: 'cancelled' });
    }
}

export default new AppointmentService();
