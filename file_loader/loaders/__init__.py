from enums import PlanType
from loaders.hse import HseAnnualLoader, HseBasicLoader
from loaders.itmo import ItmoLoader
from loaders.base import BaseLoader


def get_loader(plan_type: PlanType) -> BaseLoader:
    """"Simple factory"-like method for getting plan loaders

    Args:
        plan_type (PlanType): Plan type that should be used to determine plan loader
    """
    
    match(plan_type):
        case PlanType.HSE_BASIC_PLAN:
            return HseBasicLoader()
        
        case PlanType.HSE_ANNUAL_PLAN:
            return HseAnnualLoader()
        
        case PlanType.ITMO_PLAN:
            return ItmoLoader()