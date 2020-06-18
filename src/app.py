
import os

import sqlalchemy as db
from cerberus.validator import Validator
from elasticsearch import Elasticsearch
from flask import Flask, Response, jsonify, request, send_from_directory
from flask.templating import render_template
from flask_caching import Cache
from flask_cors import CORS
from flask_mail import Mail as FlaskMail

from paths import APP_ROOT_PATH
from src.abstract_view import AbstractView
from src.constants.cache import (USER_ORDERS_CACHE_KEY,
                                 make_user_orders_cache_key)
from src.constants.status_codes import OK_CODE
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
from src.utils.cache import make_cache_invalidator, response_filter
from src.validation_rules.authentication import AUTHENTICATION_VALIDATION_RULES
from src.validation_rules.banner.create import CREATE_BANNER_VALIDATION_RULES
from src.validation_rules.banner.update import UPDATE_BANNER_VALIDATION_RULES
from src.validation_rules.category.create import \
    CREATE_CATEGORY_VALIDATION_RULES
from src.validation_rules.category.update import \
    UPDATE_CATEGORY_VALIDATION_RULES
from src.validation_rules.confirm_registration import \
    CONFIRM_REGISTRATION_VALIDATION_RULES
from src.validation_rules.currency_rate.create import \
    CREATE_CURRENCY_RATE_VALIDATION_RULES
from src.validation_rules.feature_type.create import \
    CREATE_FEATURE_TYPE_VALIDATION_RULES
from src.validation_rules.feature_type.update import \
    UPDATE_FEATURE_TYPE_VALIDATION_RULES
from src.validation_rules.feature_value.create import \
    CREATE_FEATURE_VALUE_VALIDATION_RULES
from src.validation_rules.feature_value.update import \
    UPDATE_FEATURE_VALUE_VALIDATION_RULES
from src.validation_rules.order.create import CREATE_ORDER_VALIDATION_RULES
from src.validation_rules.order.update import UPDATE_ORDER_VALIDATION_RULES
from src.validation_rules.product.create import CREATE_PRODUCT_VALIDATION_RULES
from src.validation_rules.product.update import UPDATE_PRODUCT_VALIDATION_RULES
from src.validation_rules.product_type.create import \
    CREATE_PRODUCT_TYPE_VALIDATION_RULES
from src.validation_rules.product_type.update import \
    UPDATE_PRODUCT_TYPE_VALIDATION_RULES
from src.validation_rules.promo_code.create import \
    CREATE_PROMO_CODE_VALIDATION_RULES
from src.validation_rules.promo_code.update import \
    UPDATE_PROMO_CODE_VALIDATION_RULES
from src.validation_rules.refresh_token import REFRESH_TOKEN_VALIDATION_RULES
from src.validation_rules.registration import REGISTRATION_VALIDATION_RULES
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


