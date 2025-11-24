#Functions for Carwash Estimator Program:

def confirm_dimension_input(cue):
    """
    This function will repeatedly request a valid input from the user if invalid dimension input is entered.
    """
    while True:
        try:
            dim_input = float(input(cue))
            if dim_input < 0:
                print("Dimension input cannot be a negative value. Please enter a non-negative value.")
            else:
                return dim_input
        except ValueError:
            print("The input you have entered is invalid. Please enter a valid dimension")

def confirm_num_openings(cue):
    """
    This function will repeatedly request a valid input from the user if an invalid quantity is entered.
    """
    while True:
        try:
            num_input = int(input(cue))
            if num_input < 0:
                print("Dimension input cannot be a negative value. Please enter a non-negative value.")
                continue
            return num_input
        except ValueError:
            print("The input you have entered is invalid. Please enter a valid number")

def confirm_color_choice(cue):
    """
    This function will repeatedly request a valid input from the user if an invalid color code is entered.
    """
    color_options = ['w','bw','b']
    while True:
        color_input = input(cue)
        if color_input in color_options:
            return color_input
        else:
            print("Invalid color selected. Please choose from one of the 3 options allowed [w/bw/b]: ")

def confirm_coverage(cue):
    """
    This function will repeatedly request a valid input from the user if an invalid coverage code is entered.
    """
    coverage_options = ['w','wc','c']
    while True:
        coverage_input = input(cue)
        if coverage_input in coverage_options:
            return coverage_input
        else:
            print("Invalid coverage selected. Please choose from one of the 3 options allowed [w/wc/c]: ")

def collect_project_info():
    """
    This function gathers the project details from the user and then returns variable values/inputs
    to be utilized in the rest of the estimating process.
    """
    print("Greetings user! To create your new estimate, please provide details to the following prompts:")
    
    project_name = input("\nEnter a project name for the estimate: ")
    
    print("\nTUNNEL DIMENSIONS - please input numerical values only [in feet]")
    cw_length = confirm_dimension_input("Tunnel Length: ")
    cw_width = confirm_dimension_input("Tunnel Width: ")
    cw_height = confirm_dimension_input("Tunnel Height: ")
    
    print("\nPlease indicate choice of surface(s) to be covered by selecting one of the following [w/wc/c]")
    coverage = confirm_coverage("[w] = walls only, [wc] = walls and ceiling [c] = ceiling only\n")
    
    oh_door_dims = []
    man_door_dims =[]
    window_dims =[]
    num_oh_doors = 0
    num_man_doors = 0
    num_windows = 0
    
    #If walls included, this preemptively calculates total wall area to be used in a test later that ensures the area of openings does not exceed wall surface area.
    wall_area_test = 0
    if coverage == 'w' or coverage == 'wc':
        wall_area_test = (2 * cw_length * cw_height) + (2 * cw_width * cw_height)
    
    if coverage == 'w' or coverage == 'wc':
        num_oh_doors = confirm_num_openings("\nPlease enter the number of overhead door(s): ")
    
    if num_oh_doors > 0:
        for i in range(1, num_oh_doors + 1):
            print(f"Please enter the dimensions for Door#{i}")
            
            height = confirm_dimension_input(f"Height of OH Door#{i} [in feet]: ")
            width = confirm_dimension_input(f"Width of OH Door#{i} [in feet]: ")
            
            oh_door_dims.append((height,width))
    
    if coverage == 'w' or coverage == 'wc':
        num_man_doors = confirm_num_openings("\nPlease enter the number of man door(s): ")
    
    if num_man_doors > 0:
        for i in range(1, num_man_doors + 1):
            print(f"Please enter the dimensions for Man Door(s)#{i}")
            
            height = confirm_dimension_input(f"Height of Man Door#{i} [in feet]: ")
            width = confirm_dimension_input(f"Width of Man Door#{i} [in feet]: ")
            
            man_door_dims.append((height,width))
    
    if coverage == 'w' or coverage == 'wc':
        num_windows = confirm_num_openings("\nPlease enter the number of window(s): ")
    
    if num_windows > 0:
        for i in range(1, num_windows + 1):
            print(f"Please enter the dimensions for Window#{i}")
            
            height = confirm_dimension_input(f"Height of Window#{i} [in feet]: ")
            width = confirm_dimension_input(f"Width of Window#{i} [in feet]: ")
            
            window_dims.append((height,width))
    
    #This checks if the openings provided work with the available surface area of the wall, if it doesn't - an error message is displayed and the program restarts recursively.
    
    openings_area_test = 0
    combined_opening_dims = oh_door_dims + man_door_dims + window_dims
    height_test, width_test = zip(*combined_opening_dims)
    openings_area_test = sum(height_test) * sum(width_test)
 
    if openings_area_test > wall_area_test:
        print("Error: The total area of openings exceeds the wall area!")
        print("The estimate has been terminated.\n\n\n")
        print("... Program restarting...\n\n\n")
        return collect_project_info()
    
    wall_color = 'N/A'
    ceiling_color = 'N/A'
    
    if coverage == 'w':
        print("\nWhat color of Wall material would you like? ")
        print("[w] = white, [bw] = bright white, [b] = black")
        wall_color = confirm_color_choice("Please enter a color selection [w/bw/b]: ")
        
    elif coverage == 'wc':
        print("\nWhat color of Wall material would you like? ")
        print("[w] = white, [bw] = bright white, [b] = black\n")
        wall_color = confirm_color_choice("Please enter a color selection [w/bw/b]: ")
        
        print("\nWhat color of Ceiling material would you like? ")
        print("[w] = white, [bw] = bright white, [b] = black\n")
        ceiling_color = confirm_color_choice("Please enter a color selection [w/bw/b]: ")
    
    elif coverage == 'c':
        print("\nWhat color of Ceiling material would you like? ")
        print("[w] = white, [bw] = bright white, [b] = black\n")
        ceiling_color = confirm_color_choice("Please enter a color selection [w/bw/b]: ")
    
    return project_name, cw_length, cw_width, cw_height, coverage, oh_door_dims, man_door_dims, window_dims, wall_color, ceiling_color

