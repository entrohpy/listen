import React from "react";
import './index.scss';

const FileInput = ({
  children,
  onSubmit,
  fileRef,
}) => {

    return (
      <form action="upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="file" ref={fileRef} />
        <br />
        <button type="submit">Submit</button>
      </form>
    );
};

export default FileInput;
