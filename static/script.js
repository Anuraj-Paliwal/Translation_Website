function translat() {
    const text = document.getElementById('message-input').value;
    const chatMessages = document.getElementById('chat-messages');
    const bubblemsg = document.getElementById('message-bubble')
    const popbubble = document.getElementById('message-bubble')
    
    const userMessageElement = document.createElement('div');
    userMessageElement.className = 'message';
    userMessageElement.textContent = `You: ${text}`;
    chatMessages.appendChild(userMessageElement);

    fetch('/translat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        if (data.serial_number) {
            fetch('/speech', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ serial_number: data.serial_number })
            })
            .then(response => response.json())
            .then(data => {
                if (data.audio_url) {
                    const audioDiv = document.createElement('div');
                    const audio = new Audio(data.audio_url);
                    audio.controls = false;

                    const playPauseButton = document.createElement('button');
                    playPauseButton.className = 'audio-control';
                    playPauseButton.innerHTML = "<img src='static/img/unmute.jpeg' alt='Pause'>";
                    let isPlaying = false;

                    playPauseButton.addEventListener('click', function() {
                        if (!isPlaying) {
                            audio.play();
                            playPauseButton.innerHTML = "<img src='static/img/unmute.jpeg' alt='Pause'>";
                            isPlaying = true;
                        } else {
                            audio.pause();
                            playPauseButton.innerHTML = "<img src='static/img/muted.jpeg' alt='Play'>";
                            isPlaying = false;
                        }
                    });

                    audio.addEventListener('play', function() {
                        playPauseButton.innerHTML ="<img src='static/img/unmute.jpeg' alt='Pause'>";
                        isPlaying = true;
                    });

                    audio.addEventListener('pause', function() {
                        playPauseButton.innerHTML = "<img src='static/img/muted.jpeg' alt='play'>";
                        isPlaying = false;
                    });

                    audioDiv.className = 'audio-controls';
                    audioDiv.appendChild(playPauseButton);
                    audioDiv.appendChild(audio);
                    bubblemsg.appendChild(audioDiv);
                }
            });

            const translatedText = data.translated_text;
            const translatedMessageElement = document.createElement('div');
            translatedMessageElement.className = 'message';
            translatedMessageElement.textContent = `Bot: ${translatedText}`;
            chatMessages.appendChild(translatedMessageElement);
        }
    });
  }
                

                    const audio = new Audio(data.audio_url);
                    audio.controls = false;

                    const playPauseButton = document.createElement('button');
                    playPauseButton.className = 'audio-control';
                    playPauseButton.innerHTML = "<img src='static/img/unmute.png' alt='Pause' style = 'width: 100%; height:100%; top: 150px; left: 870px;'>";
                    let isPlaying = false;

                    playPauseButton.addEventListener('click', function() {
                        if (!isPlaying) {
                            audio.play();
                            playPauseButton.innerHTML = "<img src='static/img/unmute.png' alt='Pause' style = 'width: 100%; height:100%; top: 150px; left: 870px;'>";
                            isPlaying = true;
                        } else {
                            audio.pause();
                            playPauseButton.innerHTML = "<img src='static/img/muted.png' alt='Play' style = 'width: 100%; height:100%; top: 150px; left: 870px;'>";
                            isPlaying = false;
                        }
                    });

                    audio.addEventListener('play', function() {
                        playPauseButton.innerHTML ="<img src='static/img/unmute.png' alt='Pause' style = 'width: 100%; height:100%; top: 150px; left: 870px;'>";
                        isPlaying = true;
                    });

                    audio.addEventListener('pause', function() {
                        playPauseButton.innerHTML = "<img src='static/img/muted.png' alt='play' style = 'width: 100%; height:100%; top: 150px; left: 870px;' >";
                        isPlaying = false;
                    });

                    audioDiv.appendChild(playPauseButton);
                }
            })

            const translatedText = data.translated_text;
            const translatedMessageElement = document.createElement('div');
            translatedMessageElement.className = 'message';
            translatedMessageElement.textContent = `Bot: ${translatedText}`;
            chatMessages.appendChild(translatedMessageElement);
        }
    })
}

document.addEventListener('DOMContentLoaded', function() {
    const myModelViewer = document.getElementById('myModelViewer');
    myModelViewer.cameraOrbit = '0deg 90deg 2m';
    myModelViewer.cameraTarget = '20m 59m 700m';
    myModelViewer.cameraFov = '60deg';
    /// Edited Part (begins) - This one is to add Enter functionality for convert
    document.getElementById("message-input")
    .addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.key === 'Enter') {
        translat()
    }
    });
    // Just to check if enter input is being registered, will delete later
    function buttonCode()
    {
    alert("Button code executed.");
    }
    //////// Delete the above segment
});

