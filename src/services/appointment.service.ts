
import apiClient from './api';
import { AppointmentCreate, AppointmentResponse, Practitioner } from '../types/api.types';

export type { Practitioner };

const appointmentService = {
    getAllPractitioners: async (): Promise<Practitioner[]> => {
        const response = await apiClient.get<Practitioner[]>('/practitioners');
        return response.data;
    },

    createAppointment: async (data: AppointmentCreate): Promise<AppointmentResponse> => {
        const response = await apiClient.post<AppointmentResponse>('/appointments', data);
        return response.data;
    },

    getMyAppointments: async (status?: string): Promise<AppointmentResponse[]> => {
        const params = status ? { status } : {};
        const response = await apiClient.get<AppointmentResponse[]>('/appointments', { params });
        return response.data;
    }
};

export default appointmentService;
