function handleLike(postId) {
  fetch(`http://localhost:8000/like/${postId}`)
    .then(request => request.json())
    .then(likesCount => {
      document.querySelector(`#post-${postId}-likes`).innerText = `💖 ${likesCount}`
    })
}

function handleUnlike(postId) {
  fetch(`http://localhost:8000/unlike/${postId}`)
    .then(request => request.json())
    .then(likesCount => {
      document.querySelector(`#post-${postId}-likes`).innerText = `💖 ${likesCount}`
    })
}