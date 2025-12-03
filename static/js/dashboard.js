// Dashboard functionality

// Smooth scroll to sections
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.dashboard-section').forEach(section => {
    section.style.opacity = '0';
    section.style.transform = 'translateY(20px)';
    section.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(section);
});

// Copy share link functionality
function copyShareLink() {
    const url = window.location.href;
    navigator.clipboard.writeText(url).then(() => {
        alert('Dashboard link copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// Export functionality
function exportDashboard() {
    window.print();
}

// Theme switcher (if needed in future)
function switchTheme(theme) {
    document.body.className = `dashboard-body layout-${theme}`;
}
