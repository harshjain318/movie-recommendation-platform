/**
 * Movie Recommendation Platform 2025
 * Frontend JavaScript - Autocomplete & Interactivity
 */

document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("movie-search");
    const resultsContainer = document.getElementById("autocomplete-results");

    if (!searchInput || !resultsContainer) return;

    let debounceTimer;
    let selectedIndex = -1;

    // Debounced search as user types
    searchInput.addEventListener("input", (e) => {
        const query = e.target.value.trim();
        clearTimeout(debounceTimer);

        if (query.length < 2) {
            resultsContainer.classList.remove("active");
            resultsContainer.innerHTML = "";
            return;
        }

        debounceTimer = setTimeout(() => fetchSuggestions(query), 250);
    });

    // Keyboard navigation in autocomplete
    searchInput.addEventListener("keydown", (e) => {
        const items = resultsContainer.querySelectorAll(".autocomplete-item");
        if (!items.length) return;

        if (e.key === "ArrowDown") {
            e.preventDefault();
            selectedIndex = Math.min(selectedIndex + 1, items.length - 1);
            updateSelection(items);
        } else if (e.key === "ArrowUp") {
            e.preventDefault();
            selectedIndex = Math.max(selectedIndex - 1, -1);
            updateSelection(items);
        } else if (e.key === "Enter" && selectedIndex >= 0) {
            e.preventDefault();
            searchInput.value = items[selectedIndex].textContent;
            resultsContainer.classList.remove("active");
            document.getElementById("search-form").submit();
        }
    });

    // Close autocomplete when clicking outside
    document.addEventListener("click", (e) => {
        if (!e.target.closest(".search-container")) {
            resultsContainer.classList.remove("active");
        }
    });

    async function fetchSuggestions(query) {
        try {
            const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const suggestions = await response.json();

            if (suggestions.length === 0) {
                resultsContainer.classList.remove("active");
                resultsContainer.innerHTML = "";
                return;
            }

            resultsContainer.innerHTML = suggestions
                .map(
                    (title) =>
                        `<div class="autocomplete-item">${escapeHtml(title)}</div>`
                )
                .join("");

            resultsContainer.classList.add("active");
            selectedIndex = -1;

            // Click to select
            resultsContainer.querySelectorAll(".autocomplete-item").forEach((item) => {
                item.addEventListener("click", () => {
                    searchInput.value = item.textContent;
                    resultsContainer.classList.remove("active");
                    document.getElementById("search-form").submit();
                });
            });
        } catch (error) {
            console.error("Autocomplete error:", error);
        }
    }

    function updateSelection(items) {
        items.forEach((item, i) => {
            item.classList.toggle("selected", i === selectedIndex);
        });

        if (selectedIndex >= 0) {
            searchInput.value = items[selectedIndex].textContent;
        }
    }

    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }
});
