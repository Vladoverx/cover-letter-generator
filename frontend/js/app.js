/**
 * Main Application Entry Point
 * Coordinates all components and handles app initialization
 */
class App {
    constructor() {
        this.isInitialized = false;
    }

    async initialize() {
        if (this.isInitialized) return;

        try {
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => this.initializeApp());
            } else {
                this.initializeApp();
            }
        } catch (error) {
            console.error('Error initializing application:', error);
            UIHelpers.showAlert('Error initializing application. Please refresh the page.', 'error');
        }
    }

    initializeApp() {
        console.log('Initializing CV Generator Application...');
        
        this.checkDependencies();
        this.setupGlobalHandlers();
        this.handleInitialNavigation();
        
        this.isInitialized = true;
        console.log('CV Generator Application initialized successfully');
    }

    checkDependencies() {
        const required = [
            'apiService', 'appState', 'authComponent', 'navigationComponent',
            'profileComponent', 'coverLetterComponent', 'UIHelpers', 'FormHelpers',
            'ValidationHelpers', 'DataHelpers', 'FormBuilder'
        ];

        const missing = required.filter(component => !window[component]);
        
        if (missing.length > 0) {
            throw new Error(`Missing required components: ${missing.join(', ')}`);
        }
    }

    setupGlobalHandlers() {
        appState.subscribe('loading', ({ isLoading, message }) => {
            if (isLoading) console.log(`Loading: ${message}`);
        });

        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled promise rejection:', event.reason);
            UIHelpers.showAlert('An unexpected error occurred. Please try again.', 'error');
        });

        window.addEventListener('error', (event) => {
            console.error('Global error:', event.error);
            UIHelpers.showAlert('An unexpected error occurred. Please refresh the page.', 'error');
        });
    }

    handleInitialNavigation() {
        console.log('Handling initial navigation...');
        
        if (appState.isUserLoggedIn()) {
            const user = appState.getCurrentUser();
            if (user) {
                console.log('Restoring user session for:', user.name);
                
                appState.notifySubscribers('auth', true);
                appState.notifySubscribers('user', user);
                
                const profile = appState.getCurrentProfile();
                if (profile) {
                    appState.notifySubscribers('profile', profile);
                }
                
                navigationComponent?.showSection('profile');
                
                setTimeout(() => {
                    UIHelpers.showAlert(`Welcome back, ${user.name}!`, 'success');
                }, 100);
            } else {
                console.log('Invalid session found, clearing...');
                appState.clearUserSession();
                navigationComponent?.showSection('login');
            }
        } else {
            console.log('No existing session, showing login');
            navigationComponent?.showSection('login');
        }
    }

    // Utility methods for debugging
    getAppState() {
        return {
            user: appState.getCurrentUser(),
            profile: appState.getCurrentProfile(),
            coverLetter: appState.getCurrentCoverLetter(),
            isLoggedIn: appState.isUserLoggedIn(),
            loading: appState.getLoadingState()
        };
    }

    resetApp() {
        if (confirm('This will reset the entire application. Are you sure?')) {
            appState.clearUserSession();
            navigationComponent?.showSection('login');
            UIHelpers.showAlert('Application reset successfully.', 'info');
        }
    }
}

const app = new App();
app.initialize();

window.app = app; 