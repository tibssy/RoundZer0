document.addEventListener('DOMContentLoaded', () => {
    const header = document.getElementsByTagName("header")[0];
    const navBar = document.getElementsByClassName("navbar")[0];

    window.addEventListener("scroll", () => {
        if (window.scrollY >= 10) {
            header.classList.remove("p-2");
            navBar.classList.remove("rounded-3");
        } else {
            header.classList.add("p-2");
            navBar.classList.add("rounded-3");
        }
    });
});
