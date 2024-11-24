// JavaScript to dynamically show the preview on hover
document.addEventListener("DOMContentLoaded", function() {
    const posters = document.querySelectorAll('.movie-poster');

    posters.forEach(poster => {
        poster.addEventListener('mouseenter', function() {
            const preview = poster.querySelector('.movie-preview');
            if (preview) {
                preview.style.display = 'block';
            }
        });

        poster.addEventListener('mouseleave', function() {
            const preview = poster.querySelector('.movie-preview');
            if (preview) {
                preview.style.display = 'none';
            }
        });
    });
});
