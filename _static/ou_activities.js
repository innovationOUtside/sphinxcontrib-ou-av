function ou_activitySetup() {
  for (const toggle of document.querySelectorAll(".ou-toggle")) {
    toggle.addEventListener("click", () => {
      // Find the associated content container
      const answerContent = toggle
        .closest(".ou-activity-answer")
        .querySelector(".ou-activity-answer-content");

      if (answerContent) {
        // Toggle the visibility of the content
        answerContent.classList.toggle("ou-hidden");

        // Toggle the button state
        toggle.classList.toggle("ou-toggle-hidden");
      }
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  ou_activitySetup();

  // Initially hide all answer contents
  document
    .querySelectorAll(".ou-activity-answer-content")
    .forEach((content) => {
      content.classList.add("ou-hidden");
    });
});
