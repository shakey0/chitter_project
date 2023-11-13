
document.addEventListener('DOMContentLoaded', function() {

    const openBoxButtons = document.querySelectorAll('[data-amend-peep-tags-target], [data-delete-peep-target], [data-picture-peep-target], [data-post-peep-target], [data-amend-user-tags-target]');
    const cancelBoxButtons = document.querySelectorAll('[data-cancel-button]');
    const overlay = document.getElementById('overlay');

    openBoxButtons.forEach(button => {
        button.addEventListener('click', () => {
            const boxSelector = button.dataset.amendPeepTagsTarget || button.dataset.deletePeepTarget || button.dataset.picturePeepTarget || button.dataset.postPeepTarget || button.dataset.amendUserTagsTarget;
            const box = document.querySelector(boxSelector);
            openBox(box);
        });
    });

    overlay.addEventListener('click', () => {
        const boxes = document.querySelectorAll('.amend-p-t-box.active, .delete-peep-box.active, .picture-peep-box.active, .new-peep-container.active, .amend-u-t-box.active');
        boxes.forEach(box => {
            closeBox(box);
        });
    });

    cancelBoxButtons.forEach(button => {
        button.addEventListener('click', () => {
            const box = button.closest('.amend-p-t-box') || button.closest('.delete-peep-box') || button.closest('.picture-peep-box') || button.closest('.new-peep-container') || button.closest('.amend-u-t-box');
            closeBox(box);
        });
    });

    function openBox(box) {
        if (box == null) return;
        box.classList.add('active');
        overlay.classList.add('active');
    }

    function closeBox(box) {
        if (box == null) return;
        box.classList.remove('active');
        overlay.classList.remove('active');
    }
    
    // Save the scroll position when a form is submitted
    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", function() {
            sessionStorage.setItem("scrollPosition", window.scrollY);
        });
    });

    var scrollSaveElement = document.querySelector(".scroll-save");

    if (scrollSaveElement) {
        scrollSaveElement.addEventListener("change", function() {
            sessionStorage.setItem("scrollPosition", window.scrollY);
            document.getElementById('moodForm').submit();
        });
    }

    // Restore the scroll position once the document is loaded
    if (sessionStorage.getItem("scrollPosition") !== null) {
        window.scrollTo(0, parseInt(sessionStorage.getItem("scrollPosition")));
        sessionStorage.removeItem("scrollPosition");  // Cleanup
    }

});


function updateURL() {
    const selectedValue = document.querySelector('.select-by-tag-tag').value;
    window.location.href = '?by_tag=' + selectedValue;
}


function adjustUserNameHeaderSize() {
    const elements = document.querySelectorAll('.user-name-header-tag');
    elements.forEach(el => {
        let fontSize = parseFloat(window.getComputedStyle(el, null).getPropertyValue('font-size')); // Get current font size in pixels
        while (el.offsetWidth > 220 && fontSize > 0) { // Check if the element's width exceeds 250px
        fontSize -= 1; // Reduce the font size by 1 pixel
        el.style.fontSize = `${fontSize}px`; // Apply the new font size
        }
    });
}

adjustUserNameHeaderSize();


const chooseFilesButton = document.querySelector('.choose-files-button');

if (chooseFilesButton) {
    chooseFilesButton.addEventListener('change', function(event) {
        let files = event.target.files;
        let fileNames = Array.from(files).map(file => file.name).join(', ');
        
        document.querySelector('.file-name').textContent = fileNames ? `(${fileNames})` : '';
    });
}


function adjustVUserHeaderSize() {
    const elements = document.querySelectorAll('.v-user-header-tag');
    elements.forEach(el => {
        let fontSize = parseFloat(window.getComputedStyle(el, null).getPropertyValue('font-size')); // Get current font size in pixels
        while (el.offsetWidth > 360 && fontSize > 0) { // Check if the element's width exceeds 250px
        fontSize -= 1; // Reduce the font size by 1 pixel
        el.style.fontSize = `${fontSize}px`; // Apply the new font size
        }
    });
}

adjustVUserHeaderSize();


$(document).ready(function(){

    $('.select-mood-tag, .select-mood-tag-user').on('change', handleMoodFormSubmit);
    $('.like-button, .liked-button').on('click', handleLikeButtonClick);

    function handleMoodFormSubmit() {
        
        const $selected = $(this);
        const formData = $selected.closest('form').serialize();

        $.ajax({
            url: '/change_mood',
            type: 'POST',
            data: formData,
            success: function(response) {
                if (response.success) {
                    // Do nothing
                } else {
                    alert(response.error || 'An error occurred while processing your request.');
                }
            },
            error: function() {
                alert('An unexpected error occurred. Please try again later.');
            }
        });
    }

    function handleLikeButtonClick() {

        const $button = $(this);
        const $form = $button.closest('form');
        const $likedInput = $form.find('input[name="liked"]');
        const formData = $form.serialize();

        $.ajax({
            url: '/like',
            type: 'POST',
            data: formData,
            success: function(response) {
                if (response.success) {
                    const peepId = $button.siblings("input[name='peep_id']").val(); // Get peep_id from the hidden input
                    const $peepContainer = $(`.peep-container[data-peep-id='${peepId}']`);
                    
                    // Toggle the button's appearance and functionality based on response
                    if ($button.hasClass('liked-button')) {
                        $button.removeClass('liked-button').addClass('like-button').text('Like');
                        $likedInput.val("no");
                    } else {
                        $button.removeClass('like-button').addClass('liked-button').text('Liked');
                        $likedInput.val("yes");
                    }
                    
                    // Update the number of likes based on the response
                    const newLikeCount = response.newLikeCount;
                    const $likesCard = $peepContainer.find('.likes-card');
            
                    if (newLikeCount === 0) {
                        $likesCard.text('Ready for peeping');
                    } else if (newLikeCount === 1) {
                        $likesCard.text('Liked by 1 peeper');
                    } else {
                        $likesCard.text(`Liked by ${newLikeCount} peepers`);
                    }
                } else {
                    // Handle any errors (you can send custom error messages from your backend)
                    alert(response.error || 'An error occurred while processing your request.');
                }
            },
            error: function() {
                alert('An unexpected error occurred. Please try again later.');
            }
        });
    }
});