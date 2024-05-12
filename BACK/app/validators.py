from models.HTTPAuthError import ValidationModel
from models import Programs


def validate_inforaphics(programs_info: Programs) -> ValidationModel:
    '''
    Validates Programs info for infogaphics request.
    Checks if degrees match
    
    Arguments:
    
    programs_info -- Info of Program to revify
    '''
    
    if programs_info.count != 2:
        return ValidationModel(
            status_code=400,
            detail="Invalid IDs provided"
        )
    
    if (programs_info.programs[0].degree_id == 4 or \
        programs_info.programs[1].degree_id == 4) and \
        programs_info.programs[0].degree_id != programs_info.programs[1].degree_id:
        return ValidationModel(
            status_code=400,
            detail="Cannot match master program with different levels"
        )
    
    return ValidationModel(
                status_code=200,
                detail="OK"
    )