def net_area_and_edge_calc(cw_length ,cw_width ,cw_height, oh_door_dims, man_door_dims, window_dims, coverage):
    """
    This function takes the user inputs and calculates total wall area,openings area and edges as well as remaining bottom of wall edges to be trimmed and then takes the difference of surface area to provide the net surface area and total amount of edge length for determining trim amounts.
    """
    
    total_wall_area = 0
    total_openings_area = 0
    net_wall_area = 0
    
    total_ceiling_area = 0
    
    total_oh_door_edges = 0
    total_oh_door_area = 0
    total_oh_door_widths = 0
    
    total_man_door_edges = 0
    total_man_door_area = 0
    total_man_door_widths = 0
    
    total_window_edges = 0
    total_window_area = 0
    
    total_j_trim = 0
    total_btm_wall_trim = 0
    total_top_j_trim = 0
    total_crown_trim = 0
    total_corner_trim = 0
    ceiling_j_trim = 0
    
    #Depending what coverage was chosen, the below conditionals factor in wall-only, ceiling-only or both.
    if coverage == 'w' or coverage == 'wc':
        
        long_walls_area = 2 * cw_length * cw_height
        short_walls_area = 2 * cw_width * cw_height
        
        total_wall_area = long_walls_area + short_walls_area
    
    if coverage == 'wc' or coverage == 'c':
        
        total_ceiling_area = cw_length * cw_width
    
    #Depending on if wall-ceiling [wc] or just the wall [w] or just the ceiling [c] is selected, trim is calculated at the top edge of the wall and ceiling junction (if applicable) accordingly.
    if coverage == 'wc':
        
        total_crown_trim = (2 * cw_length) + (2 * cw_width)
        
    elif coverage == 'w':
        
        total_top_j_trim = (2 * cw_length) + (2 * cw_width)
    
    elif coverage == 'c':
        
        ceiling_j_trim = (2 * cw_length) + (2 * cw_width)
    
    #If overhead doors were included, their parameters are calculted in this conditional block.
    if len(oh_door_dims) > 0:
        
        oh_door_heights, oh_door_widths = zip(*oh_door_dims)
        total_oh_door_heights = 2 * sum(oh_door_heights)
        total_oh_door_widths = sum(oh_door_widths)
        
        total_oh_door_edges = total_oh_door_heights + total_oh_door_widths
        
        total_oh_door_area = sum(oh_door_heights) * sum(oh_door_widths)
    
    #If man doors were included, their parameters are calculated in this conditional block.
    if len(man_door_dims) > 0:
        
        man_door_heights, man_door_widths = zip(*man_door_dims)
        total_man_door_heights = 2 * sum(man_door_heights)
        total_man_door_widths = sum(man_door_widths)
        
        total_man_door_edges = total_man_door_heights + total_man_door_widths
        
        total_man_door_area = sum(man_door_heights) * sum(man_door_widths)
    
    #If windows were included, their parameters are calculated in this conditional block.
    if len(window_dims) > 0:
        
        window_heights, window_widths = zip(*window_dims)
        total_window_heights = 2 * sum(window_heights)
        total_window_widths = 2 * sum(window_widths)
        
        total_window_edges = total_window_heights + total_window_widths
    
        total_window_area = sum(window_heights) * sum(window_widths)
    
    #The calculations below conclude the totals of net area, various trimming before returning the values.
    
    if coverage == 'w' or coverage == 'wc':
        total_btm_wall_trim = (2 * cw_length) + (2 * cw_width) - total_oh_door_widths - total_man_door_widths
    
    total_openings_area = total_oh_door_area + total_man_door_area + total_window_area
    
    net_wall_area = total_wall_area - total_openings_area
    
    total_j_trim = total_btm_wall_trim + total_window_edges + total_oh_door_edges + total_man_door_edges + total_top_j_trim
    
    if coverage == 'w' or coverage == 'wc':
        total_corner_trim = 4 * cw_height
    
    return net_wall_area, total_ceiling_area, total_j_trim, total_crown_trim, total_corner_trim, ceiling_j_trim

