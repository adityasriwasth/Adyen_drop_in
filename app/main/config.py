
'''
File that stores all of the nencessary keys to process with Adyen's platform
'''

merchant_account = "TestAccountNY"
checkout_apikey = "AQEyhmfxK4zJbBZDw0m/n3Q5qf3VaY9UCJ1+XWZe9W27jmlZiniYHPZ+YtXG9dYfNdwN0H8QwV1bDb7kfNy1WIxIIkxgBw==-uA2G0DS73SlmB4EHi/YNndhli7KlCMjXHbMmm8stboc=-djvcdM2gNHq9dSvC"
client_key = "pub.v2.8115650120946270.aHR0cDovL2xvY2FsaG9zdDo4MDgw.4rIB_MfjWK0rr3305Rh3o-Tyr8s0WFVhGmLXaZ20kG4"
supported_integrations = ['dropin']

# Check to make sure variables are set
if not merchant_account or not checkout_apikey or not client_key:
    raise Exception("Please fill out information in config.ini file")
