function handleLike(postId) {
  fetch(`http://localhost:8000/like/${postId}`)
    .then(request => request.json())
    .then(likesCount => {
      document.querySelector(`#post-${postId}-likes`).innerText = `💖 ${likesCount}`

      document.querySelector(`#post-${postId}-like-container`).innerHTML = `
        <a id='post-${postId}-unlike-btn' href="#unlike" onclick="handleUnlike(${postId})">Unlike</a>
      `
    })
}

function handleUnlike(postId) {
  fetch(`http://localhost:8000/unlike/${postId}`)
    .then(request => request.json())
    .then(likesCount => {
      document.querySelector(`#post-${postId}-likes`).innerText = `💖 ${likesCount}`

      document.querySelector(`#post-${postId}-like-container`).innerHTML = `
        <a id='post-${postId}-like-btn' href="#like" onclick="handleLike(${postId})">Like</a>
      `
    })
}