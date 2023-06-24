# Python Desktop Application - <b> <em> Typing Speed Calculator </em> </b>

Using Python's "tkinter" library, I have developed an engaging desktop application that allows users to test and improve their typing speed. With a user-friendly interface, the application prompts users to type several displayed texts within a specified time limit. After completing the typing session, the application calculates the user's typing speed, providing valuable feedback and an opportunity for skill enhancement. This interactive and educational tool is perfect for individuals seeking to enhance their typing proficiency in a fun and intuitive way.

<div>
  <img src="./typing_speed_tester_output.gif" alt="Code Output">
</div>

<hr>
  <h1> Program Flowchart </h1>
  <div>
    <img src="./Typing Speed Calculator Flowchart.png" alt="Program Flowchart">
  </div>
<hr>

<h1> Guide to Build This Project <i>(Work in Progress)</i> </h1>

<b> <em> Text </em> </b>

<h3> Step 1: Setting up the UI  </h3>
<p>
  Import tkinter library. Use its <b> <em> Tk() </em> </b> class to create a screen object. Give it a title using <b> <em> title </em> </b> method. 
  Decide on a color pallete to use and store the <b> <em> #hexcodes </em> </b> in constants. Also create some tuples and store them in some constants to give
  our fonts some styling. We need a total of 7 widgets - 2 Buttons (Reset and Show overall average speed), 
  4 Labels (Heading, Sentence that user has to type, Instructions, and Speed result), and 1 Typing Area using Text. 
  We place them on screen using grid layout system.
  The overall speed result is hidden as we want it to be shown only when user has typed something and it is evaluated.
  We give them necessary colors, borders and font styles using our constants.
</p>

<h3> Step 2: Setting up Globals  </h3>
<p>
  Next step is to setup some global variables because We want some values to persist their value outside the function that will hold the logic of our application.
  One is the user entered line, previous line, a list of speeds per tries, two time tracking variables, beginning and current time, and a boolean to determine if
  user typing is allowed or not. We also need a global to keep the sentences that will be diplayed to user to type for test.
</p>

<h3> Step 3: User Starts Typing  </h3>
<p>
  Text
</p>

<h3> Step 4: Checking Speed and Accuracy  </h3>
<p>
  Text
</p>

<h3> Step 5: Automatic Reset  </h3>
<p>
  Text
</p>

<h3> Step 6: Average Speed  </h3>
<p>
  Text
</p>

<hr>
