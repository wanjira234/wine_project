from enum import Enum

class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = 'admin'
    CUSTOMER = 'customer'
    SOMMELIER = 'sommelier'

class ExperienceLevel(str, Enum):
    """Wine experience level enumeration."""
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    EXPERT = 'expert'

class DrinkingFrequency(str, Enum):
    """Wine drinking frequency enumeration."""
    RARELY = 'rarely'
    OCCASIONALLY = 'occasionally'
    REGULARLY = 'regularly'
    FREQUENTLY = 'frequently'

class Currency(str, Enum):
    """Currency enumeration."""
    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'

class WineType(str, Enum):
    """Wine type enumeration."""
    RED = 'red'
    WHITE = 'white'
    ROSE = 'rose'
    SPARKLING = 'sparkling'
    DESSERT = 'dessert'

class PriceRange(str, Enum):
    """Price range enumeration."""
    BUDGET = 'budget'
    MODERATE = 'moderate'
    PREMIUM = 'premium'
    LUXURY = 'luxury'

class BodyType(str, Enum):
    """Wine body type enumeration."""
    LIGHT = 'light'
    MEDIUM = 'medium'
    FULL = 'full'

class SweetnessLevel(str, Enum):
    """Wine sweetness level enumeration."""
    DRY = 'dry'
    OFF_DRY = 'off_dry'
    SWEET = 'sweet'
    VERY_SWEET = 'very_sweet'

class AcidityLevel(str, Enum):
    """Wine acidity level enumeration."""
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class TanninLevel(str, Enum):
    """Wine tannin level enumeration."""
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class FlavorIntensity(str, Enum):
    """Wine flavor intensity enumeration."""
    LIGHT = 'light'
    MEDIUM = 'medium'
    PRONOUNCED = 'pronounced'

class PriceSensitivity(str, Enum):
    """Price sensitivity enumeration."""
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class QualityPreference(str, Enum):
    """Quality preference enumeration."""
    STANDARD = 'standard'
    HIGH = 'high'
    PREMIUM = 'premium'

class WineCategory(str, Enum):
    """Wine category enumeration."""
    RED = 'Red Wine'
    WHITE = 'White Wine'
    ROSE = 'Rosé Wine'
    SPARKLING = 'Sparkling Wine'

class WineTraitCategory(str, Enum):
    """Wine trait category enumeration."""
    TASTE = 'taste'
    AROMA = 'aroma'
    BODY = 'body'
    TEXTURE = 'texture'
    CHARACTER = 'character'
    NOTES = 'notes'
    OTHER = 'other'

