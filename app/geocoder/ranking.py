__author__ = 'Tauren'

from app.geocoder.address import Address

def rank_address_candidates(address, addrfeat_list):
    pass



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
