#--------------------------------------------------------------------------------------------------------
# AOI Events Sample Program 2
#--------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------
# This program captures AOI Events for 10 seconds are writes them to a text file.
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
			caption = "This scenario will capture AOI events for 10 seconds and write them to a text file \"aoi_area.txt\".\n\nPlease Note:\n\nPress Esc to Stop.\nPress Enter to Start...";
			font_size = 24;
		};
		x = 0;
		y = 0;
	};
	time = 0;
	duration = response;
} my_trial;

# Capturing caption.
picture
{ 
	text
	{
		system_memory = true;
		caption = "Capturing AOI Events...";
		font_size = 24;
	};
	x = 0;
	y = 0; 
} pic_Capturing;

# Beginning of the PCL program.
begin_pcl; 

# Present the initial caption.
my_trial.present();

# Present the capturing status message.
pic_Capturing.present();

# Create a new EyeTracker object.  The object_id parameter should be the same "name"
# you registered your EyeTracker Extension with in the Extension Manager.
eye_tracker eyeTracker = new eye_tracker("ViewPoint");

# Start tracking.
eyeTracker.start_tracking();

# Start storing the AOI Data.
eyeTracker.start_data(dt_aoi);

# Create the arrays that will hold the AOI Event Data.
array<int> aoiArea[0];
array<int> aoiTime[0];

# Loop for 10 seconds while capturing the AOI Event Data.
loop
	int endTime = clock.time() + 10000; # Units are milliseconds
until 
	clock.time() > endTime
begin 
	# Check for new AOI Events.
	int aoiEventCount = eyeTracker.new_aoi_events();
	if(aoiEventCount > 0) then
		# Get the last AOI Event.
		aoi_event_data aoiEvent = eyeTracker.last_aoi_event();
	
		# Set the area and time of the AOI Event.
		aoiArea.add(aoiEvent.area());
		aoiTime.add(aoiEvent.time());
	end;
end;

# Create and open a text file.  The file will be located in Presentation's "example" folder.
output_file out = new output_file;
out.open("aoi_area.txt"); 

# Loop through all the AOI Events and write them to the file.
loop
	int index = 1; # Arrays are 1-based.
	int count = aoiArea.count();
until 
	index > count
begin 
	# Write the Area and Time.
   out.print(aoiArea[index]);
   out.print("\t");
   out.print(aoiTime[index]);
   out.print("\n");

	# Make sure we advance to the next AOI Event.
	index = index + 1;
end;

# Make sure to close the text file.
out.close();

#End of the sample code
#-------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------

