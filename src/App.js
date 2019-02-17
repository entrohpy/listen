import React, { Component } from "react";
import axios from 'axios';
import Header from "components/Header/";
import FileInput from "components/FileInput";
import "./App.scss";

class App extends Component {
  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.fileInput = React.createRef();
  }

  handleSubmit(event) {
    event.preventDefault();
    const file = this.fileInput.current.files[0];
    let fd = new FormData()
    fd.append('image', file)
    axios.post('/upload', fd, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response=> {
        alert("File uploaded.")
      })
      .catch(err=> {
        alert("Could not upload file.")
      })
  } 

  render() {
    return (
      <div className="App">
        <Header>Welcome to AntEater 1.0</Header>
        Upload file:
        <form action="upload" method="POST" enctype="multipart/form-data">
          <input type="file" name="file" />
          <br />
          <button type="submit">Submit</button>
        </form>
      </div>
    );
  }
}

export default App;
