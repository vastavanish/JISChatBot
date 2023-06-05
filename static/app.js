class ChatBox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;

        openButton.addEventListener('click', () => { this.toggleState(chatBox) });

        sendButton.addEventListener('click', () => { this.onSendButton(chatBox) })

        const node = chatBox.querySelector('input');

        node.addEventListener('keyup', ({ key }) => {
            if (key === 'Enter') {
                this.onSendButton(chatBox)
            }
        })

    }


    toggleState(chatBox) {
        this.state = !this.state;

        //Show hide the box
        if (this.state) {
            chatBox.classList.add('chatbox--active');
        } else {
            chatBox.classList.remove('chatbox--active');
        }

    }

    onSendButton(chatBox) {
        var textField = chatBox.querySelector('input')
        var text1 = textField.value;

        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }

        this.messages.push(msg1);

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(r => r.json())
            .then(r => {
                let msg2 = { name: 'Binod', message: r.answer.message };
                this.messages.push(msg2);

                console.log('Q. ' + text1 + '\n' + 'Ans. ' + r.answer.message);

                this.updateChatText(chatBox);
                textField.value = '';
                if (!r.answer.status) {
                    console.log('Cannot understand');

                    // .NET Core WebAPI
                    //----START
                    // fetch('http://localhost:5235/api/chatbot/updatemodel', {
                    //     method: 'POST',
                    //     body: JSON.stringify({ message: text1 }),
                    //     mode: 'cors',
                    //     headers: {
                    //         'Content-Type': 'application/json; charset=utf-8'
                    //     }
                    // })
                    //     .then(r => r.json())
                    //     .then(r => {
                    //         console.log('API Response for ' + text1 + ' : ' + r.message)
                    //     }).catch((error) => {
                    //         console.log('API Error ' + error);
                    //     })

                    //----END

                    fetch('http://127.0.0.1:5000/updatemodel', {
                        method: 'POST',
                        body: JSON.stringify({ message: text1 }),
                        mode: 'cors',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                        .then(r => r.json())
                        .then(r => {
                            console.log('Update model : ' + r.response)
                        })
                }

            }).catch((error) => {
                console.log('Error ' + error);
            })


    }

    updateChatText(chatBox) {
        var html = '';
        this.messages.slice().reverse().forEach((v, k) => {
            if (v.name === 'Binod') {
                html += '<div class="messages__item messages__item--visitor">' + v.message + '</div>'
            } else {
                html += '<div class="messages__item messages__item--operator">' + v.message + '</div>'
            }
        });

        const chatMessage = chatBox.querySelector('.chatbox__messages');
        chatMessage.innerHTML = html;
    }


}


const chatBox = new ChatBox();

chatBox.display();