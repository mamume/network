function handleLike(postId) {
  console.log(postId)

  fetch(`http://localhost:8000/like/${postId}`)
    .then(request => request.json())
    .then(data => console.log(data))
}