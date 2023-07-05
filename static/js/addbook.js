function addBook() {
  const name = document.getElementById('name').value;
  const book_id = document.getElementById('book_id').value;
  const category = document.getElementById('category').value;
  const status = document.getElementById('status').value;
  const copies_available = document.getElementById('copies_available').value;
  const added_on = document.getElementById('added_on').value;
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/addbook');
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onload = function() {
    if (xhr.status === 200) {
      alert('Book added successfully!');
      window.location.href = '/books';
    }
  };
  xhr.send(JSON.stringify({name, book_id, category, copies_available, status, added_on}));
}
