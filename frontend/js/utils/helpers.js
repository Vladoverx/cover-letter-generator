/**
 * Utility Helper Functions - Consolidated and Cleaned
 */

// UI and Alert Management
const UIHelpers = {
    showAlert(message, type = 'info') {
        const container = document.getElementById('alert-container');
        if (!container) return;

        const alertId = `alert-${Date.now()}`;
        const alert = document.createElement('div');
        alert.id = alertId;
        alert.className = `alert alert-${type}`;
        alert.style.marginBottom = '1rem';
        alert.innerHTML = `<p>${message}</p>`;
        
        container.appendChild(alert);
        
        // Auto-remove after 5 seconds
        setTimeout(() => alert?.remove(), 5000);
    },

    showLoading(message = 'Loading...') {
        appState.setLoadingState(true, message);
    },

    hideLoading() {
        appState.setLoadingState(false, '');
    },

    downloadFile(content, filename, type = 'text/plain') {
        const blob = new Blob([content], { type });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        
        URL.revokeObjectURL(url);
        document.body.removeChild(link);
    }
};

// Form Management
const FormHelpers = {
    clear(selector) {
        const form = document.querySelector(selector);
        form?.reset();
    },

    getData(selector) {
        const form = document.querySelector(selector);
        if (!form) throw new Error(`Form not found: ${selector}`);
        return new FormData(form);
    },

    setValue(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) element.value = value || '';
    },

    getValue(elementId) {
        const element = document.getElementById(elementId);
        return element?.value || '';
    },

    setContent(elementId, content) {
        const element = document.getElementById(elementId);
        if (element) element.textContent = content || '';
    },

    // Collect data from dynamic form sections
    collectDynamicData(containerSelector, fieldMappings) {
        const container = document.querySelector(containerSelector);
        if (!container) return [];

        return Array.from(container.querySelectorAll('.dynamic-section'))
            .map(section => {
                const item = {};
                let hasData = false;
                
                Object.entries(fieldMappings).forEach(([key, selector]) => {
                    const element = section.querySelector(selector);
                    if (element?.value) {
                        item[key] = element.value;
                        hasData = true;
                    }
                });
                
                return hasData ? item : null;
            })
            .filter(Boolean);
    }
};

// Validation Utilities
const ValidationHelpers = {
    email(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    },

    name(name) {
        return name?.trim().length >= 2;
    },

    phone(phone) {
        return !phone || /^[\+]?[1-9][\d]{0,15}$/.test(phone.replace(/[\s\-\(\)]/g, ''));
    },

    profileData(data) {
        const errors = [];
        
        if (!data.summary?.trim() || data.summary.trim().length < 10) {
            errors.push('Professional summary must be at least 10 characters long');
        }
        
        if (data.phone && !this.phone(data.phone)) {
            errors.push('Invalid phone number format');
        }
        
        return errors;
    }
};

// Data Processing
const DataHelpers = {
    parseSkills(skillsString) {
        return skillsString?.trim() 
            ? skillsString.split(',')
                .map(skill => skill.trim())
                .filter(Boolean)
                .map(name => ({ name, proficiency: null, category: null }))
            : [];
    },

    formatSkills(skills) {
        return Array.isArray(skills) 
            ? skills.map(skill => skill.name || skill).join(', ')
            : '';
    },

    formatDate(dateString) {
        return dateString ? new Date(dateString).toLocaleDateString() : '';
    },

    sanitizeFilename(filename) {
        return filename.replace(/[^a-z0-9]/gi, '_');
    }
};

// Dynamic Form Builder
const FormBuilder = {
    createSection(type, content = {}) {
        const templates = {
            experience: this.experienceTemplate,
            education: this.educationTemplate
        };
        
        const template = templates[type];
        return template ? template(content) : '';
    },

    experienceTemplate(data = {}) {
        return `
            <div class="dynamic-section">
                <button type="button" class="remove-btn">×</button>
                <div class="form-row">
                    <div class="form-group">
                        <label>Company</label>
                        <input type="text" name="experience_company" value="${data.company || ''}" placeholder="Company name">
                    </div>
                    <div class="form-group">
                        <label>Position</label>
                        <input type="text" name="experience_position" value="${data.title || ''}" placeholder="Job title">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Start Date</label>
                        <input type="month" name="experience_start_date" value="${data.start_date || ''}">
                    </div>
                    <div class="form-group">
                        <label>End Date</label>
                        <input type="month" name="experience_end_date" value="${data.end_date || ''}">
                    </div>
                </div>
                <div class="form-group">
                    <label>Description</label>
                    <textarea name="experience_description" rows="3" placeholder="Job responsibilities and achievements...">${data.description || ''}</textarea>
                </div>
            </div>
        `;
    },

    educationTemplate(data = {}) {
        return `
            <div class="dynamic-section">
                <button type="button" class="remove-btn">×</button>
                <div class="form-row">
                    <div class="form-group">
                        <label>Institution</label>
                        <input type="text" name="education_institution" value="${data.institution || ''}" placeholder="University/School name">
                    </div>
                    <div class="form-group">
                        <label>Degree</label>
                        <input type="text" name="education_degree" value="${data.degree || ''}" placeholder="Degree/Certification">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Start Date</label>
                        <input type="month" name="education_start_date" value="${data.start_date || ''}">
                    </div>
                    <div class="form-group">
                        <label>End Date</label>
                        <input type="month" name="education_end_date" value="${data.end_date || ''}">
                    </div>
                </div>
            </div>
        `;
    }
};

// Make available globally
Object.assign(window, {
    UIHelpers,
    FormHelpers,
    ValidationHelpers, 
    DataHelpers,
    FormBuilder
}); 