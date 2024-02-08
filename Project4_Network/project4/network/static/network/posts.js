const username = "{{ username }}";

// ===================================
// SECTION 0: Event listeners
// ===================================
document.addEventListener('DOMContentLoaded', function() {
    
    let path_array = window.location.pathname

    // Add the create new post if the page is not a user page.
    if (path_array.split('/')[1] != 'user'){
        create_new_post();
    }

    // Handle the follow/unfollow button if it is a user page
    if (path_array.split('/')[1] == 'user'){
        follow(path_array.split('/')[2]);
    }

    if (path_array === '/'){
        // Feed all posts
        feed_posts("all");
    } else if (path_array === '/following') {
        // Feed following posts
        feed_posts("following");
    } else if (path_array.split('/')[1] === 'user') {
        // Feed the posts from selected user
        console.log(path_array.split('/')[1]);
        console.log(path_array.split('/')[2]);
        feed_posts("from_user", path_array.split('/')[2]);
    }

})

// Check event listeners inside of 'feed_posts' function.
// The event listener for like and unlike button are placed on this function that generates them

// ===================================
// SECTION X: Fetch functions
// ===================================
function create_new_post(){
    document.querySelector('#new-post-form').onsubmit = function(event){
        // Don't submit form as usual, but handle through the js 
        event.preventDefault();
        // Store form values in variables
        const post_content = document.querySelector('#new-post-content').value;
        csrftoken = document.querySelector('#new-post-content').querySelector('[name="csrfmiddlewaretoken"]');
        // POST value to API and receive back an answer
        fetch('/create_post', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                // other headers...
            },
            body: JSON.stringify({
                post_content: post_content,
            }),
            credentials: 'same-origin',
          })
          .then(response => response.json())
          .then(result => { 
              // Print result")
              console.log("Este é o resultado")
              console.log(result);
              if (result.message === 'Post created successfully.'){
                console.log("SUCESSO!!!")
              } else {
                console.log("Vamos ver o resultado")
                console.log(result);
                console.log(result.message);
              }
          });

    }
}

function follow(username){
    // If follow form is submitted
    if (document.querySelector('#follow-form')) {

        document.querySelector('#follow-form').onsubmit = function(event){
            // Don't submit form as usual, but handle through the js 
            event.preventDefault();
            // Store form values in variables
            //csrftoken = document.querySelector('#follow-form').querySelector('[name="csrfmiddlewaretoken"]');
            // POST value to API and receive back an answer
            fetch('/follow', {
                method: 'PUT',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    // other headers...
                },
                body: JSON.stringify({
                    follow: true,
                    username: username,
                }),
                credentials: 'same-origin',
                })
            document.querySelector('#follow-form').style.display = 'none';
            document.querySelector('#unfollow-form').style.display = 'block';
        }
        
        // If UNfollow form is submitted
        document.querySelector('#unfollow-form').onsubmit = function(event){
            // Don't submit form as usual, but handle through the js 
            event.preventDefault();
            // Store form values in variables
            //csrftoken = document.querySelector('#follow-form').querySelector('[name="csrfmiddlewaretoken"]');
            // POST value to API and receive back an answer
            fetch('/follow', {
                method: 'PUT',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    // other headers...
                },
                body: JSON.stringify({
                    follow: false,
                    username: username,
                }),
                credentials: 'same-origin',
                })
                .then(response => response.text())
                .then(posts => { 
                    // Print result")
                    console.log(posts);
                })
            document.querySelector('#follow-form').style.display = 'block';
            document.querySelector('#unfollow-form').style.display = 'none';
        }
    }

}

