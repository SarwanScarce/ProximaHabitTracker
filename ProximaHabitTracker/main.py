# Used to import create_habit import new_habit
from create_habit import new_habit
# Used to import record_performance import new_record
from record_performance import new_record
# Used to import track_habits import track_a_habit
from track_habits import track_a_habit
# Used to import remove_records import remove_a_habit
from remove_records import remove_a_habit


# Used to create a habit
print('Option A: Create a Habit')

# Used to record performance
print('Option B: Record Performance')

# Used to track performance
print('Option C: Track Habits')

# Used to track performance
print('Option D: Remove a Habit')

# Used to prompt the user to choose one of the options presented
chosen_option = input('What would you like to do today?: ')

# Calls the new_habit() function to add a new habit
if (chosen_option == 'A'):
    new_habit()

# Calls the new_record() function to check off a habit
elif (chosen_option == 'B'):
    new_record()

# Calls the track_a_habit() function to analyze performance
elif (chosen_option == 'C'):
    track_a_habit()

# Calls the remove_a_habit() function to remove a habit and related records
elif (chosen_option == 'D'):
    remove_a_habit()

else:
    # Restricts the options the user can choose
    print('Please choose from options A, B, C or D')
    # The user clicks the run button to carry out another action
    print("Click Rerun to continue")