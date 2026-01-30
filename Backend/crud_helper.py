import osmium
from sqlalchemy.orm import Session
from thefuzz import process, fuzz
from .models import UserSubmission, Normalized_data
from .translit import transliterate_text

class OSMDataHandler(osmium.SimpleHandler):
    def __init__(self, target_pincode, target_city_trans):
        super().__init__()
        self.target_pincode = str(target_pincode)
        self.target_city = target_city_trans.lower()
        self.osm_city_found = None
        self.possible_matches = set()

    def _process_tags(self, tags):
        osm_postcode = tags.get('addr:postcode')
        osm_city = tags.get('addr:city', '').lower()
        
        if osm_postcode == self.target_pincode or osm_city == self.target_city:
            if not self.osm_city_found and tags.get('addr:city'):
                self.osm_city_found = tags.get('addr:city')
            
            search_tags = ['addr:street', 'addr:full', 'name', 'addr:suburb', 'addr:neighbourhood']
            for tag in search_tags:
                val = tags.get(tag)
                if val:
                    if ',' in val:
                        parts = [p.strip() for p in val.split(',')]
                        self.possible_matches.update(parts)
                    self.possible_matches.add(val)

    def node(self, n): self._process_tags(n.tags)
    def way(self, w): self._process_tags(w.tags)
    def relation(self, r): self._process_tags(r.tags)

def get_best_match(user_trans_input, possibilities):
    if not possibilities or not user_trans_input:
        return user_trans_input.title() if user_trans_input else ""
    
    result, score = process.extractOne(
        user_trans_input, 
        possibilities, 
        scorer=fuzz.partial_ratio
    )
    
    return result if score > 75 else user_trans_input.title()

def create_submission(db: Session, pin_code: int, state: str, city: str, locality: str, landmark: str):
    state_trans = transliterate_text(state)
    city_trans = transliterate_text(city)
    locality_trans = transliterate_text(locality)
    landmark_trans = transliterate_text(landmark)

    submission = UserSubmission(
        state=state_trans.lower(),
        city=city_trans.lower(),
        locality=locality_trans.lower(),
        landmark=landmark_trans.lower(),
        pin_code=pin_code
    )
    db.add(submission)
    db.flush()

    handler = OSMDataHandler(pin_code, city_trans)
    handler.apply_file("ujjain_filtered.osm.pbf") 

    final_city = handler.osm_city_found if handler.osm_city_found else city_trans.title()
    final_locality = get_best_match(locality_trans, handler.possible_matches)
    final_landmark = get_best_match(landmark_trans, handler.possible_matches)

    normalized = Normalized_data(
        id=submission.id,
        city_normalized=final_city,
        state_normalzed=state_trans.title(),
        locality_normalized=final_locality,
        landmark_normalized=final_landmark
    )

    db.add(normalized)
    db.commit()
    db.refresh(submission)

    return submission
