document.addEventListener('DOMContentLoaded', () => {
    const overlay = document.getElementById('galleryOverlay');
    const galleryImage = document.getElementById('gallery-image');
    // Helper to hide the overlay and restore scrolling
    function hideOverlay() {
        overlay.style.display = 'none';
        galleryImage.src = '';
        document.body.style.overflow = '';
    }

    // Attach click handlers to thumbnails to open the overlay
    document.querySelectorAll('.clickable-image').forEach((thumb) => {
        thumb.addEventListener('click', () => {
            galleryImage.src = thumb.dataset.imageUrl || thumb.src;
            overlay.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        });
    });

    // Close when clicking the backdrop (but not when clicking the image)
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) hideOverlay();
    });

    // Close button inside the overlay
    const btnClose = overlay.querySelector('.gallery-close');
    if (btnClose) btnClose.addEventListener('click', hideOverlay);
});
