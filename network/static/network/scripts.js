var following_btn = document.querySelectorAll('.following-btn');
var action_btn = document.querySelectorAll('.action-btn');
var like_btn = document.querySelectorAll('.like-btn');



document.addEventListener('DOMContentLoaded', function() {

  following_btn.forEach(following_btn => {
    following_btn.addEventListener('click', () => {
      var action = following_btn.dataset.action
      var user = following_btn.dataset.user

      profileFollowing(action, user)
    })
  })


  action_btn.forEach(action_btn => {
    action_btn.addEventListener('click', () => {
      var post_id = action_btn.dataset.postId;
      var post_body = document.querySelector('.post-' + post_id).textContent

      if(action_btn.innerHTML == 'Edit') {

        document.querySelector('.post-' + post_id).style.display = 'none'

        var edit_textarea = document.createElement('textarea')
        edit_textarea.classList.add('post-textarea', 'form-control')
        edit_textarea.setAttribute('spellcheck', 'false')
        edit_textarea.value = post_body.trim()
        edit_textarea.rows = '3'

        document.querySelector('.post-body-' + post_id).appendChild(edit_textarea)
        action_btn.innerHTML = 'Save'

      } else if(action_btn.innerHTML == 'Save') {
        var post = document.querySelector('.post-textarea').value

        fetch('/edit', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
          },
          body: JSON.stringify({'post_id': post_id, 'post': post})
        })

        .then(response => response.json())

        .then(data => {
          var updated_post = document.querySelector('.post-' + post_id)
          updated_post.style.display = 'block'
          updated_post.innerHTML = data.post_body

          var element = document.querySelector('.post-textarea')
          element.remove()

          action_btn.innerHTML = 'Edit'
        })
      }
    })
  })


  like_btn.forEach(like_btn => {
    like_btn.addEventListener('click', () => {
      var post_id = like_btn.dataset.postId

      if(like_btn.dataset.action === 'like') {
        likePost(like_btn, like_btn.dataset.action, post_id)
        like_btn.dataset.action = 'unlike'
      } else if(like_btn.dataset.action === 'unlike') {
        likePost(like_btn, like_btn.dataset.action, post_id)
        like_btn.dataset.action = 'like'
      }
    })
  })
})


function profileFollowing(action, user) {
  fetch('/follow', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({'action': action, 'user_profile': user})
  })

  .then(response => response.json())

  .then(data => {
    location.reload()
  })
}


function likePost(el, action, post) {
  fetch('/like', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({'action': action, 'post_id': post})
  })

  .then(response => response.json())

  .then(data => {

    if(el.classList.contains('fas')){
      el.classList.remove('fas')
      el.classList.add('far')
    } else {
      el.classList.remove('far')
      el.classList.add('fas')
    }

    document.querySelector('.likes-count-' + post).textContent = data.likes_counter
  })
}
