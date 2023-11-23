import './App.css';
import ChatWithAI from './components/chat';
import FileUploadComponent from './components/FileUploadComponent';

function App() {
  return (
    <div className="App">
      <div className="left-side">
        <FileUploadComponent/>
        <h1>content here</h1>
      </div>
      <div className='right-side'>
        <div className='CVSU-logo'>logo here</div>
        <div className='chat-area'>
          <ChatWithAI/>
        </div>  
      </div>
 
    </div>
  );
}
export default App;
