import os
import subprocess

from dotenv import load_dotenv
from telethon import TelegramClient

from FastTelethon import upload_file

# Load environment variables from the .env file
load_dotenv()

# Get API credentials from the environment variables
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone_number = os.getenv('TELEGRAM_PHONE_NUMBER')

# Create a Telethon client00
client = TelegramClient('uploader', api_id, api_hash)


async def upload_zip_slices(input_directory, output_directory, password, slice_size="2000m"):
    uploaded_folders_file = "uploaded_folders.txt"

    # Load previously uploaded folder names
    if os.path.exists(uploaded_folders_file):
        with open(uploaded_folders_file, "r") as f:
            uploaded_folders = set(line.strip() for line in f if line.strip())
    else:
        uploaded_folders = set()

    for folder_name in os.listdir(input_directory):
        if folder_name in uploaded_folders:
            print(f"Skipping already uploaded folder: {folder_name}")
            continue

        folder_path = os.path.join(input_directory, folder_name)
        if os.path.isdir(folder_path):
            print(f"Zipping folder: {folder_name}")
            zip_folder_in_slices(folder_path, output_directory, password, slice_size)

            zip_slices = [os.path.join(output_directory, f"{folder_name}.zip")]
            slice_num = 1
            while os.path.exists(os.path.join(output_directory, f"{folder_name}.zip.{slice_num:03d}")):
                zip_slices.append(os.path.join(output_directory, f"{folder_name}.zip.{slice_num:03d}"))
                slice_num += 1

            user_id = int(os.getenv('TELEGRAM_GROUP_ID'))
            try:
                user = await client.get_entity(user_id)

                for slice_path in zip_slices:
                    print(f"Uploading {slice_path} to: {user.id} {getattr(user, 'title', 'Private')}")
                    if os.path.exists(slice_path):
                        with open(slice_path, "rb") as file:
                            result = await upload_file(client, file)
                            result.name = os.path.basename(slice_path)
                            await client.send_file(user, file=result)
                            print(f"Uploaded: {slice_path}")
                    else:
                        print(f"Error: The file {slice_path} does not exist.")

                # Mark this folder as uploaded
                with open(uploaded_folders_file, "a") as f:
                    f.write(f"{folder_name}\n")

            except ValueError as e:
                print(f"Error: {e}")
                print(f"Unable to find user/group: {user_id}")

            for slice_path in zip_slices:
                if os.path.exists(slice_path):
                    os.remove(slice_path)
                    print(f"Deleted: {slice_path}")
                else:
                    print(f"Error: The file {slice_path} does not exist to delete.")


# Function to zip folder into slices with AES-256 encryption
def zip_folder_in_slices(input_folder, output_directory, password, slice_size="2000m"):
    folder_name = os.path.basename(input_folder)
    output_zip = os.path.join(output_directory, f"{folder_name}.zip")
    seven_zip_path = r"C:\Program Files\7-Zip\7z.exe"

    if not os.path.exists(seven_zip_path):
        raise FileNotFoundError(f"7-Zip executable not found at {seven_zip_path}. Please check the installation path.")

    # Use AES-256 encryption and slicing (.zip.001, .zip.002, etc.)
    command = [
        seven_zip_path, "a",
        f"-mem=AES256",  # AES-256 encryption
        f"-p{password}",  # Password for encryption
        f"-v{slice_size}",  # Set slice size to 2000m (2GB)
        f"{output_zip}",  # Output zip filename
        f"{input_folder}"  # Folder to zip
    ]

    subprocess.run(command, check=True)


# Run the Telethon client and upload the zip slices
async def main():
    await client.start(phone_number)
    input_directory = os.getenv('INPUT_DIRECTORY')  # Parent directory containing folders to zip
    output_directory = os.getenv('OUTPUT_DIRECTORY')
    password = os.getenv('ENCRYPT_PASSWORD')  # Password for the zip file
    await upload_zip_slices(input_directory, output_directory, password)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
