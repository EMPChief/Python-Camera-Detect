# CV2 Motion Detection Program

This is a Python program that uses the OpenCV (cv2) library to detect motion in a video stream. When motion is detected, the program sends an email notification.

## Prerequisites

Before running the program, make sure you have the following installed:

- Python 3.x
- OpenCV (cv2) library
- smtplib library (for sending email notifications)

## Installation

1. Clone the repository:

    ```shell
    git clone https://github.com/empchief/Python-Camera-Detect
    ```

2. Create and activate a virtual environment (optional but recommended):

    ```shell
    python -m venv venv
    ```

3. Start the virtual environment:
   - Windows:
     ```shell
     venv\Scripts\activate
     ```
   - Linux:
     ```shell
     source venv/bin/activate
     ```

4. Install the required dependencies:

    ```shell
    pip install opencv-python
    pip install smtplib
    ```

5. Install additional dependencies from the requirements.txt file:

    ```shell
    pip install -r requirements.txt
    ```

## Usage

1. Open the `main.py` file.

2. Modify the following variables according to your needs:

    ```python
    # Set the video source (0 for webcam, or provide a path to a video file)
    video_source = 0

    # Set the email configuration in a .env file
    email_mail=your-email@example.com
    email_password=email_pass
    email_host=smtp.gmail.com
    email_port=587
    ```

3. Run the program:

    ```shell
    python main.py
    ```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
