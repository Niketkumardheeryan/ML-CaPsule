// import logo from "./logo.svg";
import "./App.css";
import { useState } from "react";
function App() {
  const [file, setfile] = useState(null);
  const [breed, setbreed] = useState(null);
  const [sent, setsent] = useState(false);
  const [dat, setdat] = useState(null);
  const clickhand = async (e) => {
    setfile(e.target.files[0]);
    console.log("clicked");
  };
  const uploadagain = () => {
    setsent(false);
    window.location.reload();
  };
  const imgupload = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }
    setsent(true);
    const formData = new FormData();
    formData.append("image", file);

    const response = await fetch("/classify", {
      method: "POST",
      body: formData,
    });

    // Trigger the file input click event when the custom button is clicked

    if (response.status === 200) {
      const text = await response.text();

      // setbreed(text);
      // console.log(JSON.parse(text)["dat"]);
      console.log(JSON.parse(text));
      setbreed(JSON.parse(text)["dog"]);
      setdat(JSON.parse(text)["dat"]);
      // console.log(text["dat"]);
      // console.log(text[1]);
      // console.log(text.length);
    } else {
      console.log("Error from API.");
      // setResult("Error from API.");
    }
  };
  return (
    <div className="App">
      {!sent && (
        <div className="preupload">
          <label for="file">DOG BREED CLASSIFIER</label>
          <br />
          <input type="file" accept="image/*" onChange={clickhand} />
          <button onClick={imgupload}>submit</button>
        </div>
      )}
      <div className="onupload">
        {sent && <label for="file">DOG BREED CLASSIFIER</label>}
        {sent && <img src={URL.createObjectURL(file)} alt="file"></img>}
        {sent && <button onClick={uploadagain}>Upload again</button>}
        {breed && <h2>Dog Breed :</h2>}
        {breed && <h1 class="breed">{breed}</h1>}
        {sent && !breed && <h1>Classifying...</h1>}
        {dat && (
          <>
            <hr></hr>
            <h1>
              About :<br />
            </h1>
            <h2>{dat}</h2>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
