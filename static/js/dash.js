// Select all the time tags and loop through them
document.querySelectorAll("time").forEach(function (time) {
  // Convert the timestamp in the time tag to a JavaScript Date object
  const timestamp = new Date(time.textContent);

  // Calculate the difference between the current time and the timestamp
  const now = new Date();
  const diff = now.getTime() - timestamp.getTime();

  // Convert the difference to minutes and hours
  const diffMinutes = Math.floor(diff / 60000);
  const diffHours = Math.floor(diff / 3600000);
  const diffDays = Math.floor(diff / 86400000);

  // Format the output based on the time difference
  if (diffMinutes < 1) {
    time.textContent = "Just Now";
  } else if (diffMinutes < 60) {
    time.textContent = diffMinutes + " min ago";
  } else if (diffHours < 24) {
    time.textContent = diffHours + " hours ago";
  } else {
    time.textContent = diffDays + " days ago";
  }
});
