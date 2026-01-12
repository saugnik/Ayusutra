import axios from 'axios';

const RAG_API_URL = 'http://localhost:8000';

export interface AIResponse {
    query: string;
    answer: {
        text: string;
        confidence: string;
        evidence: string[];
        timestamp: string;
    };
    context: any[];
    processing_time: number;
}

const aiService = {
    /**
     * Send a query to the AyurGenius RAG service
     */
    askQuestion: async (query: string): Promise<AIResponse> => {
        try {
            const response = await axios.post(`${RAG_API_URL}/ask`, {
                query,
                top_k: 3
            });
            return response.data;
        } catch (error) {
            console.error('Error asking AI:', error);
            throw error;
        }
    },

    /**
     * Check if the RAG service is available
     */
    checkHealth: async (): Promise<boolean> => {
        try {
            const response = await axios.get(`${RAG_API_URL}/health`);
            return response.status === 200;
        } catch (error) {
            return false;
        }
    }
};

export default aiService;
