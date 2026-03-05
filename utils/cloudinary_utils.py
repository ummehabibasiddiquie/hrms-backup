import os
import uuid
from cloudinary.uploader import upload
from cloudinary.api import delete_resources_by_prefix, resource
import cloudinary
from config import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

def upload_file_to_cloudinary(file_path, folder="hrms_files", resource_type="auto"):
    """
    Upload a file to Cloudinary
    
    Args:
        file_path (str): Local path to the file
        folder (str): Cloudinary folder name
        resource_type (str): Type of resource (auto, image, raw, video)
    
    Returns:
        dict: Cloudinary upload response or None if failed
    """
    try:
        # Generate unique filename
        file_extension = os.path.splitext(file_path)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Upload to Cloudinary
        result = upload(
            file_path,
            folder=folder,
            public_id=unique_filename,
            resource_type=resource_type,
            use_filename=True,
            unique_filename=False
        )
        
        print(f"✅ File uploaded to Cloudinary: {result['public_id']}")
        return result
        
    except Exception as e:
        print(f"❌ Error uploading to Cloudinary: {str(e)}")
        return None

def delete_cloudinary_file(public_id, resource_type="auto"):
    """
    Delete a file from Cloudinary
    
    Args:
        public_id (str): Cloudinary public ID
        resource_type (str): Type of resource
    
    Returns:
        bool: True if deleted successfully, False otherwise
    """
    try:
        result = cloudinary.api.delete_resources([public_id], resource_type=resource_type)
        print(f"✅ File deleted from Cloudinary: {public_id}")
        return result.get("deleted", {}).get(public_id) == "deleted"
    except Exception as e:
        print(f"❌ Error deleting from Cloudinary: {str(e)}")
        return False

def get_cloudinary_url(public_id, resource_type="auto"):
    """
    Get the URL for a Cloudinary resource
    
    Args:
        public_id (str): Cloudinary public ID
        resource_type (str): Type of resource
    
    Returns:
        str: Cloudinary URL or None if not found
    """
    try:
        if not CLOUDINARY_CLOUD_NAME:
            return None
            
        url = f"https://res.cloudinary.com/{CLOUDINARY_CLOUD_NAME}/{resource_type}/upload/{public_id}"
        return url
    except Exception as e:
        print(f"❌ Error generating Cloudinary URL: {str(e)}")
        return None

def check_cloudinary_connection():
    """
    Test Cloudinary connection
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        # Try to get account info
        result = cloudinary.api.account()
        print("✅ Cloudinary connection successful")
        return True
    except Exception as e:
        print(f"❌ Cloudinary connection failed: {str(e)}")
        return False
