function sendMessage(recipientId) {
        body = document.querySelector('.text').value
        let req = new XMLHttpRequest();
        var params = 'body=' + encodeURIComponent(body) + '&' + 'recipientId=' + encodeURIComponent(recipientId);
        req.open("POST", "/send_message?" + params, true);
        req.send();
        req.onload = alert('Message sent!');

}
function func(a){
    let div = document.createElement('div')
    div.innerHTML = 'Enter Your Message!'
    let text = document.createElement('input')
    text.className = 'text'

    let button = document.createElement('button')
    document.querySelector('.message').append(div)
    document.querySelector('.message').append(text)
    document.querySelector('.message').append(button)

    button.addEventListener('click', sendMessage.bind(null, a))
}

function ready()
{
    const users = document.querySelectorAll('.message-link');

    for (let user of users)
    {
        user.addEventListener('click', func.bind(null, user.id))
    }
}
document.addEventListener("DOMContentLoaded", ready);