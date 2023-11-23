import React, { useState } from "react";


const FileUploadComponent = () => {
    const [selectedFile, setSelectedFile] = useState(null);

    //handle change selectedFile
    const handFileChange = (event) => {
        const file = event.target.files[0];

        if (file && file.type === 'application/pdf'){
            setSelectedFile(file);
        }else {
            alert('input a valid pdf file');
            event.target.value = null;
        }
    };

    //upload file to php flask server

    const handleFileUpload = async () => {
        if (!selectedFile){
            
            return alert ('Please select a file');
        }
        const fromData = new FormData();
        fromData.append('file', selectedFile);

        try {
            const response = await fetch('http://localhost:5000/upload-file', {
                method: 'POST',
                body: fromData,
            });

            if(response.ok) {
                console.log('file successfully uploaded');
            } else {
                const data = await response.json();
                console.log('Error:' + data.error)
            }
        } catch (error) {
            console.error('Error ...', error);
        }
    }
    //this is good
    return (
        <div>
            <label htmlFor="pdfInput">select a pdf file</label>
            <input 
                type="file"
                id="inputFile"
                accept=".pdf"
                onChange={handFileChange}
            />
            <button onClick={handleFileUpload}>send to server</button>
        </div>
    );
}

export default FileUploadComponent;
