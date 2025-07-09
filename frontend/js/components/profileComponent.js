/**
 * Profile Component - Cleaned and Simplified
 * Handles CV profile management including dynamic forms for experience and education
 */
class ProfileComponent {
    constructor() {
        this.setupEventListeners();
        this.setupStateSubscriptions();
    }

    setupEventListeners() {
        const profileForm = document.getElementById('profile-form');
        profileForm?.addEventListener('submit', (e) => this.handleProfileSubmit(e));

        // Dynamic section buttons
        const addExperienceBtn = document.getElementById('add-experience-btn');
        const addProjectBtn = document.getElementById('add-project-btn');
        const addEducationBtn = document.getElementById('add-education-btn');
        
        addExperienceBtn?.addEventListener('click', () => this.addSection('experience'));
        addProjectBtn?.addEventListener('click', () => this.addSection('projects'));
        addEducationBtn?.addEventListener('click', () => this.addSection('education'));

        // Use event delegation for remove buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('remove-btn')) {
                e.target.closest('.dynamic-section')?.remove();
            }
        });
    }

    setupStateSubscriptions() {
        appState.subscribe('profile', (profile) => profile && this.populateForm(profile));
    }

    async handleProfileSubmit(event) {
        event.preventDefault();
        
        if (!authComponent.requireAuthentication()) return;

        const profileData = this.collectProfileData();
        
        // Validate profile data
        const errors = ValidationHelpers.profileData(profileData);
        if (errors.length > 0) {
            UIHelpers.showAlert(errors.join('. '), 'error');
            return;
        }

        try {
            UIHelpers.showLoading('Saving profile...');
            
            const savedProfile = await this.saveProfile(profileData);
            appState.setCurrentProfile(savedProfile);
            UIHelpers.showAlert('Profile saved successfully!', 'success');
            
        } catch (error) {
            console.error('Error saving profile:', error);
            UIHelpers.showAlert('Error saving profile. Please try again.', 'error');
        } finally {
            UIHelpers.hideLoading();
        }
    }

    collectProfileData() {
        const currentUser = appState.getCurrentUser();
        const formData = FormHelpers.getData('#profile-form');
        
        return {
            user_id: currentUser.id,
            phone: formData.get('phone'),
            summary: formData.get('summary'),
            skills: DataHelpers.parseSkills(formData.get('skills')),
            experience: this.collectExperience(),
            projects: this.collectProjects(),
            education: this.collectEducation()
        };
    }

    async saveProfile(profileData) {
        const existingProfile = appState.getCurrentProfile();
        
        if (existingProfile?.id) {
            return await apiService.updateProfile(existingProfile.id, profileData);
        } else {
            return await apiService.createProfile(profileData);
        }
    }

    // Dynamic section management
    addSection(type) {
        const containerId = `${type}-container`;
        const container = document.getElementById(containerId);
        if (!container) return;

        const sectionHtml = FormBuilder.createSection(type);
        container.insertAdjacentHTML('beforeend', sectionHtml);
    }

    collectExperience() {
        const fieldMappings = {
            title: '[name="experience_position"]',
            company: '[name="experience_company"]',
            start_date: '[name="experience_start_date"]',
            end_date: '[name="experience_end_date"]',
            description: '[name="experience_description"]'
        };

        return FormHelpers.collectDynamicData('#experience-container', fieldMappings);
    }

    collectProjects() {
        const fieldMappings = {
            name: '[name="project_name"]',
            technologies: '[name="project_technologies"]',
            description: '[name="project_description"]'
        };

        const projects = FormHelpers.collectDynamicData('#projects-container', fieldMappings);
        
        // Convert technologies string to array
        return projects.map(project => ({
            ...project,
            technologies: project.technologies ? 
                project.technologies.split(',').map(tech => tech.trim()).filter(Boolean) : 
                []
        }));
    }

    collectEducation() {
        const fieldMappings = {
            degree: '[name="education_degree"]',
            institution: '[name="education_institution"]',
            start_date: '[name="education_start_date"]',
            end_date: '[name="education_end_date"]'
        };

        return FormHelpers.collectDynamicData('#education-container', fieldMappings);
    }

    // Form population methods
    populateFormFromState() {
        const profile = appState.getCurrentProfile();
        if (profile) this.populateForm(profile);
    }

    populateForm(profile) {
        // Populate basic fields
        FormHelpers.setValue('phone', profile.phone);
        FormHelpers.setValue('summary', profile.summary);
        FormHelpers.setValue('skills', DataHelpers.formatSkills(profile.skills));

        // Populate dynamic sections
        this.populateExperience(profile.experience || []);
        this.populateProjects(profile.projects || []);
        this.populateEducation(profile.education || []);
    }

    populateExperience(experiences) {
        const container = document.getElementById('experience-container');
        if (!container) return;

        // Clear existing sections except the first one
        this.clearDynamicSections(container);

        experiences.forEach((exp, index) => {
            if (index === 0) {
                // Fill the first section
                this.fillExistingSection(container.querySelector('.dynamic-section'), exp, 'experience');
            } else {
                // Add new sections for additional items
                const sectionHtml = FormBuilder.createSection('experience', exp);
                container.insertAdjacentHTML('beforeend', sectionHtml);
            }
        });
    }

    populateProjects(projects) {
        const container = document.getElementById('projects-container');
        if (!container) return;

        // Clear existing sections except the first one
        this.clearDynamicSections(container);

        projects.forEach((project, index) => {
            if (index === 0) {
                // Fill the first section
                this.fillExistingSection(container.querySelector('.dynamic-section'), project, 'projects');
            } else {
                // Add new sections for additional items
                const sectionHtml = FormBuilder.createSection('projects', project);
                container.insertAdjacentHTML('beforeend', sectionHtml);
            }
        });
    }

    populateEducation(educations) {
        const container = document.getElementById('education-container');
        if (!container) return;

        // Clear existing sections except the first one
        this.clearDynamicSections(container);

        educations.forEach((edu, index) => {
            if (index === 0) {
                // Fill the first section
                this.fillExistingSection(container.querySelector('.dynamic-section'), edu, 'education');
            } else {
                // Add new sections for additional items
                const sectionHtml = FormBuilder.createSection('education', edu);
                container.insertAdjacentHTML('beforeend', sectionHtml);
            }
        });
    }

    clearDynamicSections(container) {
        const sections = container.querySelectorAll('.dynamic-section');
        // Remove all sections except the first one
        for (let i = 1; i < sections.length; i++) {
            sections[i].remove();
        }
    }

    fillExistingSection(section, data, type) {
        if (!section) return;

        let fieldMappings = {};
        
        if (type === 'experience') {
            fieldMappings = {
                '[name="experience_company"]': data.company,
                '[name="experience_position"]': data.title,
                '[name="experience_start_date"]': data.start_date,
                '[name="experience_end_date"]': data.end_date,
                '[name="experience_description"]': data.description
            };
        } else if (type === 'projects') {
            const technologies = Array.isArray(data.technologies) ? data.technologies.join(', ') : (data.technologies || '');
            fieldMappings = {
                '[name="project_name"]': data.name,
                '[name="project_technologies"]': technologies,
                '[name="project_description"]': data.description
            };
        } else if (type === 'education') {
            fieldMappings = {
                '[name="education_institution"]': data.institution,
                '[name="education_degree"]': data.degree,
                '[name="education_start_date"]': data.start_date,
                '[name="education_end_date"]': data.end_date
            };
        }

        Object.entries(fieldMappings).forEach(([selector, value]) => {
            const element = section.querySelector(selector);
            if (element) element.value = value || '';
        });
    }
}

// Initialize and make available globally
window.profileComponent = new ProfileComponent();