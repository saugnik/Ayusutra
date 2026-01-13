import apiClient from './api';

export interface AIResponse {
    query: string;
    answer: {
        text: string;
        confidence?: string;
        evidence?: string[];
        timestamp: string;
    };
    conversation_id?: string;
    type?: string;
}

const aiService = {
    /**
     * Send a query to the AyurGenius AI Health Assistant
     */
    askQuestion: async (query: string, conversation_id?: string): Promise<AIResponse> => {
        try {
            const response = await apiClient.post('/health/ask-ai', {
                query,
                conversation_id
            });
            return response.data;
        } catch (error) {
            console.error('Error asking AI:', error);
            throw error;
        }
    },

    /**
     * Check if the AI Assistant service is available
     */
    checkHealth: async (): Promise<boolean> => {
        try {
            const response = await apiClient.get('/health/ask-ai/health'); // Assuming there might be a health check
            return response.status === 200;
        } catch (error) {
            return false;
        }
    }
};

export default aiService;
