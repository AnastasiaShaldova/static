"""Global point for collected routers."""

from app.internal.pkg.models import Routes

from app.internal.routes import image, user

__all__ = ["__routes__"]

__routes__ = Routes(
    routers=(
        image.router,
        user.router,
    ),
)


