# Semi-Autonomous Movie Director Robot (CPSC 584 Project)

This project is a semi-autonomous movie director system built for the Picrawler robot. It allows a user to control and direct the robot through a graphical user interface (GUI) while receiving a live video stream from the robot’s camera. The system uses a server running on the robot to handle commands and communication, and a local GUI application to send instructions and display feedback in real time.

Authours: Nebila Wako and Darcy Bartolome

# Running the Robot Server and GUI

Important: Always start the server on the robot before launching the GUI.

Start the Server (From the Picrawler)

Power on the Picrawler.

Connect to the robot via SSH from your local machine:
ssh <username>@<robot_ip>

Navigate to the project directory:
cd pi/picrawler/examples/project/CPSC584MovieDirectorRobot

Run the server:
sudo python3 gui_server.py

Important:
Ensure the SERVER_HOST constant in gui_server.py is set to your machine’s IP address.

Start the GUI (on Your Local Computer)

Navigate to the submitted project folder.

Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows

Install dependencies:
pip install -r requirements.txt

Run the GUI:
python gui.py

Ensure the following values in gui.py match the server configuration:
SERVER_HOST
stream_url

Both should use the same IP address as the robot server.
