// Obsługa uczestnictwa w wydarzeniach
document.addEventListener('DOMContentLoaded', function() {

    // Filtrowanie wydarzeń
    const filterForm = document.querySelector('.filter-form');
    if (filterForm) {
        filterForm.addEventListener('change', function() {
            this.submit();
        });
    }

    // Tooltips
    initializeTooltips();

    // Animacje
    initializeAnimations();

    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const dropdowns = document.querySelectorAll('.dropdown');

    if (mobileMenuToggle && navMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            navMenu.classList.toggle('active');

            // Zamknij wszystkie dropdowny przy otwieraniu/zamykaniu menu
            if (!navMenu.classList.contains('active')) {
                dropdowns.forEach(dropdown => {
                    dropdown.classList.remove('active');
                });
            }
        });

        // Zamknij menu po kliknięciu w link
        const navLinks = document.querySelectorAll('.nav-menu a');
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                // Jeśli to link w dropdownie na mobile, nie zamykaj całego menu
                if (window.innerWidth <= 768 && this.closest('.dropdown-menu')) {
                    e.stopPropagation();
                    return;
                }

                mobileMenuToggle.classList.remove('active');
                navMenu.classList.remove('active');

                // Zamknij wszystkie dropdowny
                dropdowns.forEach(dropdown => {
                    dropdown.classList.remove('active');
                });
            });
        });

        // Obsługa dropdownów na mobile
        if (window.innerWidth <= 768) {
            dropdowns.forEach(dropdown => {
                const dropdownLink = dropdown.querySelector('a');

                dropdownLink.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();

                    // Zamknij inne dropdowny
                    dropdowns.forEach(otherDropdown => {
                        if (otherDropdown !== dropdown) {
                            otherDropdown.classList.remove('active');
                        }
                    });

                    // Przełącz aktualny dropdown
                    dropdown.classList.toggle('active');
                });
            });

            // Zamknij dropdowny po kliknięciu poza menu
            document.addEventListener('click', function(e) {
                if (!e.target.closest('.nav-menu')) {
                    dropdowns.forEach(dropdown => {
                        dropdown.classList.remove('active');
                    });
                }
            });
        }

        // Zamknij menu przy resize na desktop
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768) {
                mobileMenuToggle.classList.remove('active');
                navMenu.classList.remove('active');
                dropdowns.forEach(dropdown => {
                    dropdown.classList.remove('active');
                });
            }
        });
    }
});


// Inicjalizacja tooltipów
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(event) {
    const tooltipText = this.getAttribute('data-tooltip');
    const tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip';
    tooltip.textContent = tooltipText;
    document.body.appendChild(tooltip);

    const rect = this.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
}

function hideTooltip() {
    const tooltip = document.querySelector('.custom-tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

// Animacje
function initializeAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });

    document.querySelectorAll('.event-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
}

// Wyszukiwanie w czasie rzeczywistym
let searchTimeout;
function handleSearchInput(input) {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        input.form.submit();
    }, 500);
}