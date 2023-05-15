# PokerHandsRecognition

PokerHandsRecognition is a Python program that uses a camera to recognize cards from a Texas Hold'em in-real-life (IRL) game and calculates the winning or draw statistics of each hand for two players.

## Index

- [Features](#features)
- [Files](#files)
- [Usage](#usage)
- [Authors](#authors)

## Features

- Card Recognition: The program uses computer vision techniques to identify and recognize playing cards from images captured by a camera.
- Hand Analysis: It analyzes the recognized cards to determine the best possible hand combinations, such as pairs, flushes, straights, etc.
- Montecarlo Simulation: Based on the identified hands, the program calculates the winning probabilities and statistics for each player or hand combination.
- Real-time Analysis: With the camera mode, you can continuously capture and analyze card images during a Texas Hold'em game, providing instant feedback on hand strengths.

## Files

- `camera.py`: The main Python script that runs the PokerHandsRecognition program. It captures images from the camera and performs card recognition and hand analysis.
- `card.py`: This script is responsible for recognizing all the cards and querying the trained model for predictions.
- `keras.ipynb`: A Jupyter Notebook that generates the VGG16 model. It uses images from the `images/training/labeled` directory for training.
- `montecarlo.py`: This script runs Monte Carlo simulations to determine the winning statistics.
- `images/`: A directory to store the captured images and the analyzed results. The original images and the analyzed images will be saved in this directory.
- `images/test/`: A directory containing test images that can be used to evaluate the program's performance or as examples for single photo analysis.
- `images/training/labeled/`: A directory containing labeled images used for training the card recognition model.
- `README.md`: This file that provides an overview of the repository and instructions for using the PokerHandsRecognition program.

## Usage

There are two usage options for running the program:

1. **Single Photo Analysis**: Run the program for a single photo by providing the path to the photo as an argument. You can use the test images available in the `images/test` directory as examples.

    ```shell
    python camera.py --arg {path_to_photo}
    ```

2. **Real-time Camera Analysis**: Connect a camera to your computer and run the program. It will display a frame, and when you press the 'p' key, it will take a screenshot and analyze the captured image. Once the analysis is completed, it will show the final analysis and save both the original and analyzed photos in the `images` directory. The program will then continue waiting for another 'p' key press. To exit the program, press the 'q' key.

    ```shell
    python camera.py
    ```

## Authors

- Álvaro Alonso Miguel

For any questions, support, or feedback, please feel free to contact me at alonso.miguel.alvaro1@gmail.com.
