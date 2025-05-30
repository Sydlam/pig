#--------------------------------------------------------------------------------------------------------
# AOI Events Sample Program 1
#--------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------
# The picture stimulus changes color as the eye moves.  When the eye is in the AOI, the picture stimulus
# is "blue" and when the eye is not in the AOI, the picture stimulus is "green".
#--------------------------------------------------------------------------------------------------------

# You must make 1 button active.
# To make the "Enter" button active, go to the "Settings" tab and select the "Response" button on the left.
# In the "Scenarios" box select this scenario.  In the "Active Buttons" list view, make sure there are no
# buttons active by pressing the "Clear" button to the right of the list.  In the "Devices" box, select the
# "Keyboard" item.  In the "Buttons" box, scroll down and select the "Enter" item.  Press the "Use" button
# to the right to add the "Enter" button to the "Active Buttons" list.
active_buttons = 1;
button_codes = 1;

begin;

# Initial caption.
trial
{
	trial_type = first_response;
	picture
	{
		text
		{
			system_memory = true;
			caption = "The movement of the eye moves the box in this scenario.\n\nPlease Note: This scenario will last for 60 seconds.\n\nPress Esc to Stop.\nPress Enter to Start...";
			font_size = 24;
		};
		x = 0;
		y = 0;
	};
	time = 0;
	duration = response;
} my_trial;

# Displayed when eye is not in AOI (Green).
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
} pic_notAOI;

# Displayed when eye is in AOI (Blue).
picture
{
	box
	{
		height = 75;
		width = 75;
		color = 0,0,255;
	}; 
	x = 0;
	y = 0; 
} pic_AOI;

# Beginning of the PCL program.
begin_pcl; 

# Present the initial caption.
my_trial.present();

# Get the screen width and height.
int w = display_device.width();
int h = display_device.height();
double screenWidth = double(w);
double screenHeight = double(h);

# Create a new EyeTracker object.  The object_id parameter should be the same "name"
# you registered your EyeTracker Extension with in the Extension Manager.
eye_tracker eyeTracker = new eye_tracker("ViewPoint");

# Start tracking.
eyeTracker.start_tracking();

# Start storing the Position and AOI Data.
eyeTracker.start_data(dt_position, true);
eyeTracker.start_data(dt_aoi);

# Loop for 1 minute (60 seconds) while showing the AOI Events.
loop
	int endTime = clock.time() + 60000; # Units are milliseconds
until 
	clock.time() > endTime
begin 
	# Check for new AOI Events.
	int aoiEventCount = eyeTracker.new_aoi_events();
	if(aoiEventCount > 0) then
		# Check for new Position Data.
		int posDataCount = eyeTracker.new_position_data();
		if(posDataCount > 0) then
			# Get the Position Data and scale to Screen coordinates.
			eye_position_data position = eyeTracker.last_position_data();
			double x = position.x() * (-screenWidth);
			double y = position.y() * screenHeight;
		
			# Get the last AOI Event.
			aoi_event_data aoiEvent = eyeTracker.last_aoi_event();
		
			# Get the area of the AOI.  If > 0 then AOI, else NOT AOI.
			int InAOI = aoiEvent.area();
			if(InAOI > 0) then
				# Display the AIO box.
				pic_AOI.set_part_x(1, x);
				pic_AOI.set_part_y(1, y);
				pic_AOI.present();
			else
				# Display the non AIO box.
				pic_notAOI.set_part_x(1, x); 
				pic_notAOI.set_part_y(1, y);
				pic_notAOI.present();
			end;
		end;
	end;
end;

#End of the sample code
#-------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------