class App:
    def __init__(self):
        self.flask_app = Flask(__name__)
        self.flask_app.config.from_object(os.environ.get(
            'APP_SETTINGS', 'config.DevelopmentConfig'))
        self.cache = Cache(self.flask_app)
        CORS(self.flask_app,
             origins=self.flask_app.config['ALLOWED_ORIGINS'])
        flask_mail = FlaskMail(self.flask_app)
        self.mail = Mail(flask_mail)
        self.__file_storage = AWSStorage(
            self.flask_app.config['AWS_BUCKET_NAME'],
            self.flask_app.config['AWS_DEFAULT_REGION'],
            self.flask_app.config['AWS_ACCESS_KEY_ID'],
            self.flask_app.config['AWS_SECRET_ACCESS_KEY']
        )
        engine = db.create_engine(self.flask_app.config['DB_URL'], echo=True)
        self.__db_conn = engine.connect()
        self.__es = Elasticsearch(self.flask_app.config['ELASTICSEARCH_URL'])

        self.__init_repos()
        self.__init_services()
        self.__init_search()
        self.__init_api_routes()
        self.__init_media_route()
        self.__init_sitemap_route()

    def __init_repos(self):
        self.__category_repo = CategoryRepo(self.__db_conn)
        self.__feature_type_repo = FeatureTypeRepo(self.__db_conn)
        self.__feature_value_repo = FeatureValueRepo(self.__db_conn)
        self.__language_repo = LanguageRepo(self.__db_conn)
        self.__product_type_repo = ProductTypeRepo(
            self.__db_conn, self.__file_storage)
        self.__product_repo = ProductRepo(self.__db_conn, self.__file_storage)
        self.__user_repo = UserRepo(self.__db_conn)
        self.__banner_repo = BannerRepo(self.__db_conn, self.__file_storage)
        self.__signup_repo = SignupRepo(self.__db_conn)
        self.__order_repo = OrderRepo(self.__db_conn)
        self.__promo_code_repo = PromoCodeRepo(self.__db_conn)
        self.__currency_rate_repo = CurrencyRateRepo(self.__db_conn)

    def __init_services(self):
        self.__category_service = CategoryService(
            self.__category_repo, self.__product_type_repo, self.__es)
        self.__feature_type_service = FeatureTypeService(
            self.__feature_type_repo)
        self.__feature_value_service = FeatureValueService(
            self.__feature_value_repo, self.__feature_type_repo
        )
        self.__language_service = LanguageService(self.__language_repo)
        self.__product_type_service = ProductTypeService(
            self.__product_type_repo, self.__category_repo, self.__feature_type_repo, self.__product_repo, self.__es
        )
        feature_values_policy = FeatureValuesPolicy(self.__feature_type_repo)
        self.__product_service = ProductService(
            self.__product_repo, self.__product_type_repo, self.__feature_value_repo, feature_values_policy
        )
        self.__user_service = UserService(self.__user_repo)
        self.__banner_service = BannerService(self.__banner_repo)
        self.__signup_service = SignupService(
            self.__signup_repo, self.__user_repo, self.mail)
        self.__order_service = OrderService(
            self.__order_repo, self.__product_repo, self.__promo_code_repo, self.mail)
        self.__promo_code_service = PromoCodeService(
            self.__promo_code_repo, self.__product_repo, self.__order_repo
        )
        self.__currency_rate_service = CurrencyRateService(
            self.__currency_rate_repo, self.__order_repo
        )

    def __init_search(self):
        if not self.__es.indices.exists(index="category"):
            self.__es.indices.create(index='category')
        if not self.__es.indices.exists(index="product_type"):
            self.__es.indices.create(index='product_type')

        for category in self.__category_repo.get_all():
            self.__category_service.set_to_search_index(category)

        product_types, _ = self.__product_type_repo.get_all()
        for product_type in product_types:
            self.__product_type_service.set_to_search_index(product_type)

    def __init_api_routes(self):
        authorize_middleware = AuthorizeHttpMiddleware(self.__user_service)
        language_middleware = LanguageHttpMiddleware(self.__language_repo)
        middlewares = [authorize_middleware, language_middleware]

        orders_on_respond = make_cache_invalidator(
            self.cache, USER_ORDERS_CACHE_KEY)

        self.flask_app.add_url_rule(
            '/api/auth/login',
            view_func=AbstractView.as_view(
                'login',
                concrete_view=AuthenticationView(
                    self.__user_service, Validator(
                        AUTHENTICATION_VALIDATION_RULES)
                ),
                middlewares=[language_middleware]
            ),
            methods=['POST']
        )
        self.flask_app.add_url_rule(
            '/api/auth/register',
            view_func=AbstractView.as_view(
                'register',
                concrete_view=RegistrationView(
                    self.__signup_service,
                    Validator(REGISTRATION_VALIDATION_RULES)
                ),
                middlewares=[language_middleware]
            ),
            methods=['POST']
        )
        self.flask_app.add_url_rule(
            '/api/auth/register/confirm',
            view_func=AbstractView.as_view(
                'register_confirm',
                concrete_view=ConfirmRegistrationView(
                    self.__signup_service,
                    Validator(CONFIRM_REGISTRATION_VALIDATION_RULES)
                ),
                middlewares=[language_middleware]
            ),
            methods=['POST']
        )
        self.flask_app.add_url_rule(
            '/api/auth/refresh',
            view_func=AbstractView.as_view(
                'refresh_token',
                concrete_view=RefreshTokenView(
                    self.__user_service,
                    Validator(REFRESH_TOKEN_VALIDATION_RULES)
                ),
                middlewares=[language_middleware]
            ),
            methods=['POST']

        )
        self.flask_app.add_url_rule(
            '/api/categories',
            view_func=AbstractView.as_view(
                'categories',
                concrete_view=CategoryListView(
                    Validator(CREATE_CATEGORY_VALIDATION_RULES),
                    self.__category_service,
                    CategorySerializer
                ),
                middlewares=middlewares
            ),
            methods=['GET', 'POST']
        )
        self.flask_app.add_url_rule(
            '/api/categories/<int:category_id>',
            view_func=AbstractView.as_view(
                'category',
                concrete_view=CategoryDetailView(
                    Validator(UPDATE_CATEGORY_VALIDATION_RULES),
                    self.__category_service,
                    CategorySerializer
                ),
                middlewares=middlewares
            ),
            methods=['GET', 'PUT', 'DELETE']
        )
        self.flask_app.add_url_rule(
            '/api/categories/<path:slug>',
            view_func=AbstractView.as_view(
                'category_slug',
                concrete_view=CategorySlugView(
                    self.__category_service, CategorySerializer
                ),
                middlewares=middlewares
            ),
            methods=['GET']
        )
        self.flask_app.add_url_rule(
            '/api/categories/<path:category_slug>/product_types',
            view_func=AbstractView.as_view(
                'category_product_types',
                concrete_view=ProductTypeByCategoryView(
                    self.__product_type_service,
                    ProductTypeSerializer
                ),
                middlewares=middlewares
            ),
            methods=['GET']
        )
        self.flask_app.add_url_rule(
            '/api/search/<path:query>',
            view_func=AbstractView.as_view(
                'search',
                concrete_view=SearchView(
                    self.__category_service,
                    self.__product_type_service,
                    CategorySerializer,
                    ProductTypeSerializer
                ),
                middlewares=middlewares
            ),
            methods=['GET']
        )
        self.flask_app.add_url_rule(
            '/api/feature_types',
            view_func=AbstractView.as_view(
                'feature_types',
                concrete_view=FeatureTypeListView(
                    Validator(CREATE_FEATURE_TYPE_VALIDATION_RULES),
                    self.__feature_type_service,
                    FeatureTypeSerializer
                ),
                middlewares=middlewares
            ),
            methods=['GET', 'POST']
        ),
        self.flask_app.add_url_rule(
            '/api/feature_types/<int:feature_type_id>',
            view_func=AbstractView.as_view(
                'feature_type',
                concrete_view=FeatureTypeDetailView(
                    Validator(UPDATE_FEATURE_TYPE_VALIDATION_RULES),
                    self.__feature_type_service,
                    FeatureTypeSerializer
                ),
                middlewares=middlewares
            ),
            methods=['GET', 'PUT', 'DELETE']
        )
        self.flask_app.add_url_rule(
            '/api/feature_values',
            view_func=AbstractView.as_view(
                'feature_values',
                concrete_view=FeatureValueListView(
                    Validator(CREATE_FEATURE_VALUE_VALIDATION_RULES),
                    self.__feature_value_service,
                    FeatureValueSerializer
                ),
                middlewares=middlewares
            ),
            methods=['GET', 'POST']
        )
        self.flask_app.add_url_rule(
            '/api/feature_values/<int:feature_value_id>',
            view_func=AbstractView.as_view(
                'feature_value',
                concrete_view=FeatureValueDetailView(
                    Validator(UPDATE_FEATURE_VALUE_VALIDATION_RULES),
                    self.__feature_value_service,
                    FeatureValueSerializer),
                middlewares=middlewares
            ),
            methods=['GET', 'PUT', 'DELETE']
        )
        self.flask_app.add_url_rule(
            '/api/products',
            view_func=AbstractView.as_view(
                'products',
                concrete_view=ProductListView(
                    Validator(CREATE_PRODUCT_VALIDATION_RULES),
                    self.__product_service,
                    ProductSerializer
                ),
                middlewares=middlewares
            ),
            methods=['GET', 'POST']
        )
        self.flask_app.add_url_rule(
            '/api/products/<int:product_id>',
            view_func=AbstractView.as_view(
                'product',
                concrete_view=ProductDetailView(
                    Validator(UPDATE_PRODUCT_VALIDATION_RULES),
                    self.__product_service,
                    ProductSerializer),
                middlewares=middlewares
            ),
            methods=['GET', 'PUT', 'DELETE']
        )
        self.flask_app.add_url_rule(
            '/api/product_types/<path:slug>',
            view_func=AbstractView.as_view(
                'product_type_slug',
                concrete_view=ProductTypeSlugView(
                    self.__product_type_service, ProductTypeSerializer
                ),
                middlewares=middlewares
            ),
            methods=['GET']
        )
        self.flask_app.add_url_rule(
            '/api/product_types/<int:product_type_id>/products',
            view_func=AbstractView.as_view(
                'product_type_products',
                concrete_view=ProductByProductTypeView(
                    self.__product_service, ProductSerializer),
                middlewares=middlewares
            ),
            methods=['GET']
        )
        self.flask_app.add_url_rule(
            '/api/product_types',
            view_func=AbstractView.as_view(
                'product_types',
                concrete_view=ProductTypeListView(
                    Validator(CREATE_PRODUCT_TYPE_VALIDATION_RULES),
                    self.__product_type_service,
                    ProductTypeSerializer
                ),
                middlewares=middlewares
            ),
            methods=['GET', 'POST']
        )
        self.flask_app.add_url_rule(
            '/api/product_types/<int:product_type_id>',
            view_func=AbstractView.as_view(
                'product_type',
                concrete_view=ProductTypeDetailView(
                    Validator(UPDATE_PRODUCT_TYPE_VALIDATION_RULES),
                    self.__product_type_service,
                    ProductTypeSerializer
                ),
                middlewares=middlewares
            ),
            methods=['GET', 'PUT', 'DELETE']
        )
        self.flask_app.add_url_rule(
            '/api/languages',
            view_func=self.cache.cached(60 * 60 * 24, response_filter=response_filter)(
                AbstractView.as_view(
                    'languages',
                    concrete_view=LanguageListView(
                        self.__language_service,
                        LanguageSerializer
                    ),
                    middlewares=middlewares
                )
            ),
            methods=['GET']
        )
        self.flask_app.add_url_rule(
            '/api/banners',
            view_func=AbstractView.as_view(
                'banners',
                concrete_view=BannerListView(
                    Validator(CREATE_BANNER_VALIDATION_RULES),
                    self.__banner_service,
                    BannerSerializer
                ),
                middlewares=middlewares
            ),
            methods=['GET', 'POST']
        )
        self.flask_app.add_url_rule(
            '/api/banners/<int:banner_id>',
            view_func=AbstractView.as_view(
                'banner',
                concrete_view=BannerDetailView(
                    Validator(UPDATE_BANNER_VALIDATION_RULES),
                    self.__banner_service,
                    BannerSerializer
                ),
                middlewares=middlewares
            ),
            methods=['GET', 'PUT', 'DELETE']
        )
        self.flask_app.add_url_rule(
            '/api/orders/<int:order_id>',
            view_func=AbstractView.as_view(
                'order',
                concrete_view=OrderDetailView(
                    Validator(UPDATE_ORDER_VALIDATION_RULES),
                    self.__order_service,
                    OrderSerializer
                ),
                middlewares=middlewares,
                on_respond=orders_on_respond
            ),
            methods=['GET', 'PUT', 'DELETE']
        )
        self.flask_app.add_url_rule(
            '/api/orders',
            view_func=AbstractView.as_view(
                'orders',
                concrete_view=OrderListView(
                    Validator(CREATE_ORDER_VALIDATION_RULES),
                    self.__order_service,
                    OrderSerializer
                ),
                middlewares=middlewares,
                on_respond=orders_on_respond
            ),
            methods=['GET', 'POST']
        )
        self.flask_app.add_url_rule(
            '/api/users/<int:user_id>/orders',
            view_func=(
                AbstractView.as_view(
                    'user_orders',
                    concrete_view=OrderByUserView(
                        self.__order_service,
                        OrderSerializer
                    ),
                    middlewares=middlewares,
                )
            ),
            methods=['GET', 'POST']
        )
        self.flask_app.add_url_rule(
            '/api/promo_codes/<int:promo_code_id>',
            view_func=AbstractView.as_view(
                'promo_code',
                concrete_view=PromoCodeDetailView(
                    Validator(UPDATE_PROMO_CODE_VALIDATION_RULES),
                    self.__promo_code_service,
                    PromoCodeSerializer
                ),
                middlewares=middlewares
            ),
            methods=['GET', 'PUT', 'DELETE']
        )
        self.flask_app.add_url_rule(
            '/api/promo_codes',
            view_func=AbstractView.as_view(
                'promo_codes',
                concrete_view=PromoCodeListView(
                    Validator(CREATE_PROMO_CODE_VALIDATION_RULES),
                    self.__promo_code_service,
                    PromoCodeSerializer
                ),
                middlewares=middlewares
            ),
            methods=['GET', 'POST']
        )
        self.flask_app.add_url_rule(
            '/api/promo_codes/<path:value>',
            view_func=AbstractView.as_view(
                'promo_code_value',
                concrete_view=PromoCodeValueView(
                    self.__promo_code_service,
                    PromoCodeSerializer
                ),
                middlewares=middlewares
            ),
            methods=['GET']
        )
        self.flask_app.add_url_rule(
            '/api/currency_rates',
            view_func=AbstractView.as_view(
                'currency_rates',
                concrete_view=CurrencyRateListView(
                    Validator(CREATE_CURRENCY_RATE_VALIDATION_RULES),
                    self.__currency_rate_service,
                    CurrencyRateSerializer
                ),
                middlewares=middlewares
            ),
            methods=['GET', 'POST']
        )
        self.flask_app.add_url_rule(
            '/api/currency_rates/<int:currency_rate_id>',
            view_func=AbstractView.as_view(
                'currency_rate',
                concrete_view=CurrencyRateDetailView(
                    self.__currency_rate_service,
                    CurrencyRateSerializer
                ),
                middlewares=middlewares
            ),
            methods=['HEAD', 'DELETE']
        )

    def __handle_media_request(self, path):
        abs_media_path = os.path.join(APP_ROOT_PATH, 'media')
        abs_path = os.path.join(abs_media_path, path)
        if os.path.isfile(abs_path):
            return send_from_directory(abs_media_path, path)

        return '', 404

    def __init_media_route(self):
        self.flask_app.add_url_rule(
            '/media/<path:path>',
            view_func=self.__handle_media_request,
            methods=['GET']
        )

    def __init_sitemap_route(self):
        @self.flask_app.route('/sitemap.xml')
        @self.cache.cached(timeout=60*60*24)
        def handle_sitemap_request():
            categories = self.__category_repo.get_all()
            product_types, _ = self.__product_type_repo.get_all()
            xml = render_template('sitemap.xml',
                                  categories=categories,
                                  product_types=product_types,
                                  base_url=self.flask_app.config.get('HOST'))

            return Response(xml, mimetype='text/xml')
