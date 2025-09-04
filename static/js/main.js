// Main JavaScript for Marketing Dashboard

// Utility functions
const Utils = {
    // Show loading state
    showLoading: function(element) {
        element.classList.add('loading');
    },
    
    // Hide loading state
    hideLoading: function(element) {
        element.classList.remove('loading');
    },
    
    // Format currency
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    },
    
    // Format date
    formatDate: function(date) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        }).format(new Date(date));
    },
    
    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Form handling
const FormHandler = {
    // Initialize form validation
    init: function() {
        const forms = document.querySelectorAll('form[data-validate]');
        forms.forEach(form => {
            form.addEventListener('submit', this.validateForm);
        });
    },
    
    // Validate form
    validateForm: function(e) {
        const form = e.target;
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('border-red-500');
                isValid = false;
            } else {
                input.classList.remove('border-red-500');
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            showToast('Please fill in all required fields', 'error');
        }
    }
};

// Data table functionality
const DataTable = {
    // Initialize data tables
    init: function() {
        const tables = document.querySelectorAll('table[data-sortable]');
        tables.forEach(table => {
            this.makeSortable(table);
        });
    },
    
    // Make table sortable
    makeSortable: function(table) {
        const headers = table.querySelectorAll('th[data-sort]');
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => {
                this.sortTable(table, header.dataset.sort);
            });
        });
    },
    
    // Sort table
    sortTable: function(table, column) {
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        rows.sort((a, b) => {
            const aVal = a.querySelector(`[data-sort="${column}"]`).textContent;
            const bVal = b.querySelector(`[data-sort="${column}"]`).textContent;
            return aVal.localeCompare(bVal);
        });
        
        rows.forEach(row => tbody.appendChild(row));
    }
};

// Search functionality
const SearchHandler = {
    // Initialize search
    init: function() {
        const searchInputs = document.querySelectorAll('input[data-search]');
        searchInputs.forEach(input => {
            input.addEventListener('input', Utils.debounce((e) => {
                this.performSearch(e.target);
            }, 300));
        });
    },
    
    // Perform search
    performSearch: function(input) {
        const searchTerm = input.value.toLowerCase();
        const targetSelector = input.dataset.search;
        const targets = document.querySelectorAll(targetSelector);
        
        targets.forEach(target => {
            const text = target.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                target.style.display = '';
            } else {
                target.style.display = 'none';
            }
        });
    }
};

// Modal functionality
const ModalHandler = {
    // Initialize modals
    init: function() {
        const modalTriggers = document.querySelectorAll('[data-modal]');
        modalTriggers.forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                this.openModal(trigger.dataset.modal);
            });
        });
        
        const modalCloses = document.querySelectorAll('[data-modal-close]');
        modalCloses.forEach(close => {
            close.addEventListener('click', (e) => {
                e.preventDefault();
                this.closeModal(close.closest('.modal'));
            });
        });
    },
    
    // Open modal
    openModal: function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        }
    },
    
    // Close modal
    closeModal: function(modal) {
        if (modal) {
            modal.classList.add('hidden');
            document.body.style.overflow = 'auto';
        }
    }
};

// Chart functionality (placeholder for future chart integration)
const ChartHandler = {
    // Initialize charts
    init: function() {
        // This would integrate with Chart.js or similar library
        console.log('Chart handler initialized');
    }
};

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    FormHandler.init();
    DataTable.init();
    SearchHandler.init();
    ModalHandler.init();
    ChartHandler.init();
    
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    // Add any custom initialization here
    console.log('Marketing Dashboard initialized');
});

// Export for use in other scripts
window.MarketingDashboard = {
    Utils,
    FormHandler,
    DataTable,
    SearchHandler,
    ModalHandler,
    ChartHandler
};
