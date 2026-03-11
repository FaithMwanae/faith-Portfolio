// 1. Wait for the page to fully load
document.addEventListener('DOMContentLoaded', () => {

    // --- AUTO-HIDE FLASH MESSAGES ---
    // This looks for any success messages from Flask and hides them after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    if (flashMessages) {
        setTimeout(() => {
            flashMessages.forEach(msg => {
                msg.style.transition = "opacity 1s ease";
                msg.style.opacity = "0";
                setTimeout(() => msg.remove(), 1000);
            });
        }, 5000);
    }

    // --- SMOOTH SCROLLING FOR NAVIGATION ---
    // Makes the page slide nicely when you click "About" or "Contact"
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const targetId = link.getAttribute('href');
            if (targetId.startsWith('#')) {
                e.preventDefault();
                document.querySelector(targetId).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // --- BUTTON LOADING STATE ---
    // Disables the 'Send' button after clicking to prevent duplicate emails
    const contactForm = document.querySelector('form');
    if (contactForm) {
        contactForm.addEventListener('submit', () => {
            const btn = contactForm.querySelector('button');
            btn.innerHTML = "Sending...";
            btn.style.opacity = "0.7";
            btn.disabled = true;
        });
    }

});