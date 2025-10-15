/**
 * API Service for Calendar ERP Chatbot
 * Handles all communication with the FastAPI backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Custom error class for API errors
 */
class ApiError extends Error {
  constructor(message, status, data) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }
}

/**
 * Check if the backend is healthy and ready
 * @returns {Promise<Object>} Health status
 */
export const checkHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new ApiError(
        'Health check failed',
        response.status,
        await response.json()
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) throw error;
    throw new ApiError('Failed to connect to backend', 0, { error: error.message });
  }
};

/**
 * Get system information
 * @returns {Promise<Object>} System info including model and database status
 */
export const getSystemInfo = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/info`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new ApiError(
        'Failed to get system info',
        response.status,
        await response.json()
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) throw error;
    throw new ApiError('Failed to get system info', 0, { error: error.message });
  }
};

/**
 * Send a message to the chatbot
 * @param {string} message - User's message
 * @returns {Promise<Object>} Chatbot response with answer and sources
 */
export const sendMessage = async (message) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: message,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new ApiError(
        errorData.detail || 'Failed to send message',
        response.status,
        errorData
      );
    }

    const data = await response.json();
    return {
      answer: data.answer,
      sources: data.sources || [],
      timestamp: new Date().toISOString(),
    };
  } catch (error) {
    if (error instanceof ApiError) throw error;
    throw new ApiError('Failed to send message', 0, { error: error.message });
  }
};

/**
 * Initialize the database (admin function)
 * @returns {Promise<Object>} Initialization result
 */
export const initializeDatabase = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/initialize`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new ApiError(
        'Failed to initialize database',
        response.status,
        await response.json()
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) throw error;
    throw new ApiError('Failed to initialize database', 0, { error: error.message });
  }
};

export { ApiError };
