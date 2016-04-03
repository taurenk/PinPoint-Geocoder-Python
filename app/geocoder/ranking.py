__author__ = 'Tauren'


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


def rank_address_candidates(street, city, zip, addrfeat_candidates):
    pass