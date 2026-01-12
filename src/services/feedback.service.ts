/**
 * Feedback Service
 * API calls for feedback and ratings
 */

import apiClient from './api';
import { Feedback, FeedbackCreate } from '../types/api.types';

class FeedbackService {
    /**
     * Submit feedback for a session
     */
    async submitFeedback(feedbackData: FeedbackCreate): Promise<Feedback> {
        const response = await apiClient.post<Feedback>('/feedback', feedbackData);
        return response.data;
    }
}

export default new FeedbackService();