def final_adjustment_and_cost(net_wall_area, total_ceiling_area, total_j_trim, total_crown_trim, total_corner_trim, ceiling_j_trim, coverage, wall_color, ceiling_color, surface_rate, j_trim_rate, crown_trim_rate, corner_trim_rate):
    """
    This function takes the total calculated values and applies a color and cost factor to the total values.
    """
    
    cost_wall = 0
    cost_j = 0
    cost_corner = 0
    cost_crown = 0
    cost_ceiling = 0
    cost_ceiling_j = 0
    
    #Calculates cost of wall area and wall related J trim based on color selected.
    if coverage == 'w' or coverage == 'wc':
        if wall_color == 'w':
            cost_wall = surface_rate[0] * net_wall_area
            cost_j = j_trim_rate[0] * total_j_trim
            cost_corner = corner_trim_rate[0] * total_corner_trim
        elif wall_color == 'bw':
            cost_wall = surface_rate[1] * net_wall_area
            cost_j = j_trim_rate[1] * total_j_trim
            cost_corner = corner_trim_rate[1] * total_corner_trim
        elif wall_color == 'b':
            cost_wall = surface_rate[2] * net_wall_area
            cost_j = j_trim_rate[2] * total_j_trim
            cost_corner = corner_trim_rate[2] * total_corner_trim
    
    #Calcualtes crown trim as transition material only in the case that wall and ceiling are selected.
    if coverage == 'wc':
        cost_crown = crown_trim_rate * total_crown_trim
    
    #Calculates cost of ceiling area based on color selected.
    if coverage == 'c' or coverage == 'wc':
        if ceiling_color == 'w':
            cost_ceiling = surface_rate[0] * total_ceiling_area
        elif ceiling_color == 'bw':
            cost_ceiling = surface_rate[1] * total_ceiling_area
        elif ceiling_color == 'b':
            cost_ceiling = surface_rate[2] * total_ceiling_area
    #Calculates the cost of ceiling j trim if only ceiling is chosen and also based on color choice.
    if coverage == 'c':
        if ceiling_color == 'w':
            cost_ceiling_j = j_trim_rate[0] * ceiling_j_trim
        elif ceiling_color == 'bw':
            cost_ceiling_j = j_trim_rate[1] * ceiling_j_trim
        elif ceiling_color == 'b':
            cost_ceiling_j = j_trim_rate[2] * ceiling_j_trim
    
    total_cost = cost_wall + cost_ceiling + cost_j + cost_ceiling_j + cost_corner + cost_crown
    
    return total_cost, cost_wall, cost_ceiling, cost_j, cost_ceiling_j, cost_corner, cost_crown
    
def estimate_summary(project_name, cw_length, cw_width, cw_height, coverage, total_cost, cost_wall, cost_ceiling, cost_j, cost_ceiling_j, cost_corner, cost_crown, wall_color, ceiling_color, net_wall_area, total_ceiling_area, total_j_trim, total_crown_trim, total_corner_trim, ceiling_j_trim):
    """
    The purpose of this function is to output a cost summary based on all the processed information.
    """
    summary = f"""
=============================
Project Name: {project_name}
-----------------------------
Carwash Dimensions: {cw_length} ft X {cw_width} ft X {cw_height} ft
Coverage Type: {coverage}

Wall Area: {net_wall_area} sq. ft (openings deducted)
Wall J Trim Total: {total_j_trim} ft (openings and exposed edges, ie. bottom of wall, or top if no ceiling)
Wall Corner Trim: {total_corner_trim} ft (vertical wall corners)
Wall Color: {wall_color}
Wall Trim Color: {wall_color}

Ceiling Area: {total_ceiling_area} sq. ft
Ceiling J Trim Total: {ceiling_j_trim} ft
Ceiling Color: {ceiling_color}
Ceiling Trim Color: {ceiling_color}

Crown Trim Total: {total_crown_trim} ft (wall to ceiling transitions, if applicable)

Cost Breakdown:
-----------------------------
Cost of Wall Material: ${cost_wall:,.2f}
Cost of Ceiling Material: ${cost_ceiling:,.2f}

Cost of Wall J Trim: ${cost_j:.2f}
Cost of Ceiling J Trim: ${cost_ceiling_j:,.2f}

Cost of Corner Trim: ${cost_corner:,.2f}

Cost of Crown Trim: ${cost_crown:,.2f}

TOTAL COST: ${total_cost:,.2f}
=============================
"""
    return summary
    
def save_estimate(project_name, conclusion):
    """
    This function allows the user to save the estimate to a text file.
    """
    
    print("\nWould you like to save this project estimate?")
    choice = input("[y] = yes // [n] = no:\n")
    
    valid_choices = ('y', 'n')
    
    if choice not in valid_choices:
        print("The input you have entered is invalid. Please enter a valid input [y] or [n]")
        return save_estimate(project_name, conclusion)
        
    if choice == 'y':
        with open(project_name, 'w') as file:
            file.write(conclusion)
        print(f"The estimate has been saved as: <{project_name}>")
    else:
        print("The estimate has not been saved.")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    