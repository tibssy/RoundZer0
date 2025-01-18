document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector("header");
    const navBar = document.querySelector(".navbar");

    const handleScroll = () => {
        const isScrolled = window.scrollY >= 10;
        header.classList.toggle("p-2", !isScrolled);
        navBar.classList.toggle("rounded-3", !isScrolled);
    };

    window.addEventListener("scroll", handleScroll);

    const messages = document.querySelectorAll('.alert.fade.show');
    messages.forEach(message => {
        message.classList.add('fade-out');
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(message);
            bsAlert.close();
        }, 3000);
    });
});
