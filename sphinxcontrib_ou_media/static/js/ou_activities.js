function ou_activitySetup() {
  for (const toggle of document.querySelectorAll(".ou-toggle")) {
    toggle.addEventListener("click", () => {
      // Toggle the class on the button
      toggle.classList.toggle("ou-toggle-hidden");

      // Find the associated content container
      const answerContent = toggle
        .closest(".ou-activity-answer")
        .querySelector(".ou-activity-answer-content");

      // Toggle the visibility of the content
      if (answerContent) {
        answerContent.style.display =
          answerContent.style.display === "none" ? "block" : "none";
      }
    });
  }
}

// Add an event listener for 'DOMContentLoaded'
document.addEventListener("DOMContentLoaded", () => {
  // Call the function when the DOM is fully loaded
  ou_activitySetup();

  // Initially hide all answer contents
  // TO DO this should be relative to show/hide state?
  document
    .querySelectorAll(".ou-activity-answer-content")
    .forEach((content) => {
      content.style.display = "none";
    });
});
