const img = document.getElementById("img");
const inputFile = document.getElementById("input");
const upload = document.getElementById("upload");

const prediction = document.getElementById("prediction");

inputFile.onchange = function () {
  let input = this.files[0];
  //Displaying the Uploaded Image
  img.src = window.URL.createObjectURL(input);
  upload.innerHTML = "Image Uploaded Successfully!";
  img.style.border = "auto";
  prediction.innerHTML = "Prediction Loading ...";

  //Loading model
  mobilenet.load().then((model) => {
    // Classify the image.
    console.log(img);
    model.classify(img).then((predictions) => {
      console.log("Predictions: ");
      prediction.innerHTML =
        "This image is predicted to be a " +
        predictions[0].className +
        " with " +
        predictions[0].probability.toFixed(2) * 100 +
        " % confidence";
      console.log(predictions);
    });
  });
};
