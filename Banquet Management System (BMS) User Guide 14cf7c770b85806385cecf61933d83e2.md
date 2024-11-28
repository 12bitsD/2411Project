# Banquet Management System (BMS) User Guide

## Table of Contents

1. [Introduction](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
2. [System Requirements](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
3. [Installation Guide](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
4. [Functional Guide](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
    - [Banquet Management](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
        - [Creating a New Banquet](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
        - [Updating Banquet Information](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
        - [Deleting a Banquet](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
    - [Meal Management](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
        - [Adding a Meal](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
        - [Editing a Meal](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
        - [Deleting a Meal](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
    - [Attendee Management](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
        - [Adding an Attendee](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
        - [Editing an Attendee](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
        - [Deleting an Attendee](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
    - [Registration Management](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
        - [Adding a Registration](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
        - [Deleting a Registration](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
5. [Troubleshooting](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
    - [Common Issues](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
        - [1. Unable to Launch BMS Program](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
        - [2. Database Connection Failure](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
        - [3. Error While Adding Records](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
        - [4. Unable to Delete Records](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
    - [Error Message Explanations](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
6. [Appendix](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
    - [Glossary](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
7. [Review and Testing](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)
8. [Formatting and Design](https://www.notion.so/Banquet-Management-System-BMS-User-Guide-14cf7c770b85806385cecf61933d83e2?pvs=21)

---

## Introduction

Welcome to the **Banquet Management System (BMS)** user guide. BMS is designed to help administrators efficiently organize and manage various banquet events, streamline attendee registration processes, and generate analytical reports to support decision-making.

This user guide will walk you through the steps to install, configure, and use BMS effectively, ensuring you can leverage all its features to their fullest potential.

## System Requirements

### Software Requirements

- **Operating System**: Windows 10 or higher, macOS, Linux
- **Python**: Version 3.6 or higher
- **Database**: SQLite3
- **Dependencies**:
    - `tkinter`
    - `ttkbootstrap`
    - `sqlite3`

## Installation Guide

### 1. Install Python

If Python is not already installed on your computer, follow these steps:

1. Visit the [Python Official Website](https://www.python.org/downloads/) to download the latest version suitable for your operating system.
2. Run the downloaded installer.
3. **Important**: Check the box that says “Add Python to PATH” before clicking “Install Now”.
4. After installation, open Command Prompt (Windows) or Terminal (macOS/Linux) and verify the installation by typing:
    
    ```bash
    python --version
    
    ```
    
    You should see the Python version number displayed.
    

### 2. Install Required Python Libraries

Open Command Prompt or Terminal and run the following command to install the necessary Python libraries:

```bash
pip install ttkbootstrap

```

**Note**: `tkinter` and `sqlite3` are typically included with Python installations, so no additional installation is required for these libraries.

### 3. Download BMS Files

1. Download the `Interface.py` and `out.sql` files from the project repository or the provided link.
2. Save both files in the same directory, for example, `C:\\BMS\\` on Windows or `/Users/YourName/BMS/` on macOS/Linux.

### 4. Configure the Database

1. Open Command Prompt or Terminal and navigate to the BMS directory:
    
    ```bash
    cd C:\\BMS\\
    
    ```
    
    Replace `C:\\BMS\\` with the path to your BMS folder.
    
2. Initialize the SQLite database by running the following command:
    
    ```bash
    sqlite3 banquet.db < out.sql
    
    ```
    
    This command creates the `banquet.db` database and sets up the required tables as defined in the `out.sql` file.
    

### 5. Run BMS

Navigate to the BMS directory in Command Prompt or Terminal and execute the following command to launch BMS:

```bash
python Interface.py

```

The BMS main interface should now launch, allowing you to start using the system's functionalities.

## Functional Guide

### Banquet Management

### Creating a New Banquet

1. From the main interface, click on **Banquet Management** in the menu bar and select **Manage Banquets**.
2. In the **Banquet Manager** window, click the **Add** button at the bottom.
3. In the **Add Banquet** window, fill in the following details:
    - **Name**: Enter the banquet name.
    - **Date Time**: Enter the banquet date and time (e.g., `2024-11-15 18:00`).
    - **Address**: Enter the banquet address.
    - **Location**: Enter the specific location within the address.
    - **Contact First Name**: Enter the first name of the contact staff.
    - **Contact Last Name**: Enter the last name of the contact staff.
    - **Available**: Enter `Y` for available or `N` for not available.
    - **Quota**: Enter the maximum number of attendees.
4. After filling in all required fields, click the **Add** button to save the banquet information.

### Updating Banquet Information

1. In the **Banquet Manager** window, select the banquet record you wish to update from the list.
2. Click the **Edit** button at the bottom.
3. In the **Edit Banquet** window, modify the necessary information.
4. After making changes, click the **Save** button to update the banquet details.

### Deleting a Banquet

1. In the **Banquet Manager** window, select the banquet record you wish to delete.
2. Click the **Delete** button at the bottom.
3. A confirmation prompt will appear. Click **Confirm** to proceed with the deletion.

### Meal Management

### Adding a Meal

1. From the main interface, click on **Meal Management** in the menu bar and select **Manage Meals**.
2. In the **Meal Manager** window, click the **Add** button at the bottom.
3. In the **Add Meal** window, fill in the following details:
    - **BIN**: Select the associated Banquet Identification Number from the dropdown list.
    - **Type**: Enter the meal type (e.g., Fish, Chicken, Beef, Vegetarian).
    - **Dish Name**: Enter the name of the dish.
    - **Price**: Enter the price of the dish.
    - **Special Cuisine**: Enter any special cuisine details (optional).
4. After filling in all required fields, click the **Add** button to save the meal information.

### Editing a Meal

1. In the **Meal Manager** window, select the meal record you wish to edit from the list.
2. Click the **Edit** button at the bottom.
3. In the **Edit Meal** window, modify the necessary information.
4. After making changes, click the **Save** button to update the meal details.

### Deleting a Meal

1. In the **Meal Manager** window, select the meal record you wish to delete.
2. Click the **Delete** button at the bottom.
3. A confirmation prompt will appear. Click **Confirm** to proceed with the deletion.

### Attendee Management

### Adding an Attendee

1. From the main interface, click on **Attendee Management** in the menu bar and select **Manage Attendees**.
2. In the **Attendee Manager** window, click the **Add** button at the bottom.
3. In the **Add Attendee** window, fill in the following details:
    - **Account ID**: Enter the attendee's email address (must include `@`).
    - **First Name**: Enter the attendee's first name (English letters only).
    - **Last Name**: Enter the attendee's last name (English letters only).
    - **Address**: Enter the attendee's address.
    - **Attendee Type**: Enter the type of attendee (e.g., Staff, Student, Alumni, Guest).
    - **Password**: Enter the account password.
    - **Mobile Number**: Enter an 8-digit mobile number.
    - **Affiliated Organization**: Enter the affiliated organization (e.g., PolyU, HKCC, SPEED, Others).
4. After filling in all required fields, click the **Add** button to save the attendee information.

### Editing an Attendee

1. In the **Attendee Manager** window, select the attendee record you wish to edit from the list.
2. Click the **Edit** button at the bottom.
3. In the **Edit Attendee** window, modify the necessary information. Note that the **Account ID** field is read-only and cannot be changed.
4. After making changes, click the **Save** button to update the attendee details.

### Deleting an Attendee

1. In the **Attendee Manager** window, select the attendee record you wish to delete.
2. Click the **Delete** button at the bottom.
3. A confirmation prompt will appear. Click **Confirm** to proceed with the deletion.

### Registration Management

### Adding a Registration

1. From the main interface, click on **Registration Management** in the menu bar and select **Manage Registrations**.
2. In the **Registration Manager** window, click the **Add** button at the bottom.
3. In the **Add Registration** window, fill in the following details:
    - **Registration Date**: Enter the registration date (e.g., `2024-11-01`).
    - **Account ID**: Select the attendee's Account ID from the dropdown list.
    - **BIN**: Select the associated Banquet Identification Number from the dropdown list.
    - **Drink Choice**: Enter the drink choice (e.g., Tea, Coffee, Lemon Tea).
    - **Meal Choice**: Enter the Meal ID corresponding to the selected meal.
    - **Remarks**: Enter any remarks (e.g., seating preferences).
    - **Seat Number**: Enter the seat number (must be unique within the same banquet).
4. The system will automatically check if the selected banquet has available seats:
    - If the banquet has available seats (i.e., current registrations are less than or equal to the quota), the registration will be successful, and the information will be saved.
    - If the banquet is full (i.e., registrations exceed the quota), a regret message will be displayed, and the registration will fail.
5. After filling in all required fields, click the **Add** button to save the registration information.

### Deleting a Registration

1. In the **Registration Manager** window, select the registration record you wish to delete from the list.
2. Click the **Delete** button at the bottom.
3. A confirmation prompt will appear. Click **Confirm** to proceed with the deletion.

## Troubleshooting

### Common Issues

### 1. Unable to Launch BMS Program

**Solution**:

- Ensure Python and all required Python libraries are correctly installed.
- Verify that the `banquet.db` database file exists in the BMS directory and has been properly initialized.
- Check if any other applications are using the necessary resources or ports required by BMS.

### 2. Database Connection Failure

**Solution**:

- Ensure the `banquet.db` file exists in the BMS directory.
- Make sure the database file is not being used by another program.
- Verify that the table names in `out.sql` match those referenced in the code. For example, ensure that the `Banquet` table is correctly referenced without typos.

### 3. Error While Adding Records

**Solution**:

- Ensure all required fields are filled out.
- Check that the input data formats are correct (e.g., email contains `@`, mobile number is 8 digits).
- Confirm that the seat number is unique within the selected banquet.

### 4. Unable to Delete Records

**Solution**:

- Ensure you have selected the correct record to delete.
- Verify that deleting the record does not violate any foreign key constraints.
- Make sure you have the necessary permissions to perform delete operations.

### Error Message Explanations

- **"Invalid input"**: Some of your input fields do not meet the required criteria. Please review and re-enter the information.
- **"Please select a banquet/meal/attendee/registration"**: No record has been selected. Please select a record from the list before attempting the action.
- **"UNIQUE constraint failed"**: You are attempting to add a record that violates a uniqueness constraint, such as duplicate seat numbers or Account IDs.

## Appendix

### Glossary

- **BIN (Banquet Identification Number)**: A unique identifier assigned to each banquet to distinguish different events.
- **Attendee**: A user who has registered and is participating in a banquet event.
- **Meal**: The various food options available at a banquet, such as Fish, Chicken, Beef, and Vegetarian.
- **Registration**: The record of an attendee's enrollment in a specific banquet, including their chosen meal and other preferences.

---

## Review and Testing

To ensure the accuracy and usability of this user guide, the following steps are recommended:

1. **User Testing**: Have several users with varying technical backgrounds follow the user guide to operate BMS and provide their feedback.
2. **Feedback Collection**: Gather input on any issues or suggestions users encountered while using the guide.
3. **Revisions and Updates**: Incorporate user feedback to correct errors, clarify instructions, and add necessary information to enhance the guide’s effectiveness.

## Formatting and Design

To make the user guide easy to read and navigate, adhere to the following formatting and design principles:

- **Clear Headings and Subheadings**: Use hierarchical headings to organize content, making it easy for users to locate specific sections.
- **Step-by-Step Lists and Bullet Points**: Utilize ordered lists for procedures and bullet points for important notes or features.
- **Charts and Screenshots**: Include visual aids like charts and screenshots to illustrate steps and enhance understanding.
- **Highlight Key Points**: Use bold or italics to emphasize crucial steps or important warnings.

---

*Thank you for using the Banquet Management System (BMS). We hope this user guide assists you in successfully installing, configuring, and utilizing the system.*