import sys, os
sys.path.append(os.path.expanduser('~/.hermes/skills/social-media/moltbook-autonomous-operations'))
from scripts.challenge_solver import solve_challenge

c1 = "L oB sT eR] ~eX pErS sS^s A tT hIr Ty F iV e[ nEu-ToNs- ClA wW ~foR ce| aNd- cOl LiD eS/ wItH< aNoTh Er] lO bS tEr- pRoD uC eS^ tW eL vE[ aN tEn Na- TaP s, uM| wHaT/ iS^ tHe- tOt Al< Im PuLsE* wHeN] tH iR tY F iV e* tW eL vE?"
print("C1:", solve_challenge(c1))

c2 = "A] LoBsTeR- ClAw] FoRcE Is^ ThIr]tY \tWo NoOtOnS~ TiMeS< FiV e, Um, DuRiNg] DoMiNaNcE fIgHtS\\ HoW} MuCh| ToTaL^ FoRcE?"
print("C2:", solve_challenge(c2))
