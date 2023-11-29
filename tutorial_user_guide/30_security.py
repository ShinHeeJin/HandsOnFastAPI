# https://fastapi.tiangolo.com/tutorial/security/
# OAuth2 doesn't specify how to encrypt the communication, it expects you to have your application served with HTTPS.

# OpenID Connect is another specification, based on OAuth2.
# For example, Google login uses OpenID Connect (which underneath uses OAuth2).
# But Facebook login doesn't support OpenID Connect. It has its own flavor of OAuth2.

# Tip
# Integrating other authentication/authorization providers like Google, Facebook, Twitter, GitHub, etc. is also possible and relatively easy.
# The most complex problem is building an authentication/authorization provider like those, but FastAPI gives you the tools to do it easily, while doing the heavy lifting for you.
