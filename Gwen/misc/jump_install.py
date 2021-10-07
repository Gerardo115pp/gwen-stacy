import os

# necesary steps or configurations needed to run jump
# installer will look for install fucntion in this file and will execute it on its corresponding directory
def install() -> None:
    # we only need to assure that checkpoints.json exists
    checkpoint_file = os.path.join(os.getcwd(), 'checkpoints.json')
    if not os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'w') as f:
            f.write('{}')
    