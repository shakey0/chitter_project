document.addEventListener('DOMContentLoaded', function() {

    const openBoxButtons = document.querySelectorAll('[data-amend-peep-tags-target], [data-delete-peep-target], [data-picture-peep-target]')
    const cancelBoxButtons = document.querySelectorAll('[data-cancel-button]')
    const overlay = document.getElementById('overlay')

    openBoxButtons.forEach(button => {
        button.addEventListener('click', () => {
            const boxSelector = button.dataset.amendPeepTagsTarget || button.dataset.deletePeepTarget || button.dataset.picturePeepTarget;
            const box = document.querySelector(boxSelector);
            openBox(box)
        })
    })

    overlay.addEventListener('click', () => {
        const boxes = document.querySelectorAll('.amend-p-t-box.active, .delete-peep-box.active, .picture-peep-box.active')
        boxes.forEach(box => {
            closeBox(box)
        })
    })

    cancelBoxButtons.forEach(button => {
        button.addEventListener('click', () => {
            const box = button.closest('.amend-p-t-box') || button.closest('.delete-peep-box') || button.closest('.picture-peep-box');
            closeBox(box)
        })
    })

    function openBox(box) {
        if (box == null) return
        box.classList.add('active')
        overlay.classList.add('active')
    }

    function closeBox(box) {
        if (box == null) return
        box.classList.remove('active')
        overlay.classList.remove('active')
    }

    function updateURL() {
        const selectedValue = document.querySelector('.select-by-tag-tag').value;
        window.location.href = '?by_tag=' + selectedValue;
    }
});


// document.addEventListener("DOMContentLoaded", function(event) {
    
//     // Save the scroll position when a form is submitted
//     document.querySelectorAll("form").forEach(form => {
//         form.addEventListener("submit", function(event) {
//             sessionStorage.setItem("scrollPosition", window.scrollY);
//         });
//     });

//     // Save the scroll position when the link is clicked
//     document.querySelectorAll(".select_peep_tags-button, .delete_peep-button, .image_message-tag, .cancel-button, .close-button").forEach(button => {
//         button.addEventListener("click", function(event) {
//             sessionStorage.setItem("scrollPosition", window.scrollY);

//             // Prevent default navigation, then proceed after a short delay
//             event.preventDefault();
//             setTimeout(() => {
//                 window.location.href = event.target.href;
//             }, 50);
//         });
//     });

//     // Restore the scroll position once the document is loaded
//     if (sessionStorage.getItem("scrollPosition") !== null) {
//         window.scrollTo(0, parseInt(sessionStorage.getItem("scrollPosition")));
//         sessionStorage.removeItem("scrollPosition");  // Cleanup
//     }
// });
