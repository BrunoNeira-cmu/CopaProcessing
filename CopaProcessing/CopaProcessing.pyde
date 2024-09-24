# Import necessary libraries
from processing.data import Table, TableRow

# Global variables
data = None  # This will hold the CSV data
current_pass_index = 0  # Keep track of which pass we're animating
start_time = 0  # Time when a pass animation starts
is_animating = False  # Flag to indicate if a pass is being animated
pass_duration = 0  # Duration of the current pass

# Starting and ending coordinates for the current pass
start_x = 0
start_y = 0
end_x = 0
end_y = 0

# Particle position (for animation)
current_x = 0
current_y = 0

# Scaling factor (6x)
SCALE_FACTOR = 6

# Flag to retain trails
retain_trails = False


def setup():
    global data
    size(720, 480)  # Set the window size to 720x480 pixels
    data = loadTable("/Users/brunoneira/Documents/Uni/Classes/year 4/Designing Human Centered Software/HW4/CopaProcessing/ecuador_passes_v1.csv", "header")  # Load the CSV file with headers    
    background(0)  # Black background
    frameRate(60)  # Set frame rate for smooth animation

def draw():
    global current_x, current_y, start_time, is_animating, current_pass_index, pass_duration
    
    # Only reset background if trails are not retained
    if not retain_trails:
        background(0)
    
    # Check if a pass is being animated
    if is_animating:
        elapsed_time = (millis() - start_time) / 1000.0  # Time since animation started (in seconds)
        
        # Calculate the progress of the animation (0 to 1)
        progress = min(elapsed_time / pass_duration, 1)
        
        # Calculate the current position of the pass using linear interpolation
        current_x = lerp(start_x, end_x, progress)
        current_y = lerp(start_y, end_y, progress)
        
        # Draw the trail (line) from start to the current position
        stroke(255, 255, 0)  # Yellow color
        strokeWeight(2)
        line(start_x, start_y, current_x, current_y)
        
        # Draw the particle (circle) representing the tip of the pass
        fill(255, 255, 0)
        noStroke()
        ellipse(current_x, current_y, 10, 10)
        
        # Check if the pass animation is done
        if progress >= 1:
            is_animating = False  # Stop animating the current pass
            current_pass_index += 1  # Move to the next pass
            
            # If we've reached the end of the dataset, reset
            if current_pass_index >= data.getRowCount():
                current_pass_index = 0

    else:
        # Start animating the next pass
        start_next_pass()

def start_next_pass():
    global start_time, is_animating, pass_duration
    global start_x, start_y, end_x, end_y, current_x, current_y
    
    # Get the next pass data
    row = data.getRow(current_pass_index)
    
    # Extract the starting and ending coordinates
    # Scale the coordinates by the scaling factor (6x)
    start_x = row.getFloat("start_x") * SCALE_FACTOR
    start_y = row.getFloat("start_y") * SCALE_FACTOR
    end_x = row.getFloat("end_x") * SCALE_FACTOR
    end_y = row.getFloat("end_y") * SCALE_FACTOR
    
    # Set the current position to the start
    current_x = start_x
    current_y = start_y
    
    # Get the duration of the pass and set up animation
    pass_duration = row.getFloat("duration")
    start_time = millis()  # Record the time when the animation starts
    is_animating = True  # Start animating

def keyPressed():
    global retain_trails
    # Toggle retaining trails when space bar is pressed
    if key == ' ':
        retain_trails = not retain_trails
    
    # Reset the canvas when backspace/delete is pressed
    if key == DELETE or key == BACKSPACE:
        background(0)
