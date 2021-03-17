import pytest

from rblchecker.probe import Probe

@pytest.mark.parametrize(
    'host, expected', [
        ('192.168.0.1', ['192.168.0.1']),
        ('1.1.1.1', ['1.1.1.1']),
        ('fe80::1', ['fe80::1']),
        ('1::', ['1::']),
        ('ipv4only.arpa', ['192.0.0.170', '192.0.0.171']),
        ('localhost', ['127.0.0.1', '::1']),
    ])
def test_resolveToIPs(host, expected):
    probe = Probe(host)
    assert probe._resolveToIPs().sort() == expected.sort()

@pytest.mark.parametrize(
    'ip, dnsbl, expected', [
        ('192.0.2.99', 'bad.example.com', '99.2.0.192.bad.example.com'),
        ('2001:db8:1:2:3:4:567:89ab', 'ugly.example.com', 'b.a.9.8.7.6.5.0.4.0.0.0.3.0.0.0.2.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ugly.example.com'),
    ])
def test_generateLookupUrl(ip, dnsbl, expected):
    probe = Probe(ip)
    assert probe._generateLookupUrl(ip, dnsbl) == expected