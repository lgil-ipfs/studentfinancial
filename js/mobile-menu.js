function initMobileMenu() {
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    const body = document.body;

    if (mobileNavToggle && navLinks) {
        // Remove existing listeners if any (simple way is to clone and replace, but here we'll just check)
        // For simplicity in this static site, we'll assume it's called once per load or after dynamic load.
        
        mobileNavToggle.addEventListener('click', () => {
            mobileNavToggle.classList.toggle('active');
            navLinks.classList.toggle('active');
            
            if (navLinks.classList.contains('active')) {
                body.style.overflow = 'hidden';
            } else {
                body.style.overflow = '';
            }
        });

        const links = navLinks.querySelectorAll('a');
        links.forEach(link => {
            link.addEventListener('click', () => {
                mobileNavToggle.classList.remove('active');
                navLinks.classList.remove('active');
                body.style.overflow = '';
            });
        });
    }
}

document.addEventListener('DOMContentLoaded', initMobileMenu);

