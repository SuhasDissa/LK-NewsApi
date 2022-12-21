from sources.adaderana import AdaDerana
from sources.gossiplanka import GossipLanka
from sources.lankacnews import LankaCNews

supported_sites = {
    "gossiplanka": {
        "website": GossipLanka
    },
    "adaderana": {
        "website": AdaDerana
    },
    "lankacnews": {
        "website": LankaCNews
    }
}
