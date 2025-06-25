/**
 * Authentication Component - Cleaned and Simplified
 * Handles user login, registration, and session management
 */
class AuthComponent {
    constructor() {
        this.setupEventListeners();
        this.setupStateSubscriptions();
    }

    setupEventListeners() {
        const loginForm = document.getElementById('login-form');
        loginForm?.addEventListener('submit', (e) => this.handleLogin(e));
    }

    setupStateSubscriptions() {
        appState.subscribe('auth', (isLoggedIn) => this.updateNavigation(isLoggedIn));
        appState.subscribe('user', (user) => user && this.displayUser(user));
    }

    async handleLogin(event) {
        event.preventDefault();
        
        const formData = FormHelpers.getData('#login-form');
        const { name, email } = Object.fromEntries(formData);

        // Validate input
        const validationError = this.validateLoginData({ name, email });
        if (validationError) {
            UIHelpers.showAlert(validationError, 'error');
            return;
        }

        try {
            UIHelpers.showLoading('Authenticating...');
            
            // Find or create user
            const user = await this.findOrCreateUser({ name, email });
            if (user) {
                await this.completeLogin(user);
                UIHelpers.showAlert(`Welcome ${user.id ? 'back' : 'to Covy'}, ${user.name}!`, 'success');
            }
            
        } catch (error) {
            console.error('Login error:', error);
            UIHelpers.showAlert('Authentication failed. Please try again.', 'error');
        } finally {
            UIHelpers.hideLoading();
        }
    }

    validateLoginData({ name, email }) {
        if (!ValidationHelpers.name(name)) {
            return 'Please enter a valid name (at least 2 characters).';
        }
        if (!ValidationHelpers.email(email)) {
            return 'Please enter a valid email address.';
        }
        return null;
    }

    async findOrCreateUser({ name, email }) {
        // Try to find existing user
        const existingUser = await this.findUserByEmail(email);
        
        if (existingUser) {
            // Verify name matches
            if (existingUser.name.toLowerCase() === name.toLowerCase()) {
                return existingUser;
            } else {
                throw new Error('Name does not match the email address in our records.');
            }
        }
        
        // Create new user
        return await this.createUser({ name, email });
    }

    async findUserByEmail(email) {
        try {
            const users = await apiService.getAllUsers();
            return users.find(user => user.email.toLowerCase() === email.toLowerCase());
        } catch (error) {
            console.error('Error finding user:', error);
            return null;
        }
    }

    async createUser(userData) {
        try {
            return await apiService.createUser(userData);
        } catch (error) {
            console.error('Error creating user:', error);
            throw new Error('Failed to create account. Please try again.');
        }
    }

    async completeLogin(user) {
        // Update application state
        appState.setCurrentUser(user);
        
        // Load existing profile
        await this.loadUserProfile(user.id);
        
        // Navigate to profile section
        navigationComponent?.showSection('profile');
    }

    async loadUserProfile(userId) {
        try {
            const profile = await apiService.getUserProfile(userId);
            appState.setCurrentProfile(profile);
        } catch (error) {
            // No existing profile found - expected for new users
            console.log('No existing profile found');
        }
    }

    displayUser(user) {
        // Update display elements
        FormHelpers.setContent('display-name', user.name);
        FormHelpers.setContent('display-email', user.email);
    }

    updateNavigation(isLoggedIn) {
        const navStates = {
            'login-nav': !isLoggedIn,
            'profile-nav': isLoggedIn,
            'generate-nav': isLoggedIn,
            'history-nav': isLoggedIn,
            'logout-nav': isLoggedIn
        };

        Object.entries(navStates).forEach(([elementId, shouldShow]) => {
            const element = document.getElementById(elementId);
            if (element) element.style.display = shouldShow ? 'block' : 'none';
        });
    }

    logout() {
        if (!confirm('Are you sure you want to logout?')) return;
        
        // Clear application state and forms
        appState.clearUserSession();
        ['#login-form', '#profile-form', '#cover-letter-form'].forEach(FormHelpers.clear);
        
        // Navigate to login
        navigationComponent?.showSection('login');
        UIHelpers.showAlert('Logged out successfully.', 'info');
    }

    requireAuthentication() {
        if (appState.isUserLoggedIn()) return true;
        
        UIHelpers.showAlert('Please login first.', 'error');
        navigationComponent?.showSection('login');
        return false;
    }
}

// Initialize and make available globally
window.authComponent = new AuthComponent(); 