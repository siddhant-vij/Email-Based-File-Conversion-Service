# Email-Based File Conversion Service

This service allows users to convert documents between different formats via email. Users send an email with the subject line indicating the desired conversion formats (e.g., "[DOCX] to [PDF]") and the document as an attachment. The service processes the request and sends back the converted file.

## Table of Contents

1. [Features](#features)
1. [Installation](#installation)
1. [Configuration](#configuration)
1. [Usage](#usage)
1. [Security](#security)
1. [Contributing](#contributing)
1. [Future Enhancements](#future-enhancements)
1. [License](#license)

## Features

- Parses email subject lines to determine the requested file conversion formats.
- Converts DOCX files to PDF (with scope for adding more formats).
- Handles invalid subject lines and unsupported conversion requests with informative failure emails.
- Command-line interface for local testing.

## Installation
1. Ensure Python 3.x is installed.
2. Clone this repository.
3. Install dependencies: `pip install -r requirements.txt`.

## Configuration
Create a `.env` file in the project root with the following contents:
- `EMAIL_USER`: Your email username.
- `EMAIL_PASSWORD`: Your email password.
- `IMAP_SERVER`: IMAP server address (e.g., imap.gmail.com).
- `SMTP_SERVER`: SMTP server address (e.g., smtp.gmail.com).

## Usage
- Create a `temp` directory in the project root.
- Copy the `.env copy` file to the `.env` file & edit with your own details.
- Run the server with file conversion service using `python src/main.py`.
- Send an email to the configured email address with the subject line formatted as "[Format-1] to [Format-2]" and include the file to be converted as an attachment.

## Security
- The `.env` file is not committed to version control to keep credentials secure - only the template file is.
- Proper validation and error handling are in place to prevent misuse.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. **Fork the Project**
2. **Create your Feature Branch**: 
    ```bash
    git checkout -b feature/AmazingFeature
    ```
3. **Commit your Changes**: 
    ```bash
    git commit -m 'Add some AmazingFeature'
    ```
4. **Push to the Branch**: 
    ```bash
    git push origin feature/AmazingFeature
    ```
5. **Open a Pull Request**

## Future Enhancements
- Extend the service to support additional file format conversions.
- Improve error handling and user feedback mechanisms.

## License

Distributed under the MIT License. See [`LICENSE`](https://github.com/siddhant-vij/Email-Based-File-Conversion-Service/blob/main/LICENSE) for more information.
