const table = document.querySelector("#table");
const search = document.querySelector("#search");

// Add event listener to search input
search.addEventListener("keyup", () => {
  const searchText = search.value.toLowerCase();
  const rows = table.querySelectorAll("tbody tr");
  rows.forEach((row) => {
    const columns = row.querySelectorAll("td");
    let found = false;
    columns.forEach((column) => {
      if (column.textContent.toLowerCase().includes(searchText)) {
        found = true;
      }
    });
    if (found) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  });
});

function submit(user_id, book_id) {
  // create an XHR object
  const xhr = new XMLHttpRequest();

  // set the request method and URL
  xhr.open("POST", "/return");

  // set the request headers
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

  // set the request body
  const requestBody = `book_id=${book_id}&user_id=${user_id}`;

  // handle the response
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        alert(xhr.responseText);
        location.reload();
      } else {
        alert("Something went wrong");
      }
    }
  };
  // send the request
  xhr.send(requestBody);
}
