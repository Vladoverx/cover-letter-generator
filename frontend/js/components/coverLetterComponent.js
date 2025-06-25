/**
 * Cover Letter Component
 * Handles cover letter generation and history management
 */
class CoverLetterComponent {
    constructor() {
        this.setupEventListeners();
        this.setupStateSubscriptions();
    }

    setupEventListeners() {
        // Form submission
        const coverLetterForm = document.getElementById('cover-letter-form');
        coverLetterForm?.addEventListener('submit', (e) => this.handleGenerate(e));

        // Character count for job description
        const jobDescTextarea = document.getElementById('job-description');
        jobDescTextarea?.addEventListener('input', this.updateCharacterCount);

        // Event delegation for dynamic history actions
        document.addEventListener('click', (e) => this.handleHistoryAction(e));
    }

    setupStateSubscriptions() {
        appState.subscribe('coverLetter', (coverLetter) => {
            if (coverLetter) this.displayLetter(coverLetter);
        });
    }

    async handleGenerate(event) {
        event.preventDefault();
        
        if (!authComponent.requireAuthentication()) return;

        if (!appState.hasValidProfile()) {
            UIHelpers.showAlert('Please save your CV profile first before generating a cover letter.', 'error');
            navigationComponent?.showSection('profile');
            return;
        }

        const generateData = this.collectGenerateData();
        
        // Validate required fields
        if (!this.validateGenerateData(generateData)) return;

        try {
            this.setGenerateButtonLoading(true);
            
            const coverLetter = await apiService.generateCoverLetter(generateData);
            appState.setCurrentCoverLetter(coverLetter);
            UIHelpers.showAlert('Cover letter generated successfully!', 'success');
            
        } catch (error) {
            console.error('Error generating cover letter:', error);
            UIHelpers.showAlert('Error generating cover letter. Please try again.', 'error');
        } finally {
            this.setGenerateButtonLoading(false);
        }
    }

    collectGenerateData() {
        const currentUser = appState.getCurrentUser();
        const formData = FormHelpers.getData('#cover-letter-form');
        
        const jobTitle = formData.get('job_title');
        const companyName = formData.get('company_name');
        
        return {
            user_id: currentUser.id,
            job_title: jobTitle,
            company_name: companyName,
            job_description: formData.get('job_description'),
            title: `Cover Letter for ${jobTitle}${companyName ? ` at ${companyName}` : ''}`
        };
    }

    validateGenerateData({ job_title, company_name, job_description }) {
        if (!job_title || !company_name || !job_description) {
            UIHelpers.showAlert('Please fill in all required fields.', 'error');
            return false;
        }
        return true;
    }

    displayLetter(coverLetter) {
        const letterContainer = document.getElementById('generated-letter');
        const letterText = document.getElementById('letter-text');
        
        if (letterText) {
            letterText.value = coverLetter.content;
            letterText.readOnly = true;
        }
        
        if (letterContainer) {
            letterContainer.style.display = 'block';
            letterContainer.scrollIntoView({ behavior: 'smooth' });
        }
    }

    // History Management
    async loadHistory() {
        if (!appState.hasValidUser()) return;

        try {
            UIHelpers.showLoading('Loading cover letter history...');
            
            const currentUser = appState.getCurrentUser();
            const response = await apiService.getUserCoverLetters(currentUser.id);
            this.displayHistory(response.items || []);
            
        } catch (error) {
            console.error('Error loading cover letter history:', error);
            UIHelpers.showAlert('Error loading cover letter history.', 'error');
        } finally {
            UIHelpers.hideLoading();
        }
    }

    displayHistory(coverLetters) {
        const historyContainer = document.getElementById('letter-history');
        if (!historyContainer) return;
        
        if (!coverLetters || coverLetters.length === 0) {
            historyContainer.innerHTML = `
                <div class="alert alert-info">
                    <p>No cover letters found. Generate your first cover letter to see it here!</p>
                </div>
            `;
            return;
        }
        
        historyContainer.innerHTML = coverLetters.map(letter => this.createHistoryItem(letter)).join('');
    }

    createHistoryItem(letter) {
        return `
            <div class="history-item">
                <h4>${letter.job_title} at ${letter.company_name}</h4>
                <div class="meta">
                    Created: ${DataHelpers.formatDate(letter.created_at)}
                </div>
                <div class="preview">
                    ${letter.content.substring(0, 200)}...
                </div>
                <div class="history-actions">
                    <button type="button" class="btn btn-primary" data-action="view" data-letter-id="${letter.id}">View</button>
                    <button type="button" class="btn btn-danger" data-action="delete" data-letter-id="${letter.id}">Delete</button>
                </div>
            </div>
        `;
    }

    handleHistoryAction(event) {
        const { action, letterId } = event.target.dataset;
        if (!action || !letterId) return;

        const actions = {
            view: () => this.viewLetter(letterId),
            delete: () => this.deleteLetter(letterId)
        };

        actions[action]?.();
    }

    async viewLetter(letterId) {
        try {
            const coverLetter = await apiService.getCoverLetter(letterId);
            appState.setCurrentCoverLetter(coverLetter);
            
            // Populate the generate form with the letter data
            FormHelpers.setValue('job-title', coverLetter.job_title);
            FormHelpers.setValue('company-name', coverLetter.company_name);
            FormHelpers.setValue('job-description', coverLetter.job_description);
            
            navigationComponent?.showSection('generate');
            
        } catch (error) {
            console.error('Error loading cover letter:', error);
            UIHelpers.showAlert('Error loading cover letter.', 'error');
        }
    }

    async deleteLetter(letterId) {
        if (!confirm('Are you sure you want to delete this cover letter?')) return;
        
        try {
            await apiService.deleteCoverLetter(letterId);
            UIHelpers.showAlert('Cover letter deleted successfully!', 'success');
            this.loadHistory();
            
        } catch (error) {
            console.error('Error deleting cover letter:', error);
            UIHelpers.showAlert('Error deleting cover letter.', 'error');
        }
    }

    // UI Utilities
    updateCharacterCount() {
        const textarea = document.getElementById('job-description');
        const charCount = document.getElementById('char-count');
        if (textarea && charCount) {
            charCount.textContent = textarea.value.length;
        }
    }

    setGenerateButtonLoading(isLoading) {
        const generateBtn = document.getElementById('generate-btn');
        if (!generateBtn) return;

        generateBtn.disabled = isLoading;
        generateBtn.innerHTML = isLoading 
            ? '<span class="loading"></span>Generating...'
            : '<span class="btn-text">Generate Cover Letter</span>';
    }
}

// Initialize and make available globally
window.coverLetterComponent = new CoverLetterComponent(); 