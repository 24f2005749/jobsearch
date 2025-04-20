// Wait for DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get form element
    const searchForm = document.querySelector('form');
    
    if (searchForm) {
        // Add submit event listener to show loading state
        searchForm.addEventListener('submit', function() {
            const submitButton = document.querySelector('.search-button');
            if (submitButton) {
                submitButton.textContent = 'Searching...';
                submitButton.disabled = true;
            }
        });
    }
    
    // Add job card hover effects
    const jobCards = document.querySelectorAll('.job-card');
    jobCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.1)';
            this.style.transition = 'transform 0.3s, box-shadow 0.3s';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 5px rgba(0, 0, 0, 0.1)';
        });
    });
});