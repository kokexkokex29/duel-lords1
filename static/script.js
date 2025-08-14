// Duel Lords Tournament Bot - Client Side JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations
    initializeAnimations();
    
    // Check bot status periodically
    checkBotStatus();
    setInterval(checkBotStatus, 30000); // Check every 30 seconds
    
    // Initialize tooltips and other Bootstrap components
    initializeBootstrapComponents();
    
    // Add smooth scrolling
    addSmoothScrolling();
    
    // Initialize particle effects for hero section
    initializeParticles();
});

function initializeAnimations() {
    // Fade in animations for cards
    const cards = document.querySelectorAll('.feature-card, .command-category, .stat-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('fadeIn');
                }, index * 100);
            }
        });
    }, {
        threshold: 0.1
    });
    
    cards.forEach(card => {
        observer.observe(card);
    });
}

function checkBotStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            updateStatusBadge(data.status === 'online');
        })
        .catch(error => {
            console.error('Error checking bot status:', error);
            updateStatusBadge(false);
        });
}

function updateStatusBadge(isOnline) {
    const statusBadge = document.querySelector('.status-badge');
    const statusIcon = statusBadge?.querySelector('i');
    const statusText = statusBadge?.querySelector('span');
    
    if (statusBadge && statusIcon && statusText) {
        if (isOnline) {
            statusIcon.className = 'fas fa-circle text-success';
            statusText.textContent = 'Bot Online & Ready';
            statusBadge.style.borderColor = '#43b581';
        } else {
            statusIcon.className = 'fas fa-circle text-danger';
            statusText.textContent = 'Bot Offline';
            statusBadge.style.borderColor = '#f04747';
        }
    }
}

function initializeBootstrapComponents() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

function addSmoothScrolling() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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
}

function initializeParticles() {
    // Create floating particles in hero section
    const heroSection = document.querySelector('.hero-section');
    if (!heroSection) return;
    
    for (let i = 0; i < 20; i++) {
        createParticle(heroSection);
    }
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.cssText = `
        position: absolute;
        width: ${Math.random() * 4 + 2}px;
        height: ${Math.random() * 4 + 2}px;
        background: rgba(255, 255, 255, ${Math.random() * 0.5 + 0.2});
        border-radius: 50%;
        left: ${Math.random() * 100}%;
        top: ${Math.random() * 100}%;
        pointer-events: none;
        animation: float ${Math.random() * 10 + 10}s infinite linear;
    `;
    
    container.appendChild(particle);
    
    // Remove particle after animation
    setTimeout(() => {
        if (particle.parentNode) {
            particle.parentNode.removeChild(particle);
        }
    }, 20000);
}

// Leaderboard specific functions
function updateLeaderboardCharts() {
    // This function would be called if we have real-time data updates
    console.log('Updating leaderboard charts...');
}

function formatPlayerStats(player) {
    const totalMatches = player.wins + player.losses + player.draws;
    const winRate = totalMatches > 0 ? (player.wins / totalMatches * 100) : 0;
    const kdRatio = player.deaths > 0 ? (player.kills / player.deaths) : player.kills;
    
    return {
        totalMatches,
        winRate: Math.round(winRate * 10) / 10,
        kdRatio: Math.round(kdRatio * 100) / 100
    };
}

// Utility functions
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Could not copy text: ', err);
        showToast('Failed to copy', 'error');
    });
}

function showToast(message, type = 'info') {
    // Create toast notification
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : 'success'} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    // Add to page
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    toastContainer.appendChild(toast);
    
    // Show toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

// Add loading states for buttons
document.addEventListener('click', function(e) {
    if (!e.target) return;
    
    const btn = e.target.classList && e.target.classList.contains('btn') ? e.target : e.target.closest('.btn');
    if (btn) {
        // Don't add loading state to certain buttons
        if (btn.classList.contains('no-loading') || btn.getAttribute('href')) {
            return;
        }
        
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        btn.disabled = true;
        
        // Reset after 2 seconds (or when page changes)
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }, 2000);
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl+/ to show help
    if (e.ctrlKey && e.key === '/') {
        e.preventDefault();
        showToast('Use Discord slash commands to interact with the bot!', 'info');
    }
    
    // Ctrl+L to go to leaderboard
    if (e.ctrlKey && e.key === 'l') {
        e.preventDefault();
        window.location.href = '/leaderboard';
    }
    
    // Ctrl+H to go home
    if (e.ctrlKey && e.key === 'h') {
        e.preventDefault();
        window.location.href = '/';
    }
});

// Easter egg - Konami code
let konamiCode = [];
const konamiSequence = [
    'ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown',
    'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight',
    'KeyB', 'KeyA'
];

document.addEventListener('keydown', function(e) {
    konamiCode.push(e.code);
    
    if (konamiCode.length > konamiSequence.length) {
        konamiCode.shift();
    }
    
    if (konamiCode.length === konamiSequence.length) {
        let match = true;
        for (let i = 0; i < konamiSequence.length; i++) {
            if (konamiCode[i] !== konamiSequence[i]) {
                match = false;
                break;
            }
        }
        
        if (match) {
            activateEasterEgg();
            konamiCode = []; // Reset
        }
    }
});

function activateEasterEgg() {
    showToast('🏆 DUEL LORDS CHAMPION MODE ACTIVATED! 🏆', 'success');
    
    // Add special effects
    document.body.style.animation = 'rainbow 2s infinite';
    
    // Add rainbow animation
    if (!document.querySelector('#rainbow-style')) {
        const style = document.createElement('style');
        style.id = 'rainbow-style';
        style.textContent = `
            @keyframes rainbow {
                0% { filter: hue-rotate(0deg); }
                100% { filter: hue-rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Reset after 5 seconds
    setTimeout(() => {
        document.body.style.animation = '';
    }, 5000);
}

// Performance monitoring
function logPerformance() {
    if ('performance' in window) {
        const navigation = performance.getEntriesByType('navigation')[0];
        console.log('Page Load Time:', navigation.loadEventEnd - navigation.loadEventStart, 'ms');
        
        const resources = performance.getEntriesByType('resource');
        console.log('Resources loaded:', resources.length);
    }
}

// Log performance after page load
window.addEventListener('load', logPerformance);

// Add visual feedback for interactive elements
document.addEventListener('mouseenter', function(e) {
    if (e.target && e.target.classList && 
        (e.target.classList.contains('feature-card') || 
         e.target.classList.contains('podium-card') || 
         e.target.classList.contains('stat-card'))) {
        e.target.style.transform = 'translateY(-5px) scale(1.02)';
    }
}, true);

document.addEventListener('mouseleave', function(e) {
    if (e.target && e.target.classList &&
        (e.target.classList.contains('feature-card') || 
         e.target.classList.contains('podium-card') || 
         e.target.classList.contains('stat-card'))) {
        e.target.style.transform = '';
    }
}, true);
