import apiClient from './api';

export interface AgentAction {
    type: string;
    label: string;
    data: any;
}

export interface ChatResponse {
    reply: string;
    conversation_id: string;
    actions?: AgentAction[];
}

export interface Reminder {
    id: number;
    title: string;
    message?: string;
    frequency: string;
    time: string;
    is_active: boolean;
}

// Store conversation ID for maintaining context across messages
let currentConversationId: string | null = null;

export const agentService = {
    // Send message to agent
    chat: async (message: string): Promise<ChatResponse> => {
        // Build payload with conversation_id in context if available
        const payload: { question: string; context?: { conversation_id: string } } = {
            question: message
        };

        if (currentConversationId) {
            payload.context = { conversation_id: currentConversationId };
        }

        const response = await apiClient.post('/health/ask-ai', payload);

        // Store conversation ID for subsequent messages
        if (response.data.conversation_id) {
            currentConversationId = response.data.conversation_id;
        }

        // Map backend's 'answer' field to frontend's 'reply' field
        return {
            reply: response.data.answer,
            conversation_id: response.data.conversation_id,
            actions: response.data.actions || []
        };
    },

    // Reset conversation (useful when starting a new chat session)
    resetConversation: () => {
        currentConversationId = null;
    },

    // Confirm actions to be executed
    confirmActions: async (actions: AgentAction[]) => {
        const response = await apiClient.post('/api/agent/confirm-actions', actions);
        return response.data;
    },

    // Get active reminders
    getReminders: async (): Promise<Reminder[]> => {
        const response = await apiClient.get<Reminder[]>('/api/reminders');
        return response.data;
    }
};
