function clear(elementClass)
    {
        document.getElementById(elementClass).value = ''
    }

function chatClickListener(){
     const chats = document.getElementsByClassName("chat");
                    const chatSelected = e => {
                        selectedChatId = e.target.id;
                        console.log('selectedChatId', selectedChatId)
                        document.querySelectorAll(".message").forEach(el => el.remove());
                        refreshMessages();
                    }

                    if (selectedChatId != null)
                        {
                            refreshMessages();
                        }
                    for (let chat of chats) {
                        chat.addEventListener("click", chatSelected);
                        }
}


function responseSort(res) {
    let array = [];
    for (el in res)
        {
            console.log('el', el);
            res[el]['id'] = el;
            array.push(res[el]);
        }
    array.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    console.log(array);
    return array;
}

function refreshMessages()
{
    let requestMessage = new XMLHttpRequest();
    var params = 'chat_Id=' + encodeURIComponent(selectedChatId);
    requestMessage.open("GET", "/_get_chat_messages?" + params, true);
    requestMessage.send();
    requestMessage.onload = function()
        {
            document.querySelectorAll(".message").forEach(el => el.remove());
            let response = JSON.parse(requestMessage.response);
            let responseArray = responseSort(response);

            for (let i = 0; i < responseArray.length; i++)
                {
                    let divMessage = document.createElement('div');
                    divMessage.className = "message";
                    divMessage.innerHTML = responseArray[i].body;
                    document.querySelector('#message-holder').append(divMessage);
                }
        }
}


function setMessageCounter(count){
    let messageCounter = document.querySelector("#message-counter");
    messageCounter.innerHTML = count;
};


function sendButtonPressed()
    {
        body = document.getElementById('send-message').value
        let req = new XMLHttpRequest();
        var params = 'body=' + encodeURIComponent(body) + '&' + 'chat_Id=' + encodeURIComponent(selectedChatId);
        req.open("POST", "/send_message?" + params, true);
        req.send();
        clear('send-message');
        req.onload = refreshMessages;
    }


function get_chats()
{
    let request = new XMLHttpRequest();
    var params = 'userName=' + encodeURIComponent(currentUserName);
    request.open("GET", "/_get_chats?" + params, true);
    console.log(params)
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
					console.log(response)
					response = responseSort(response);
                    for (let i = 0; i < response.length; i++)
						{
							let div = document.createElement('div');
							div.className = "chat";
							div.id = response[i].id;
							let userName = response[i].users.username
							let lastMessage = response[i].last_message
							div.innerHTML = response[i].id + " " + userName + " " + lastMessage;
							document.querySelector('#chat-holder').append(div);
						}
//                    }
				}

                chatClickListener();
                setMessageCounter(6);
    }


}
let selectedChatId = null;
function ready()
    {
        const b = document.querySelector('.button');
        b.addEventListener('click', sendButtonPressed);
        get_chats();
        let timerId = setInterval(() => get_chats(), 8000);
    }

document.addEventListener("DOMContentLoaded", ready);
