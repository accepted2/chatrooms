document.addEventListener('DOMContentLoaded', function () {
    const ChatRoomName = JSON.parse(document.getElementById('json-chatroomname').textContent);
    const ChatRoomId = JSON.parse(document.getElementById('json-chatroomid').textContent);

    const username = JSON.parse(document.getElementById('json-username').textContent);
    const CurrentPage = window.location.pathname
    console.log(CurrentPage);
    console.log(ChatRoomName);
    const isInChat = CurrentPage.includes(`/rooms/${ChatRoomId}/`)
    console.log(isInChat)
    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    const chatSocket = new WebSocket(
        protocol + window.location.host + '/ws/' + ChatRoomName + '/'
    );

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log(data);
        if (data.message) {
            console.log('Received message to client id', data.message);
            if (data.username !== username) {

                showNotification(data.username, (data.room).replace(/-/g, ' ').replace(/\b\w/g, c => c
                    .toUpperCase()))
                document.getElementById('notification-sound').play()

            } else {

                document.getElementById('sent-sound').play()
            }

            const messageClass = (data.username === username) ? 'sent' : 'received';

            let html = `
        <div class="message-container ${messageClass}">
            <div class="message-header">
                <strong style="color: rgb(109, 224, 109);">${data.username}</strong>
                <span class="message-time">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
            </div>
            <div class="message-body">
                ${data.message}
            </div>
        </div>`;

            document.getElementById('chat-messages').innerHTML += html;
            document.getElementById('chat-messages').scrollTop = document.getElementById('chat-messages')
                .scrollHeight;
        } else {
            alert('NO message');
        }
    };

    chatSocket.onclose = function (e) {
        console.log('Socket is closed');
    };

    document.getElementById('send-button').onclick = function (e) {
        e.preventDefault();
        const messageInput = document.getElementById('message-input');
        const message = messageInput.value;

        chatSocket.send(JSON.stringify({
            'message': message,
            'username': username,
            'room': ChatRoomName,
        }));
        messageInput.value = '';
    };

    window.onload = function () {
        const chatMessages = document.getElementById('chat-messages');
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    };

    function showNotification(sender, message) {
        console.log('Показ уведомления для', sender, message); // Логируем вызов функции
        const notificationContainer = document.getElementById('chat-notifications');
        const notification = document.createElement('div');
        notification.classList.add('notification');
        notification.innerHTML = `<strong>${sender} send message in </strong> ${message}`;
        notificationContainer.appendChild(notification);
        const notificationSound = document.getElementById('notification-sound');
        if (notificationSound) {
            notificationSound.play(); // Убедитесь, что звук правильно проигрывается
        }
        setTimeout(() => {
            notification.remove();
        }, 4000);
    }

})