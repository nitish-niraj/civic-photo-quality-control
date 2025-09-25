import piexif
from PIL import Image
from PIL.ExifTags import TAGS
import json
from datetime import datetime
from typing import Dict, Optional, Tuple
import os

class MetadataExtractor:
    """Extracts and validates image metadata."""
    
    @staticmethod
    def extract_metadata(image_path: str) -> Dict:
        """
        Extract comprehensive metadata from image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with extracted metadata
        """
        try:
            metadata = {
                "file_info": MetadataExtractor._get_file_info(image_path),
                "exif_data": MetadataExtractor._extract_exif(image_path),
                "gps_data": None,
                "camera_info": None,
                "timestamp": None
            }
            
            # Extract GPS data if available
            if metadata["exif_data"]:
                metadata["gps_data"] = MetadataExtractor._extract_gps(
                    metadata["exif_data"]
                )
                metadata["camera_info"] = MetadataExtractor._extract_camera_info(
                    metadata["exif_data"]
                )
                metadata["timestamp"] = MetadataExtractor._extract_timestamp(
                    metadata["exif_data"]
                )
            
            # Validate against required fields
            metadata["validation"] = MetadataExtractor._validate_required_fields(metadata)
            
            return metadata
            
        except Exception as e:
            return {
                "error": f"Metadata extraction failed: {str(e)}",
                "file_info": MetadataExtractor._get_file_info(image_path),
                "exif_data": None,
                "gps_data": None,
                "camera_info": None,
                "timestamp": None
            }
    
    @staticmethod
    def _get_file_info(image_path: str) -> Dict:
        """Get basic file information."""
        stat = os.stat(image_path)
        return {
            "filename": os.path.basename(image_path),
            "file_size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
        }
    
    @staticmethod
    def _extract_exif(image_path: str) -> Optional[Dict]:
        """Extract EXIF data from image."""
        try:
            with Image.open(image_path) as img:
                exif_dict = piexif.load(img.info.get('exif', b''))
                
                # Convert to readable format
                readable_exif = {}
                for ifd in ("0th", "Exif", "GPS", "1st"):
                    readable_exif[ifd] = {}
                    for tag in exif_dict[ifd]:
                        tag_name = piexif.TAGS[ifd][tag]["name"]
                        readable_exif[ifd][tag_name] = exif_dict[ifd][tag]
                
                return readable_exif
                
        except Exception:
            return None
    
    @staticmethod
    def _extract_gps(exif_data: Dict) -> Optional[Dict]:
        """Extract GPS coordinates from EXIF data."""
        try:
            gps_data = exif_data.get("GPS", {})
            if not gps_data:
                return None
            
            # Extract coordinates
            lat = MetadataExtractor._convert_gps_coordinate(
                gps_data.get("GPSLatitude"),
                gps_data.get("GPSLatitudeRef", b'N')
            )
            lon = MetadataExtractor._convert_gps_coordinate(
                gps_data.get("GPSLongitude"),
                gps_data.get("GPSLongitudeRef", b'E')
            )
            
            if lat is None or lon is None:
                return None
            
            return {
                "latitude": lat,
                "longitude": lon,
                "altitude": gps_data.get("GPSAltitude"),
                "timestamp": gps_data.get("GPSTimeStamp")
            }
            
        except Exception:
            return None
    
    @staticmethod
    def _convert_gps_coordinate(coord_tuple: Tuple, ref: bytes) -> Optional[float]:
        """Convert GPS coordinate from EXIF format to decimal degrees."""
        if not coord_tuple or len(coord_tuple) != 3:
            return None
        
        try:
            degrees = float(coord_tuple[0][0]) / float(coord_tuple[0][1])
            minutes = float(coord_tuple[1][0]) / float(coord_tuple[1][1])
            seconds = float(coord_tuple[2][0]) / float(coord_tuple[2][1])
            
            decimal_degrees = degrees + (minutes / 60.0) + (seconds / 3600.0)
            
            if ref.decode() in ['S', 'W']:
                decimal_degrees = -decimal_degrees
            
            return decimal_degrees
            
        except (ZeroDivisionError, TypeError, ValueError):
            return None
    
    @staticmethod
    def _extract_camera_info(exif_data: Dict) -> Optional[Dict]:
        """Extract camera information from EXIF data."""
        try:
            exif_section = exif_data.get("0th", {})
            camera_section = exif_data.get("Exif", {})
            
            return {
                "make": exif_section.get("Make", b'').decode('utf-8', errors='ignore'),
                "model": exif_section.get("Model", b'').decode('utf-8', errors='ignore'),
                "software": exif_section.get("Software", b'').decode('utf-8', errors='ignore'),
                "lens_model": camera_section.get("LensModel", b'').decode('utf-8', errors='ignore'),
                "focal_length": camera_section.get("FocalLength"),
                "f_number": camera_section.get("FNumber"),
                "exposure_time": camera_section.get("ExposureTime"),
                "iso": camera_section.get("ISOSpeedRatings")
            }
            
        except Exception:
            return None
    
    @staticmethod
    def _extract_timestamp(exif_data: Dict) -> Optional[str]:
        """Extract timestamp from EXIF data."""
        try:
            exif_section = exif_data.get("Exif", {})
            datetime_original = exif_section.get("DateTimeOriginal", b'').decode('utf-8', errors='ignore')
            
            if datetime_original:
                # Convert EXIF timestamp format to ISO format
                dt = datetime.strptime(datetime_original, "%Y:%m:%d %H:%M:%S")
                return dt.isoformat()
            
            return None
            
        except Exception:
            return None
    
    @staticmethod
    def _validate_required_fields(metadata: Dict) -> Dict:
        """Validate metadata against required fields."""
        required_fields = [
            "timestamp",
            "camera_make_model", 
            "orientation",
            "iso",
            "shutter_speed",
            "aperture"
        ]
        
        found_fields = []
        missing_fields = []
        
        # Check timestamp
        if metadata.get("timestamp"):
            found_fields.append("timestamp")
        else:
            missing_fields.append("timestamp")
        
        # Check camera info
        camera_info = metadata.get("camera_info", {})
        if camera_info and (camera_info.get("make") or camera_info.get("model")):
            found_fields.append("camera_make_model")
        else:
            missing_fields.append("camera_make_model")
        
        # Check EXIF data for technical details
        exif_data = metadata.get("exif_data", {})
        if exif_data:
            exif_section = exif_data.get("0th", {})
            camera_section = exif_data.get("Exif", {})
            
            # Orientation
            if exif_section.get("Orientation"):
                found_fields.append("orientation")
            else:
                missing_fields.append("orientation")
            
            # ISO
            if camera_section.get("ISOSpeedRatings"):
                found_fields.append("iso")
            else:
                missing_fields.append("iso")
            
            # Shutter speed
            if camera_section.get("ExposureTime"):
                found_fields.append("shutter_speed")
            else:
                missing_fields.append("shutter_speed")
            
            # Aperture
            if camera_section.get("FNumber"):
                found_fields.append("aperture")
            else:
                missing_fields.append("aperture")
        else:
            missing_fields.extend(["orientation", "iso", "shutter_speed", "aperture"])
        
        completeness_percentage = (len(found_fields) / len(required_fields)) * 100
        
        # Determine quality level
        if completeness_percentage >= 85:
            quality_level = "excellent"
        elif completeness_percentage >= 70:
            quality_level = "acceptable"
        else:
            quality_level = "poor"
        
        return {
            "required_fields": required_fields,
            "found_fields": found_fields,
            "missing_fields": missing_fields,
            "completeness_percentage": round(completeness_percentage, 1),
            "quality_level": quality_level,
            "meets_requirements": completeness_percentage >= 70
        }
    
    @staticmethod
    def validate_location(gps_data: Dict, boundaries: Dict) -> Dict:
        """Validate if GPS coordinates are within city boundaries."""
        if not gps_data:
            return {
                "within_boundaries": False,
                "reason": "No GPS data available"
            }
        
        lat = gps_data.get("latitude")
        lon = gps_data.get("longitude")
        
        if lat is None or lon is None:
            return {
                "within_boundaries": False,
                "reason": "Invalid GPS coordinates"
            }
        
        within_bounds = (
            boundaries["min_lat"] <= lat <= boundaries["max_lat"] and
            boundaries["min_lon"] <= lon <= boundaries["max_lon"]
        )
        
        return {
            "within_boundaries": within_bounds,
            "latitude": lat,
            "longitude": lon,
            "reason": "Valid location" if within_bounds else "Outside city boundaries"
        }
