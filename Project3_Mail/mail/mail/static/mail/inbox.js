
//////////////////////////////////////////////
//DOCUMENT EVENT LISTENER
document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  //Send email when user clicks on button (onsubmit and logic is inside function)
  send_email();

  // Archive when user clicks on archive button (maybe would be better if done as send_email fuction?)
  document.querySelector('#message-archive-button').addEventListener('click', function(){
    const email_id = document.querySelector('#message-archive-button').getAttribute('data-email-id');
    console.log(email_id);
    if (document.querySelector('#message-archive-button').value === 'archive'){
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
      })
      .then(response => {
        console.log(response);
        //return response.json();
        load_mailbox('inbox');
      })
    } else {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false
        })
      })
      .then(response => {
        console.log(response);
        //return response.json();
        load_mailbox('inbox');
      })
    }

  })

  // Reply when Reply button is clicked (maybe would be better if done as send_email fuction?)
  document.querySelector('#message-reply-button').addEventListener('click', function(){
    const reply_id = document.querySelector('#message-reply-button').getAttribute('data-email-id');
    fetch(`/emails/${reply_id}`)
    .then(response => response.json())
    .then(email => {
        // Print email
        console.log(email);
        compose_email('reply', email);
    });
  })

});

/////////////////////////////////////////////////////////////////
function alert_output(type, message){
  const alert = document.querySelector('#alert-block')
  alert.className = type;
  alert.innerHTML = message;
}

/////////////////////////////////////////////////////////////////
function compose_email(message = null, email_to_feed = null) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#message-view').style.display = 'none';
  document.querySelector('#alert-block').innerHTML = "";

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // If compose has reply argument, feed email being replied on the form
  if (message === 'reply') {
    document.querySelector('#compose-recipients').value = email_to_feed.recipients;
    if (email_to_feed.subject.substring(0, 4) === 'RE: ') {
      document.querySelector('#compose-subject').value = email_to_feed.subject;      
    } else {
      document.querySelector('#compose-subject').value = `RE: ${email_to_feed.subject}`;
    }
    document.querySelector('#compose-body').value = `On ${email_to_feed.timestamp} ${email_to_feed.sender} wrote: ${email_to_feed.body}`;
  }

}

/////////////////////////////////////////////////////////////////
function send_email(){
  document.querySelector('#compose-form').onsubmit = function(event){
    event.preventDefault();
    //Obtain values from form
    const recipients = document.querySelector('#compose-recipients').value
    const subject = document.querySelector('#compose-subject').value
    const body = document.querySelector('#compose-body').value
    
    //POST values to API, receive back an answer
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        if (result.message === 'Email sent successfully.'){
          load_mailbox('inbox');
          alert_output('alert-success', result.message);
        } else {
          alert_output('alert-danger', result.error);
        }
    });
  }
}

/////////////////////////////////////////////////////////////////
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#message-view').style.display = 'none';
  document.querySelector('#alert-block').innerHTML = "";


  // Clear the mailbox
  document.querySelector('#emails-view').innerHTML = "";

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get the mail list from API
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      // ... do something else with emails ...
      emails.forEach(function(element){
        email_item = document.createElement('div');
        email_item.classList.add('email-item');
        if (element.read === true){email_item.classList.add('email-read');}
        if (element.read === false){email_item.classList.add('email-unread');}
        email_sender = document.createElement('div');
        email_subject = document.createElement('div');
        email_date = document.createElement('div');
        
        email_sender.innerHTML = element.sender;
        email_subject.innerHTML = element.subject;
        email_date.innerHTML = element.timestamp;

        email_sender.classList.add('email-sender');
        email_subject.classList.add('email-subject');
        email_date.classList.add('email-timestamp');

        email_item.append(email_sender);
        email_item.append(email_subject);
        email_item.append(email_date);

        //Listen for click and run show email function
        email_item.addEventListener('click', function() {
          load_email(element, mailbox);
        });

        document.querySelector('#emails-view').append(email_item);
      })
  });
}

/////////////////////////////////////////////////////////////////
function load_email(element, mailbox){

  // Show the message view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#message-view').style.display = 'block';
  document.querySelector('#alert-block').innerHTML = "";

  document.querySelector('#message-sender').innerHTML = element.sender;
  document.querySelector('#message-recipients').innerHTML = element.recipients;
  document.querySelector('#message-subject').innerHTML = element.subject;
  document.querySelector('#message-timestamp').innerHTML = element.timestamp;
  document.querySelector('#message-body').innerHTML = element.body;

  // Add email id to Reply button
  document.querySelector('#message-reply-button').setAttribute('data-email-id', element.id);

  if (mailbox === 'inbox' || mailbox === 'archive') {
    // Mark as read
    fetch(`/emails/${element.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    });

    //Show the archive ou unarchive button
    document.querySelector('#message-archive-button').style.display = 'inline-block';
      if (element.archived === false){
        document.querySelector('#message-archive-button').innerHTML = "Archive";
        document.querySelector('#message-archive-button').value = "archive";
        document.querySelector('#message-archive-button').setAttribute('data-email-id', element.id);
      } else {
        document.querySelector('#message-archive-button').innerHTML = "Unarchive";
        document.querySelector('#message-archive-button').value = "unarchive";
        document.querySelector('#message-archive-button').setAttribute('data-email-id', element.id);
      }
    }


    if (mailbox === 'sent'){
      // Hide the archive button
      document.querySelector('#message-archive-button').style.display = 'none';
    }
  
}

  /*=====================================================================================
  REVIEW

  1. What maybe could have been better
    1.1 - [Button Archive/Unarchive] Instead of having the same button and changing the innerHTMl
    and value to handle logic, it could have been better to have two separate buttons. This would
    also need two separate eventListeners. Maybe we would get some cleaner code for showing/hiding
    the buttons instead of changing the values, but would have more messy code with 2 functions 
    to handle the clicking of the buttons.
    1.2 - Event listener for reply and archive buttons could have been stored in separate functions,
    the same as was done for the send email button.
    1.3 - A function could have generalized the view that one wishes to show
      function show_view('view_name'). The logic inside would hide the views not in argument and 
      show the view passed in to the function as an argument.
    1.4 - The name of the function compose_email could have been named lead_compose_email. This would
    be more consistent with other function names, such as load_mailbox and load_email.


    2. Interesting learnings
      2.1 How to pass an argument to and eventListener.
      In order to do that, you must use a anonimous function on the event listener, and have a
      single line inside calling another function which accepts an argument.
      On this project, this logic was used on the eventListener for clicking on an email
      item on the mailboxes (lines 175-178). On this case, we needed to add a different eventListener
      for each email item, and when clicked, pass the email id of the clicked element to
      the load_email function.