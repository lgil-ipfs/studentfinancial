/**
 * Helper to load HTML components into the page
 */
async function loadComponent(elementId, filePath, callback) {
    const element = document.getElementById(elementId);
    if (!element) return;

    try {
        const response = await fetch(filePath);
        if (!response.ok) throw new Error(`Could not fetch ${filePath}`);
        const html = await response.text();
        element.outerHTML = html; // Replace placeholder with content
        if (callback) callback();
    } catch (error) {
        console.error('Error loading component:', error);
    }
}

// Load components
document.addEventListener('DOMContentLoaded', () => {
    loadComponent('header-placeholder', 'header.html', () => {
        // Re-initialize mobile menu after header is loaded
        if (typeof initMobileMenu === 'function') {
            initMobileMenu();
        }
    });
    loadComponent('footer-placeholder', 'footer.html');
});
