#--------------------------------------------------------------------------------------------------------
# Calibration Sample Program 3
#--------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------
# This program calibrates 12 points sequentially displaying a white cross for each calibration point.
#--------------------------------------------------------------------------------------------------------

begin; 
 
# The default picture stimulus of the presentation is a white cross. 
# If you want to have your own picture stimulus then it has to be created
# with name "et_calibration" like shown below.
picture
{ 
	box
	{
		height = 75;
		width = 75;
		color = 0,255,0;
	}; 
 
	x = 0;
	y = 0; 
} pic;
 
# Beginning of the PCL program.
begin_pcl; 
 
# Create a new EyeTracker object.  The object_id parameter should be the same "name"
# you registered your EyeTracker Extension with in the Extension Manager.
eye_tracker eyeTracker = new eye_tracker("ViewPoint");
 
#Call the calibrate function
#calibrate function parameters
#1. Calibration type it has be set to 10
#2. parameter1 : number of stimulus points
#   (b>0) : a positive value --> reset ViewPoint number of calibration points (NOTE: removes previous calibrations)
#   (b==-1) : a negative one --> do not respecify, just use the current ViewPoint specification.
#3. parameter2 : auto calibrate(-1) or point calibrate(point number to be calibrated)
#   (b>0) : a positive value --> calibrate only that point number.
#   (b==-1) : a negative one --> do sequential calibration
#   (b==-2) : a negative two --> do random calibration (currently locally randomized internal to the EyeTracker2 interface, not ViewPoint random sequence)
#4. parameter3 : timeOut value in seconds  

# Calibrates 12 points sequentially.
eyeTracker.calibrate(10,12.0,-1.0,2.0);
 
# Calibrates 12 points randomly.
#eyeTracker.calibrate(10,12.0,-2.0,2.0);

# Calibrates only point 1 (single point).  Does not reset the calibration data.
#eyeTracker.calibrate(10,-1.0,1.0,2.0);
