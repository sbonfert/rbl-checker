class Listing(object):

    def __init__(self, host:str, ip: str, bl: str):
        self._host = host
        self._ip = ip
        self._bl = bl
        self._reason = str()

    def __eq__(self, other):
        return self._host == other._host and self._ip == other._ip  and self._bl == other._bl

    def __hash__(self):
        return hash(self._host) ^ hash(self._ip) ^ hash(self._bl)

    def addReason(self, reason: str) -> None:
        self._reason += reason
    
    def getDescription(self) -> str:
        description = 'Host ' + self._host + '('+ self._ip + ') was listed on blacklist ' + self._bl + '.\n'
        if self._reason == '':
            description += 'No reason was given.\n'
        else:
            description += 'The provided reason is: ' + self._reason + '\n'
        description += "\n"
        return description