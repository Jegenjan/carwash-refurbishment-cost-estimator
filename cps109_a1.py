#Simple Carwash Tunnel Estimator Program:

#These are sub-functions which are used by the collect_project_info() function in validating inputs.
from CWE_Funcs import confirm_dimension_input
from CWE_Funcs import confirm_num_openings
from CWE_Funcs import confirm_color_choice
from CWE_Funcs import confirm_coverage

#There are 5 main functions that make up this program which run in the following order:
    
from CWE_Funcs import collect_project_info #Step 1
from CWE_Funcs import net_area_and_edge_calc #Step 2
from CWE_Funcs import final_adjustment_and_cost #Step 3
from CWE_Funcs import estimate_summary #Step 4
from CWE_Funcs import save_estimate #Step 5

#The general flow of this program is to have a function be called which then returns a tuple of variables which are then unpacked and fed as arguments into the next function in the sequence or for other functions to use further down the line, such as estimate_summary.

#This variable holds the function which gathers important details and numerical data from the user to be used in the estimating process.
project_info = collect_project_info()

project_name, cw_length, cw_width, cw_height, coverage, oh_door_dims, man_door_dims, window_dims, wall_color, ceiling_color = project_info

#This variable holds the function that will take all the user input date from project_info and calculate material amounts based on info inputted by the user
calculated_values = net_area_and_edge_calc(cw_length ,cw_width ,cw_height, oh_door_dims, man_door_dims, window_dims, coverage)

net_wall_area, total_ceiling_area, total_j_trim, total_crown_trim, total_corner_trim, ceiling_j_trim = calculated_values

#These preset values are the assigned costs for material types
surface_rate = (2.47, 3.02, 4.73) # $ / sq. ft - (white, bright white, black)
j_trim_rate = (0.82, 0.90, 1.15) # $ / ft - (white, bright white, black)
crown_trim_rate = 2.85 # $ / ft
corner_trim_rate = (2.62, 2.86, 3.28) # $ / ft - (white, bright white, black)

#This variable holds the function which will filter through the calculated data and determine their costs based on calculated values
finalize_details = final_adjustment_and_cost (net_wall_area, total_ceiling_area, total_j_trim, total_crown_trim, total_corner_trim, ceiling_j_trim, coverage, wall_color, ceiling_color, surface_rate, j_trim_rate, crown_trim_rate, corner_trim_rate)

total_cost, cost_wall, cost_ceiling, cost_j, cost_ceiling_j, cost_corner, cost_crown = finalize_details

#This variable holds the function which collects all the variables of interest in one place and returns the end result to the user.
conclusion = estimate_summary(project_name, cw_length, cw_width, cw_height, coverage, total_cost, cost_wall, cost_ceiling, cost_j, cost_ceiling_j, cost_corner, cost_crown, wall_color, ceiling_color, net_wall_area, total_ceiling_area, total_j_trim, total_crown_trim, total_corner_trim, ceiling_j_trim)

print(conclusion)

#Allows the user to export the estimate to a text document.
save_estimate(project_name, conclusion)





