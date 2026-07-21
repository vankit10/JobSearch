// ==========================================================
// Job Agent Dashboard JavaScript
// ==========================================================

document.addEventListener("DOMContentLoaded", function () {

    // -----------------------------
    // Live Search
    // -----------------------------
    const searchInput = document.querySelector(
        'input[name="keyword"]'
    );

    if (searchInput) {

        let timer;

        searchInput.addEventListener("keyup", function () {

            clearTimeout(timer);

            timer = setTimeout(function () {

                const form = searchInput.closest("form");

                if (form) {
                    form.submit();
                }

            }, 500);

        });

    }

    // -----------------------------
    // Favorites
    // -----------------------------
    document.querySelectorAll(".favorite-btn").forEach(function (button) {

        const jobId = button.dataset.job;

        if (!jobId) return;

        let favorites = JSON.parse(
            localStorage.getItem("favorites") || "[]"
        );

        if (favorites.includes(jobId)) {
            button.classList.add("btn-warning");
        }

        button.addEventListener("click", function () {

            favorites = JSON.parse(
                localStorage.getItem("favorites") || "[]"
            );

            if (favorites.includes(jobId)) {

                favorites = favorites.filter(
                    id => id !== jobId
                );

                button.classList.remove("btn-warning");

            } else {

                favorites.push(jobId);

                button.classList.add("btn-warning");

            }

            localStorage.setItem(
                "favorites",
                JSON.stringify(favorites)
            );

        });

    });

    // -----------------------------
    // Browser Notifications
    // -----------------------------
    if ("Notification" in window) {

        Notification.requestPermission();

    }

    // -----------------------------
    // Auto Refresh Countdown
    // -----------------------------
    const timerElement =
        document.getElementById("refreshCountdown");

    let seconds = 60;

    if (timerElement) {

        timerElement.innerHTML = seconds;

        setInterval(function () {

            seconds--;

            timerElement.innerHTML = seconds;

            if (seconds <= 0) {

                location.reload();

            }

        }, 1000);

    }

    // -----------------------------
    // Fade In Animation
    // -----------------------------
    document.querySelectorAll(".card").forEach(function (card) {

        card.classList.add("fade-in");

    });

    // -----------------------------
    // Loading Overlay
    // -----------------------------
    document.querySelectorAll("a").forEach(function (link) {

        link.addEventListener("click", function () {

            const overlay =
                document.getElementById("loadingOverlay");

            if (overlay) {

                overlay.classList.remove("d-none");

            }

        });

    });

});