__author__ = 'Tauren'

from app.geocoder.address import Address

def rank_address_candidates(address, addrfeat_list):
    """
    :param address: Address Object
    :param addrfeat_list: list if addrfeat candidates
    :return: list of addrfeat objects with a rank_score set and sorted from high/low value
    """

    for addrfeat in addrfeat_list:
        addrfeat.rank = 0

        # Street
        if address.address_line_1 == addrfeat.fullname:
            addrfeat.rank += 1

        # zipcode
        if address.zip == addrfeat.zipl or address.zip == addrfeat.zipr:
            addrfeat.rank += 1

        # side of street
        if check_number_range(addrfeat.lfromhn, addrfeat.ltohn, address.number):
            addrfeat.rank += 1
        elif check_number_range(addrfeat.rfromhn, addrfeat.rtohn, address.number):
            addrfeat.rank += 1

    addrfeat_list.sort(key=lambda x: x.rank, reverse=True)
    return addrfeat_list

def check_number_range(fromnum, tonum, target):
    """ Given a target street number, deterime if it's in range
    :param fromnum:
    :param tonum:
    :param target:
    :return: True/False
    """
    if fromnum <= target <= tonum:
        return True
    elif fromnum >= target >= tonum:
        return True
    return False


# def rank_candidates(self, address, candidates):
#         """ Scoring Algorithm for potential candidates
#         1. zip
#         """
#         """
#         0   1       2     3         4            5           6      7       8     9     10    11
#         gid, tlid, name, score, predirabrv, pretypabrv,suftypabrv, zipl, lcity, zipr, rcity, state, " +\
#         12         13      14       15     16
#         lfromhn, ltohn, rfromhn, rtohn, ST_asText(geom)
#         """
#         candidate_list = []
#         for candidate in candidates:
#             score = 0
#
#             # Street Score
#             if candidate[2] == address.street1: score += 1
#             else: score += 1/candidate[3]
#
#             # street type
#             if candidate[6]:
#                 if candidate[6].upper() == address.street1_type: score += 1
#
#             # TODO:Pre/Post Directions
#
#             # zipcode
#             if candidate[7] == address.zip: score += 1
#             elif candidate[9] == address.zip: score += 1
#
#             # city
#             if candidate[8] == address.city: score += 2
#             elif candidate[10] == address.city: score += 2
#
#             # Figure out ranges piece
#             # TODO: Add which side the point was hitp->this will help in interpolation.
#             addr_score = 0
#             side_flag = None
#             if address.number:
#                 i = 12
#                 while i <= 15:
#                     try:
#                         if candidate[i] and '-' in candidate[i]: candidate[i]=self.convert_number(candidate[i])
#                         if (candidate[i+1] and '-' in candidate[i+1]): candidate[i+1]=self.convert_number(candidate[i+1])
#                         addr_score += self.check_range(
#                                 int(candidate[i]), int(candidate[i+1]), int(address.number) )
#                         if addr_score:
#                             if i==12: side_flag='L'
#                             else: side_flag='R'
#                     except:
#                         pass #Just pass for now aka TODO
#                     i+=2
#             score += addr_score
#             candidate_list.append(candidate + [score] + [side_flag] )
#
#         # Sort list by score
#         candidate_list.sort(key=lambda x: x[17], reverse=True)
#         if len(candidate_list) >= 5:
#             return candidate_list[:4]
#         else:
#             return candidate_list