class WineTrait(str, Enum):
    """Wine trait enumeration."""
    # Taste traits
    SWEET = 'sweet'
    DRY = 'dry'
    TART = 'tart'
    CRISP = 'crisp'
    TANGY = 'tangy'
    JUICY = 'juicy'
    RICH = 'rich'
    SMOOTH = 'smooth'
    SOFT = 'soft'
    SHARP = 'sharp'

    # Aroma traits
    ALMOND = 'almond'
    ANISE = 'anise'
    APPLE = 'apple'
    APRICOT = 'apricot'
    BERRY = 'berry'
    BLACK_CHERRY = 'black_cherry'
    BLACKBERRY = 'blackberry'
    BLUEBERRY = 'blueberry'
    CITRUS = 'citrus'
    PEACH = 'peach'
    PEAR = 'pear'
    PLUM = 'plum'
    RASPBERRY = 'raspberry'
    STRAWBERRY = 'strawberry'
    TROPICAL_FRUIT = 'tropical_fruit'
    VANILLA = 'vanilla'
    CHOCOLATE = 'chocolate'
    COFFEE = 'coffee'
    CARAMEL = 'caramel'
    HONEY = 'honey'
    SPICE = 'spice'
    CINNAMON = 'cinnamon'
    NUTMEG = 'nutmeg'
    PEPPER = 'pepper'

    # Body traits
    LIGHT_BODIED = 'light_bodied'
    MEDIUM_BODIED = 'medium_bodied'
    FULL_BODIED = 'full_bodied'
    DENSE = 'dense'
    THICK = 'thick'
    WEIGHT = 'weight'
    ROBUST = 'robust'
    HEARTY = 'hearty'

    # Texture traits
    SILKY = 'silky'
    VELVETY = 'velvety'
    ROUND = 'round'
    PLUSH = 'plush'
    SUPPLE = 'supple'
    FIRM = 'firm'
    TANNIN = 'tannin'
    GRIPPING = 'gripping'

    # Character traits
    COMPLEX = 'complex'
    ELEGANT = 'elegant'
    FRESH = 'fresh'
    VIBRANT = 'vibrant'
    BRIGHT = 'bright'
    POWERFUL = 'powerful'
    CONCENTRATED = 'concentrated'
    REFINED = 'refined'

    # Notes traits
    FLORAL = 'floral'
    HERBAL = 'herbal'
    EARTHY = 'earthy'
    MINERAL = 'mineral'
    OAK = 'oak'
    SMOKE = 'smoke'
    LEATHER = 'leather'
    TOBACCO = 'tobacco'
    CEDAR = 'cedar'

    # Additional traits
    BAKED = 'baked'
    BAKING_SPICES = 'baking_spices'
    BLACK_CURRANT = 'black_currant'
    BLACK_PEPPER = 'black_pepper'
    BLACK_TEA = 'black_tea'
    BOYSENBERRY = 'boysenberry'
    BRAMBLE = 'bramble'
    BUTTER = 'butter'
    CANDY = 'candy'
    CARDAMOM = 'cardamom'
    CASSIS = 'cassis'
    CHALK = 'chalk'
    CHERRY = 'cherry'
    CLEAN = 'clean'
    CLOSED = 'closed'
    CLOVE = 'clove'
    COCOA = 'cocoa'
    COLA = 'cola'
    CRANBERRY = 'cranberry'
    CREAM = 'cream'
    DARK = 'dark'
    DARK_CHOCOLATE = 'dark_chocolate'
    DEPTH = 'depth'
    DRIED_HERB = 'dried_herb'
    DUST = 'dust'
    EARTH = 'earth'
    EDGY = 'edgy'
    ELDERBERRY = 'elderberry'
    FENNEL = 'fennel'
    FLOWER = 'flower'
    FOREST_FLOOR = 'forest_floor'
    FRENCH_OAK = 'french_oak'
    FRUIT = 'fruit'
    GAME = 'game'
    GRAPEFRUIT = 'grapefruit'
    GRAPHITE = 'graphite'
    GREEN = 'green'
    GRIPPY = 'grippy'
    HERB = 'herb'
    HONEYSUCKLE = 'honeysuckle'
    JAM = 'jam'
    LAVENDER = 'lavender'
    LEAFY = 'leafy'
    LEAN = 'lean'
    LEMON = 'lemon'
    LEMON_PEEL = 'lemon_peel'
    LENGTH = 'length'
    LICORICE = 'licorice'
    LIME = 'lime'
    LUSH = 'lush'
    MEATY = 'meaty'
    MELON = 'melon'
    MILK_CHOCOLATE = 'milk_chocolate'
    MINERALITY = 'minerality'
    MINT = 'mint'
    OLIVE = 'olive'
    ORANGE = 'orange'
    ORANGE_PEEL = 'orange_peel'
    PENCIL_LEAD = 'pencil_lead'
    PINE = 'pine'
    PINEAPPLE = 'pineapple'
    POLISHED = 'polished'
    POMEGRANATE = 'pomegranate'
    PURPLE = 'purple'
    PURPLE_FLOWER = 'purple_flower'
    REFRESHING = 'refreshing'
    RESTRAINED = 'restrained'
    RIPE = 'ripe'
    ROSE = 'rose'
    SAGE = 'sage'
    SALT = 'salt'
    SAVORY = 'savory'
    SMOKED_MEAT = 'smoked_meat'
    SPARKLING = 'sparkling'
    STEEL = 'steel'
    STONE = 'stone'
    SUCCULENT = 'succulent'
    TAR = 'tar'
    TEA = 'tea'
    THYME = 'thyme'
    TIGHT = 'tight'
    TOAST = 'toast'
    WARM = 'warm'
    WET_ROCKS = 'wet_rocks'
    WHITE = 'white'
    WHITE_PEPPER = 'white_pepper'
    WOOD = 'wood'

class WineRegion(str, Enum):
    """Wine region enumeration."""
    # France
    BORDEAUX = 'bordeaux'
    BURGUNDY = 'burgundy'
    CHAMPAGNE = 'champagne'
    RHONE = 'rhone'
    LOIRE = 'loire'
    PROVENCE = 'provence'
    
    # Italy
    TUSCANY = 'tuscany'
    PIEDMONT = 'piedmont'
    VENETO = 'veneto'
    SICILY = 'sicily'
    
    # Spain
    RIOJA = 'rioja'
    RIBERA_DEL_DUERO = 'ribera_del_duero'
    PRIORAT = 'priorat'
    
    # United States
    NAPA_VALLEY = 'napa_valley'
    SONOMA = 'sonoma'
    OREGON = 'oregon'
    WASHINGTON = 'washington'
    
    # Other Old World
    MOSEL = 'mosel'  # Germany
    DOURO = 'douro'  # Portugal
    BAROSSA = 'barossa'  # Australia
    MARLBOROUGH = 'marlborough'  # New Zealand
    MENDOZA = 'mendoza'  # Argentina
    STELLENBOSCH = 'stellenbosch'  # South Africa
    CASABLANCA = 'casablanca'  # Chile 