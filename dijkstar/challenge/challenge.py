# Once Unop a Dijkstar Challenge
import os, sys, subprocess
from time import sleep

from timeout import timeout, TimeoutError
time = int(os.getenv("TIMEOUT",10))

ship_name = "ShippyMcShipFace"

# Challenge Intro
def render_intro():
    intro = [f"You were on your way to your honeymoon in Bora Bora when your ship, {ship_name}, breaks down. You find "
             f"yourself stranded in the middle of the Pacific Ocean.",
             f"Thankfully you have just subscribed to the new global Starlunk network for a very affordable $110/month! "
             f"Unfortunately, adversaries have corrupted the binary that is used to determine what string of satellites to "
             f"route packets through within the Starlunk network. Because you have been spending countless hours on Youtube "
             f"learning about the new network, you know that the nearest base station to you is in Honolulu, Hawaii. You also "
             f"managed to find the corrupted binary on the internet before you left for your trip. You and all those aboard "
             f"{ship_name} are counting on you to patch the binary so that you can uncover the route to send your packets "
             f"in order to get help. \n",
             f"Do you have what it takes to save yourself and those aboard {ship_name}?\n"
    ]

    for row in intro:
        print(row)
        sleep(0.05)
    
    return

@timeout(time)
def challenge():
    print(f"Please submit the resulting route from {ship_name} to Honolulu. Only include Satellite ID's with the 'Starlunk-' omitted. "
          f"For instance if the output from the corrected binary was: \n\n"
          f"{ship_name}\nStarlunk-00-901\nStarlunk-06-22\nStarlunk-105-38\nHonolulu\n\n"
          f"You would submit: '00-901, 06-22, 105-38' without the quotes.\n"
          f"Your answer:")
    answer = input()

    if answer.replace(" ", "").replace("\n", "").strip() == calculate_route():
        return True

    return False

def calculate_route():
    # Run once_unop_a_dijkstar and get the output. Split by the new lines and strip off first and last elements (non-Starlunk satellites).
    sats = subprocess.check_output("/challenge/test.sh").decode("utf-8").split("\n")[1:-2]

    # Strip off the "Starlunk-" part of the name and the trailing '"'
    result = []
    for sat in sats:
        result.append(sat.split("Starlunk-")[1][:-1])

    return ",".join(result)


if __name__ == "__main__":
    
    render_intro()
    
    try:
        success = challenge()
    except TimeoutError:
        sys.stdout.write("\nTimeout, Bye\n")
        sys.exit(1)
    
    if success:
        print(f"You saved those aboard {ship_name}! Here's your flag:")
        flag = os.getenv('FLAG')
        print(flag)

    else:
        print("That didn't work, try again!")
