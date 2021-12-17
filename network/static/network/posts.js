// Source => https://stackoverflow.com/questions/40893537/fetch-set-cookies-and-csrf
function getCookie(name) {
  if (!document.cookie) {
    return null;
  }

  const xsrfCookies = document.cookie.split(';')
    .map(c => c.trim())
    .filter(c => c.startsWith(name + '='));

  if (xsrfCookies.length === 0) {
    return null;
  }
  return decodeURIComponent(xsrfCookies[0].split('=')[1]);
}

function editPost(postId) {
  editedText = document.querySelector(`#edit-post-${postId}`).value.trim()
  data = {
    id: postId,
    text: editedText
  }

  fetch('http://localhost:8000/edit/', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json; charset=UTF-8',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(data),
  })
    .then(res => res.json())
    .then(({ likes_count, owner_id, owner_username, post_id, text, created_at }) => {
      console.log(created_at)
      const editAnchor = document.createElement("a")
      editAnchor.innerText = "Edit"
      editAnchor.addEventListener("click", (e, created_at) => handleEdit(e, created_at))
      editAnchor.setAttribute('href', "#edit")
      console.log(String(editAnchor))

      const postCard = document.querySelector(`#post-card-${postId}`)
      const frag = document.createRange().createContextualFragment(`
        <a href='http://localhost:8000/profile/${owner_id}'><b>${owner_username}</b></a>
      `)
      frag.appendChild(editAnchor)
      const frag2 = document.createRange().createContextualFragment(`
        <input class="post-id" type="hidden" value=${post_id} />
          <div class="post-text">${text}</div>
          <div class="text-secondary">
            <div>${created_at}</div>
            <div>💖 ${likes_count}</div>
            <div>Comment</div>
        </div>
      `)
      postCard.replaceChildren(frag)
      postCard.appendChild(frag2)
    })
}

function handleEdit(e) {
  editLink = e.target
  const parent = editLink.parentNode
  const postText = parent.querySelector('.post-text').innerText
  const postId = parent.querySelector(".post-id").value

  parent.innerHTML = `
    <div class="mb-3">
      <label for="edit-post-${postId}" class="form-label">Edit Post</label>
      <textarea id="edit-post-${postId}" name="edited-text" class="form-control" rows="3">
        ${postText}
      </textarea>
      <input type="hidden" name="postId" value=${postId} />
    </div>
    <button onclick='editPost(${postId})' class="btn btn-primary">Save</button>
  `
}