/**
 * API Service - Handles all HTTP requests to the backend
 */
class ApiService {
    constructor() {
        this.baseUrl = 'http://localhost:8000/api/v1';
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            if (response.status === 204) {
                return null;
            }

            const text = await response.text();
            
            if (!response.ok) {
                let errorMessage = `HTTP error! status: ${response.status}`;
                if (text) {
                    try {
                        const errorData = JSON.parse(text);
                        errorMessage = errorData?.detail || errorMessage;
                    } catch (e) {
                        // Not a JSON error, use the raw text if it's not too long
                        errorMessage = text.substring(0, 100);
                    }
                }
                throw new Error(errorMessage);
            }

            if (!text) {
                return null;
            }
            
            return JSON.parse(text);
        } catch (error) {
            console.error(`API request failed: ${endpoint}`, error);
            throw error;
        }
    }

    // User endpoints
    async getAllUsers() {
        return this.request('/users/');
    }

    async createUser(userData) {
        return this.request('/users/', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    // CV Profile endpoints
    async getUserProfile(userId) {
        return this.request(`/cv/profile/user/${userId}`);
    }

    async createProfile(profileData) {
        return this.request('/cv/profile', {
            method: 'POST',
            body: JSON.stringify(profileData)
        });
    }

    async updateProfile(profileId, profileData) {
        return this.request(`/cv/profile/${profileId}`, {
            method: 'PUT',
            body: JSON.stringify(profileData)
        });
    }

    // Cover Letter endpoints
    async generateCoverLetter(generateData) {
        return this.request('/cover-letters/generate', {
            method: 'POST',
            body: JSON.stringify(generateData)
        });
    }

    async getCoverLetter(letterId) {
        return this.request(`/cover-letters/${letterId}`);
    }

    async updateCoverLetter(letterId, letterData) {
        return this.request(`/cover-letters/${letterId}`, {
            method: 'PUT',
            body: JSON.stringify(letterData)
        });
    }

    async deleteCoverLetter(letterId) {
        return this.request(`/cover-letters/${letterId}`, {
            method: 'DELETE'
        });
    }

    async getUserCoverLetters(userId) {
        return this.request(`/cover-letters/user/${userId}`);
    }
}

// Export a singleton instance
window.apiService = new ApiService(); 