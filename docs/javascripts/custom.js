document.addEventListener("DOMContentLoaded", function() {
    /* پیدا کردن دکمه‌های باز و بسته‌شونده‌ای که فقط در سطح اول منوی اصلی هستند */
    var firstLevelToggles = document.querySelectorAll('.md-sidebar--primary .md-nav--primary > .md-nav__list > .md-nav__item--nested > .md-nav__toggle');
    
    firstLevelToggles.forEach(function(toggle) {
        toggle.checked = true; /* تغییر وضعیت به حالت باز شده */
    });
});