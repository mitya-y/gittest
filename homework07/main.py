from research.age import age_predict
from research.network import *
from vkapi.friends import get_friends
from vkapi.session import Session

fenjks = 426266451
pavel = 47885893
dima = 323656355
mitya = 226163149
zlaty = 644110549

print(age_predict(zlaty))

# ans = get_friends(zlaty, fields=["first_name", "last_name", "bdate"])
# from pprint import pprint
# pprint(ans)

# s = Session("https://example.com")
# for i in range(10):
#     _ = s.get("")
# exit()

net = ego_network(fenjks)
# plot_ego_network(net)
plot_communities(net)
