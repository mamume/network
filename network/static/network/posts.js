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

function editPost(postId, parent) {
  console.log(parent)
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
    .then(data => {
      console.log(data)
      // parent.innerHTML = `
      //   <a href={% url 'profile' post.owner.id %}><b>{{ post.owner }}</b></a>
      //   {% if request.user == post.owner %}
      //     <a href="#edit" class="edit-link">Edit</a>
      //     <input class="post-id" type="hidden" value={{ post.id }} />
      //   {% endif %}
      //   <div class="post-text">{{ post.text }}</div>
      //   <div class="text-secondary">
      //       <div>{{ post.created_at }}</div>
      //       <div>💖 {{ post.likes.count }}</div>
      //       <div>Comment</div>
      //   </div>
      // `
    })
}

document.addEventListener('DOMContentLoaded', () => {
  editLinks = document.querySelectorAll('.edit-link').forEach(editLink => {
    editLink.addEventListener('click', () => {
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
          <button onclick="editPost(${postId})" class="btn btn-primary">Save</button>
      `
    })
  })
})