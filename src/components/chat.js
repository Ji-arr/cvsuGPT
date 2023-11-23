import React, { useState } from 'react';
import './chat.css'


const ChatWithAI = () => {
  // Declare a state variable to hold the input value
  const [input1, setInputValue] = useState('');
  const [result, setResult] = useState('');
  const [typing, setTyping] = useState(false);
  const [messages, setMessage] = useState([
    {
      content: "Hello, I am Groot",
      sender: "Groot"
    }
  ]);



    const handleSend = async () => {
        if (input1) {
  
          const userMessage = {
            content: input1,
            sender: "User"
          }

          setMessage(prevMessages => [...prevMessages, userMessage]);
          setInputValue('');
          setTyping(true);


          try {
            const response = await fetch('http://localhost:5000/get-result', {
              method:'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({input1}),
            })

            if (!response.ok){
              throw new Error('Network response was not ok');
            } 
            const data = await response.json();

            const aiMessage = {
              content: data.result,
              sender: "Groot",
            };

            setMessage(prevMessages => [...prevMessages, aiMessage]);
            console.log(data.result);
            setResult(data.result);
            setTyping(false);
            console.log('All messages:', messages);
          } catch(error) {
            console.error('Error:', error);
          }  
        }

      };

      {/*split the result from json response into multiple line text 
      ->json response
              this is first sentence\n this is second sentece

      ->expected output:  
                this is first sentece
                ... second sentence
      */}
      const renderResultWithLineBreaks = () => {
        if (result !== null ) {
          const lines = result.split('\n');
          return lines.map((line, index) => (
            <React.Fragment key={index}>
              {line}
              <br/>
            </React.Fragment>
          ))
        }
      };

      
  return (
    <div>
      
      <div className='h3Content'></div>
      {/*style whiteSpace: 'pre-line' to render text stored text in json format to multiple line*/}
      <div className='MessageList' style={{ whiteSpace: 'pre-line' }}> 
        {messages.map((message, index) => (
          <div key={index} className={`message-container ${message.sender === 'User' ? 'user-message' : ''}`}>
            <strong>{message.sender}:</strong> {message.content}
          </div>
        ))}
        <div className='IsTyping'>{typing ? <p>{messages[0].sender} is Typing...</p>: null}</div>
      </div>
      <div className='Result'>
        {/* Display the input value */}
          {result !== null && <p>Result: {renderResultWithLineBreaks()}</p>}
      </div>

      <div className='InputQuery'>
        {/* Input field with an onChange event handler */}
        <textarea
          type="text"
          rows={Math.min(input1.split('\n').length, 5) || 1} //make input multiple line with maxvalue
          value={input1}
          onChange={(e) => {
            setInputValue(e.target.value);}}
        />
          <button onClick={handleSend}>Send</button>
              <br />

              
      </div>
    </div>
  );
};

export default ChatWithAI;

