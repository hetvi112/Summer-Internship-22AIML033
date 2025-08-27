document.getElementById("recommendation-form").addEventListener("submit", function(event) {
  event.preventDefault();

  const name = document.getElementById("rec-name").value || "Anonymous";
  const message = document.getElementById("rec-message").value;

  if (message.trim() === "") {
    alert("Please enter a recommendation message!");
    return;
  }

  // Create new recommendation element
  const newRec = document.createElement("p");
  newRec.textContent = `"${message}" - ${name}`;

  // Add to list
  document.getElementById("recommendation-list").appendChild(newRec);

  // Reset form
  document.getElementById("recommendation-form").reset();

  // Popup alert
  alert("Thank you for your recommendation!");
});
