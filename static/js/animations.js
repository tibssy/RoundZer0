document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector("header");
    const navBar = document.querySelector(".navbar");

    /**
     * Adjusts the header and navbar styles based on the scroll position.
     */
    const handleScroll = () => {
        const isScrolled = window.scrollY >= 10;
        header.classList.toggle("p-2", !isScrolled);
        navBar.classList.toggle("rounded-3", !isScrolled);
    };

    // Listen for scroll events to adjust styles dynamically.
    window.addEventListener("scroll", handleScroll);

    const messages = document.querySelectorAll('.alert.fade.show');

    /**
     * Adds a fade-out effect to alert messages and closes them after a delay.
     */
    messages.forEach(message => {
        message.classList.add('fade-out'); // Add fade-out animation.
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(message);
            bsAlert.close(); // Close the alert after 3 seconds.
        }, 3000);
    });
});
