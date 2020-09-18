import os

import sqlalchemy as db
from flask import Flask, Response, request, send_from_directory
from flask.templating import render_template
from flask_caching import Cache
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail as FlaskMail

from paths import APP_ROOT_PATH
from src.abstract_view import AbstractView
from src.mail import Mail
from src.middleware.http.authorize import AuthorizeHttpMiddleware
from src.middleware.http.language import LanguageHttpMiddleware
from src.repos.banner import BannerRepo
from src.repos.category import CategoryRepo
from src.repos.currency_rate import CurrencyRateRepo
from src.repos.feature_type import FeatureTypeRepo
from src.repos.feature_value import FeatureValueRepo
from src.repos.language import LanguageRepo
from src.repos.order import OrderRepo
from src.repos.product import ProductRepo
from src.repos.product_type import ProductTypeRepo
from src.repos.promo_code import PromoCodeRepo
from src.repos.signup import SignupRepo
from src.repos.user import UserRepo
from src.serializers.banner import BannerSerializer
from src.serializers.category import CategorySerializer
from src.serializers.currency_rate import CurrencyRateSerializer
from src.serializers.feature_type import FeatureTypeSerializer
from src.serializers.feature_value import FeatureValueSerializer
from src.serializers.language import LanguageSerializer
from src.serializers.order import OrderSerializer
from src.serializers.product import ProductSerializer
from src.serializers.product_type import ProductTypeSerializer
from src.serializers.promo_code import PromoCodeSerializer
from src.services.banner import BannerService
from src.services.category import CategoryService
from src.services.currency_rate import CurrencyRateService
from src.services.feature_type import FeatureTypeService
from src.services.feature_value import FeatureValueService
from src.services.language import LanguageService
from src.services.order import OrderService
from src.services.product import FeatureValuesPolicy, ProductService
from src.services.product_type import ProductTypeService
from src.services.promo_code import PromoCodeService
from src.services.signup import SignupService
from src.services.user import UserService
from src.storage.aws_storage import AWSStorage
from src.utils.cache import response_filter
from src.cache.category_product_types import CategoryProductTypesCache
from src.validation_rules.authentication import AuthenticationDataValidator
from src.validation_rules.banner.create import CreateBannerDataValidator
from src.validation_rules.banner.update import UpdateBannerDataValidator
from src.validation_rules.category.create import CreateCategoryDataValidator
from src.validation_rules.category.update import UpdateCategoryDataValidator
from src.validation_rules.confirm_registration import ConfirmRegistrationDataValidator
from src.validation_rules.currency_rate.create import CreateCurrencyRateDataValidator
from src.validation_rules.feature_type.create import CreateFeatureTypeDataValidator
from src.validation_rules.feature_type.update import UpdateFeatureTypeDataValidator
from src.validation_rules.feature_value.create import CreateFeatureValueDataValidator
from src.validation_rules.feature_value.update import UpdateFeatureValueDataValidator
from src.validation_rules.order.create import CreateOrderDataValidator
from src.validation_rules.order.update import UpdateOrderDataValidator
from src.validation_rules.product.create import CreateProductDataValidator
from src.validation_rules.product.update import UpdateProductDataValidator
from src.validation_rules.product_type.create import CreateProductTypeDataValidator
from src.validation_rules.product_type.update import UpdateProductTypeDataValidator
from src.validation_rules.promo_code.create import CreatePromoCodeDataValidator
from src.validation_rules.promo_code.update import UpdatePromoCodeDataValidator
from src.validation_rules.refresh_token import RefreshTokenDataValidator
from src.validation_rules.registration import RegistrationDataValidator
from src.views.authentication import AuthenticationView
from src.views.banner.detail import BannerDetailView
from src.views.banner.list import BannerListView
from src.views.category.detail import CategoryDetailView
from src.views.category.list import CategoryListView
from src.views.category.slug import CategorySlugView
from src.views.confirm_registration import ConfirmRegistrationView
from src.views.currency_rate.detail import CurrencyRateDetailView
from src.views.currency_rate.list import CurrencyRateListView
from src.views.feature_type.detail import FeatureTypeDetailView
from src.views.feature_type.list import FeatureTypeListView
from src.views.feature_value.detail import FeatureValueDetailView
from src.views.feature_value.list import FeatureValueListView
from src.views.language.list import LanguageListView
from src.views.order.by_user import OrderByUserView
from src.views.order.detail import OrderDetailView
from src.views.order.list import OrderListView
from src.views.product.by_product_type import ProductByProductTypeView
from src.views.product.detail import ProductDetailView
from src.views.product.list import ProductListView
from src.views.product_type.by_category import ProductTypeByCategoryView
from src.views.product_type.detail import ProductTypeDetailView
from src.views.product_type.list import ProductTypeListView
from src.views.product_type.slug import ProductTypeSlugView
from src.views.promo_code.detail import PromoCodeDetailView
from src.views.promo_code.list import PromoCodeListView
from src.views.promo_code.value import PromoCodeValueView
from src.views.refresh_token import RefreshTokenView
from src.views.registration import RegistrationView
from src.views.search import SearchView
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


