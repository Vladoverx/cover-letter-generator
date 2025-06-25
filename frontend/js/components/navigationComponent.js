/**
 * Navigation Component - Cleaned and Simplified
 * Handles section navigation and updates active navigation states
 */
class NavigationComponent {
    constructor() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => this.handleNavClick(e));
        });
    }

    handleNavClick(event) {
        event.preventDefault();
        
        const { section, action } = event.target.dataset;
        
        if (section) {
            this.showSection(section);
        } else if (action === 'logout') {
            authComponent?.logout();
        }
    }

    showSection(sectionId) {
        // Check authentication for protected sections
        if (!appState.isUserLoggedIn() && sectionId !== 'login') {
            UIHelpers.showAlert('Please login first.', 'error');
            this.showSection('login');
            return;
        }
        
        // Update UI
        this.updateSectionVisibility(sectionId);
        this.updateActiveNavigation(sectionId);
        this.loadSectionData(sectionId);
    }

    updateSectionVisibility(activeSection) {
        document.querySelectorAll('.section').forEach(section => {
            section.classList.toggle('active', section.id === activeSection);
        });
    }

    updateActiveNavigation(activeSection) {
        document.querySelectorAll('.nav-link').forEach(link => {
            const isActive = link.dataset.section === activeSection;
            link.classList.toggle('active', isActive);
        });
    }

    loadSectionData(sectionId) {
        const sectionLoaders = {
            history: () => appState.isUserLoggedIn() && coverLetterComponent?.loadHistory(),
            profile: () => appState.isUserLoggedIn() && profileComponent?.populateFormFromState()
        };

        sectionLoaders[sectionId]?.();
    }

    // Convenience navigation methods
    navigateToProfile() { this.showSection('profile'); }
    navigateToGenerate() { this.showSection('generate'); }
    navigateToHistory() { this.showSection('history'); }
    navigateToLogin() { this.showSection('login'); }
}

// Initialize and make available globally
window.navigationComponent = new NavigationComponent(); 