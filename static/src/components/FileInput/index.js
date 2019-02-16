import React from "react";
import './index.scss';

const FileInput = ({
  children,
  onSubmit,
  fileRef,
}) => {

    return (
      <form onSubmit={onSubmit}>
        <input type="file" ref={fileRef} />
        <br />
        <button type="submit">Submit</button>
      </form>
    );
};

export default FileInput;
