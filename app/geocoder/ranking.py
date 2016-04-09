__author__ = 'Tauren'

from app.models import AddressResult
from Levenshtein import distance

def rank_city_candidates(addr_city, addr_state, addr_zip, city_candidates):

    for candidate in city_candidates:
        if addr_city and addr_city.title() == candidate.city:
            candidate.score += 2
        if addr_state == candidate.state_code:
            candidate.score += 1
        if addr_zip == candidate.zip:
            candidate.score += 1

    city_candidates.sort(key=lambda x: x.score, reverse=True)
    return city_candidates


def rank_address_results(street, city, state_abbrevation, zip, address_results_candidates):

    for candidate in address_results_candidates:
        print("Rank Candidate: %s" % (candidate.street_fullname))
        if street == candidate.street_fullname:
            candidate.score += 2

        if city == candidate.city_name:
            candidate.score += 1

        if state_abbrevation == candidate.state_abbreviation:
            candidate.score += 1

        if zip == candidate.zipcode:
            candidate.score += 1

    address_results_candidates.sort(key=lambda x: x.score, reverse=True)
    return address_results_candidates