function feed_posts(subset, creator=null) { 
    // GET to request to receive the posts
    fetch(`/get_posts?subset=${subset}&creator=${creator}`)
    .then(response => response.json())
    .then(posts => { 
        if (posts.error == "Subset argument should be either 'all', 'following', 'from_user'. If 'from_user', you should specify a username on argument 'creator'"){
            console.log("Eroooooooo")
            // Else (if no error)
        } else {
            console.log("SUCESSO")
            // For each post, add card, and handle interactions on card
            for (var i = 0; i < posts.length; i++) {
                console.log(posts[i]);
                card = create_post_html(posts[i].id, posts[i].creator, posts[i].timestamp, posts[i].content, posts[i].number_of_likes, posts[i].liked, posts[i].is_creator);
              
                // Add eventlistener for like button
                card.querySelector('#like_button').addEventListener('click', function(event){
                console.log('Click');
                // If like button is clicked, call like_post function and pass on its id
                if (event.target.id === "like_button"){
                    like_post(event.target.dataset.id)
                }
                })
                // Add eventlistener for unlike button
                card.querySelector('#unlike_button').addEventListener('click', function(event){
                console.log('Click')
                // If like button is clicked, call unlike_post function and pass on its id
                if (event.target.id === "unlike_button"){
                    unlike_post(event.target.dataset.id)
                }
                })

                //*

                // Add eventListener for Edit button
                card.querySelector('#edit-button').addEventListener('click', function(event){
                    console.log('Click edit')
                    // If like button is clicked, call edit function and pass on its id
                    if (event.target.id === "edit-button"){
                        console.log("Yes, a edit button was clicked")
                        post_id = event.target.dataset.id
                        document.querySelector(`#card-content[data-id='${post_id}']`).style.display = 'none';
                        edit_form = document.createElement('div');
                        edit_form.setAttribute('csrfmiddlewaretoken', getCookie('csrftoken'))
                        edit_form.id = "edit-form"
                        edit_form_text = document.createElement('textarea');
                        edit_form_text.className = "form-control mb-2"
                        edit_form_text.innerHTML= document.querySelector(`#card-content[data-id='${post_id}']`).innerHTML
                        edit_form_text.id = "edit-form-text"
                        edit_form_submit_button = document.createElement('button')
                        edit_form_submit_button.className = "btn btn-primary"
                        edit_form_submit_button.id = "edit-form-submit-button"
                        edit_form_submit_button.innerHTML = "Submit changes"
                        //edit_form_submit_button.setAttribute('type', "submit")
                        edit_form.append(edit_form_text);
                        edit_form.append(edit_form_submit_button);
                        document.querySelector(`.card-body[data-id='${post_id}']`).append(edit_form);
                        document.querySelector(`#edit-button[data-id='${post_id}']`).style.display = 'none'

                        // Add event submit to the edit form
                        //*  AAAAAAAAAAAAAAAQUI COMEÇA O TRABALHO DEPOIS DO SUBMIT
                        document.querySelector('#edit-form-submit-button').addEventListener('click', function(event){
                            // Don't submit form as usual, but handle through the js 
                            event.preventDefault();
                            // Store form values in variables
                            const post_content = document.querySelector('#edit-form-text').value;
                            // POST value to API and receive back an answer
                            fetch('/edit_post', {
                                method: 'POST',
                                headers: {
                                    'X-CSRFToken': getCookie('csrftoken'),
                                    // other headers...
                                },
                                body: JSON.stringify({
                                    post_content: post_content,
                                    post_id: post_id,
                                }),
                                credentials: 'same-origin',
                            })
                            .then(response => response.json())
                            .then(result => { 
                                // Print result")
                                console.log("Este é o resultado")
                                console.log(result);
                                if (result.message === 'Post created successfully.'){
                                    console.log("SUCESSO!!!")
                                } else {
                                    console.log("Vamos ver o resultado")
                                    console.log(result);
                                    console.log(result.message);
                                }
                            });
                            
                            document.querySelector(`#card-content[data-id='${post_id}']`).style.display = 'block';
                            document.querySelector(`#card-content[data-id='${post_id}']`).innerHTML = edit_form_text.value;
                            document.querySelector(`#edit-button[data-id='${post_id}']`).style.display = 'block'
                            document.querySelector('#edit-form').remove()
                        
                        })
                        //*/  AAAAAAAAAAAAAAQUI TERMINA O TRABALHO DO SUBMIT


                    }
                })
                    //*/
                document.querySelector('#posts-feed').append(card);
            }
        }
    })
};

function like_post(post_id){
    let csrftoken = getCookie('csrftoken');
    console.log(post_id)
    if (post_id != null) {
        // Like post
        fetch(`/like_post/${post_id}`, {
          method: 'PUT',
          body: JSON.stringify({
              liked: true,
              username: username,
          }),
          headers: {"X-CSRFToken": csrftoken},
          credentials: 'same-origin',
        })
        document.querySelector(`#like_button[data-id='${post_id}']`).style.display = 'none';
        document.querySelector(`#unlike_button[data-id='${post_id}']`).style.display = 'block';
        document.querySelector(`#like_counter[data-id='${post_id}']`).innerHTML = 1 + parseInt(document.querySelector(`#like_counter[data-id='${post_id}']`).innerHTML)
    }
}

