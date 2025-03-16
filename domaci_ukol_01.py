from dataclasses import dataclass
@dataclass
class Locality:
    name: str
    locality_coefficient: float

from abc import ABC, abstractmethod    
@dataclass
class Property(ABC):
    locality: Locality 

    @abstractmethod
    def calculate_tax(self) -> float :
        pass 
    def get_coefficient(self,estate_type:str) -> float:
        if estate_type == "land":
            return  0.85
        elif estate_type == "building site":
            return 9
        elif estate_type == "forrest":
            return 0.35
        elif estate_type == "garden":
            return 2
        elif estate_type == "apartment" or estate_type == "house" or estate_type == "office":
            return 15
        else:
            return 0
    
   
    def translate_to_czech(self,estate_type:str) -> str:
        if estate_type == "land":
            return  "zemedelsky pozemek"
        elif estate_type == "building site":
            return "stavebni pozemek"
        elif estate_type == "forrest":
            return "les"
        elif estate_type == "garden":
            return "zahrada"
        elif estate_type == "apartment":
            return "byt"
        elif estate_type == "house":
            return "dum"
        elif estate_type == "office":
            return "kancelar"
        else:
            return "Nenalezeno"
    
    def __str__(self):
        return f" Lokalita {self.locality.name} (koeficient {self.locality.locality_coefficient}),"
        
import math 
@dataclass
class Estate(Property):
    estate_type: str
    area: float
    def calculate_tax(self) -> int:
        tax = self.area * self.get_coefficient(self.estate_type) * self.locality.locality_coefficient
        zaokrouhlene = math.ceil(tax)
        return zaokrouhlene
    def __str__(self) -> str:
        dan = str(self.calculate_tax())
        return super().__str__() + f"{self.translate_to_czech(self.estate_type)}, {self.area} metru, dan {dan} Kc."

@dataclass
class Residence(Property):
    estate_type: str
    area: float
    commercial: bool 
    def calculate_tax(self) -> float:
        tax = self.area * self.get_coefficient(self.estate_type) * self.locality.locality_coefficient
        if self.commercial == True: 
            tax = tax * 2 
        return tax 
    
    def info_commercial(self) -> str:
        if self.commercial == True:
            return " komercni nemovitost"
        else:
            return ""
        
    def __str__(self) -> str:
        dan = str(self.calculate_tax())
        return super().__str__() + f"{self.translate_to_czech(self.estate_type)},{self.info_commercial()}, {self.area} metru, dan {dan} Kc."

loc_Brno = Locality ("Brno", 3)
loc_Manetin = Locality("Manetin", 0.8)

manetin_pozemek = Estate(loc_Manetin, "land", 900)
manetin_dum = Residence(loc_Manetin, "house", 120,False)
brno_kancelar = Residence(loc_Brno, "office", 90, True)
print(manetin_pozemek.__str__())
print(manetin_dum.__str__())
print(brno_kancelar.__str__())



@dataclass
class TaxReport: 
    name: str
    property_list = []
    def add_property(self,property:Property):
        self.property_list.append(property)

    def tax_calculation(self) -> float:
        tax: float = 0 
        item: Property
        for item in self.property_list:
            tax += item.calculate_tax()
        return tax 

  
danove_priznani = TaxReport("Petra")
danove_priznani.add_property(manetin_pozemek)
danove_priznani.add_property(manetin_dum)
danove_priznani.add_property(brno_kancelar)

print(f"{danove_priznani.name} ma platit dan v celkove vysi {danove_priznani.tax_calculation()} Kc. ")