class App:
    def __init__(self):
        self.flask_app = Flask(__name__)
        self.__init_config()

        if self.flask_app.config.get("SENTRY_DSN") is not None:
            sentry_sdk.init(
                dsn=self.flask_app.config["SENTRY_DSN"],
                integrations=[FlaskIntegration()],
            )

        self.cache = Cache(self.flask_app)
        self.__init_cors()
        self.__init_mail_client()
        self.__init_limiter()
        self.__init_file_storage()

        self.__db_engine = db.create_engine(self.flask_app.config["DB_URL"], echo=True)

        self.__init_repos()
        self.__init_services()
        self.__init_api_routes()
        self.__init_media_route()
        self.__init_sitemap_route()

    def __init_repos(self):
        self.__category_repo = CategoryRepo(self.__db_engine)
        self.__feature_type_repo = FeatureTypeRepo(self.__db_engine)
        self.__feature_value_repo = FeatureValueRepo(self.__db_engine)
        self.__language_repo = LanguageRepo(self.__db_engine)
        self.__product_type_repo = ProductTypeRepo(
            self.__db_engine, self.__file_storage
        )
        self.__product_repo = ProductRepo(self.__db_engine, self.__file_storage)
        self.__user_repo = UserRepo(self.__db_engine)
        self.__banner_repo = BannerRepo(self.__db_engine, self.__file_storage)
        self.__signup_repo = SignupRepo(self.__db_engine)
        self.__order_repo = OrderRepo(self.__db_engine)
        self.__promo_code_repo = PromoCodeRepo(self.__db_engine)
        self.__currency_rate_repo = CurrencyRateRepo(self.__db_engine)

    def __init_services(self):
        self.__category_service = CategoryService(
            self.__category_repo, self.__product_type_repo
        )
        self.__feature_type_service = FeatureTypeService(self.__feature_type_repo)
        self.__feature_value_service = FeatureValueService(
            self.__feature_value_repo, self.__feature_type_repo
        )
        self.__language_service = LanguageService(self.__language_repo)
        self.__product_type_service = ProductTypeService(
            self.__product_type_repo,
            self.__category_repo,
            self.__feature_type_repo,
            self.__product_repo,
        )
        feature_values_policy = FeatureValuesPolicy(self.__feature_type_repo)
        self.__product_service = ProductService(
            self.__product_repo,
            self.__product_type_repo,
            self.__feature_value_repo,
            feature_values_policy,
        )
        self.__user_service = UserService(self.__user_repo)
        self.__banner_service = BannerService(self.__banner_repo)
        self.__signup_service = SignupService(
            self.__signup_repo, self.__user_repo, self.mail
        )
        self.__order_service = OrderService(
            self.__order_repo, self.__product_repo, self.__promo_code_repo, self.mail
        )
        self.__promo_code_service = PromoCodeService(
            self.__promo_code_repo, self.__product_repo, self.__order_repo
        )
        self.__currency_rate_service = CurrencyRateService(
            self.__currency_rate_repo, self.__order_repo
        )

    def __init_api_routes(self):
        authorize_middleware = AuthorizeHttpMiddleware(self.__user_service)
        language_middleware = LanguageHttpMiddleware(self.__language_repo)
        middlewares = [authorize_middleware, language_middleware]

        category_product_types_cache = CategoryProductTypesCache(self.cache)

        self.flask_app.add_url_rule(
            "/api/auth/login",
            view_func=AbstractView.as_view(
                "login",
                concrete_view=AuthenticationView(
                    self.__user_service, AuthenticationDataValidator()
                ),
                middlewares=[language_middleware],
            ),
            methods=["POST"],
        )
        self.flask_app.add_url_rule(
            "/api/auth/register",
            view_func=AbstractView.as_view(
                "register",
                concrete_view=RegistrationView(
                    self.__signup_service, RegistrationDataValidator()
                ),
                middlewares=[language_middleware],
            ),
            methods=["POST"],
        )
        self.flask_app.add_url_rule(
            "/api/auth/register/confirm",
            view_func=AbstractView.as_view(
                "register_confirm",
                concrete_view=ConfirmRegistrationView(
                    self.__signup_service, ConfirmRegistrationDataValidator(),
                ),
                middlewares=[language_middleware],
            ),
            methods=["POST"],
        )
        self.flask_app.add_url_rule(
            "/api/auth/refresh",
            view_func=AbstractView.as_view(
                "refresh_token",
                concrete_view=RefreshTokenView(
                    self.__user_service, RefreshTokenDataValidator()
                ),
                middlewares=[language_middleware],
            ),
            methods=["POST"],
        )
        self.flask_app.add_url_rule(
            "/api/categories",
            view_func=AbstractView.as_view(
                "categories",
                concrete_view=CategoryListView(
                    CreateCategoryDataValidator(),
                    self.__category_service,
                    CategorySerializer,
                ),
                middlewares=middlewares,
                on_respond=category_product_types_cache.get_invalidate_hook(),
            ),
            methods=["GET", "POST"],
        )
        self.flask_app.add_url_rule(
            "/api/categories/<int:category_id>",
            view_func=AbstractView.as_view(
                "category",
                concrete_view=CategoryDetailView(
                    UpdateCategoryDataValidator(),
                    self.__category_service,
                    CategorySerializer,
                ),
                middlewares=middlewares,
                on_respond=category_product_types_cache.get_invalidate_hook(),
            ),
            methods=["GET", "PUT", "DELETE"],
        )
        self.flask_app.add_url_rule(
            "/api/categories/<path:slug>",
            view_func=AbstractView.as_view(
                "category_slug",
                concrete_view=CategorySlugView(
                    self.__category_service, CategorySerializer
                ),
                middlewares=middlewares,
            ),
            methods=["GET"],
        )
        self.flask_app.add_url_rule(
            "/api/categories/<path:category_slug>/product_types",
            view_func=self.cache.cached(
                60*60,
                response_filter=response_filter,
                make_cache_key=category_product_types_cache.make_cache_key,
            )(
                AbstractView.as_view(
                    "category_product_types",
                    concrete_view=ProductTypeByCategoryView(
                        self.__product_type_service, ProductTypeSerializer
                    ),
                    middlewares=middlewares,
                )
            ),
            methods=["GET"],
        )
        self.flask_app.add_url_rule(
            "/api/search/<path:query>",
            view_func=AbstractView.as_view(
                "search",
                concrete_view=SearchView(
                    self.__category_service,
                    self.__product_type_service,
                    CategorySerializer,
                    ProductTypeSerializer,
                ),
                middlewares=middlewares,
            ),
            methods=["GET"],
        )
        self.flask_app.add_url_rule(
            "/api/feature_types",
            view_func=AbstractView.as_view(
                "feature_types",
                concrete_view=FeatureTypeListView(
                    CreateFeatureTypeDataValidator(),
                    self.__feature_type_service,
                    FeatureTypeSerializer,
                ),
                middlewares=middlewares,
            ),
            methods=["GET", "POST"],
        ),
        self.flask_app.add_url_rule(
            "/api/feature_types/<int:feature_type_id>",
            view_func=AbstractView.as_view(
                "feature_type",
                concrete_view=FeatureTypeDetailView(
                    UpdateFeatureTypeDataValidator(),
                    self.__feature_type_service,
                    FeatureTypeSerializer,
                ),
                middlewares=middlewares,
            ),
            methods=["GET", "PUT", "DELETE"],
        )
        self.flask_app.add_url_rule(
            "/api/feature_values",
            view_func=AbstractView.as_view(
                "feature_values",
                concrete_view=FeatureValueListView(
                    CreateFeatureValueDataValidator(),
                    self.__feature_value_service,
                    FeatureValueSerializer,
                ),
                middlewares=middlewares,
            ),
            methods=["GET", "POST"],
        )
        self.flask_app.add_url_rule(
            "/api/feature_values/<int:feature_value_id>",
            view_func=AbstractView.as_view(
                "feature_value",
                concrete_view=FeatureValueDetailView(
                    UpdateFeatureValueDataValidator(),
                    self.__feature_value_service,
                    FeatureValueSerializer,
                ),
                middlewares=middlewares,
            ),
            methods=["GET", "PUT", "DELETE"],
        )
        self.flask_app.add_url_rule(
            "/api/products",
            view_func=AbstractView.as_view(
                "products",
                concrete_view=ProductListView(
                    CreateProductDataValidator(),
                    self.__product_service,
                    ProductSerializer,
                ),
                middlewares=middlewares,
            ),
            methods=["GET", "POST"],
        )
        self.flask_app.add_url_rule(
            "/api/products/<int:product_id>",
            view_func=AbstractView.as_view(
                "product",
                concrete_view=ProductDetailView(
                    UpdateProductDataValidator(),
                    self.__product_service,
                    ProductSerializer,
                ),
                middlewares=middlewares,
            ),
            methods=["GET", "PUT", "DELETE"],
        )
        self.flask_app.add_url_rule(
            "/api/product_types/<path:slug>",
            view_func=AbstractView.as_view(
                "product_type_slug",
                concrete_view=ProductTypeSlugView(
                    self.__product_type_service, ProductTypeSerializer
                ),
                middlewares=middlewares,
            ),
            methods=["GET"],
        )
        self.flask_app.add_url_rule(
            "/api/product_types/<int:product_type_id>/products",
            view_func=AbstractView.as_view(
                "product_type_products",
                concrete_view=ProductByProductTypeView(
                    self.__product_service, ProductSerializer
                ),
                middlewares=middlewares,
            ),
            methods=["GET"],
        )
        self.flask_app.add_url_rule(
            "/api/product_types",
            view_func=AbstractView.as_view(
                "product_types",
                concrete_view=ProductTypeListView(
                    CreateProductTypeDataValidator(),
                    self.__product_type_service,
                    ProductTypeSerializer,
                ),
                middlewares=middlewares,
                on_respond=category_product_types_cache.get_invalidate_hook(),
            ),
            methods=["GET", "POST"],
        )
        self.flask_app.add_url_rule(
            "/api/product_types/<int:product_type_id>",
            view_func=AbstractView.as_view(
                "product_type",
                concrete_view=ProductTypeDetailView(
                    UpdateProductTypeDataValidator(),
                    self.__product_type_service,
                    ProductTypeSerializer,
                ),
                middlewares=middlewares,
                on_respond=category_product_types_cache.get_invalidate_hook(),
            ),
            methods=["GET", "PUT", "DELETE"],
        )
        self.flask_app.add_url_rule(
            "/api/languages",
            view_func=self.cache.cached(60 * 60 * 24, response_filter=response_filter)(
                AbstractView.as_view(
                    "languages",
                    concrete_view=LanguageListView(
                        self.__language_service, LanguageSerializer
                    ),
                    middlewares=middlewares,
                )
            ),
            methods=["GET"],
        )
        self.flask_app.add_url_rule(
            "/api/banners",
            view_func=AbstractView.as_view(
                "banners",
                concrete_view=BannerListView(
                    CreateBannerDataValidator(), self.__banner_service, BannerSerializer
                ),
                middlewares=middlewares,
            ),
            methods=["GET", "POST"],
        )
        self.flask_app.add_url_rule(
            "/api/banners/<int:banner_id>",
            view_func=AbstractView.as_view(
                "banner",
                concrete_view=BannerDetailView(
                    UpdateBannerDataValidator(),
                    self.__banner_service,
                    BannerSerializer,
                ),
                middlewares=middlewares,
            ),
            methods=["GET", "PUT", "DELETE"],
        )
        self.flask_app.add_url_rule(
            "/api/orders/<int:order_id>",
            view_func=AbstractView.as_view(
                "order",
                concrete_view=OrderDetailView(
                    UpdateOrderDataValidator(), self.__order_service, OrderSerializer,
                ),
                middlewares=middlewares,
            ),
            methods=["GET", "PUT", "DELETE"],
        )
        self.flask_app.add_url_rule(
            "/api/orders",
            view_func=AbstractView.as_view(
                "orders",
                concrete_view=OrderListView(
                    CreateOrderDataValidator(), self.__order_service, OrderSerializer,
                ),
                middlewares=middlewares,
            ),
            methods=["GET", "POST"],
        )
        self.flask_app.add_url_rule(
            "/api/users/<int:user_id>/orders",
            view_func=(
                AbstractView.as_view(
                    "user_orders",
                    concrete_view=OrderByUserView(
                        self.__order_service, OrderSerializer
                    ),
                    middlewares=middlewares,
                )
            ),
            methods=["GET", "POST"],
        )
        self.flask_app.add_url_rule(
            "/api/promo_codes/<int:promo_code_id>",
            view_func=AbstractView.as_view(
                "promo_code",
                concrete_view=PromoCodeDetailView(
                    UpdatePromoCodeDataValidator(),
                    self.__promo_code_service,
                    PromoCodeSerializer,
                ),
                middlewares=middlewares,
            ),
            methods=["GET", "PUT", "DELETE"],
        )
        self.flask_app.add_url_rule(
            "/api/promo_codes",
            view_func=AbstractView.as_view(
                "promo_codes",
                concrete_view=PromoCodeListView(
                    CreatePromoCodeDataValidator(),
                    self.__promo_code_service,
                    PromoCodeSerializer,
                ),
                middlewares=middlewares,
            ),
            methods=["GET", "POST"],
        )
        self.flask_app.add_url_rule(
            "/api/promo_codes/<path:value>",
            view_func=AbstractView.as_view(
                "promo_code_value",
                concrete_view=PromoCodeValueView(
                    self.__promo_code_service, PromoCodeSerializer
                ),
                middlewares=middlewares,
            ),
            methods=["GET"],
        )
        self.flask_app.add_url_rule(
            "/api/currency_rates",
            view_func=AbstractView.as_view(
                "currency_rates",
                concrete_view=CurrencyRateListView(
                    CreateCurrencyRateDataValidator(),
                    self.__currency_rate_service,
                    CurrencyRateSerializer,
                ),
                middlewares=middlewares,
            ),
            methods=["GET", "POST"],
        )
        self.flask_app.add_url_rule(
            "/api/currency_rates/<int:currency_rate_id>",
            view_func=AbstractView.as_view(
                "currency_rate",
                concrete_view=CurrencyRateDetailView(
                    self.__currency_rate_service, CurrencyRateSerializer
                ),
                middlewares=middlewares,
            ),
            methods=["HEAD", "DELETE"],
        )

    def __handle_media_request(self, path):
        abs_media_path = os.path.join(APP_ROOT_PATH, "media")
        abs_path = os.path.join(abs_media_path, path)
        if os.path.isfile(abs_path):
            return send_from_directory(abs_media_path, path)

        return "", 404

    def __init_media_route(self):
        self.flask_app.add_url_rule(
            "/media/<path:path>", view_func=self.__handle_media_request, methods=["GET"]
        )

    def __init_sitemap_route(self):
        @self.flask_app.route("/sitemap.xml")
        @self.cache.cached(timeout=60 * 60 * 24)
        def handle_sitemap_request():
            categories = self.__category_repo.get_all()
            product_types, _ = self.__product_type_repo.get_all()
            xml = render_template(
                "sitemap.xml",
                categories=categories,
                product_types=product_types,
                base_url=self.flask_app.config.get("HOST"),
            )

            return Response(xml, mimetype="text/xml")

    def __init_limiter(self):
        limiter = Limiter(
            self.flask_app, key_func=get_remote_address, default_limits=["60/minute"],
        )

        @limiter.request_filter
        def limiter_request_filter():
            return request.method.lower() == "options" or "localhost" in request.host

    def __init_file_storage(self):
        self.__file_storage = AWSStorage(
            self.flask_app.config["AWS_BUCKET_NAME"],
            self.flask_app.config["AWS_DEFAULT_REGION"],
            self.flask_app.config["AWS_ACCESS_KEY_ID"],
            self.flask_app.config["AWS_SECRET_ACCESS_KEY"],
        )

    def __init_mail_client(self):
        flask_mail = FlaskMail(self.flask_app)
        self.mail = Mail(flask_mail)

    def __init_cors(self):
        CORS(self.flask_app, origins=self.flask_app.config["ALLOWED_ORIGINS"])

    def __init_config(self):
        self.flask_app.config.from_object(
            os.environ.get("APP_SETTINGS", "config.DevelopmentConfig")
        )