function unlike_post(post_id){
    let csrftoken = getCookie('csrftoken');
    console.log(post_id)
    if (post_id != null) {
        // Mark as read
        fetch(`/like_post/${post_id}`, {
          method: 'PUT',
          body: JSON.stringify({
              liked: false,
              username: username,
          }),
          headers: {"X-CSRFToken": csrftoken},
          credentials: 'same-origin',
        })
        document.querySelector(`#like_button[data-id='${post_id}']`).style.display = 'block';
        document.querySelector(`#unlike_button[data-id='${post_id}']`).style.display = 'none';
        document.querySelector(`#like_counter[data-id='${post_id}']`).innerHTML = -1 + parseInt(document.querySelector(`#like_counter[data-id='${post_id}']`).innerHTML)
    }
}
// ==================================
// SECTION 2: HTML Builder
// ==================================
function create_post_html(id, creator, date, content, number_of_likes, liked, is_creator){

    // Create the form of a single post
    let card = document.createElement('div');
    card.className="card mx-3 mt-3";
    let card_header = document.createElement('div');
    card_header.className="card-header";
    let card_header_div = document.createElement('div');
    card_header_div.className="d-flex justify-content-between";
    let card_title = document.createElement('h5');
    card_title.className ="card-title";
    // Add the username on the title
    let card_link = document.createElement('a')
    card_link.setAttribute('href', `/user/${creator}`)
    card_link.innerHTML=creator;
    let card_edit_button = document.createElement('button');
    card_edit_button.className="btn btn-primary py-0";
    card_edit_button.innerHTML="Edit";
    card_edit_button.id = 'edit-button'
    card_edit_button.setAttribute('data-id', id);
    if (is_creator == false) {
        card_edit_button.style.display = 'none'
    }

    let card_subtitle = document.createElement('h6');
    card_subtitle.className="card-subtitle";
    // Add the date on the subtitle
    card_subtitle.innerHTML=date;
    let card_body = document.createElement('div');
    card_body.className="card-body";
    card_body.setAttribute('data-id', id);
    let card_content = document.createElement('p');
    card_content.id = "card-content"
    card_content.setAttribute('data-id', id);
    card_content.className="card-text";
    // Add content on the content field
    card_content.innerHTML=content;
    let card_footer = document.createElement('div');
    card_footer.className="card-footer p-1";
    let card_footer_like_div = document.createElement('div');
    card_footer_like_div.className="col-1 text-center";
    
    let like_emoji = document.createElement('span');
    like_emoji.innerHTML = "❤️"
    
    let like_counter = document.createElement('span');
    like_counter.id = "like_counter";
    like_counter.setAttribute('data-id', id);
    like_counter.className="m-0 text-muted fw-bold";
    like_counter.style="font-size: 14px";
    like_counter.innerHTML =`${number_of_likes}`;
    let like_button = document.createElement('button');
    like_button.className="btn btn-light py-0 px-4 fw-bold text-muted";
    like_button.setAttribute('data-id', id);
    like_button.id = "like_button";
    like_button.innerHTML="Like";
    if (liked === true) {
        like_button.style.display = 'none'
    }

    let unlike_button = document.createElement('button');
    unlike_button.className="btn btn-light py-0 px-4 fw-bold text-muted";
    unlike_button.setAttribute('data-id', id);
    unlike_button.id = "unlike_button";
    unlike_button.innerHTML="Unlike";
    if (liked === false) {
        unlike_button.style.display = 'none'
    }

    card_footer_like_div.append(like_emoji);
    card_footer_like_div.append(like_counter);
    card_footer_like_div.append(like_button);
    card_footer_like_div.append(unlike_button);
    card_footer.append(card_footer_like_div);

    card_body.append(card_content);

    card_title.append(card_link);
    card_header_div.append(card_title);
    card_header_div.append(card_edit_button);

    card_header.append(card_header_div);
    card_header.append(card_subtitle);

    card.append(card_header);
    card.append(card_body);
    card.append(card_footer);

    return card;
}



// ===================================
// SECTION X: Utilities
// ===================================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}