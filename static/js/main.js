// main.js -- shared front-end behavior across all modules.
// Empty for now (Module 1 is server-rendered forms only, no JS needed);
// later modules (e.g. Disease Detection image preview, Alert badge polling)
// will add their functions here or in module-specific files.

document.addEventListener("DOMContentLoaded", () => {
  // Auto-dismiss flash messages after 5 seconds for a cleaner UX.
  document.querySelectorAll(".alert").forEach((alertEl) => {
    setTimeout(() => {
      const alert = bootstrap.Alert.getOrCreateInstance(alertEl);
      alert.close();
    }, 5000);
  });
});
