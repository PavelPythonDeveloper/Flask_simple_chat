function sendMessage() {
    alert('Message was send!')
}
function func(a){
    alert('alalalalalalla')
    let div = document.createElement('div')
    div.innerHTML = 'Enter Your Message!'
    let text = document.createElement('input')
    let button = document.createElement('button')
    document.querySelector('.message').append(div)
    document.querySelector('.message').append(text)
    document.querySelector('.message').append(button)
    button.addEventListener('click', sendMessage)
}

function ready()
{
    const users = document.querySelectorAll('.message-link');

    for (let user of users)
    {
        user.addEventListener('click', func.bind(null, user.id))

//        let div = document.createElement('input');
//        div.className = 'accc';
//        //div.className = "chat";2
//        div.id = '1'
//
//
//        div.innerHTML = 'llkjlkjlkjlkjlkjlkjlkjkljlkj'
//        //    console.log(user);
//            user.append(div);
    }
}
document.addEventListener("DOMContentLoaded", ready);