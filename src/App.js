import React, { Component } from "react";
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
    alert(`Selected file - ${this.fileInput.current.files[0].name}`);
  }

  render() {
    return (
      <div className="App">
        <Header>Welcome to AntEater 1.0</Header>
        Upload file:
        <FileInput onSubmit={this.handleSubmit} fileRef={this.fileInput} />
      </div>
    );
  }
}

export default App;
