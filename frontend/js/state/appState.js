/**
 * Application State Management
 * Centralized state container with clear interfaces for state updates
 */
class AppState {
    constructor() {
        this.state = {
            currentUser: null,
            currentProfile: null,
            currentCoverLetter: null,
            isLoggedIn: false,
            isLoading: false,
            loadingMessage: ''
        };
        
        this.subscribers = new Map();
        
        // Load persisted state on initialization
        this.loadPersistedState();
    }
    
    // Persist state to localStorage
    persistState() {
        try {
            const stateToPersist = {
                currentUser: this.state.currentUser,
                currentProfile: this.state.currentProfile,
                isLoggedIn: this.state.isLoggedIn
            };
            localStorage.setItem('cvGeneratorState', JSON.stringify(stateToPersist));
        } catch (error) {
            console.error('Error persisting state:', error);
        }
    }
    
    // Load persisted state from localStorage
    loadPersistedState() {
        try {
            const persistedState = localStorage.getItem('cvGeneratorState');
            if (persistedState) {
                const parsedState = JSON.parse(persistedState);
                this.state.currentUser = parsedState.currentUser;
                this.state.currentProfile = parsedState.currentProfile;
                this.state.isLoggedIn = parsedState.isLoggedIn || false;
            }
        } catch (error) {
            console.error('Error loading persisted state:', error);
            // Clear corrupted data
            localStorage.removeItem('cvGeneratorState');
        }
    }
    
    // Clear persisted state
    clearPersistedState() {
        try {
            localStorage.removeItem('cvGeneratorState');
        } catch (error) {
            console.error('Error clearing persisted state:', error);
        }
    }

    // State getters
    getCurrentUser() {
        return this.state.currentUser;
    }

    getCurrentProfile() {
        return this.state.currentProfile;
    }

    getCurrentCoverLetter() {
        return this.state.currentCoverLetter;
    }

    isUserLoggedIn() {
        return this.state.isLoggedIn;
    }

    getLoadingState() {
        return {
            isLoading: this.state.isLoading,
            message: this.state.loadingMessage
        };
    }

    // State setters
    setCurrentUser(user) {
        this.state.currentUser = user;
        this.state.isLoggedIn = !!user;
        this.persistState(); // Persist after state change
        this.notifySubscribers('user', user);
        this.notifySubscribers('auth', this.state.isLoggedIn);
    }

    setCurrentProfile(profile) {
        this.state.currentProfile = profile;
        this.persistState(); // Persist after state change
        this.notifySubscribers('profile', profile);
    }

    setCurrentCoverLetter(coverLetter) {
        this.state.currentCoverLetter = coverLetter;
        // Note: We don't persist cover letters as they can be large and are temporary
        this.notifySubscribers('coverLetter', coverLetter);
    }

    setLoadingState(isLoading, message = '') {
        this.state.isLoading = isLoading;
        this.state.loadingMessage = message;
        this.notifySubscribers('loading', { isLoading, message });
    }

    clearUserSession() {
        this.state.currentUser = null;
        this.state.currentProfile = null;
        this.state.currentCoverLetter = null;
        this.state.isLoggedIn = false;
        this.clearPersistedState(); // Clear persisted data
        this.notifySubscribers('auth', false);
        this.notifySubscribers('user', null);
        this.notifySubscribers('profile', null);
        this.notifySubscribers('coverLetter', null);
    }

    // Subscription system for components to react to state changes
    subscribe(event, callback) {
        if (!this.subscribers.has(event)) {
            this.subscribers.set(event, new Set());
        }
        this.subscribers.get(event).add(callback);

        // Return unsubscribe function
        return () => {
            this.subscribers.get(event)?.delete(callback);
        };
    }

    notifySubscribers(event, data) {
        const eventSubscribers = this.subscribers.get(event);
        if (eventSubscribers) {
            eventSubscribers.forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`Error in state subscriber for ${event}:`, error);
                }
            });
        }
    }

    // Utility methods
    hasValidUser() {
        return this.state.currentUser && this.state.currentUser.id;
    }

    hasValidProfile() {
        return this.state.currentProfile && this.state.currentProfile.id;
    }
}

// Export a singleton instance
window.appState = new AppState(); 