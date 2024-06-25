/**
 * Enable the toggle button on OU activities.
 */
function activitySetup() {
    for(const toggle of document.querySelectorAll('.ou-toggle')) {
        toggle.addEventListener('click', () => {
            toggle.classList.toggle('ou-toggle-hidden');
        });
    }
}

// Add an event listener for 'DOMContentLoaded'
document.addEventListener('DOMContentLoaded', () => {
    // Call the function when the DOM is fully loaded
    activitySetup();
});