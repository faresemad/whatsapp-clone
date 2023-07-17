
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const message = data['message'];
    const user = data['user'];
    const chatLog = document.querySelector('#chat-log');
    const loggedUser = JSON.parse(document.getElementById('logged-user').textContent);
    const msgDiv = document.createElement('div');
    if (user == loggedUser) {
        // create div element in the chat-log div element with class left-msg
        msgDiv.classList.add('msg', 'left-msg');
        // create div element with class msg-img
        const msgImgDiv = document.createElement('div');
        msgImgDiv.classList.add('msg-img');
        // create div element with class msg-bubble
        const msgBubbleDiv = document.createElement('div');
        msgBubbleDiv.classList.add('msg-bubble');
        // create div element with class msg-info
        const msgInfoDiv = document.createElement('div');
        msgInfoDiv.classList.add('msg-info');
        // create div element with class msg-info-name
        const msgInfoNameDiv = document.createElement('div');
        msgInfoNameDiv.classList.add('msg-info-name');
        msgInfoNameDiv.innerHTML = user;
        // create div element with class msg-info-time
        const msgInfoTimeDiv = document.createElement('div');
        msgInfoTimeDiv.classList.add('msg-info-time');
        msgInfoTimeDiv.innerHTML = new Date().toLocaleTimeString();
        // create div element with class msg-text
        const msgTextDiv = document.createElement('div');
        msgTextDiv.classList.add('msg-text');
        msgTextDiv.innerHTML = message;
        // append the div elements to the chat-log div element
        msgInfoDiv.appendChild(msgInfoNameDiv);
        msgInfoDiv.appendChild(msgInfoTimeDiv);
        msgBubbleDiv.appendChild(msgInfoDiv);
        msgBubbleDiv.appendChild(msgTextDiv);
        msgDiv.appendChild(msgImgDiv);
        msgDiv.appendChild(msgBubbleDiv);
        chatLog.appendChild(msgDiv);
    } else {
        // create div element in the chat-log div element with class right-msg
        msgDiv.classList.add('msg', 'right-msg');
        // create div element with class msg-img
        const msgImgDiv = document.createElement('div');
        msgImgDiv.classList.add('msg-img');
        // create div element with class msg-bubble
        const msgBubbleDiv = document.createElement('div');
        msgBubbleDiv.classList.add('msg-bubble');
        // create div element with class msg-info
        const msgInfoDiv = document.createElement('div');
        msgInfoDiv.classList.add('msg-info');
        // create div element with class msg-info-name
        const msgInfoNameDiv = document.createElement('div');
        msgInfoNameDiv.classList.add('msg-info-name');
        msgInfoNameDiv.innerHTML = user;
        // create div element with class msg-info-time
        const msgInfoTimeDiv = document.createElement('div');
        msgInfoTimeDiv.classList.add('msg-info-time');
        msgInfoTimeDiv.innerHTML = new Date().toLocaleTimeString();
        // create div element with class msg-text
        const msgTextDiv = document.createElement('div');
        msgTextDiv.classList.add('msg-text');
        msgTextDiv.innerHTML = message;
        // append the div elements to the chat-log div element
        msgInfoDiv.appendChild(msgInfoNameDiv);
        msgInfoDiv.appendChild(msgInfoTimeDiv);
        msgBubbleDiv.appendChild(msgInfoDiv);
        msgBubbleDiv.appendChild(msgTextDiv);
        msgDiv.appendChild(msgImgDiv);
        msgDiv.appendChild(msgBubbleDiv);
        chatLog.appendChild(msgDiv);
    }
}

    // < div class="chat-message-form" >
    //     <input type="text" id="chat-message-input" placeholder="Type your message here...">
    //         <button id="chat-message-submit">Send</button>
    //     </div>