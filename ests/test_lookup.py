from survey_ip.lookup import geoip_lookup_ipapi, rdap_lookup

def test_geoip_works_for_public_ip():
    res = geoip_lookup_ipapi("8.8.8.8")
    assert res.get("ip") == "8.8.8.8"
    assert "country" in res

def test_rdap_for_cloudflare():
    res = rdap_lookup("1.1.1.1")
    assert isinstance(res, dict)
