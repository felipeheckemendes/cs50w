document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  //Send email when user clicks on button
  send_email();

  // Archive when user clicks on archive button
  document.querySelector('#message-archive-button').addEventListener('click', function(){
    const email_id = document.querySelector('#message-archive-button').getAttribute('data-email-id');
    console.log("THIS IS THE EMAIL ID:");
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

  // Reply when Reply button is clicked
  document.querySelector('#message-reply-button').addEventListener('click', function(){
    const reply_id = document.querySelector('#message-reply-button').getAttribute('data-email-id');
    fetch(`/emails/${reply_id}`)
    .then(response => response.json())
    .then(email => {
        // Print email
        console.log(email);
        compose_email('reply', email);
        // ... do something else with email ...
    });
  })

});

/////////////////////////////////////////////////////////////////
//Function to output alert to alert div
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

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Se for uma resposta, preencher os formulários
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
function load_email(element, mailbox){

  // Show the message view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#message-view').style.display = 'block';

  document.querySelector('#message-sender').innerHTML = element.sender;
  document.querySelector('#message-recipients').innerHTML = element.recipients;
  document.querySelector('#message-subject').innerHTML = element.subject;
  document.querySelector('#message-timestamp').innerHTML = element.timestamp;
  document.querySelector('#message-body').innerHTML = element.body;

  // Add email id to Reply button
  document.querySelector('#message-reply-button').setAttribute('data-email-id', element.id);

  if (mailbox === 'inbox' || mailbox === 'archive') {
    console.log("PASSED INBOX OR ARCHIVE IF TEST");
    // Mark as read
    fetch(`/emails/${element.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    });

    //Show the archive ou unarchive button
    console.log("ABOUT TO SHOW THE ARCHIVE BUTTON");
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

/////////////////////////////////////////////////////////////////
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#message-view').style.display = 'none';

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

        email_item.append(email_sender);
        email_item.append(email_subject);
        email_item.append(email_date);

        //Listen for click and run show email function
        email_item.addEventListener('click', function() {
          console.log(`ABOUT TO LOAD AN EMAIL FROM MAILBOX ${mailbox}`)
          load_email(element, mailbox);
        });

        document.querySelector('#emails-view').append(email_item);
      })
  });
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
          console.log("Houve algum erro");
          alert_output('alert-danger', result.error);
        }
    });
  }
}