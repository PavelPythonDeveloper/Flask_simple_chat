function refreshMessages() {
                        document.querySelectorAll(".message").forEach(el => el.remove());
                        let requestMessage = new XMLHttpRequest();
                        var params = 'chat_Id=' + encodeURIComponent(selectedChatId);
                        requestMessage.open("GET", "/_get_chat_messages?" + params, true);
                        requestMessage.send();
                        requestMessage.onload = function()
                        {
                            let response = JSON.parse(requestMessage.response);
                            console.log(response);
                            for (let key in response)
                            {

                                let divMessage = document.createElement('div');
                                divMessage.className = "message";
                                text = response[key].body;
                                console.log(text);
                                divMessage.innerHTML = text;
                                document.querySelector('#message-holder').append(divMessage);
                            }
                        }
}
function setMessageCounter(count){
    let messageCounter = document.querySelector("#message-counter");
    messageCounter.innerHTML = count;
};

function sendButtonPressed() {
    console.log('Button pressed!');
    body = document.getElementById('send-message').value
    let req = new XMLHttpRequest();
    var params = 'body=' + encodeURIComponent(body) + '&' + 'chat_Id=' + encodeURIComponent(selectedChatId);
    req.open("POST", "/send_message?" + params, true);
    req.send();
    req.onload = refreshMessages;


}
function get_chats()
{

    let request = new XMLHttpRequest();
    var params = 'userId=' + encodeURIComponent(currentUserId);
    request.open("GET", "/_get_chats?" + params, true);
    request.send();
    request.onload = function()
	{
        if (request.status != 200)
		{
            alert(`Error ${request.status}: ${request.statusText}`);
        } else
				{
					document.querySelectorAll(".chat").forEach(el => el.remove());
					let response = JSON.parse(request.response);
					for (var key in response)
						{
							let div = document.createElement('div');
							div.className = "chat";
							div.id = key;
							let chatName = key;
							let userName = response[key].users.username
							let lastMessage = response[key].last_message
							div.innerHTML = chatName + " " + userName + " " + lastMessage;
							document.querySelector('#chat-holder').append(div);
						}
				}
                    const chats = document.getElementsByClassName("chat");
                    const chatSelected = e => {
                        selectedChatId = e.target.id;
                        console.log(selectedChatId);
                        document.querySelectorAll(".message").forEach(el => el.remove());
                        console.log(e.target.id);

                        refreshMessages();
                    }

                    for (let chat of chats) {
                        console.log(chat.id);
                        chat.addEventListener("click", chatSelected);
                        }

                setMessageCounter(6)
    }

}
function ready() {
    let selectedChatId = null;
const b = document.querySelector('.button');
b.addEventListener('click', sendButtonPressed);
get_chats();

let timerId = setInterval(() => get_chats(), 4000);
}


document.addEventListener("DOMContentLoaded", ready);
