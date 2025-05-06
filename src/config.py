"""Configuration file"""
from dataclasses import dataclass


@dataclass
class Config:
    """Configuration class for entire project"""
    use_profile: bool = True
    web_profile: bool = True  # for web ratings
    quick: bool = False
