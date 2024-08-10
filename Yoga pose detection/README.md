# Yoga Pose detection

<h1>Description</h1>
This project as the name suggests can predict the yoga pose which you are doing in front of the webcam.<br>
This project comprise of three python scripts namely,<br>
Data Collection<br>
Data Training<br>
And finally Inference script.<br>
As all of the name suggest do there respective work.<br>

For this project I used mediapipe pose detection to detect the human body pose and after that I made model with simple Dense network using keras and trained the model on the data. After that i just ran the inference file to do the prediction.<br>

<h1>Requirements</h1>
<code>pip install mediapipe</code><br>
<code>pip install keras</code><br>
<code>pip install tensorflow</code><br>
<code>pip install opencv-python</code><br>
<code>pip install numpy</code><br>

<h1>How to Run?</h1>
<h2>Adding Data</h2>
  To add data you have to run <b>python data_collection.py</b> and  have to provide the name of asana you want to add.
 <h2>Training</h2>
  To train just run <b>python data_training.py</b> to train the model on newly added data.
  <h2>Running</h2>
  To Run just run <b>python inference.py</b> and new window will pop up which will be running the predictions.
  
  
  

  
